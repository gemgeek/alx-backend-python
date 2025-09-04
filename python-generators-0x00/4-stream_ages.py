#!/usr/bin/python3
seed = __import__('seed')

# Generator that yields user ages one by one
def stream_user_ages():
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT age FROM user_data")
    for row in cursor.fetchall():  # loop 1
        yield row['age']
    connection.close()

# Function to calculate average age
def calculate_average_age():
    total = 0
    count = 0
    for age in stream_user_ages():  # loop 2
        total += age
        count += 1
    if count == 0:
        return 0
    return total / count

if __name__ == "__main__":
    average_age = calculate_average_age()
    print(f"Average age of users: {average_age}")