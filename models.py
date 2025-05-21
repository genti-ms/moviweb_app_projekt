from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    movies = relationship("Movie", back_populates="user")

class Movie(Base):
    __tablename__ = "movies"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    director = Column(String)
    year = Column(Integer)
    rating = Column(Float)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="movies")
