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
    