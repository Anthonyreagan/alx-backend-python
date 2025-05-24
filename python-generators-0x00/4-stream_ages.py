import mysql.connector
from mysql.connector import  Error
import seed

def stream_user_ages():
    connection = None
    my_cursor = None

    try:
        connection = seed.connect_to_prodev()
        print("connection established")
        my_cursor = connection.cursor(dictionary=True)

        my_cursor.execute("SELECT age FROM user_data")

        while True:
            row = my_cursor.fetchone()
            if row is None:
                break
            yield row["age"]

    except Error as e:
        print(f"Database Error: {e}")
    finally:
        if my_cursor:
            my_cursor.close()
        if connection:
            connection.close()


def average_users_age():
    age_total = 0
    user_total = 0

    for age in stream_user_ages():
        age_total += age
        user_total += 1

    if user_total == 0:
        return 0

    avg = age_total / user_total
    return avg

if __name__ == '__main__':
    for age in stream_user_ages():
        print(age)
    average =  average_users_age()
    print(f"Average age of the users is {average:.2F}")





