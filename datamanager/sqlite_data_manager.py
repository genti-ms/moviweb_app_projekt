from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from .data_manager_interface import DataManagerInterface
from .models import Base, User, Movie, Review


class SQLiteDataManager(DataManagerInterface):
    def __init__(self, db_file_name):
        """
        Initialize the DataManager with a SQLite database.

        Args:
            db_file_name (str): Path to the SQLite database file.
        """
        self.engine = create_engine(f"sqlite:///{db_file_name}")
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def get_all_users(self):
        """
        Return a list of all users as dicts containing 'id' and 'name'.

        Returns:
            list[dict]: List of users with keys 'id' and 'name'.
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

        Args:
            user_id (int): The ID of the user.

        Returns:
            dict|None: User dict with 'id' and 'name', or None if not found.
        """
        session = self.Session()
        try:
            user = session.query(User).filter_by(id=user_id).first()
            if user:
                return {"id": user.id, "name": user.name}
            return None
        finally:
            session.close()

    def user_exists(self, user_id):
        """
        Check if a user exists by their ID.

        Args:
            user_id (int): The ID of the user.

        Returns:
            bool: True if the user exists, False otherwise.
        """
        session = self.Session()
        try:
            return session.query(User).filter_by(id=user_id).count() > 0
        finally:
            session.close()

    def get_user_movies(self, user_id):
        """
        Return a list of movies belonging to a user as dicts.
        Uses a JOIN query for better performance.

        Args:
            user_id (int): The user ID whose movies to retrieve.

        Returns:
            list[dict]: List of movies with details, empty if none found.
        """
        session = self.Session()
        try:
            # JOIN User and Movie to get movies directly without lazy loading
            movies = (
                session.query(Movie)
                .join(User, Movie.user_id == User.id)
                .filter(User.id == user_id)
                .all()
            )
            return [
                {
                    "id": movie.id,
                    "name": movie.name,
                    "director": movie.director,
                    "year": movie.year,
                    "rating": movie.rating,
                }
                for movie in movies
            ]
        finally:
            session.close()

    def get_movie_by_id(self, movie_id):
        """
        Return a movie dict by ID or None if not found.

        Args:
            movie_id (int): The movie ID.

        Returns:
            dict|None: Movie details or None if not found.
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

        Args:
            name (str): Name of the new user.

        Raises:
            SQLAlchemyError: If database operation fails.
        """
        session = self.Session()
        try:
            user = User(name=name)
            session.add(user)
            session.commit()
        except SQLAlchemyError:
            session.rollback()
            raise
        finally:
            session.close()

    def add_movie(self, name, director, year, rating, user_id):
        """
        Add a new movie with the specified details for a user.

        Args:
            name (str): Movie name.
            director (str|None): Movie director.
            year (int|None): Release year.
            rating (float|None): Movie rating.
            user_id (int): ID of the user who owns the movie.

        Raises:
            SQLAlchemyError: If database operation fails.
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
        except SQLAlchemyError:
            session.rollback()
            raise
        finally:
            session.close()

    def update_movie(self, movie_id, name=None, director=None, year=None, rating=None):
        """
        Update the fields of a movie if specified.

        Args:
            movie_id (int): ID of the movie to update.
            name (str|None): New name.
            director (str|None): New director.
            year (int|None): New year.
            rating (float|None): New rating.

        Returns:
            bool: True if update succeeded, False if movie not found.

        Raises:
            SQLAlchemyError: If database operation fails.
        """
        session = self.Session()
        try:
            movie = session.query(Movie).filter_by(id=movie_id).first()
            if not movie:
                return False
            if name is not None:
                movie.name = name
            if director is not None:
                movie.director = director
            if year is not None:
                movie.year = year
            if rating is not None:
                movie.rating = rating
            session.commit()
            return True
        except SQLAlchemyError:
            session.rollback()
            raise
        finally:
            session.close()

    def delete_movie(self, movie_id):
        """
        Delete a movie by its ID.

        Args:
            movie_id (int): ID of the movie to delete.

        Raises:
            SQLAlchemyError: If database operation fails.
        """
        session = self.Session()
        try:
            movie = session.query(Movie).filter_by(id=movie_id).first()
            if movie:
                session.delete(movie)
                session.commit()
        except SQLAlchemyError:
            session.rollback()
            raise
        finally:
            session.close()

    def add_review(self, user_id, movie_id, review_text, rating):
        """
        Add a review for a movie by a specific user.

        Args:
            user_id (int): ID of the user making the review.
            movie_id (int): ID of the movie being reviewed.
            review_text (str): Review content.
            rating (float): Review rating.

        Raises:
            SQLAlchemyError: If database operation fails.
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
        except SQLAlchemyError:
            session.rollback()
            raise
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
