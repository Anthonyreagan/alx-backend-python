import mysql.connector
from mysql.connector import Error
import uuid
import csv
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
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        raise


def create_database(connection: mysql.connector.connection.MySQLConnection) -> None:
    """Create the ALX_prodev database if it doesn't exist"""
    cursor = connection.cursor()
    try:
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
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
        connection.commit()
    except Error as e:
        print(f"Error creating table: {e}")
        raise
    finally:
        cursor.close()


def insert_data(connection: mysql.connector.connection.MySQLConnection, csv_file: str) -> None:
    """Insert data from CSV into the database"""
    cursor = connection.cursor()
    try:
        with open(csv_file, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Generate UUID if not present
                if 'user_id' not in row or not row['user_id']:
                    row['user_id'] = str(uuid.uuid4())

                # Insert if not exists
                cursor.execute("SELECT 1 FROM user_data WHERE user_id = %s", (row['user_id'],))
                if not cursor.fetchone():
                    cursor.execute("""
                        INSERT INTO user_data (user_id, name, email, age)
                        VALUES (%s, %s, %s, %s)
                    """, (row['user_id'], row['name'], row['email'], float(row['age'])))
        connection.commit()
    except Error as e:
        print(f"Error inserting data: {e}")
        connection.rollback()
        raise
    finally:
        cursor.close()


def stream_users(connection: mysql.connector.connection.MySQLConnection) -> dict:
    """Generator that streams users from database one by one"""
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