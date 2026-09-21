from database import DB_PATH, initialize_database

if __name__ == "__main__":
    initialize_database()
    print(f"Created/updated {DB_PATH}")
