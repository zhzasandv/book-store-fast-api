<script setup lang="ts">
import type { Author } from '~/types/book'

const config = useRuntimeConfig()

const { data, pending, error } = useFetch<Author[]>(
  `${config.public.apiBase}/api/v1/authors/`
)

const authors = computed(() => data.value ?? [])
</script>

<template>
  <section class="listing-page">
    <div class="listing-header">
      <p class="listing-kicker">Люди и книги</p>
      <h2 class="listing-title">Авторы</h2>
      <p class="listing-text">
        Переход с карточки открывает библиотеку уже с фильтром по выбранному автору.
      </p>
    </div>

    <div v-if="pending" class="state-message">Загрузка авторов...</div>
    <div v-else-if="error" class="state-message error">Не удалось загрузить авторов.</div>
    <div v-else class="listing-grid">
      <NuxtLink
        v-for="author in authors"
        :key="author.id"
        class="listing-card"
        :to="{
          path: '/library',
          query: {
            author_id: String(author.id),
            author_name: `${author.first_name} ${author.last_name}`,
          },
        }"
      >
        <p class="listing-card-label">Автор</p>
        <h3>{{ author.first_name }} {{ author.last_name }}</h3>
        <span class="listing-card-action">Открыть подборку</span>
      </NuxtLink>
    </div>
  </section>
</template>

<style scoped>
.listing-page {
  width: min(1100px, 100%);
  margin: 0 auto;
}

.listing-header {
  margin-bottom: 1.35rem;
  padding: 1.6rem 1.7rem;
  border-radius: 1.8rem;
  background:
    linear-gradient(145deg, rgba(255, 255, 255, 0.05), rgba(255, 255, 255, 0.015)),
    rgba(13, 14, 23, 0.84);
  border: 1px solid rgba(255, 255, 255, 0.08);
}

.listing-kicker {
  margin: 0 0 0.45rem;
  color: #f2c96d;
  text-transform: uppercase;
  letter-spacing: 0.18em;
  font-size: 0.82rem;
}

.listing-title {
  margin: 0;
  font-size: clamp(1.9rem, 3vw, 2.8rem);
}

.listing-text {
  margin: 0.9rem 0 0;
  color: #c9c1b5;
}

.state-message {
  text-align: center;
  padding: 3rem 0;
  color: #c9c1b5;
}

.state-message.error {
  color: #fca5a5;
}

.listing-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 1.15rem;
}

.listing-card {
  display: grid;
  gap: 0.9rem;
  padding: 1.4rem;
  border-radius: 1.5rem;
  text-decoration: none;
  background:
    linear-gradient(160deg, rgba(249, 115, 22, 0.12), rgba(255, 255, 255, 0.03)),
    rgba(13, 14, 23, 0.84);
  border: 1px solid rgba(255, 255, 255, 0.08);
  transition: transform 0.25s ease, border-color 0.25s ease;
}

.listing-card:hover {
  transform: translateY(-4px);
  border-color: rgba(249, 115, 22, 0.4);
}

.listing-card h3,
.listing-card-label,
.listing-card-action {
  margin: 0;
}

.listing-card-label {
  color: #f9a257;
  text-transform: uppercase;
  letter-spacing: 0.16em;
  font-size: 0.75rem;
}

.listing-card-action {
  color: #fdc08b;
}

@media (max-width: 900px) {
  .listing-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 560px) {
  .listing-grid {
    grid-template-columns: 1fr;
  }
}
</style>
