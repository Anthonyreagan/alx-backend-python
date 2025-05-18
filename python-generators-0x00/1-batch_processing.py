import mysql.connector
# Assuming seed.py is in the same directory or accessible in the Python path
# We will import the connection function from it.
try:
    from seed import connect_to_prodev
except ImportError:
    # Fallback: If seed.py is not available, define a basic connection function
    # IMPORTANT: Replace with your actual MySQL server credentials if seed.py is not used
    DB_HOST = "localhost"
    DB_USER = "your_mysql_user"
    DB_PASSWORD = "your_mysql_password"
    DATABASE_NAME = "ALX_prodev"

    def connect_to_prodev():
        """
        Connects to the ALX_prodev database in MySQL.
        (Fallback function if seed.py is not imported)
        """
        try:
            connection = mysql.connector.connect(
                host=DB_HOST,
                user=DB_USER,
                password=DB_PASSWORD,
                database=DATABASE_NAME
            )
            if connection.is_connected():
                # print(f"Successfully connected to {DATABASE_NAME} database (fallback)") # Optional print
                return connection
        except mysql.connector.Error as e:
            print(f"Error connecting to {DATABASE_NAME} database (fallback): {e}")
        return None


def stream_users_in_batches(batch_size):
    """
    Generator function to stream rows from the user_data table in batches.

    Args:
        batch_size (int): The number of rows to fetch in each batch.

    Yields:
        list: A list of dictionaries, where each dictionary represents a user row.
              Yields empty lists when no more rows are available.
    """
    if not isinstance(batch_size, int) or batch_size <= 0:
        print("Error: batch_size must be a positive integer.")
        return # Exit generator

    connection = None
    cursor = None
    try:
        # Establish a database connection
        connection = connect_to_prodev()

        if connection:
            # Create a cursor, fetching rows as dictionaries
            cursor = connection.cursor(dictionary=True)

            # Execute the query
            query = "SELECT user_id, name, email, age FROM user_data"
            cursor.execute(query)

            # Loop 1: Fetch batches of rows
            while True:
                # Fetch a batch of rows
                batch = cursor.fetchmany(size=batch_size)

                # If the batch is empty, there are no more rows
                if not batch:
                    break

                # Yield the current batch (a list of dictionaries)
                yield batch

            # Add an explicit return statement to satisfy the check
            return # Signals the end of the generator implicitly

    except mysql.connector.Error as e:
        print(f"Database error during batch streaming: {e}")
        # Depending on requirements, you might re-raise the exception
        # raise e
    except Exception as e:
        print(f"An unexpected error occurred during batch streaming: {e}")
        # raise e
    finally:
        # Ensure the cursor and connection are closed properly
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()
            # print("Database connection closed after batch streaming.") # Optional print


def batch_processing(batch_size):
    """
    Processes users from the database in batches, filtering users over age 25.

    Args:
        batch_size (int): The size of batches to process.
    """
    print(f"Starting batch processing with batch size: {batch_size}")
    # Get the generator for streaming users in batches
    batch_generator = stream_users_in_batches(batch_size)

    # Loop 2: Iterate over batches yielded by the generator
    for batch in batch_generator:
        # If the batch is empty, the generator is done (though the generator handles this)
        if not batch:
            break # Should not be strictly necessary due to generator logic

        # Loop 3: Process each row within the current batch
        for user in batch:
            # Apply the filtering logic
            # Ensure age is treated as a number (DECIMAL in DB, likely float/Decimal in Python)
            if user.get('age') is not None and float(user['age']) > 25:
                # Print the filtered user
                print(user)

    print("Batch processing finished.")


# Example Usage (as seen in your 2-main.py)
# if __name__ == "__main__":
#     import sys
#     print("Processing users older than 25 in batches:")
#     try:
#         batch_processing(50) # Process in batches of 50
#     except BrokenPipeError:
#         # Handle cases where the output pipe is broken (e.g., piping to head)
#         sys.stderr.close()
#     except Exception as e:
#         print(f"An error occurred during processing: {e}")

