export interface Author {
  id: number
  name: string
}

export interface Genre {
  id: number
  name: string
}

export interface Book {
  id: number
  name: string
  price: number
  title: string
  publication_date: string
  genre: Genre
  authors: Author[]
  image_url: string | null
}
