from flask import Flask, render_template, request, redirect, url_for, abort, flash
from datamanager.sqlite_data_manager import SQLiteDataManager

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # TODO: Move secret key to environment variable for security

# Initialize DataManager with the correct database file
data_manager = SQLiteDataManager('db.sqlite')


def get_user_or_404(user_id):
    """Helper to get user or abort with 404."""
    user = data_manager.get_user_by_id(user_id)
    if not user:
        abort(404, description="User not found")
    return user


def get_movie_or_404(movie_id):
    """Helper to get movie or abort with 404."""
    movie = data_manager.get_movie_by_id(movie_id)
    if not movie:
        abort(404, description="Movie not found")
    return movie


@app.route('/')
def home():
    """Home page route - simple welcome message."""
    return render_template('home.html')


@app.route('/users')
def list_users():
    """
    List all users registered in the app.
    Fetches users from DataManager and passes them to the users.html template.
    """
    users = data_manager.get_all_users()
    return render_template('users.html', users=users)


@app.route('/users/<int:user_id>')
def user_movies(user_id):
    """
    Display all favorite movies of a specific user identified by user_id.
    Pass user info and movie list to the user_movies.html template.
    """
    user = get_user_or_404(user_id)
    movies = data_manager.get_user_movies(user_id)
    return render_template('user_movies.html', user=user, movies=movies)


@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    """
    Show a form to add a new user (GET).
    Process the form submission to create a new user (POST).
    """
    if request.method == 'POST':
        username = request.form.get('username')
        if not username:
            flash("Username is required.", "error")
            return render_template('add_user.html'), 400

        data_manager.add_user(username)
        flash(f"User '{username}' was successfully added.", "success")
        return redirect(url_for('list_users'))

    return render_template('add_user.html')


@app.route('/users/<int:user_id>/add_movie', methods=['GET', 'POST'])
def add_movie(user_id):
    """
    Show form to add a movie for the user (GET).
    On form submission, add the movie to the user's favorite list (POST).
    """
    user = get_user_or_404(user_id)

    if request.method == 'POST':
        title = request.form.get('title')
        director = request.form.get('director')
        year = request.form.get('year')
        rating = request.form.get('rating')

        if not title:
            flash("Movie title is required.", "error")
            return render_template('add_movie.html', user=user), 400

        data_manager.add_movie(title, director, year, rating, user_id)
        flash(f"Movie '{title}' was successfully added.", "success")
        return redirect(url_for('user_movies', user_id=user_id))

    return render_template('add_movie.html', user=user)


@app.route('/users/<int:user_id>/update_movie/<int:movie_id>',
           methods=['GET', 'POST'])
def update_movie(user_id, movie_id):
    """
    Display a form pre-filled with movie details for editing (GET).
    Update the movie details in the database upon submission (POST).
    """
    user = get_user_or_404(user_id)
    movie = get_movie_or_404(movie_id)

    if request.method == 'POST':
        title = request.form.get('title')
        director = request.form.get('director')
        year = request.form.get('year')
        rating = request.form.get('rating')

        if not title:
            flash("Movie title is required.", "error")
            return render_template('update_movie.html', user=user, movie=movie), 400

        data_manager.update_movie(movie_id, title, director, year, rating)
        flash(f"Movie '{title}' was successfully updated.", "success")
        return redirect(url_for('user_movies', user_id=user_id))

    return render_template('update_movie.html', user=user, movie=movie)


@app.route('/users/<int:user_id>/delete_movie/<int:movie_id>')
def delete_movie(user_id, movie_id):
    """
    Delete a movie by its ID from a user's list.
    Redirect back to the user's movie list with a success flash message.
    """
    user = get_user_or_404(user_id)
    movie = get_movie_or_404(movie_id)

    data_manager.delete_movie(movie_id)
    flash(f"Movie '{movie['name']}' has been successfully deleted.", "success")
    return redirect(url_for('user_movies', user_id=user_id))


@app.errorhandler(404)
def page_not_found(e):
    """Render a custom 404 error page."""
    return render_template('404.html', error=e), 404


@app.errorhandler(500)
def internal_server_error(e):
    """Render a custom 500 error page."""
    return render_template('500.html', error=e), 500


if __name__ == '__main__':
    app.run(debug=True)
