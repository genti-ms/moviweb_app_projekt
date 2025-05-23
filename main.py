from sqlite_data_manager import SQLiteDataManager

def main():
    """
    Simple script to demonstrate adding users and movies
    and then fetching and printing them from the database.
    """
    dm = SQLiteDataManager("db.sqlite")

    # Add users
    dm.add_user("Anna")
    dm.add_user("Max")

    # Add movies for users
    dm.add_movie("Inception", "Christopher Nolan", 2010, 8.8, 1)
    dm.add_movie("The Matrix", "The Wachowskis", 1999, 8.7, 1)
    dm.add_movie("Interstellar", "Christopher Nolan", 2014, 8.6, 2)

    # Fetch and print all users
    users = dm.get_all_users()
    print("Users:", users)

    # Fetch and print movies for user with id=1
    user1_movies = dm.get_user_movies(1)
    print("Movies for user 1:", user1_movies)

if __name__ == "__main__":
    main()
