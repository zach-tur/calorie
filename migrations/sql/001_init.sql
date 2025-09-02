# python
DDL = """
CREATE TABLE IF NOT EXISTS items (
  id INTEGER PRIMARY KEY,
  item_name TEXT NOT NULL COLLATE NOCASE UNIQUE,
  grams_base INTEGER NOT NULL,
  carbohydrate REAL NOT NULL,
  protein REAL NOT NULL,
  fat REAL NOT NULL,
  fiber REAL NOT NULL
);
CREATE TABLE IF NOT EXISTS daily_log (
  id INTEGER PRIMARY KEY,
  date TEXT NOT NULL,
  item_name TEXT NOT NULL,
  grams INTEGER NOT NULL
);
CREATE TABLE IF NOT EXISTS weight_log (
  id INTEGER PRIMARY KEY,
  date TEXT NOT NULL,
  weight REAL NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_daily_log_date ON daily_log(date);
"""
with get_conn() as conn:
    conn.executescript(DDL)
