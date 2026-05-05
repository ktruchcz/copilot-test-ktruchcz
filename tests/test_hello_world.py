"""pytest tests for hello_world – port of HelloWorldTest.java."""

import sys
from pathlib import Path

import pytest

# Make 'src' importable without installing the package
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from hello_world import Greeting, TimeOfDay, season_of  # noqa: E402


# ---------------------------------------------------------------------------
# Greeting dataclass
# ---------------------------------------------------------------------------


def test_greeting_stores_fields() -> None:
    g = Greeting(recipient="World", message="Hello")
    assert g.recipient == "World"
    assert g.message == "Hello"


def test_greeting_formatted_contains_recipient_and_message() -> None:
    g = Greeting(recipient="Alice", message="Hi")
    result = g.formatted()
    assert "Alice" in result, "formatted output should contain recipient"
    assert "Hi" in result, "formatted output should contain message"


def test_greeting_rejects_blank_recipient() -> None:
    with pytest.raises((ValueError, TypeError)):
        Greeting(recipient="", message="Hello")


def test_greeting_rejects_blank_message() -> None:
    with pytest.raises((ValueError, TypeError)):
        Greeting(recipient="World", message="   ")


# ---------------------------------------------------------------------------
# TimeOfDay enum
# ---------------------------------------------------------------------------


def test_time_of_day_morning_for_hour_less_than_12() -> None:
    assert TimeOfDay.of(0) == TimeOfDay.MORNING
    assert TimeOfDay.of(11) == TimeOfDay.MORNING


def test_time_of_day_afternoon_for_hour_12_to_16() -> None:
    assert TimeOfDay.of(12) == TimeOfDay.AFTERNOON
    assert TimeOfDay.of(16) == TimeOfDay.AFTERNOON


def test_time_of_day_evening_for_hour_17_and_above() -> None:
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
def test_season_of_returns_correct_season(month: int, expected: str) -> None:
    assert season_of(month) == expected
