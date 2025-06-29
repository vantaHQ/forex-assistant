import sqlite3


def init_db():
    conn = sqlite3.connect("trading_assistant.db")
    cur = conn.cursor()

    cur.execute(
        """CREATE TABLE IF NOT EXISTS trades (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        symbol TEXT,
        open_time TEXT,
        close_time TEXT,
        volume REAL,
        result REAL,
        strategy TEXT,
        notes TEXT
    )"""
    )

    cur.execute(
        """CREATE TABLE IF NOT EXISTS journal (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        entry_time TEXT,
        summary TEXT,
        sentiment TEXT
    )"""
    )

    conn.commit()
    conn.close()
    print("✅ Database initialized successfully.")


if __name__ == "__main__":
    init_db()
