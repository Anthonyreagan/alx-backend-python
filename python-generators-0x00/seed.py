import mysql.connector
from mysql.connector import Error
import uuid
import csv
from typing import Generator, Dict, Any
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database configuration
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_USER = os.getenv('DB_USER', 'root')
DB_PASSWORD = os.getenv('DB_PASSWORD', '')
DB_NAME = 'ALX_prodev'


def connect_db() -> mysql.connector.connection.MySQLConnection:
    """Connect to the MySQL database server"""
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD
        )
        print("Connected to MySQL server")
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        raise


def create_database(connection: mysql.connector.connection.MySQLConnection) -> None:
    """Create the ALX_prodev database if it doesn't exist"""
    cursor = connection.cursor()
    try:
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
        print(f"Database {DB_NAME} created or already exists")
    except Error as e:
        print(f"Error creating database: {e}")
        raise
    finally:
        cursor.close()


def connect_to_prodev() -> mysql.connector.connection.MySQLConnection:
    """Connect to the ALX_prodev database in MySQL"""
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        print(f"Connected to database {DB_NAME}")
        return connection
    except Error as e:
        print(f"Error connecting to database {DB_NAME}: {e}")
        raise


def create_table(connection: mysql.connector.connection.MySQLConnection) -> None:
    """Create the user_data table if it doesn't exist"""
    cursor = connection.cursor()
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_data (
                user_id VARCHAR(36) PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                age DECIMAL(10,2) NOT NULL,
                INDEX (user_id)
            )
        """)
        print("Table user_data created or already exists")
        connection.commit()
    except Error as e:
        print(f"Error creating table: {e}")
        raise
    finally:
        cursor.close()


def read_csv_data(file_path: str) -> Generator[Dict[str, Any], None, None]:
    """Generator to read CSV data row by row"""
    with open(file_path, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            yield row


def insert_data(connection: mysql.connector.connection.MySQLConnection, data: Dict[str, Any]) -> None:
    """Insert data into the database if it doesn't exist"""
    cursor = connection.cursor()
    try:
        # Check if user exists
        cursor.execute("SELECT 1 FROM user_data WHERE user_id = %s", (data['user_id'],))
        if cursor.fetchone() is None:
            cursor.execute("""
                INSERT INTO user_data (user_id, name, email, age)
                VALUES (%s, %s, %s, %s)
            """, (data['user_id'], data['name'], data['email'], float(data['age'])))
            connection.commit()
    except Error as e:
        print(f"Error inserting data: {e}")
        connection.rollback()
        raise
    finally:
        cursor.close()


def stream_users(connection: mysql.connector.connection.MySQLConnection) -> Generator[Dict[str, Any], None, None]:
    """Generator to stream users from database one by one"""
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute("SELECT user_id, name, email, age FROM user_data")
        while True:
            row = cursor.fetchone()
            if row is None:
                break
            yield row
    finally:
        cursor.close()


def main():
    # Step 1: Connect to MySQL server
    connection = connect_db()

    # Step 2: Create database
    create_database(connection)
    connection.close()

    # Step 3: Connect to ALX_prodev database
    prodev_connection = connect_to_prodev()

    # Step 4: Create table
    create_table(prodev_connection)

    # Step 5: Insert data from CSV
    csv_file = 'user_data.csv'
    if os.path.exists(csv_file):
        for row in read_csv_data(csv_file):
            # Ensure user_id exists or generate one
            if 'user_id' not in row or not row['user_id']:
                row['user_id'] = str(uuid.uuid4())
            insert_data(prodev_connection, row)
        print("Data inserted successfully")
    else:
        print(f"CSV file {csv_file} not found")

    # Step 6: Demonstrate streaming
    print("\nStreaming users from database:")
    for user in stream_users(prodev_connection):
        print(user)

    prodev_connection.close()


if __name__ == "__main__":
    main()