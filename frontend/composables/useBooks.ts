import type { BookListResponse } from '~/types/book'

function normalizePositiveNumber(value: string | string[] | undefined, fallback: number) {
  const raw = Array.isArray(value) ? value[0] : value
  const parsed = Number.parseInt(raw ?? '', 10)
  return Number.isFinite(parsed) && parsed > 0 ? parsed : fallback
}

function normalizeText(value: string | string[] | undefined) {
  const raw = Array.isArray(value) ? value[0] : value
  const normalized = raw?.trim() ?? ''
  return normalized.length > 0 ? normalized : undefined
}

export function useBooks() {
  const config = useRuntimeConfig()
  const route = useRoute()

  const page = computed(() => normalizePositiveNumber(route.query.page, 1))
  const pageSize = 10
  const searchQuery = computed(() => normalizeText(route.query.q))
  const genreId = computed(() => normalizePositiveNumber(route.query.genre_id, 0) || undefined)
  const authorId = computed(() => normalizePositiveNumber(route.query.author_id, 0) || undefined)

  const query = computed(() => ({
    page: page.value,
    page_size: pageSize,
    ...(searchQuery.value ? { q: searchQuery.value } : {}),
    ...(genreId.value ? { genre_id: genreId.value } : {}),
    ...(authorId.value ? { author_id: authorId.value } : {}),
  }))

  const { data, pending, error } = useFetch<BookListResponse>(
    `${config.public.apiBase}/api/v1/books/`,
    {
      query,
      watch: [query],
    }
  )

  const booksResponse = computed(() => data.value ?? {
    items: [],
    total: 0,
    page: page.value,
    page_size: pageSize,
    total_pages: 0,
  })

  return {
    booksResponse,
    books: computed(() => booksResponse.value.items),
    total: computed(() => booksResponse.value.total),
    totalPages: computed(() => booksResponse.value.total_pages),
    page,
    pageSize,
    searchQuery,
    genreId,
    authorId,
    pending,
    error,
  }
}
