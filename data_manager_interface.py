from abc import ABC, abstractmethod

class DataManagerInterface(ABC):

    @abstractmethod
    def get_all_users(self):
        """Return a list or dictionary of all users"""
        pass

    @abstractmethod
    def get_user_movies(self, user_id):
        """Return a list of movies for the specified user"""
        pass
