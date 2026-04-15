<script setup lang="ts">
const route = useRoute()
const router = useRouter()
const { buildLibraryQuery } = useLibraryQuery()

const isHomePage = computed(() => route.path === '/')
const searchInput = ref('')

watch(
  () => route.query.q,
  (value) => {
    searchInput.value = typeof value === 'string' ? value : ''
  },
  { immediate: true }
)

const navigationItems = [
  { label: 'Главная', to: '/' },
  { label: 'Библиотека', to: '/library' },
  { label: 'Жанры', to: '/genres' },
  { label: 'Авторы', to: '/authors' },
]

async function submitSearch() {
  const nextQuery = searchInput.value.trim()

  await router.push({
    path: '/library',
    query: buildLibraryQuery({
      q: nextQuery || null,
      page: null,
    }),
  })
}
</script>

<template>
  <div class="app-shell" :class="{ compact: !isHomePage }">
    <div class="background-glow background-glow-left" />
    <div class="background-glow background-glow-right" />

    <header class="site-header">
      <nav class="main-nav" aria-label="Основная навигация">
        <NuxtLink
          v-for="item in navigationItems"
          :key="item.to"
          class="nav-link"
          :class="{ active: route.path === item.to }"
          :to="item.to"
        >
          {{ item.label }}
        </NuxtLink>
      </nav>

      <div class="brand-block" :aria-hidden="!isHomePage">
        <NuxtLink class="brand-link" to="/" aria-label="На главную">
          <div class="brand-mark" aria-hidden="true">
            <svg viewBox="0 0 160 160" class="brand-logo">
              <defs>
                <linearGradient id="logoFill" x1="0%" y1="0%" x2="100%" y2="100%">
                  <stop offset="0%" stop-color="#f6c453" />
                  <stop offset="50%" stop-color="#f97316" />
                  <stop offset="100%" stop-color="#ef4444" />
                </linearGradient>
              </defs>
              <path d="M28 44c0-8 6-14 14-14h40c21 0 39 17 39 39 0 22-18 39-39 39H42c-8 0-14-6-14-14V44Z" fill="url(#logoFill)" opacity="0.95" />
              <path d="M48 48h28c14 0 26 11 26 26s-12 26-26 26H48V48Z" fill="#16151f" opacity="0.92" />
              <path d="M82 44h36c8 0 14 6 14 14v38c0 8-6 14-14 14H82c18-6 29-20 29-36 0-16-11-29-29-30Z" fill="#fff2cf" opacity="0.9" />
              <circle cx="103" cy="76" r="8" fill="#f97316" />
              <path d="M57 60h15M57 74h23M57 88h18" stroke="#f8fafc" stroke-width="6" stroke-linecap="round" />
            </svg>
          </div>

          <div class="brand-copy">
            <p class="brand-kicker">Aster Archive</p>
            <h1 class="brand-title">Книжный причал</h1>
          </div>
        </NuxtLink>
      </div>

      <form class="global-search" @submit.prevent="submitSearch">
        <input
          v-model="searchInput"
          class="global-search-input"
          type="search"
          placeholder="Искать книги, авторов и жанры"
        />
        <button class="global-search-button" type="submit">
          Найти
        </button>
      </form>
    </header>

    <main class="page-stage">
      <NuxtPage />
    </main>
  </div>
</template>

<style>
:root {
  --bg-base: #0d0d14;
  --bg-panel: rgba(20, 20, 31, 0.82);
  --bg-panel-strong: rgba(12, 12, 22, 0.92);
  --line-soft: rgba(255, 255, 255, 0.1);
  --text-main: #f8f5ee;
  --text-muted: #bdb8ae;
  --accent-gold: #f6c453;
  --accent-orange: #f97316;
  --accent-ink: #1f1a17;
}

html,
body,
#__nuxt {
  min-height: 100%;
}

body {
  margin: 0;
  background:
    radial-gradient(circle at 15% 20%, rgba(246, 196, 83, 0.18), transparent 22%),
    radial-gradient(circle at 82% 18%, rgba(249, 115, 22, 0.16), transparent 24%),
    linear-gradient(180deg, #17111a 0%, #0d0d14 40%, #090a11 100%);
  color: var(--text-main);
  font-family: Georgia, 'Times New Roman', serif;
}

a {
  color: inherit;
}

.app-shell {
  position: relative;
  min-height: 100vh;
  overflow-x: hidden;
}

.background-glow {
  position: fixed;
  z-index: 0;
  width: 32rem;
  height: 32rem;
  filter: blur(80px);
  opacity: 0.26;
  pointer-events: none;
}

.background-glow-left {
  top: -8rem;
  left: -10rem;
  background: #f59e0b;
}

.background-glow-right {
  top: 8rem;
  right: -12rem;
  background: #c2410c;
}

.site-header,
.page-stage {
  position: relative;
  z-index: 1;
}

.site-header {
  min-height: 48vh;
  display: grid;
  align-content: start;
  justify-items: center;
  gap: 1rem;
  padding: 1.5rem 1.25rem 1.2rem;
  transition:
    min-height 1.35s cubic-bezier(0.16, 1, 0.3, 1),
    padding 1.35s cubic-bezier(0.16, 1, 0.3, 1),
    gap 1.35s cubic-bezier(0.16, 1, 0.3, 1),
    background-color 1.15s ease,
    border-color 1.15s ease;
}

.app-shell.compact .site-header {
  position: sticky;
  top: 0;
  min-height: auto;
  gap: 0.78rem;
  padding: 0.9rem 1.25rem 1rem;
  background: rgba(9, 10, 17, 0.72);
  backdrop-filter: blur(20px);
  border-bottom: 1px solid var(--line-soft);
}

.main-nav {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 0.6rem;
  padding: 0.45rem;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.08);
  transition:
    padding 1.15s cubic-bezier(0.16, 1, 0.3, 1),
    gap 1.15s cubic-bezier(0.16, 1, 0.3, 1),
    background-color 1s ease,
    transform 1.15s cubic-bezier(0.16, 1, 0.3, 1);
}

.app-shell.compact .main-nav {
  gap: 0.55rem;
  padding: 0.4rem;
  transform: translateY(-0.05rem);
}

.nav-link {
  padding: 0.7rem 1.15rem;
  border-radius: 999px;
  color: var(--text-muted);
  text-decoration: none;
  letter-spacing: 0.04em;
  font-size: 0.92rem;
  transition:
    padding 0.75s cubic-bezier(0.22, 1, 0.36, 1),
    background-color 0.25s ease,
    color 0.25s ease,
    transform 0.25s ease;
}

.app-shell.compact .nav-link {
  padding: 0.62rem 1rem;
}

.nav-link:hover,
.nav-link.active {
  background: rgba(246, 196, 83, 0.14);
  color: var(--text-main);
  transform: translateY(-1px);
}

.brand-block {
  max-height: 14rem;
  opacity: 1;
  overflow: hidden;
  pointer-events: auto;
  transform: translateY(0) scale(1);
  transform-origin: center top;
  transition:
    max-height 1.35s cubic-bezier(0.16, 1, 0.3, 1),
    opacity 1.05s ease,
    transform 1.35s cubic-bezier(0.16, 1, 0.3, 1);
}

.app-shell.compact .brand-block {
  max-height: 0;
  opacity: 0;
  pointer-events: none;
  transform: translateY(-1.2rem) scale(0.9);
}

.brand-link {
  display: grid;
  justify-items: center;
  gap: 0.7rem;
  text-decoration: none;
}

.brand-mark {
  width: 4.9rem;
  height: 4.9rem;
  padding: 0.55rem;
  border-radius: 1.4rem;
  background:
    linear-gradient(145deg, rgba(255, 245, 220, 0.12), rgba(249, 115, 22, 0.08)),
    rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(246, 196, 83, 0.28);
  box-shadow: 0 20px 80px rgba(0, 0, 0, 0.35);
}

.brand-logo {
  width: 100%;
  height: 100%;
  display: block;
}

.brand-copy {
  text-align: center;
}

.brand-kicker {
  margin: 0 0 0.35rem;
  color: #f2c96d;
  font-size: 0.76rem;
  letter-spacing: 0.24em;
  text-transform: uppercase;
}

.brand-title {
  margin: 0;
  font-size: clamp(2rem, 4.8vw, 3.9rem);
  line-height: 1;
  font-weight: 700;
  letter-spacing: 0.03em;
}

.global-search {
  width: min(42rem, calc(100vw - 2rem));
  display: grid;
  grid-template-columns: minmax(0, 1fr) auto;
  gap: 0.75rem;
  transition:
    transform 1.35s cubic-bezier(0.16, 1, 0.3, 1),
    width 1.35s cubic-bezier(0.16, 1, 0.3, 1),
    gap 1.15s cubic-bezier(0.16, 1, 0.3, 1),
    opacity 1s ease;
}

.app-shell.compact .global-search {
  width: min(38rem, calc(100vw - 2rem));
  transform: translateY(-0.25rem);
}

.global-search-input,
.global-search-button {
  border: 0;
  border-radius: 999px;
  font: inherit;
}

.global-search-input {
  min-width: 0;
  padding: 1rem 1.35rem;
  background: rgba(255, 249, 240, 0.88);
  color: #201b18;
  box-shadow: inset 0 0 0 1px rgba(68, 40, 18, 0.12);
  transition:
    padding 1.15s cubic-bezier(0.16, 1, 0.3, 1),
    box-shadow 0.4s ease;
}

.global-search-button {
  padding: 0 1.5rem;
  background: linear-gradient(135deg, var(--accent-gold), var(--accent-orange));
  color: var(--accent-ink);
  font-weight: 700;
  cursor: pointer;
  transition:
    padding 1.15s cubic-bezier(0.16, 1, 0.3, 1),
    transform 0.25s ease;
}

.app-shell.compact .global-search-input {
  padding: 0.82rem 1.2rem;
}

.app-shell.compact .global-search-button {
  padding: 0 1.25rem;
}

.page-stage {
  padding: 0 1.25rem 3rem;
  animation: page-reveal 0.75s cubic-bezier(0.22, 1, 0.36, 1);
}

@keyframes page-reveal {
  from {
    opacity: 0;
    transform: translateY(0.7rem);
  }

  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@media (max-width: 720px) {
  .site-header {
    padding-top: 1.2rem;
  }

  .main-nav {
    width: 100%;
    border-radius: 1.25rem;
  }

  .nav-link {
    flex: 1 1 calc(50% - 0.6rem);
    text-align: center;
  }

  .global-search {
    grid-template-columns: 1fr;
  }

  .global-search-button {
    min-height: 3.25rem;
  }

  .app-shell.compact .brand-block {
    transform: scale(0.82);
  }

  .page-stage {
    padding-left: 1rem;
    padding-right: 1rem;
  }
}
</style>
