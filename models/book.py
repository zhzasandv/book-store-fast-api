from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, Table
from sqlalchemy.orm import relationship
from database import Base


book_author = Table(
    "market_book_authors",
    Base.metadata,
    Column("book_id", Integer, ForeignKey("market_book.id")),
    Column("author_id", Integer, ForeignKey("market_author.id")),
)


class Author(Base):
    __tablename__ = "market_author"

    id = Column(Integer, primary_key=True)
    first_name = Column(String(30))
    last_name = Column(String(30))

    books = relationship("Book", secondary=book_author, back_populates="authors")


class Genre(Base):
    __tablename__ = "market_genre"

    id = Column(Integer, primary_key=True)
    name = Column(String(20))

    books = relationship("Book", back_populates="genre")


class Book(Base):
    __tablename__ = "market_book"

    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    price = Column(Numeric(7, 2))
    title = Column(String(1000))
    publication_date = Column(String(15))
    oblojka = Column(String, nullable=True)
    genre_id = Column(Integer, ForeignKey("market_genre.id"))

    genre = relationship("Genre", back_populates="books")
    authors = relationship("Author", secondary=book_author, back_populates="books")
