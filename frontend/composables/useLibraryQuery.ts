export function useLibraryQuery() {
  const route = useRoute()

  function getStringParam(value: string | string[] | undefined) {
    return typeof value === 'string' && value.trim() ? value.trim() : undefined
  }

  function buildLibraryQuery(overrides: Record<string, string | undefined> = {}) {
    const query: Record<string, string> = {}

    const q = overrides.q ?? getStringParam(route.query.q)
    const genreId = overrides.genre_id ?? getStringParam(route.query.genre_id)
    const authorId = overrides.author_id ?? getStringParam(route.query.author_id)
    const page = overrides.page ?? getStringParam(route.query.page)

    if (q) {
      query.q = q
    }

    if (genreId) {
      query.genre_id = genreId
    }

    if (authorId) {
      query.author_id = authorId
    }

    if (page && page !== '1') {
      query.page = page
    }

    return query
  }

  return { buildLibraryQuery }
}
