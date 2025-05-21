from sqlite_data_manager import SQLiteDataManager

def main():
    dm = SQLiteDataManager("db.sqlite")

    dm.add_user("Anna")
    dm.add_user("Max")

    dm.add_movie("Inception", "Christopher Nolan", 2010, 8.8, 1)
    dm.add_movie("The Matrix", "The Wachowskis", 1999, 8.7, 1)
    dm.add_movie("Interstellar", "Christopher Nolan", 2014, 8.6, 2)

    print("Users:", dm.get_all_users())
    print("Movies for user 1:", dm.get_user_movies(1))

if __name__ == "__main__":
    main()
