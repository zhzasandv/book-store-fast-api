<template>
  <section class="home-page">
    <div class="home-card">
      <p class="home-kicker">Домашняя палуба</p>
      <h2 class="home-title">Каталог, который начинается как витрина, а работает как библиотека.</h2>
      <p class="home-text">
        На главной остаются только атмосфера и поиск. Дальше пользователь уходит в библиотеку, жанры и авторов,
        а шапка сайта плавно поднимается наверх и превращается в рабочую навигацию.
      </p>

      <div class="home-actions">
        <NuxtLink class="home-link primary" to="/library">
          Открыть библиотеку
        </NuxtLink>
        <NuxtLink class="home-link" to="/genres">
          Смотреть жанры
        </NuxtLink>
        <NuxtLink class="home-link" to="/authors">
          Смотреть авторов
        </NuxtLink>
      </div>
    </div>
  </section>
</template>

<style scoped>
.home-page {
  display: flex;
  justify-content: center;
  padding-bottom: 5rem;
}

.home-card {
  width: min(52rem, 100%);
  padding: 2rem 2.2rem;
  border-radius: 2rem;
  background:
    linear-gradient(145deg, rgba(255, 255, 255, 0.07), rgba(255, 255, 255, 0.02)),
    rgba(14, 15, 25, 0.76);
  border: 1px solid rgba(255, 255, 255, 0.08);
  box-shadow: 0 30px 80px rgba(0, 0, 0, 0.28);
  text-align: center;
}

.home-kicker {
  margin: 0 0 0.85rem;
  color: #f2c96d;
  text-transform: uppercase;
  letter-spacing: 0.18em;
  font-size: 0.84rem;
}

.home-title {
  margin: 0;
  font-size: clamp(2rem, 4vw, 3.3rem);
  line-height: 1.04;
}

.home-text {
  margin: 1.2rem auto 0;
  max-width: 40rem;
  color: #c9c1b5;
  font-size: 1.04rem;
  line-height: 1.7;
}

.home-actions {
  display: flex;
  justify-content: center;
  gap: 0.8rem;
  flex-wrap: wrap;
  margin-top: 1.8rem;
}

.home-link {
  padding: 0.9rem 1.3rem;
  border-radius: 999px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  background: rgba(255, 255, 255, 0.05);
  color: #f8f5ee;
  text-decoration: none;
}

.home-link.primary {
  background: linear-gradient(135deg, #f6c453, #f97316);
  color: #231a14;
  border-color: transparent;
  font-weight: 700;
}

@media (max-width: 640px) {
  .home-card {
    padding: 1.5rem;
  }
}
</style>
