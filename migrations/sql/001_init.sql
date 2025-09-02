-- migrations/001_init.sql

-- Items: per-grams_base macros, case-insensitive unique names
CREATE TABLE IF NOT EXISTS items (
  id INTEGER PRIMARY KEY,
  item_name TEXT NOT NULL COLLATE NOCASE UNIQUE,
  grams_base INTEGER NOT NULL,
  carbohydrate REAL NOT NULL,
  protein REAL NOT NULL,
  fat REAL NOT NULL,
  fiber REAL NOT NULL
);

-- Daily log: date + item name + grams consumed
CREATE TABLE IF NOT EXISTS daily_log (
  id INTEGER PRIMARY KEY,
  date TEXT NOT NULL,          -- ISO YYYY-MM-DD
  item_name TEXT NOT NULL,     -- references items.item_name by text
  grams INTEGER NOT NULL
);

-- Weight log
CREATE TABLE IF NOT EXISTS weight_log (
  id INTEGER PRIMARY KEY,
  date TEXT NOT NULL,          -- ISO YYYY-MM-DD
  weight REAL NOT NULL
);

-- Index for fast daily queries
CREATE INDEX IF NOT EXISTS idx_daily_log_date ON daily_log(date);
