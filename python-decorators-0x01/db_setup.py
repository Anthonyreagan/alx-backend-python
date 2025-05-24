import sqlite3

def database_setup():

    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()

    cursor.execute('''
       CREATE TABLE IF NOT EXISTS users (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          name TEXT NOT NULL,
          email TEXT UNIQUE
          );
    ''')

    users = [
        ('Alice', 'alice@email.com'),
        ('John', 'john@email.com'),
        ('Mary', 'mary@email.com'),
        ('Tony', 'tony@email.com'),
    ]

    cursor.executemany("INSERT OR IGNORE INTO users (name, email) VALUES (?,?)", users)
    connection.commit()
    connection.close()
    print("Database setup complete")

if __name__ == '__main__':
    database_setup()