from data_manager_interface import DataManagerInterface

class DataManager(DataManagerInterface):
    def __init__(self):
        # Example in-memory data storage
        self.users = {
            1: {"name": "Anna", "movies": [101, 102]},
            2: {"name": "Max", "movies": [103]}
        }
        self.movies = {
            101: {"name": "Inception", "director": "Christopher Nolan", "year": 2010, "rating": 8.8},
            102: {"name": "The Matrix", "director": "The Wachowskis", "year": 1999, "rating": 8.7},
            103: {"name": "Interstellar", "director": "Christopher Nolan", "year": 2014, "rating": 8.6}
        }

    def get_all_users(self):
        return self.users

    def get_user_movies(self, user_id):
        if user_id not in self.users:
            return []
        movie_ids = self.users[user_id]["movies"]
        return [self.movies[movie_id] for movie_id in movie_ids if movie_id in self.movies]


