# ------------------------------------------------------------
# clean.py: cleaning and quality rules (Project 3)
#
# WHAT IT DOES
#   normalize_address() turns any spelling of an address into
#   one standard form, so the same place always matches.
#   Quality rules (coming in Part B) flag impossible or
#   unusable listings, with a reason.
#
# USED BY
#   tests/test_clean.py checks every function here.
#   import_redfin.py will use it (Part C). Later projects rely
#   on the standardized address to match county records.
#
# IF YOU EDIT IT
#   Run  python3 -m pytest  after every change.
#   Changing how addresses are standardized changes how they
#   match. Add a test for any new rule or abbreviation.
# ------------------------------------------------------------


import re

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