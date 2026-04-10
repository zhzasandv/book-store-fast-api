<script setup lang="ts">
const { searchQuery, books, pending, error } = useBooks()
</script>

<template>
  <div class="page">
    <header class="header">
      <h1 class="site-title">книжки для программистов</h1>
    </header>

    <section class="search-section">
      <input
        v-model="searchQuery"
        class="search-input"
        type="text"
        placeholder="Поиск по названию, автору, жанру..."
      />
    </section>

    <section class="catalog">
      <div v-if="pending" class="state-message">Загрузка...</div>
      <div v-else-if="error" class="state-message error">Не удалось загрузить книги. Убедитесь, что бэкенд запущен.</div>
      <div v-else-if="books.length === 0" class="state-message">Ничего не найдено.</div>
      <div v-else class="books-grid">
        <div v-for="book in books" :key="book.id" class="book-card">
          <div class="book-cover">
            <img v-if="book.image_url" :src="book.image_url" :alt="book.name" />
            <div v-else class="no-cover">нет обложки</div>
          </div>
          <div class="book-info">
            <h3 class="book-name">{{ book.name }}</h3>
            <p class="book-authors">{{ book.authors.map(a => a.name).join(', ') }}</p>
            <p class="book-genre">{{ book.genre.name }}</p>
            <p class="book-price">{{ book.price }} ₸</p>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<style scoped>
* {
  box-sizing: border-box;
}

.page {
  min-height: 100vh;
  background: #0f0f0f;
  color: #e8e8e8;
  font-family: 'Segoe UI', sans-serif;
  padding: 0 0 60px;
}

.header {
  background: #1a1a2e;
  padding: 32px 40px;
  border-bottom: 2px solid #4f46e5;
}

.site-title {
  margin: 0;
  font-size: 2rem;
  font-weight: 700;
  color: #a5b4fc;
  letter-spacing: 0.5px;
}

.search-section {
  max-width: 700px;
  margin: 40px auto 0;
  padding: 0 20px;
}

.search-input {
  width: 100%;
  padding: 14px 20px;
  font-size: 1rem;
  border: 2px solid #2d2d4e;
  border-radius: 12px;
  background: #1e1e2e;
  color: #e8e8e8;
  outline: none;
  transition: border-color 0.2s;
}

.search-input::placeholder {
  color: #666;
}

.search-input:focus {
  border-color: #4f46e5;
}

.catalog {
  max-width: 1200px;
  margin: 40px auto 0;
  padding: 0 20px;
}

.state-message {
  text-align: center;
  color: #888;
  font-size: 1.1rem;
  margin-top: 60px;
}

.state-message.error {
  color: #f87171;
}

.books-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 24px;
}

.book-card {
  background: #1e1e2e;
  border-radius: 12px;
  overflow: hidden;
  border: 1px solid #2d2d4e;
  transition: transform 0.2s, border-color 0.2s;
  cursor: pointer;
}

.book-card:hover {
  transform: translateY(-4px);
  border-color: #4f46e5;
}

.book-cover {
  width: 100%;
  height: 260px;
  overflow: hidden;
  background: #12121f;
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
  color: #444;
  font-size: 0.85rem;
}

.book-info {
  padding: 14px;
}

.book-name {
  margin: 0 0 6px;
  font-size: 0.95rem;
  font-weight: 600;
  color: #e8e8e8;
  line-height: 1.3;
}

.book-authors {
  margin: 0 0 4px;
  font-size: 0.8rem;
  color: #a0a0c0;
}

.book-genre {
  margin: 0 0 10px;
  font-size: 0.75rem;
  color: #6b7280;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.book-price {
  margin: 0;
  font-size: 1rem;
  font-weight: 700;
  color: #a5b4fc;
}
</style>
