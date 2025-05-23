#!/usr/bin/python3
from seed import connect_db, create_database, connect_to_prodev, create_table, insert_data, stream_users


# Initialize database
print("Setting up database...")
connection = connect_db()
create_database(connection)
connection.close()

# Connect to specific database
connection = connect_to_prodev()
create_table(connection)

# Insert data from CSV
print("Inserting data...")
insert_data(connection, 'user_data.csv')

# Stream users using generator
print("\nStreaming users:")
for user in stream_users(connection):
    print(user)

connection.close()