import os, sqlite3

HERE = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(os.path.join(HERE, ".."))
DB_PATH = os.path.join(PROJECT_ROOT, "data", "data.db")
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)


def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    print("data.db intialized")
    return conn


def init_db():
    with open(
        os.path.join(PROJECT_ROOT, "migrations", "sql", "001_init.sql"), "r"
    ) as f:
        ddl = f.read()
    with get_conn() as conn:
        conn.executescript(ddl)


# inserts or updates item in item database
def upsert_item(conn, name, grams_base, carb, prot, fat, fiber):
    conn.execute(
        """
        INSERT INTO items(item_name, grams_base, carbohydrate, protein, fat, fiber)
        VALUES(?, ?, ?, ?, ?, ?)
        ON CONFLICT(item_name) DO UPDATE SET
          grams_base=excluded.grams_base,
          carbohydrate=excluded.carbohydrate,
          protein=excluded.protein,
          fat=excluded.fat,
          fiber=excluded.fiber
    """,
        (name, grams_base, carb, prot, fat, fiber),
    )


def add_daily_entry(conn, date_iso, item_name, grams):
    conn.execute(
        "INSERT INTO daily_log(date, item_name, grams) VALUES(?, ?, ?)",
        (date_iso, item_name, grams),
    )


def get_daily_totals(conn, date_iso):
    sql = """
    SELECT
      COALESCE(SUM(i.carbohydrate * (d.grams * 1.0 / i.grams_base)), 0) AS carbs,
      COALESCE(SUM(i.protein      * (d.grams * 1.0 / i.grams_base)), 0) AS protein,
      COALESCE(SUM(i.fat          * (d.grams * 1.0 / i.grams_base)), 0) AS fat,
      COALESCE(SUM(i.fiber        * (d.grams * 1.0 / i.grams_base)), 0) AS fiber
    FROM daily_log d
    JOIN items i ON i.item_name = d.item_name
    WHERE d.date = ?
    """
    cur = conn.execute(sql, (date_iso,))
    row = cur.fetchone()
    return dict(carbs=row[0], protein=row[1], fat=row[2], fiber=row[3])


def get_entries_with_macros_for_date(conn, date_iso):
    sql = """
    SELECT d.id, d.item_name, d.grams,
           i.carbohydrate * (d.grams * 1.0 / i.grams_base) AS carbs,
           i.protein      * (d.grams * 1.0 / i.grams_base) AS protein,
           i.fat          * (d.grams * 1.0 / i.grams_base) AS fat,
           i.fiber        * (d.grams * 1.0 / i.grams_base) AS fiber
    FROM daily_log d
    JOIN items i ON i.item_name = d.item_name
    WHERE d.date = ?
    ORDER BY d.id
    """
    return list(conn.execute(sql, (date_iso,)))
