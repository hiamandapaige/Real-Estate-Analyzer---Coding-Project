from app.clean import normalize_address


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