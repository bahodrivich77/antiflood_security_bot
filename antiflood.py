import time

users = {}

LIMIT = 5
SECONDS = 10


async def flood(user_id):
    now = time.time()

    if user_id not in users:
        users[user_id] = []

    users[user_id].append(now)

    users[user_id] = [
        t for t in users[user_id]
        if now - t < SECONDS
    ]

    return len(users[user_id]) >= LIMIT
