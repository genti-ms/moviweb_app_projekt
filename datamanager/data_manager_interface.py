from abc import ABC, abstractmethod

class DataManagerInterface(ABC):

    @abstractmethod
    def get_all_users(self):
        """
        Return a list of users.

        Returns:
            List[dict]: A list of users, each user represented as a dictionary with keys 'id' and 'name'.
        """
        pass

    @abstractmethod
    def get_user_movies(self, user_id):
        """
        Return all movies for a specific user.

        Args:
            user_id (int): The ID of the user.

        Returns:
            List[dict]: A list of movies belonging to the user.
        """
        pass
