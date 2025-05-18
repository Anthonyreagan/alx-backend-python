import mysql.connector
from mysql.connector import Error

def stream_users_in_batches(batch_size):
    """Generator that fetches users in batches from the database"""
    try:
        # Establish database connection
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='ALX_prodev'
        )
        
        cursor = connection.cursor(dictionary=True)
        
        # Execute query to fetch all users
        cursor.execute("SELECT * FROM user_data")
        
        # Fetch rows in batches
        while True:
            batch = cursor.fetchmany(batch_size)
            if not batch:
                break
            yield batch
            
    except Error as e:
        print(f"Database error: {e}", file=sys.stderr)
    finally:
        # Clean up resources
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals():
            connection.close()

def batch_processing(batch_size):
    """Process batches of users and filter those over age 25"""
    # First loop: iterate through batches
    for batch in stream_users_in_batches(batch_size):
        # Second loop: iterate through users in batch
        for user in batch:
            # Third loop: filter condition (implicit in if statement)
            if user['age'] > 25:
                print(user)
