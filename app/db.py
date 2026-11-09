# ------------------------------------------------------------
# db.py: the filing cabinet (SQLite database)
#
# WHAT IT DOES
#   Knows where the database lives (data/properties.db),
#   designs the properties table, and saves Properties into it.
#   Run directly to create the table:  python3 -m app.db
#
# USED BY
#   import_redfin.py calls save_properties().
#   Every later project opens the database through get_connection().
#
# IF YOU EDIT IT
#   Changing the table design does NOT change a table that
#   already exists (IF NOT EXISTS skips it). To rebuild:
#     1. Delete data/properties.db
#     2. python3 -m app.db
#     3. Move your CSVs from data/raw back to data/inbox
#     4. python3 -m app.import_redfin
#   Column names must match the fields in models.py.
# ------------------------------------------------------------

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
    address_key TEXT,
    problems TEXT,
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
    status, property_type, sale_type, address_key, problems
) VALUES (
    :address, :city, :state, :zip_code, :price, :source, :date_seen,
    :sqft, :beds, :year_built, :lot_size, :baths, :latitude, :longitude,
    :status, :property_type, :sale_type, :address_key, :problems
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