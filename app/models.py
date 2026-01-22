from sqlalchemy import Table, Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship

from app.database import Base


favorite_books = Table(
    "favorites",   # ✅ вот так!
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("book_id", Integer, ForeignKey("books.id"), primary_key=True),
)


book_authors = Table(
    "book_authors",
    Base.metadata,
    Column("book_id", ForeignKey("books.id"), primary_key=True),
    Column("author_id", ForeignKey("authors.id"), primary_key=True),
)


book_genres = Table(
    "book_genres",
    Base.metadata,
    Column("book_id", ForeignKey("books.id"), primary_key=True),
    Column("genre_id", ForeignKey("genres.id"), primary_key=True),
)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String, default="client", nullable=False)

    favorites = relationship(
        "Book", secondary=favorite_books, back_populates="liked_by")


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)

    authors = relationship(
        "Author", secondary=book_authors, back_populates="books")
    genres = relationship("Genre", secondary=book_genres,
                          back_populates="books")

    liked_by = relationship(
        "User", secondary=favorite_books, back_populates="favorites")


class Author(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    books = relationship("Book", secondary=book_authors,
                         back_populates="authors")


class Genre(Base):
    __tablename__ = "genres"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

    books = relationship("Book", secondary=book_genres,
                         back_populates="genres")
