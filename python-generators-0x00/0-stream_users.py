import mysql.connector
import sys
from mysql.connector import Error

def stream_users_in_batches(batch_size):
    """Generator that streams user data in batches"""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='ALX_prodev'
        )
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user_data")

        while True:
            batch = cursor.fetchmany(batch_size)
            if not batch:
                break
            yield batch

    except Error as e:
        print(f"Database error: {e}", file=sys.stderr)
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals():
            connection.close()

def batch_processing(batch_size):
    """Process user batches and filter age > 25"""
    for batch in stream_users_in_batches(batch_size):
        for user in batch:
            if user['age'] > 25:
                print(user)
