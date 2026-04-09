"""Hello World application – Python migration from Java 21."""

from __future__ import annotations

import sys
from datetime import date
from enum import Enum, auto


class Greeting:
    """Immutable value object holding a greeting message."""

    def __init__(self, recipient: str, message: str) -> None:
        if not recipient or not recipient.strip():
            raise ValueError("recipient must not be blank")
        if not message or not message.strip():
            raise ValueError("message must not be blank")
        self._recipient = recipient
        self._message = message

    @property
    def recipient(self) -> str:
        return self._recipient

    @property
    def message(self) -> str:
        return self._message

    def formatted(self) -> str:
        """Returns a fully-formatted greeting string."""
        return (
            "╔══════════════════════════════╗\n"
            f"║  {self._message}, {self._recipient}!  ║\n"
            "╚══════════════════════════════╝\n"
        )


class TimeOfDay(Enum):
    """Simple enum used to represent the time of day."""

    MORNING = auto()
    AFTERNOON = auto()
    EVENING = auto()

    @staticmethod
    def of(hour: int) -> "TimeOfDay":
        """Map an hour (0-23) to the appropriate TimeOfDay."""
        if hour < 12:
            return TimeOfDay.MORNING
        if hour < 17:
            return TimeOfDay.AFTERNOON
        return TimeOfDay.EVENING


def season_of(month: int) -> str:
    """Return the meteorological season for the given month (1-12)."""
    if month in (12, 1, 2):
        return "Winter"
    if month in (3, 4, 5):
        return "Spring"
    if month in (6, 7, 8):
        return "Summer"
    return "Autumn"


def main() -> None:
    today = date.today()

    time_of_day = TimeOfDay.of(today.day % 24)
    salutation_map = {
        TimeOfDay.MORNING: "Good morning",
        TimeOfDay.AFTERNOON: "Good afternoon",
        TimeOfDay.EVENING: "Good evening",
    }
    salutation = salutation_map[time_of_day]

    greeting = Greeting("World", salutation)
    print(greeting.formatted(), end="")

    info = (
        f"Python version : {sys.version.split()[0]}\n"
        f"Today's date  : {today} ({season_of(today.month)})\n"
    )
    print(info, end="")


if __name__ == "__main__":
    main()
