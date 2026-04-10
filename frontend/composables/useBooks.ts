import type { Book } from '~/types/book'

export function useBooks() {
  const config = useRuntimeConfig()
  const searchQuery = ref('')

  const { data: books, pending, error } = useFetch<Book[]>(`${config.public.apiBase}/api/v1/books/`)

  const filteredBooks = computed(() => {
    if (!books.value) return []
    const q = searchQuery.value.toLowerCase().trim()
    if (!q) return books.value
    return books.value.filter(book =>
      book.name.toLowerCase().includes(q) ||
      book.title.toLowerCase().includes(q) ||
      book.authors.some(a => a.name.toLowerCase().includes(q)) ||
      book.genre.name.toLowerCase().includes(q)
    )
  })

  return { searchQuery, filteredBooks, pending, error }
}
