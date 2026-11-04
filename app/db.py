import sqlite3
from dataclasses import asdict
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
    property_type TEXT,
    sale_type TEXT,
    UNIQUE (address, zip_code)
);
"""


def init_db():
    conn = get_connection()
    conn.execute(CREATE_PROPERTIES_TABLE)
    conn.commit()
    conn.close()


INSERT_PROPERTY = """
INSERT OR IGNORE INTO properties (
    address, city, state, zip_code, price, source, date_seen,
    sqft, beds, year_built, lot_size, baths, latitude, longitude,
    status, property_type, sale_type
) VALUES (
    :address, :city, :state, :zip_code, :price, :source, :date_seen,
    :sqft, :beds, :year_built, :lot_size, :baths, :latitude, :longitude,
    :status, :property_type, :sale_type
);
"""


def save_properties(properties):
    conn = get_connection()
    added = 0
    for prop in properties:
        values = asdict(prop)
        values["date_seen"] = prop.date_seen.isoformat()
        cursor = conn.execute(INSERT_PROPERTY, values)
        added += cursor.rowcount
    conn.commit()
    conn.close()
    return added


if __name__ == "__main__":
    init_db()
    print(f"Database ready at {DB_PATH}")
    