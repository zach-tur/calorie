import os
import textual
import textual_dev

import sqlite3

DB_PATH = os.path.join(os.path.dirname(__file__), "data", "data.db")
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)


def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


with open(
    os.path.join(os.path.dirname(__file__), "migrations", "001_init.sql"), "r"
) as f:
    ddl = f.read()
with get_conn() as conn:
    conn.executescript(ddl)

# con = sqlite3.connect("dbhere.db")


def main():
    print("Hello from calorie!")


if __name__ == "__main__":
    main()
