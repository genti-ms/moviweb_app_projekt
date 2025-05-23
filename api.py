from flask import Blueprint, jsonify, request
from datamanager.sqlite_data_manager import SQLiteDataManager


api = Blueprint('api', __name__)
data_manager = SQLiteDataManager("db.sqlite")  #

@api.route('/users', methods=['GET'])
def get_users():
    """
    Get a list of all users.

    Returns:
        JSON list of users, each user is a dict with 'id' and 'name'.
    """
    users = data_manager.get_all_users()
    return jsonify(users)


@api.route('/users/<int:user_id>/movies', methods=['GET'])
def get_user_movies(user_id):
    """
    Get all favorite movies for a specific user.

    Args:
        user_id (int): The ID of the user.

    Returns:
        JSON list of movies if found,
        or JSON error message with 404 status if no movies or user not found.
    """
    movies = data_manager.get_user_movies(user_id)
    if movies:
        return jsonify(movies)
    else:
        return jsonify({"error": "User or movies not found"}), 404


@api.route('/users/<int:user_id>/movies', methods=['POST'])
def add_user_movie(user_id):
    """
    Add a new movie for a specific user.

    Expects JSON body with at least:
        - name (str): The movie name (required)
        - director (str, optional)
        - year (int, optional)
        - rating (float, optional)

    Args:
        user_id (int): The ID of the user.

    Returns:
        JSON success message with 201 status on success,
        or JSON error message with 400 status if required data missing.
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "Request body must be JSON"}), 400

    name = data.get("name")
    director = data.get("director")
    year = data.get("year")
    rating = data.get("rating")

    if not name:
        return jsonify({"error": "Movie name is required"}), 400

    data_manager.add_movie(name, director, year, rating, user_id)
    return jsonify({"message": f"Movie '{name}' added for user {user_id}"}), 201
