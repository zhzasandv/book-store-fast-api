<template>
  <section class="home-page">
    <div class="home-card">
      <p class="home-kicker">Домашняя палуба</p>
      <h2 class="home-title">
        Место, где книги, знания и читатели встречаются в одном пространстве
      </h2>
      <p class="home-text">
        Наш каталог создан для тех, кто ищет книги для учебы, профессионального роста
        или чтения для себя. От основ программирования до профессиональной разработки:
        все необходимые материалы собраны в одном каталоге.
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
  padding-bottom: 3rem;
}

.home-card {
  width: min(48rem, 100%);
  padding: 1.55rem 1.8rem;
  border-radius: 1.35rem;
  background:
    linear-gradient(145deg, rgba(255, 255, 255, 0.07), rgba(255, 255, 255, 0.02)),
    rgba(14, 15, 25, 0.76);
  border: 1px solid rgba(255, 255, 255, 0.08);
  box-shadow: 0 20px 56px rgba(0, 0, 0, 0.24);
  text-align: center;
}

.home-kicker {
  margin: 0 0 0.65rem;
  color: #f2c96d;
  text-transform: uppercase;
  letter-spacing: 0.18em;
  font-size: 0.84rem;
}

.home-title {
  margin: 0;
  font-size: clamp(1.65rem, 2.5vw, 2.7rem);
  line-height: 1.08;
}

.home-text {
  margin: 0.9rem auto 0;
  max-width: 38rem;
  color: #c9c1b5;
  font-size: 1rem;
  line-height: 1.58;
}

.home-actions {
  display: flex;
  justify-content: center;
  gap: 0.8rem;
  flex-wrap: wrap;
  margin-top: 1.25rem;
}

.home-link {
  padding: 0.78rem 1.15rem;
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
