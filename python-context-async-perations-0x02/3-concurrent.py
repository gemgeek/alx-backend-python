#!/usr/bin/env python3
import asyncio
import aiosqlite

DB_NAME = "example.db"

# 🔹 Fetch all users
async def async_fetch_users():
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("SELECT * FROM users") as cursor:
            return await cursor.fetchall()

# 🔹 Fetch users older than 40
async def async_fetch_older_users():
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("SELECT * FROM users WHERE age > 40") as cursor:
            return await cursor.fetchall()

# 🔹 Run both queries concurrently
async def fetch_concurrently():
    results_all, results_older = await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )

    print("All Users:")
    for row in results_all:
        print(row)

    print("\nUsers older than 40:")
    for row in results_older:
        print(row)

# 🔹 Entry point
if __name__ == "__main__":
    asyncio.run(fetch_concurrently())