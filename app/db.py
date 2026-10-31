import sqlite3
from pathlib import Path

DB_PATH = Path("data") / "properties.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


CREATE_PROPERTIES_TABLE = """
CREATE TABLE IF NOT EXISTS properties (
    id INTEGER PRIMARY KEY,
    address TEXT NOT NULL,
    city TEXT NOT NULL,
    state TEXT NOT NULL,
    zip_code TEXT NOT NULL,
    price INTEGER NOT NULL,
    source TEXT NOT NULL,
    date_seen TEXT NOT NULL,
    sqft INTEGER,
    beds INTEGER,
    year_built INTEGER,
    lot_size INTEGER,
    baths REAL,
    latitude REAL,
    longitude REAL,
    status TEXT,
    UNIQUE (address, zip_code)
);
"""


def init_db():
    conn = get_connection()
    conn.execute(CREATE_PROPERTIES_TABLE)
    conn.commit()
    conn.close()


if __name__ == "__main__":
    init_db()
    print(f"Database ready at {DB_PATH}")

