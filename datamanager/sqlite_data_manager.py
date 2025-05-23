from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .data_manager_interface import DataManagerInterface
from .models import Base, User, Movie, Review




class SQLiteDataManager(DataManagerInterface):
    def __init__(self, db_file_name):
        """
        Initialize the DataManager with a SQLite database.
        """
        self.engine = create_engine(f"sqlite:///{db_file_name}")
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def get_all_users(self):
        """
        Return a list of all users as dicts containing 'id' and 'name'.
        """
        session = self.Session()
        try:
            users = session.query(User).all()
            return [{"id": user.id, "name": user.name} for user in users]
        finally:
            session.close()

    def get_user_by_id(self, user_id):
        """
        Return a user dict by ID or None if not found.
        """
        session = self.Session()
        try:
            user = session.query(User).filter_by(id=user_id).first()
            if user:
                return {"id": user.id, "name": user.name}
            return None
        finally:
            session.close()

    def get_user_movies(self, user_id):
        """
        Return a list of movies belonging to a user as dicts.
        """
        session = self.Session()
        try:
            user = session.query(User).filter_by(id=user_id).first()
            if not user:
                return []
            movies = [
                {
                    "id": movie.id,
                    "name": movie.name,
                    "director": movie.director,
                    "year": movie.year,
                    "rating": movie.rating,
                }
                for movie in user.movies
            ]
            return movies
        finally:
            session.close()

    def get_movie_by_id(self, movie_id):
        """
        Return a movie dict by ID or None if not found.
        """
        session = self.Session()
        try:
            movie = session.query(Movie).filter_by(id=movie_id).first()
            if movie:
                return {
                    "id": movie.id,
                    "name": movie.name,
                    "director": movie.director,
                    "year": movie.year,
                    "rating": movie.rating,
                    "user_id": movie.user_id,
                }
            return None
        finally:
            session.close()

    def add_user(self, name):
        """
        Add a new user with the given name.
        """
        session = self.Session()
        try:
            user = User(name=name)
            session.add(user)
            session.commit()
        finally:
            session.close()

    def add_movie(self, name, director, year, rating, user_id):
        """
        Add a new movie with the specified details for a user.
        """
        session = self.Session()
        try:
            movie = Movie(
                name=name,
                director=director,
                year=year,
                rating=rating,
                user_id=user_id,
            )
            session.add(movie)
            session.commit()
        finally:
            session.close()

    def update_movie(self, movie_id, name=None, director=None, year=None, rating=None):
        """
        Update the fields of a movie if specified.
        """
        session = self.Session()
        try:
            movie = session.query(Movie).filter_by(id=movie_id).first()
            if movie:
                if name is not None:
                    movie.name = name
                if director is not None:
                    movie.director = director
                if year is not None:
                    movie.year = year
                if rating is not None:
                    movie.rating = rating
                session.commit()
        finally:
            session.close()

    def delete_movie(self, movie_id):
        """
        Delete a movie by its ID.
        """
        session = self.Session()
        try:
            movie = session.query(Movie).filter_by(id=movie_id).first()
            if movie:
                session.delete(movie)
                session.commit()
        finally:
            session.close()

    def add_review(self, user_id, movie_id, review_text, rating):
        """
        Add a review for a movie by a specific user.
        """
        session = self.Session()
        try:
            review = Review(
                user_id=user_id,
                movie_id=movie_id,
                review_text=review_text,
                rating=rating,
            )
            session.add(review)
            session.commit()
        finally:
            session.close()

    def get_reviews_for_movie(self, movie_id):
        """
        Retrieve all reviews for a given movie along with the reviewer's username.

        Args:
            movie_id (int): The ID of the movie to get reviews for.

        Returns:
            list of dict: Each dict contains 'review_text', 'rating', and 'username'.
        """
        session = self.Session()
        try:
            reviews = (
                session.query(Review, User)
                .join(User, Review.user_id == User.id)
                .filter(Review.movie_id == movie_id)
                .all()
            )
            return [
                {
                    "review_text": review.review_text,
                    "rating": review.rating,
                    "username": user.name,
                }
                for review, user in reviews
            ]
        finally:
            session.close()


