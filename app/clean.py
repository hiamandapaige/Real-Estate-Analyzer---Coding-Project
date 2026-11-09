# ------------------------------------------------------------
# clean.py: cleaning and quality rules (Project 3)
#
# WHAT IT DOES
#   normalize_address() turns any spelling of an address into
#   one standard form, so the same place always matches.
#   find_problems() runs every quality rule on one Property and
#   returns a list of reasons it can't be trusted (empty = clean).
#
#   clean_properties() fills in address_key and problems on
#   every Property, and print_quality_report() summarizes it.
# USED BY
#   tests/test_clean.py checks every function here.
#   import_redfin.py will use it (Part C). Later projects rely
#   on the standardized address to match county records.
#
#   import_redfin.py runs clean_properties() on every import.
# IF YOU EDIT IT
#   Run  python3 -m pytest  after every change.
#   New rule? Write the function, add it to RULES, add a test.
#   Changing the settings below changes what gets flagged.
# ------------------------------------------------------------

import re
from datetime import date

# ---------- Settings ----------
TARGET_ZIPS = ["39157"]      # the ZIP codes in your market
MIN_PRICE = 10_000           # anything cheaper is a typo, not a house
MIN_SQFT_PER_BED = 150       # less space than this per bedroom is impossible

# Different spellings of the same word, mapped to one short form.
ABBREVIATIONS = {
    "STREET": "ST",
    "AVENUE": "AVE",
    "DRIVE": "DR",
    "ROAD": "RD",
    "LANE": "LN",
    "COURT": "CT",
    "CIRCLE": "CIR",
    "COVE": "CV",
    "PLACE": "PL",
    "TRAIL": "TRL",
    "BOULEVARD": "BLVD",
    "PARKWAY": "PKWY",
    "HIGHWAY": "HWY",
    "NORTH": "N",
    "SOUTH": "S",
    "EAST": "E",
    "WEST": "W",
    "APT": "UNIT",
    "APARTMENT": "UNIT",
    "STE": "UNIT",
    "SUITE": "UNIT",
}


def normalize_address(address):
    """Turn an address into one standard form, so the same place always matches."""
    text = address.upper()
    text = text.replace("#", " UNIT ")
    text = re.sub(r"[.,]", " ", text)
    words = text.split()

    short_words = []
    for word in words:
        short_words.append(ABBREVIATIONS.get(word, word))

    return " ".join(short_words)


# ---------- Quality rules ----------
# Each rule looks at one Property.
# It returns a reason (text) if something is wrong, or None if it's fine.

def check_price(prop):
    if prop.price < MIN_PRICE:
        return f"price ${prop.price:,} is below ${MIN_PRICE:,}"
    return None


def check_land_with_bedrooms(prop):
    if prop.property_type == "Vacant Land" and prop.beds is not None and prop.beds > 0:
        return f"vacant land listed with {prop.beds} bedrooms"
    return None


def check_size_for_bedrooms(prop):
    if prop.sqft is None or prop.beds is None:
        return None  # unknown isn't wrong, so there's nothing to check
    if prop.sqft < prop.beds * MIN_SQFT_PER_BED:
        return f"{prop.sqft} sq ft is too small for {prop.beds} bedrooms"
    return None


def check_year_built(prop):
    if prop.year_built is None:
        return None
    latest = date.today().year + 1  # homes under construction may list next year
    if prop.year_built > latest or prop.year_built < 1800:
        return f"year built {prop.year_built} is impossible"
    return None


def check_floor_plan(prop):
    if prop.sale_type == "New Construction Plan":
        return "builder floor plan, not a real house for sale"
    return None


def check_property_type(prop):
    if prop.property_type is None or prop.property_type == "Unknown":
        return "property type unknown"
    return None


def check_area(prop):
    if prop.zip_code not in TARGET_ZIPS:
        return f"ZIP {prop.zip_code} is outside your market"
    return None


# Every rule, in the order they run. A new rule must be added here.
RULES = [
    check_price,
    check_land_with_bedrooms,
    check_size_for_bedrooms,
    check_year_built,
    check_floor_plan,
    check_property_type,
    check_area,
]


def find_problems(prop):
    """Run every rule on one Property. Returns a list of reasons; empty means clean."""
    problems = []
    for rule in RULES:
        reason = rule(prop)
        if reason is not None:
            problems.append(reason)
    return problems




# ---------- Cleaning a whole file ----------

def clean_properties(properties):
    """Fill in address_key and problems on each Property. Returns the flagged ones."""
    flagged = []
    for prop in properties:
        prop.address_key = normalize_address(prop.address)
        problems = find_problems(prop)
        if problems:
            prop.problems = "; ".join(problems)
            flagged.append(prop)
        else:
            prop.problems = None
    return flagged


def print_quality_report(file_name, properties, flagged, added):
    """Print what came in, what's clean, and what was flagged and why."""
    clean_count = len(properties) - len(flagged)
    print()
    print(f"Data-quality report: {file_name}")
    print(f"  Rows read:               {len(properties)}")
    print(f"  Addresses standardized:  {len(properties)}")
    print(f"  Clean:                   {clean_count}")
    print(f"  Flagged:                 {len(flagged)}")
    for prop in flagged:
        print(f"    - {prop.address}: {prop.problems}")
    print(f"  New rows saved:          {added}")