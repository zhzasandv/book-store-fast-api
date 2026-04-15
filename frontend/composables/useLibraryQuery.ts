export function useLibraryQuery() {
  const route = useRoute()

  type QueryValue = string | null | undefined
  type QueryKey = 'q' | 'genre_id' | 'genre_name' | 'author_id' | 'author_name' | 'page'
  type QueryOverrides = Partial<Record<QueryKey, QueryValue>>

  function getStringParam(value: string | string[] | undefined) {
    return typeof value === 'string' && value.trim() ? value.trim() : undefined
  }

  function getQueryValue(name: keyof QueryOverrides, overrides: QueryOverrides) {
    if (Object.hasOwn(overrides, name)) {
      return overrides[name] === null ? undefined : overrides[name]
    }

    return getStringParam(route.query[name])
  }

  function buildLibraryQuery(overrides: QueryOverrides = {}) {
    const query: Record<string, string> = {}

    const q = getQueryValue('q', overrides)
    const genreId = getQueryValue('genre_id', overrides)
    const genreName = getQueryValue('genre_name', overrides)
    const authorId = getQueryValue('author_id', overrides)
    const authorName = getQueryValue('author_name', overrides)
    const page = getQueryValue('page', overrides)

    if (q) {
      query.q = q
    }

    if (genreId) {
      query.genre_id = genreId
    }

    if (genreId && genreName) {
      query.genre_name = genreName
    }

    if (authorId) {
      query.author_id = authorId
    }

    if (authorId && authorName) {
      query.author_name = authorName
    }

    if (page && page !== '1') {
      query.page = page
    }

    return query
  }

  return { buildLibraryQuery }
}
