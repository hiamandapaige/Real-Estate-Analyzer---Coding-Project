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