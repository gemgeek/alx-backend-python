#!/usr/bin/python3
seed = __import__('seed')

def paginate_users(page_size, offset):
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}")
    rows = cursor.fetchall()
    connection.close()
    return rows

# Generator function for lazy pagination
def lazy_pagination(page_size):
    offset = 0
    while True:  # only one loop, fetch next page lazily
        page = paginate_users(page_size, offset)
        if not page:  # if no more rows, stop
            break
        yield page  # yield the current page
        offset += page_size  # move to next page