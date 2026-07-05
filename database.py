import aiosqlite

DB = "bot.db"


async def init_db():
    async with aiosqlite.connect(DB) as db:
        await db.execute("""
        CREATE TABLE IF NOT EXISTS warns(
            user_id INTEGER,
            warns INTEGER DEFAULT 0
        )
        """)

        await db.execute("""
        CREATE TABLE IF NOT EXISTS blacklist(
            word TEXT UNIQUE
        )
        """)

        await db.commit()


async def add_warn(user_id):
    async with aiosqlite.connect(DB) as db:
        cur = await db.execute(
            "SELECT warns FROM warns WHERE user_id=?",
            (user_id,)
        )
        row = await cur.fetchone()

        if row:
            await db.execute(
                "UPDATE warns SET warns=warns+1 WHERE user_id=?",
                (user_id,)
            )
        else:
            await db.execute(
                "INSERT INTO warns VALUES(?,1)",
                (user_id,)
            )

        await db.commit()


async def get_warn(user_id):
    async with aiosqlite.connect(DB) as db:
        cur = await db.execute(
            "SELECT warns FROM warns WHERE user_id=?",
            (user_id,)
        )
        row = await cur.fetchone()
        return row[0] if row else 0
