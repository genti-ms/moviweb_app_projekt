from data_manager import DataManager

def main():
    dm = DataManager()
    users = dm.get_all_users()
    print("Users:", users)

    user_id = 1
    movies = dm.get_user_movies(user_id)
    print(f"Movies for user {user_id}:", movies)

if __name__ == "__main__":
    main()
