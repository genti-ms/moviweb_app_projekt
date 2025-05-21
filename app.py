from flask import Flask, jsonify
from datamanager.sqlite_data_manager import SQLiteDataManager

app = Flask(__name__)
data_manager = SQLiteDataManager('db.sqlite')


@app.route('/')
def home():
    """
    Home route of the MovieWeb App.

    Returns:
        str: Welcome message.
    """
    return "Welcome to MovieWeb App!"


@app.route('/users')
def list_users():
    """
    Returns a JSON list of all users.

    Returns:
        Response: JSON list containing user data (id and name).
    """
    users = data_manager.get_all_users()
    return jsonify(users)


if __name__ == '__main__':
    app.run(debug=True)
