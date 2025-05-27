from flask import Blueprint, jsonify, request, current_app

api = Blueprint('api', __name__)

def get_data_manager():
    """
    Retrieve the DataManager instance from the Flask app configuration.

    Raises:
        RuntimeError: If no DataManager is configured in the app.

    Returns:
        SQLiteDataManager: The data manager instance used for data operations.
    """
    data_manager = current_app.config.get("DATA_MANAGER")
    if not data_manager:
        raise RuntimeError("Data manager not configured in app.")
    return data_manager


@api.route('/users', methods=['GET'])
def get_users():
    """
    Retrieve all users.

    Returns:
        Response: JSON response containing a list of all users.
    """
    data_manager = get_data_manager()
    users = data_manager.get_all_users()
    return jsonify(users)


@api.route('/users/<int:user_id>/movies', methods=['GET'])
def get_user_movies(user_id):
    """
    Retrieve all favorite movies for a given user.

    Args:
        user_id (int): ID of the user whose movies are requested.

    Returns:
        Response: JSON response containing the list of movies for the user,
                  or an error message with 404 status if not found.
    """
    data_manager = get_data_manager()
    movies = data_manager.get_user_movies(user_id)
    if movies:
        return jsonify(movies)
    else:
        return jsonify({"error": "User or movies not found"}), 404


@api.route('/users/<int:user_id>/movies', methods=['POST'])
def add_user_movie(user_id):
    """
    Add a new movie to a user's favorite list.

    Expects JSON body with keys:
        - name (str): Movie name (required)
        - director (str, optional)
        - year (int, optional)
        - rating (float, optional)

    Args:
        user_id (int): ID of the user to add the movie to.

    Returns:
        Response: JSON success message with 201 status on success,
                  or error message with 400 status if data is invalid.
    """
    data_manager = get_data_manager()
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
