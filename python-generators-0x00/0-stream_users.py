import mysql.connector
from mysql.connector import Error

import os
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_USER = os.getenv('DB_USER', 'root')
DB_PASSWORD = os.getenv('DB_PASSWORD', '')
DB_NAME = 'ALX_prodev'

def stream_users():
    conn = None
    my_cursor = None
    try:
        conn = mysql.connector.connect(
            host = DB_HOST,
            user = DB_USER,
            passwd = DB_PASSWORD,
            database = DB_NAME
        )
        print("connection established")


        my_cursor = conn.cursor(dictionary = True)

        my_cursor.execute(" SELECT * FROM user_data")

        while True:
            row = my_cursor.fetchone()
            if row is None:
                break
            yield row

    except Error as e:
        print(f"Database error : {e}")
        raise
    finally:

            my_cursor.close()
            conn.close()
            print("Database connection closed.")

if __name__ == "__main__":
  print("\nStreaming users:")
for user in stream_users():
    print(user)


