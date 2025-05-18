#!/usr/bin/python3
import mysql.connector
from mysql.connector import Error

def stream_user_ages():
    """Generator that streams user ages one by one from database"""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='ALX_prodev'
        )
        cursor = connection.cursor()
        
        # Only select age column to minimize data transfer
        cursor.execute("SELECT age FROM user_data")
        
        while True:
            row = cursor.fetchone()
            if row is None:
                break
            yield row[0]  # Yield just the age value
            
    except Error as e:
        print(f"Database error: {e}")
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals():
            connection.close()

def calculate_average_age():
    """Calculates average age using the streaming generator"""
    total = 0
    count = 0
    
    # First loop: iterate through ages from generator
    for age in stream_user_ages():
        total += age
        count += 1
    
    # Calculate average if we have data
    if count > 0:
        average = total / count
        print(f"Average age of users: {average:.2f}")
    else:
        print("No user data found")

if __name__ == "__main__":
    calculate_average_age()
