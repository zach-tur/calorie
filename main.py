import os
import textual
import textual_dev

import sqlite3
import src.sql_handling as db


def main():
    print("Hello from calorie!")
    db.init_db()


if __name__ == "__main__":
    main()
