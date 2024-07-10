import sqlite3

def init_db():
    conn = sqlite3.connect('corptalk.db')
    print("db connection")

if __name__ == "__main__":
    init_db()