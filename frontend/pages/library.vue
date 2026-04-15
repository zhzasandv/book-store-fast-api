<script setup lang="ts">
import type { Author, Genre } from '~/types/book'

const router = useRouter()
const route = useRoute()
const config = useRuntimeConfig()
const { buildLibraryQuery } = useLibraryQuery()
const genreNamesStorageKey = 'libraryGenreNames'
const authorNamesStorageKey = 'libraryAuthorNames'
const savedGenreNames = ref<Record<string, string>>({})
const savedAuthorNames = ref<Record<string, string>>({})

const { books, total, totalPages, page, genreId, authorId, pending, error } = useBooks()

const { data: genresData } = useFetch<Genre[]>(
  `${config.public.apiBase}/api/v1/genres/`
)

const { data: authorsData } = useFetch<Author[]>(
  `${config.public.apiBase}/api/v1/authors/`
)

const genres = computed(() => genresData.value ?? [])
const authors = computed(() => authorsData.value ?? [])

const pageNumbers = computed(() => Array.from({ length: totalPages.value }, (_, index) => index + 1))
const previousPage = computed(() => Math.max(page.value - 1, 1))
const nextPage = computed(() => Math.min(page.value + 1, Math.max(totalPages.value, 1)))
const selectedGenre = computed(() => (genreId.value ? String(genreId.value) : ''))
const selectedAuthor = computed(() => (authorId.value ? String(authorId.value) : ''))
const selectedGenreModel = computed({
  get: () => selectedGenre.value,
  set: (value) => {
    void applyGenreFilter(value)
  },
})
const selectedAuthorModel = computed({
  get: () => selectedAuthor.value,
  set: (value) => {
    void applyAuthorFilter(value)
  },
})
const selectedGenreName = computed(() => {
  const value = route.query.genre_name
  if (typeof value === 'string' && value.trim()) {
    return value.trim()
  }

  return selectedGenre.value ? savedGenreNames.value[selectedGenre.value] : undefined
})
const selectedAuthorName = computed(() => {
  const value = route.query.author_name
  if (typeof value === 'string' && value.trim()) {
    return value.trim()
  }

  return selectedAuthor.value ? savedAuthorNames.value[selectedAuthor.value] : undefined
})
const genresWithoutSelected = computed(() => (
  genreId.value
    ? genres.value.filter((genre) => genre.id !== genreId.value)
    : genres.value
))
const authorsWithoutSelected = computed(() => (
  authorId.value
    ? authors.value.filter((author) => author.id !== authorId.value)
    : authors.value
))
const selectedGenreOption = computed(() => {
  if (!genreId.value) {
    return null
  }

  const genre = genres.value.find((item) => item.id === genreId.value)
  const genreFromBooks = books.value.find((book) => book.genre.id === genreId.value)?.genre

  return genre ?? genreFromBooks ?? {
    id: genreId.value,
    name: selectedGenreName.value ?? `Жанр #${genreId.value}`,
  }
})
const selectedAuthorOption = computed(() => {
  if (!authorId.value) {
    return null
  }

  const author = authors.value.find((item) => item.id === authorId.value)
  const authorFromBooks = books.value
    .flatMap((book) => book.authors)
    .find((item) => item.id === authorId.value)

  if (author ?? authorFromBooks) {
    return author ?? authorFromBooks
  }

  const [firstName = 'Автор', ...lastNameParts] = selectedAuthorName.value?.split(' ') ?? []

  return {
    id: authorId.value,
    first_name: firstName,
    last_name: lastNameParts.join(' ') || `#${authorId.value}`,
  }
})

function saveFilterNames() {
  if (!import.meta.client) {
    return
  }

  const genreNames = Object.fromEntries(genres.value.map((genre) => [String(genre.id), genre.name]))
  const authorNames = Object.fromEntries(
    authors.value.map((author) => [String(author.id), `${author.first_name} ${author.last_name}`])
  )

  savedGenreNames.value = { ...savedGenreNames.value, ...genreNames }
  savedAuthorNames.value = { ...savedAuthorNames.value, ...authorNames }
  localStorage.setItem(genreNamesStorageKey, JSON.stringify(savedGenreNames.value))
  localStorage.setItem(authorNamesStorageKey, JSON.stringify(savedAuthorNames.value))
}

function readSavedFilterNames() {
  if (!import.meta.client) {
    return
  }

  try {
    savedGenreNames.value = JSON.parse(localStorage.getItem(genreNamesStorageKey) ?? '{}')
    savedAuthorNames.value = JSON.parse(localStorage.getItem(authorNamesStorageKey) ?? '{}')
  } catch {
    savedGenreNames.value = {}
    savedAuthorNames.value = {}
  }
}

async function applyGenreFilter(rawValue: string) {
  const value = rawValue || null
  const genre = value ? genres.value.find((item) => String(item.id) === value) : null
  const selectedName = genre?.name ?? (value ? savedGenreNames.value[value] : null)

  await router.push({
    query: buildLibraryQuery({
      genre_id: value,
      genre_name: selectedName,
      page: null,
    }),
  })
}

async function applyAuthorFilter(rawValue: string) {
  const value = rawValue || null
  const author = value ? authors.value.find((item) => String(item.id) === value) : null
  const selectedName = author
    ? `${author.first_name} ${author.last_name}`
    : value
      ? savedAuthorNames.value[value]
      : null

  await router.push({
    query: buildLibraryQuery({
      author_id: value,
      author_name: selectedName,
      page: null,
    }),
  })
}

onMounted(readSavedFilterNames)
watch([genres, authors], saveFilterNames)
</script>

<template>
  <section class="library-page">
    <div class="library-heading">
      <div>
        <p class="library-kicker">Библиотека</p>
        <h2 class="library-title">Каталог книг</h2>
      </div>

      <div class="library-stats">
        <p>Найдено: {{ total }}</p>
        <p>Страница {{ page }}<span v-if="totalPages"> из {{ totalPages }}</span></p>
      </div>
    </div>

    <section class="filters-panel">
      <label class="filter-field">
        <span class="filter-label">Жанр</span>
        <select
          :key="`genre-${selectedGenre}-${selectedGenreOption?.name ?? ''}`"
          v-model="selectedGenreModel"
          class="filter-select"
        >
          <option value="">Все жанры</option>
          <option v-if="selectedGenreOption" :value="String(selectedGenreOption.id)">
            {{ selectedGenreOption.name }}
          </option>
          <option v-for="genre in genresWithoutSelected" :key="genre.id" :value="String(genre.id)">
            {{ genre.name }}
          </option>
        </select>
      </label>

      <label class="filter-field">
        <span class="filter-label">Автор</span>
        <select
          :key="`author-${selectedAuthor}-${selectedAuthorOption?.first_name ?? ''}-${selectedAuthorOption?.last_name ?? ''}`"
          v-model="selectedAuthorModel"
          class="filter-select"
        >
          <option value="">Все авторы</option>
          <option v-if="selectedAuthorOption" :value="String(selectedAuthorOption.id)">
            {{ selectedAuthorOption.first_name }} {{ selectedAuthorOption.last_name }}
          </option>
          <option v-for="author in authorsWithoutSelected" :key="author.id" :value="String(author.id)">
            {{ author.first_name }} {{ author.last_name }}
          </option>
        </select>
      </label>
    </section>

    <section class="catalog-panel">
      <div v-if="pending" class="state-message">Загрузка каталога...</div>
      <div v-else-if="error" class="state-message error">
        Не удалось загрузить книги. Убедитесь, что бэкенд запущен.
      </div>
      <div v-else-if="books.length === 0" class="state-message">По текущим параметрам ничего не найдено.</div>
      <template v-else>
        <div class="books-grid">
          <article v-for="book in books" :key="book.id" class="book-card">
            <div class="book-cover">
              <img v-if="book.image_url" :src="book.image_url" :alt="book.name" />
              <div v-else class="no-cover">нет обложки</div>
            </div>
            <div class="book-info">
              <p class="book-genre">{{ book.genre.name }}</p>
              <h3 class="book-name">{{ book.name }}</h3>
              <p class="book-authors">
                {{ book.authors.map(a => `${a.first_name} ${a.last_name}`).join(', ') }}
              </p>
              <p class="book-title">{{ book.title }}</p>
              <p class="book-price">{{ book.price }} ₸</p>
            </div>
          </article>
        </div>

        <nav v-if="totalPages > 1" class="pagination" aria-label="Пагинация каталога">
          <NuxtLink
            class="pagination-link"
            :class="{ disabled: page === 1 }"
            :to="{ query: buildLibraryQuery({ page: String(previousPage) }) }"
          >
            ←
          </NuxtLink>

          <NuxtLink
            v-for="pageNumber in pageNumbers"
            :key="pageNumber"
            class="pagination-link"
            :class="{ active: pageNumber === page }"
            :to="{ query: buildLibraryQuery({ page: String(pageNumber) }) }"
          >
            {{ pageNumber }}
          </NuxtLink>

          <NuxtLink
            class="pagination-link"
            :class="{ disabled: page === totalPages }"
            :to="{ query: buildLibraryQuery({ page: String(nextPage) }) }"
          >
            →
          </NuxtLink>
        </nav>
      </template>
    </section>
  </section>
</template>

<style scoped>
.library-page {
  width: min(1180px, 100%);
  margin: 0 auto;
  display: grid;
  gap: 1.35rem;
}

.library-heading,
.filters-panel,
.catalog-panel {
  border-radius: 1.8rem;
  background:
    linear-gradient(145deg, rgba(255, 255, 255, 0.05), rgba(255, 255, 255, 0.015)),
    rgba(13, 14, 23, 0.84);
  border: 1px solid rgba(255, 255, 255, 0.08);
}

.library-heading {
  display: flex;
  justify-content: space-between;
  gap: 1rem;
  align-items: end;
  padding: 1.6rem 1.7rem;
}

.library-kicker {
  margin: 0 0 0.45rem;
  color: #f2c96d;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  font-size: 0.8rem;
}

.library-title {
  margin: 0;
  font-size: clamp(1.8rem, 3vw, 2.8rem);
}

.library-stats {
  text-align: right;
  color: #bdb8ae;
}

.library-stats p {
  margin: 0.2rem 0;
}

.filters-panel {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 240px));
  gap: 1rem;
  padding: 1.35rem 1.5rem;
}

.filter-field {
  display: grid;
  gap: 0.55rem;
}

.filter-label {
  color: #c8bba1;
  font-size: 0.92rem;
}

.filter-select {
  width: 100%;
  min-width: 0;
  padding: 0.95rem 1rem;
  border-radius: 1rem;
  border: 1px solid rgba(255, 255, 255, 0.1);
  background: rgba(255, 248, 239, 0.92);
  color: #241d18;
  font: inherit;
}

.catalog-panel {
  padding: 1.6rem;
}

.state-message {
  text-align: center;
  color: #bdb8ae;
  padding: 3rem 0;
}

.state-message.error {
  color: #fca5a5;
}

.books-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 1.12rem;
}

.book-card {
  overflow: hidden;
  border-radius: 1.3rem;
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(255, 255, 255, 0.08);
}

.book-cover {
  height: 250px;
  background: rgba(8, 8, 14, 0.8);
  display: flex;
  align-items: center;
  justify-content: center;
}

.book-cover img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.no-cover {
  color: #6c665f;
}

.book-info {
  display: grid;
  gap: 0.55rem;
  padding: 1rem;
}

.book-genre {
  margin: 0;
  color: #f2c96d;
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.14em;
}

.book-name,
.book-authors,
.book-title,
.book-price {
  margin: 0;
}

.book-name {
  font-size: 1.05rem;
}

.book-authors,
.book-title {
  color: #cdc5b8;
}

.book-title {
  line-height: 1.55;
}

.book-price {
  color: #f8b74f;
  font-weight: 700;
}

.pagination {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 0.65rem;
  margin-top: 1.5rem;
}

.pagination-link {
  min-width: 2.75rem;
  height: 2.75rem;
  padding: 0 0.85rem;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.06);
  border: 1px solid rgba(255, 255, 255, 0.08);
  text-decoration: none;
}

.pagination-link.active {
  background: linear-gradient(135deg, #f6c453, #f97316);
  color: #231a14;
  font-weight: 700;
}

.pagination-link.disabled {
  pointer-events: none;
  opacity: 0.45;
}

@media (max-width: 1040px) {
  .books-grid {
    grid-template-columns: repeat(3, minmax(0, 1fr));
  }
}

@media (max-width: 760px) {
  .library-heading,
  .filters-panel {
    grid-template-columns: 1fr;
    display: grid;
  }

  .library-stats {
    text-align: left;
  }

  .books-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 540px) {
  .catalog-panel,
  .library-heading,
  .filters-panel {
    padding-left: 1rem;
    padding-right: 1rem;
  }

  .books-grid {
    grid-template-columns: 1fr;
  }
}
</style>
