import sqlite3


class ExecuteQuery:
    def __init__(self, query, params=None):
        self.query = query
        self.params = params if params is not None else ()
        self.conn = None
        self.cursor = None

    def __enter__(self):
        # Establish connection and create cursor
        self.conn = sqlite3.connect('users.db')
        self.cursor = self.conn.cursor()

        # Execute the query with parameters
        self.cursor.execute(self.query, self.params)

        # Return the cursor to fetch results
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Close cursor and connection
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()

        # Return False to propagate any exceptions
        return False


if __name__ == "__main__":
    query = "SELECT * FROM users WHERE age > ?"
    params = (25,)

    with ExecuteQuery(query, params) as cursor:
        results = cursor.fetchall()
        print(results)
