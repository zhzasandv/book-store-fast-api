import type { Book } from '~/types/book'

export function useBooks() {
  const config = useRuntimeConfig()
  const searchQuery = ref('')

  const { data, pending, error } = useFetch<Book[]>(
    () => searchQuery.value.trim()
      ? `${config.public.apiBase}/api/v1/books/search?q=${encodeURIComponent(searchQuery.value.trim())}`
      : `${config.public.apiBase}/api/v1/books/`,
    { watch: [searchQuery] }
  )

  const books = computed(() => data.value ?? [])

  return { searchQuery, books, pending, error }
}
