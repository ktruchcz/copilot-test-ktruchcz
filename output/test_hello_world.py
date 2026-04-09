"""pytest test suite – mirrors HelloWorldTest.java (JUnit 5 → pytest)."""

import pytest

from hello_world import Afternoon, Evening, Greeting, Morning, TimeOfDay, season_of


# ---------------------------------------------------------------------------
# Greeting
# ---------------------------------------------------------------------------

def test_greeting_stores_fields():
    g = Greeting("World", "Hello")
    assert g.recipient == "World"
    assert g.message == "Hello"


def test_greeting_formatted_contains_recipient_and_message():
    g = Greeting("Alice", "Hi")
    result = g.formatted()
    assert "Alice" in result
    assert "Hi" in result


def test_greeting_rejects_blank_recipient():
    with pytest.raises(ValueError):
        Greeting("", "Hello")


def test_greeting_rejects_blank_message():
    with pytest.raises(ValueError):
        Greeting("World", "   ")


def test_greeting_rejects_none_recipient():
    with pytest.raises(ValueError):
        Greeting(None, "Hello")  # type: ignore[arg-type]


def test_greeting_rejects_none_message():
    with pytest.raises(ValueError):
        Greeting("World", None)  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# TimeOfDay
# ---------------------------------------------------------------------------

def test_time_of_day_morning_for_hour_less_than_12():
    assert isinstance(TimeOfDay.of(0), Morning)
    assert isinstance(TimeOfDay.of(11), Morning)


def test_time_of_day_afternoon_for_hour_12_to_16():
    assert isinstance(TimeOfDay.of(12), Afternoon)
    assert isinstance(TimeOfDay.of(16), Afternoon)


def test_time_of_day_evening_for_hour_17_and_above():
    assert isinstance(TimeOfDay.of(17), Evening)
    assert isinstance(TimeOfDay.of(23), Evening)


# ---------------------------------------------------------------------------
# season_of – parameterised over all 12 months
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("month,expected", [
    (12, "Winter"),
    (1,  "Winter"),
    (2,  "Winter"),
    (3,  "Spring"),
    (4,  "Spring"),
    (5,  "Spring"),
    (6,  "Summer"),
    (7,  "Summer"),
    (8,  "Summer"),
    (9,  "Autumn"),
    (10, "Autumn"),
    (11, "Autumn"),
])
def test_season_of_returns_correct_season(month, expected):
    assert season_of(month) == expected
