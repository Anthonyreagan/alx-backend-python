import mysql.connector
from mysql.connector import Error

def stream_users():
    """Generator function that streams rows from user_data table one by one"""
    try:
        # Establish database connection
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='ALX_prodev'
        )
        
        cursor = connection.cursor(dictionary=True)  # Use dictionary cursor to get rows as dicts
        
        # Execute query to fetch all users
        cursor.execute("SELECT * FROM user_data")
        
        # Fetch rows one by one and yield them
        while True:
            row = cursor.fetchone()
            if row is None:
                break
            yield row
            
    except Error as e:
        print(f"Database error: {e}")
    finally:
        # Clean up resources
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals():
            connection.close()