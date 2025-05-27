import os
import re
from flask import Flask, render_template, request, redirect, url_for, abort, flash
from dotenv import load_dotenv
from datamanager.sqlite_data_manager import SQLiteDataManager
from api import api

data_manager = SQLiteDataManager('db.sqlite')

app = Flask(__name__)
app.config['DATA_MANAGER'] = data_manager

# Initialize DataManager with the correct database file
DATABASE_PATH = os.getenv("DATABASE_PATH", "db.sqlite")
data_manager = SQLiteDataManager(DATABASE_PATH)

app.register_blueprint(api, url_prefix='/api')


def get_user_or_404(user_id):
    """Helper to get user or abort with 404."""
    user = data_manager.get_user_by_id(user_id)
    if not user:
        abort(404, description="User not found")
    return user


def get_movie_or_404(movie_id, user_id=None):
    """Helper to get movie or abort. If user_id provided, ensure movie belongs to user."""
    movie = data_manager.get_movie_by_id(movie_id)
    if not movie or (user_id and movie['user_id'] != user_id):
        abort(404, description="Movie not found or unauthorized")
    return movie


@app.route('/')
def home():
    """Home page route - simple welcome message."""
    return render_template('home.html')


@app.route('/users')
def list_users():
    """List all users."""
    users = data_manager.get_all_users()
    return render_template('users.html', users=users)


@app.route('/users/<int:user_id>')
def user_movies(user_id):
    """Display all movies of a specific user."""
    user = get_user_or_404(user_id)
    movies = data_manager.get_user_movies(user_id)
    return render_template('user_movies.html', user=user, movies=movies, data_manager=data_manager)


@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    """Add new user with validation."""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()

        if not username:
            flash("Username is required.", "error")
            return render_template('add_user.html'), 400
        if len(username) > 50 or not re.match(r"^[a-zA-Z0-9_ ]+$", username):
            flash("Invalid username.", "error")
            return render_template('add_user.html'), 400
        if data_manager.user_exists(username):
            flash("Username already exists.", "error")
            return render_template('add_user.html'), 400

        data_manager.add_user(username)
        flash(f"User '{username}' added.", "success")
        return redirect(url_for('list_users'))

    return render_template('add_user.html')


@app.route('/users/<int:user_id>/add_movie', methods=['GET', 'POST'])
def add_movie(user_id):
    """Add a movie for a user with full validation."""
    user = get_user_or_404(user_id)

    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        director = request.form.get('director', '').strip()
        year = request.form.get('year', '').strip()
        rating = request.form.get('rating', '').strip()

        if not title:
            flash("Title is required.", "error")
            return render_template('add_movie.html', user=user), 400

        try:
            year = int(year)
            if not (1900 <= year <= 2025):
                raise ValueError
        except ValueError:
            flash("Year must be between 1900 and 2025.", "error")
            return render_template('add_movie.html', user=user), 400

        try:
            rating = float(rating)
            if not (0 <= rating <= 10):
                raise ValueError
        except ValueError:
            flash("Rating must be between 0 and 10.", "error")
            return render_template('add_movie.html', user=user), 400

        data_manager.add_movie(title, director, year, rating, user_id)
        flash(f"Movie '{title}' added.", "success")
        return redirect(url_for('user_movies', user_id=user_id))

    return render_template('add_movie.html', user=user)


@app.route('/users/<int:user_id>/update_movie/<int:movie_id>', methods=['GET', 'POST'])
def update_movie(user_id, movie_id):
    """Update movie info with validation and ownership check."""
    user = get_user_or_404(user_id)
    movie = get_movie_or_404(movie_id, user_id)

    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        director = request.form.get('director', '').strip()
        year = request.form.get('year', '').strip()
        rating = request.form.get('rating', '').strip()

        if not title:
            flash("Title is required.", "error")
            return render_template('update_movie.html', user=user, movie=movie), 400

        try:
            year = int(year)
            if not (1900 <= year <= 2025):
                raise ValueError
        except ValueError:
            flash("Year must be between 1900 and 2025.", "error")
            return render_template('update_movie.html', user=user, movie=movie), 400

        try:
            rating = float(rating)
            if not (0 <= rating <= 10):
                raise ValueError
        except ValueError:
            flash("Rating must be between 0 and 10.", "error")
            return render_template('update_movie.html', user=user, movie=movie), 400

        data_manager.update_movie(movie_id, title, director, year, rating)
        flash(f"Movie '{title}' updated.", "success")
        return redirect(url_for('user_movies', user_id=user_id))

    return render_template('update_movie.html', user=user, movie=movie)


@app.route('/users/<int:user_id>/delete_movie/<int:movie_id>', methods=['POST'])
def delete_movie(user_id, movie_id):
    """Delete a movie securely (POST only) with ownership check."""
    user = get_user_or_404(user_id)
    movie = get_movie_or_404(movie_id, user_id)

    data_manager.delete_movie(movie_id)
    flash(f"Movie '{movie['name']}' deleted.", "success")
    return redirect(url_for('user_movies', user_id=user_id))


@app.route('/users/<int:user_id>/movies/<int:movie_id>/add_review', methods=['GET', 'POST'])
def add_review(user_id, movie_id):
    """Add a review to a user's movie."""
    user = get_user_or_404(user_id)
    movie = get_movie_or_404(movie_id, user_id)

    if request.method == 'POST':
        review_text = request.form.get('review_text', '').strip()
        rating = request.form.get('rating', '').strip()

        if not review_text or not rating:
            flash("Review text and rating required.", "error")
            return render_template('add_review.html', user=user, movie=movie), 400

        try:
            rating = int(rating)
            if not (0 <= rating <= 10):
                raise ValueError
        except ValueError:
            flash("Rating must be 0–10.", "error")
            return render_template('add_review.html', user=user, movie=movie), 400

        data_manager.add_review(user_id, movie_id, review_text, rating)
        flash("Review added!", "success")
        return redirect(url_for('user_movies', user_id=user_id))

    return render_template('add_review.html', user=user, movie=movie)


@app.errorhandler(404)
def page_not_found(e):
    """Custom 404 error page."""
    return render_template('404.html', error=e), 404


@app.errorhandler(500)
def internal_server_error(e):
    """Custom 500 error page."""
    return render_template('500.html', error=e), 500


if __name__ == '__main__':
    app.run(debug=True)
