from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class User(Base):
    """
    ORM model for users table.
    Each user has a unique id and a name.
    """
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    movies = relationship("Movie", back_populates="user")
    reviews = relationship("Review", back_populates="user")  # Neue Beziehung

class Movie(Base):
    """
    ORM model for movies table.
    Each movie has a name, director, year, rating and belongs to a user.
    """
    __tablename__ = "movies"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    director = Column(String(100), nullable=True)
    year = Column(Integer, nullable=True)
    rating = Column(Float, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="movies")
    reviews = relationship("Review", back_populates="movie")  # Neue Beziehung

class Review(Base):
    """
    ORM model for reviews table.
    Each review belongs to a user and a movie and contains text and a rating.
    """
    __tablename__ = "reviews"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    movie_id = Column(Integer, ForeignKey("movies.id"))
    review_text = Column(String, nullable=False)
    rating = Column(Float, nullable=True)

    user = relationship("User", back_populates="reviews")
    movie = relationship("Movie", back_populates="reviews")
