"""Tests for hello_world.py – mirrors the original Java JUnit test suite."""

import pytest

from hello_world import Greeting, TimeOfDay, season_of


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
    assert "Alice" in result, "formatted output should contain recipient"
    assert "Hi" in result, "formatted output should contain message"


def test_greeting_rejects_blank_recipient():
    with pytest.raises(ValueError):
        Greeting("", "Hello")


def test_greeting_rejects_blank_message():
    with pytest.raises(ValueError):
        Greeting("World", "   ")


# ---------------------------------------------------------------------------
# TimeOfDay
# ---------------------------------------------------------------------------


def test_time_of_day_morning_for_hour_less_than_12():
    assert TimeOfDay.of(0) == TimeOfDay.MORNING
    assert TimeOfDay.of(11) == TimeOfDay.MORNING


def test_time_of_day_afternoon_for_hour_12_to_16():
    assert TimeOfDay.of(12) == TimeOfDay.AFTERNOON
    assert TimeOfDay.of(16) == TimeOfDay.AFTERNOON


def test_time_of_day_evening_for_hour_17_and_above():
    assert TimeOfDay.of(17) == TimeOfDay.EVENING
    assert TimeOfDay.of(23) == TimeOfDay.EVENING


# ---------------------------------------------------------------------------
# season_of
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "month, expected",
    [
        (12, "Winter"),
        (1, "Winter"),
        (2, "Winter"),
        (3, "Spring"),
        (4, "Spring"),
        (5, "Spring"),
        (6, "Summer"),
        (7, "Summer"),
        (8, "Summer"),
        (9, "Autumn"),
        (10, "Autumn"),
        (11, "Autumn"),
    ],
)
def test_season_of_returns_correct_season(month, expected):
    assert season_of(month) == expected
