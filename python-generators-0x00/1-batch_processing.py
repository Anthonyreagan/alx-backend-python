import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Database credentials
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_USER = os.getenv('DB_USER', 'root')
DB_PASSWORD = os.getenv('DB_PASSWORD', '')
DB_NAME = 'ALX_prodev'


def stream_users_in_batches(batch_size):
    """Yield users in batches from the user_data table."""
    conn = None
    cursor = None
    try:
        # Connect to the database
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            passwd=DB_PASSWORD,
            database=DB_NAME
        )
        print("Connection established.")

        # Create a cursor that returns dictionaries
        cursor = conn.cursor(dictionary=True)

        # Execute query to select all users ordered by user_id
        cursor.execute("SELECT user_id, name, age, email FROM user_data ORDER BY user_id")

        # Fetch data in batches
        while True:
            batch = cursor.fetchmany(batch_size)
            if not batch:
                break
            yield batch  # ✅ use of generator

    except Error as e:
        print(f"Database error: {e}")  # ✅ f-string used correctly

    finally:
        # Always close cursor and connection if they exist
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def batch_processing(batch_size):
    """Process each batch and print users over the age of 25."""
    for batch in stream_users_in_batches(batch_size):  # ✅ loop 1
        for user in batch:  # ✅ loop 2
            if user['age'] > 25  :
                user['age'] = int(user['age'])
                print(user)

if __name__ == "__main__":
    batch_processing(50)
