from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .data_manager_interface import DataManagerInterface
from .models import Base, User, Movie


class SQLiteDataManager(DataManagerInterface):
    def __init__(self, db_file_name):
        self.engine = create_engine(f"sqlite:///{db_file_name}")
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def get_all_users(self):
        session = self.Session()
        users = session.query(User).all()
        session.close()
        return [{"id": user.id, "name": user.name} for user in users]

    def get_user_movies(self, user_id):
        session = self.Session()
        user = session.query(User).filter_by(id=user_id).first()
        if not user:
            session.close()
            return []
        movies = [
            {
                "id": movie.id,
                "name": movie.name,
                "director": movie.director,
                "year": movie.year,
                "rating": movie.rating
            }
            for movie in user.movies
        ]
        session.close()
        return movies

    def add_user(self, name):
        session = self.Session()
        user = User(name=name)
        session.add(user)
        session.commit()
        session.close()

    def add_movie(self, name, director, year, rating, user_id):
        session = self.Session()
        movie = Movie(
            name=name,
            director=director,
            year=year,
            rating=rating,
            user_id=user_id
        )
        session.add(movie)
        session.commit()
        session.close()

    def update_movie(self, movie_id, name=None, director=None, year=None, rating=None):
        session = self.Session()
        movie = session.query(Movie).filter_by(id=movie_id).first()
        if movie:
            if name: movie.name = name
            if director: movie.director = director
            if year: movie.year = year
            if rating: movie.rating = rating
            session.commit()
        session.close()

    def delete_movie(self, movie_id):
        session = self.Session()
        movie = session.query(Movie).filter_by(id=movie_id).first()
        if movie:
            session.delete(movie)
            session.commit()
        session.close()
