from datetime import date
from pathlib import Path

import pandas as pd

from app.db import save_properties
from app.models import Property

INBOX = Path("data/inbox")
RAW = Path("data/raw")


def to_text(value):
    if pd.isna(value):
        return None
    return str(value)


def to_int(value):
    if pd.isna(value):
        return None
    return int(value)


def to_float(value):
    if pd.isna(value):
        return None
    return float(value)


def row_to_property(row, seen_on):
    return Property(
        address=to_text(row["ADDRESS"]),
        city=to_text(row["CITY"]),
        state=to_text(row["STATE OR PROVINCE"]),
        zip_code=to_text(row["ZIP OR POSTAL CODE"]),
        price=to_int(row["PRICE"]),
        source="redfin",
        date_seen=seen_on,
        sqft=to_int(row["SQUARE FEET"]),
        beds=to_int(row["BEDS"]),
        year_built=to_int(row["YEAR BUILT"]),
        lot_size=to_int(row["LOT SIZE"]),
        baths=to_float(row["BATHS"]),
        latitude=to_float(row["LATITUDE"]),
        longitude=to_float(row["LONGITUDE"]),
        status=to_text(row["STATUS"]),
        property_type=to_text(row["PROPERTY TYPE"]),
        sale_type=to_text(row["SALE TYPE"]),
    )


def load_redfin_csv(path):
    df = pd.read_csv(path, dtype={"ZIP OR POSTAL CODE": str})
    df = df.dropna(subset=["ADDRESS"])

    today = date.today()
    properties = []
    for _, row in df.iterrows():
        properties.append(row_to_property(row, today))
    return properties


def import_inbox():
    files = sorted(INBOX.glob("*.csv"))
    if not files:
        print("No CSV files in data/inbox")
        return

    for path in files:
        properties = load_redfin_csv(path)
        added = save_properties(properties)
        path.rename(RAW / path.name)
        print(f"{path.name}: read {len(properties)}, saved {added} new")


if __name__ == "__main__":
    import_inbox() 

    


