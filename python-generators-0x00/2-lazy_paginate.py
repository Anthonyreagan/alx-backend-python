import mysql.connector
from mysql.connector import Error
import  seed

def paginate_users(page_size, offset):
    conn = None
    my_cursor = None

    try:
        conn = seed.connect_to_prodev()
        my_cursor = conn.cursor(dictionary=True)
        my_cursor.execute(f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}")

        rows = my_cursor.fetchall()
        return rows

    except Error as e:
        print(f"Database Error: {e}")

    finally:
        # Always close cursor and connection if they exist
        if my_cursor:
            my_cursor.close()
        if conn:
            conn.close()

def lazy_paginate(page_size):
    offset = 0

    while True:
        page = paginate_users(page_size,offset)
        if not page:
            break
        yield page

        offset =+ page_size

if __name__ == '__main__':
    for page in lazy_paginate(2):
        print("\n =====New page=====")
        for users in page:
            print(users)




