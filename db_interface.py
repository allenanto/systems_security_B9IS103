import sqlite3

def init_db():
    conn = sqlite3.connect('corptalk.db')

    #Creating User table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            mobile TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')

    print("Db createdn")

def create_user(name, email, mobile, password):
    with sqlite3.connect('corptalk.db') as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (name, email, mobile, password) VALUES (?, ?, ?, ?)",
                           (name, email, mobile, password))
            conn.commit()
            print("User added")

# if __name__ == "__main__":
#     init_db()