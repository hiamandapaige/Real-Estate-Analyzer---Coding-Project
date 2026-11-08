# ------------------------------------------------------------
# test_clean.py: automatic checks for app/clean.py
#
# WHAT IT DOES
#   Each test_ function feeds clean.py a known input and
#   asserts the expected output.
#   Run all tests:  python3 -m pytest
#
# IF A TEST FAILS
#   Either the code broke, or the rule changed on purpose and
#   the test needs updating. Decide which before "fixing" it.
#
# IF YOU EDIT IT
#   Every new rule in clean.py gets at least one test here.
#   Test function names must start with test_ or pytest skips them.
# ------------------------------------------------------------

from dataclasses import replace
from datetime import date

from app.clean import (
    check_area,
    check_floor_plan,
    check_land_with_bedrooms,
    check_price,
    check_property_type,
    check_size_for_bedrooms,
    check_year_built,
    find_problems,
    normalize_address,
)
from app.models import Property

# A normal, believable house. Each test copies it and breaks one thing.
GOOD_HOME = Property(
    address="123 Main St",
    city="Ridgeland",
    state="MS",
    zip_code="39157",
    price=250000,
    source="test",
    date_seen=date(2026, 11, 8),
    sqft=1800,
    beds=3,
    baths=2.0,
    year_built=2005,
    property_type="Single Family Residential",
    sale_type="MLS Listing",
)


# ---------- normalize_address ----------

def test_uppercases_and_trims():
    assert normalize_address("  123 Main St  ") == "123 MAIN ST"


def test_shortens_street_words():
    assert normalize_address("123 North Main Street") == "123 N MAIN ST"


def test_removes_punctuation_and_extra_spaces():
    assert normalize_address("123  N. Main St.,") == "123 N MAIN ST"


def test_unit_numbers_match():
    assert normalize_address("45 Oak Ave Apt 4") == normalize_address("45 Oak Avenue #4")


def test_same_place_written_two_ways():
    assert normalize_address("127 Carl Avenue") == normalize_address("127 carl ave.")


# ---------- Quality rules ----------

def test_good_home_has_no_problems():
    assert find_problems(GOOD_HOME) == []


def test_price_too_low_is_flagged():
    assert check_price(replace(GOOD_HOME, price=1)) is not None


def test_land_with_bedrooms_is_flagged():
    land = replace(GOOD_HOME, property_type="Vacant Land", beds=3)
    assert check_land_with_bedrooms(land) is not None


def test_land_without_bedrooms_is_fine():
    land = replace(GOOD_HOME, property_type="Vacant Land", beds=None, sqft=None)
    assert check_land_with_bedrooms(land) is None


def test_tiny_house_with_many_bedrooms_is_flagged():
    assert check_size_for_bedrooms(replace(GOOD_HOME, sqft=400, beds=5)) is not None


def test_unknown_size_is_not_flagged():
    assert check_size_for_bedrooms(replace(GOOD_HOME, sqft=None)) is None


def test_future_year_built_is_flagged():
    assert check_year_built(replace(GOOD_HOME, year_built=2099)) is not None


def test_floor_plan_is_flagged():
    assert check_floor_plan(replace(GOOD_HOME, sale_type="New Construction Plan")) is not None


def test_unknown_property_type_is_flagged():
    assert check_property_type(replace(GOOD_HOME, property_type="Unknown")) is not None


def test_outside_zip_is_flagged():
    assert check_area(replace(GOOD_HOME, zip_code="39110")) is not None


def test_one_home_can_have_several_problems():
    messy = replace(GOOD_HOME, property_type="Vacant Land", beds=4, zip_code="39110")
    assert len(find_problems(messy)) == 2