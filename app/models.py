# ------------------------------------------------------------
# models.py: the Property "form"
#
# WHAT IT DOES
#   Defines Property: the fields every listing has (address,
#   price, beds...) and the type of each field.
#
# USED BY
#   import_redfin.py fills out one Property per CSV row.
#   db.py saves Properties. Field names must match column names.
#
# IF YOU EDIT IT
#   Adding, renaming, or removing a field also means updating:
#     - db.py: the CREATE TABLE columns and INSERT placeholders
#     - import_redfin.py: row_to_property()
#   Then rebuild the database (see db.py). An existing table
#   never changes on its own.
# ------------------------------------------------------------

from dataclasses import dataclass
from datetime import date


@dataclass
class Property:
    # Required: every property must have these
    address: str
    city: str
    state: str
    zip_code: str
    price: int
    source: str
    date_seen: date

    # Optional: blank unless provided
    sqft: int | None = None
    beds: int | None = None
    year_built: int | None = None
    lot_size: int | None = None
    baths: float | None = None
    latitude: float | None = None
    longitude: float | None = None
    status: str | None = None

    property_type: str | None = None
    sale_type: str | None = None
    