"""Hello World application migrated from Java 21 to Python.

Demonstrates Python equivalents of:
- Dataclasses (Java records)
- Enums (Java sealed interfaces / pattern matching)
- Match statements (Java switch expressions)
- f-strings (Java text blocks)
"""

from __future__ import annotations

import sys
from dataclasses import dataclass
from datetime import datetime
from enum import Enum, auto


@dataclass(frozen=True)
class Greeting:
    """Immutable value object holding a greeting message (equivalent to Java record)."""

    recipient: str
    message: str

    def __post_init__(self) -> None:
        if not self.recipient or not self.recipient.strip():
            raise ValueError("recipient must not be blank")
        if not self.message or not self.message.strip():
            raise ValueError("message must not be blank")

    def formatted(self) -> str:
        """Return a fully-formatted greeting string."""
        return (
            "╔══════════════════════════════╗\n"
            f"║  {self.message}, {self.recipient}!  ║\n"
            "╚══════════════════════════════╝\n"
        )


class TimeOfDay(Enum):
    """Enumeration representing a time-of-day period."""

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
    """Return the meteorological season for the given month number (1-12)."""
    match month:
        case 12 | 1 | 2:
            return "Winter"
        case 3 | 4 | 5:
            return "Spring"
        case 6 | 7 | 8:
            return "Summer"
        case 9 | 10 | 11:
            return "Autumn"
        case _:
            raise ValueError(f"Invalid month: {month}")


def main() -> None:
    now = datetime.now()
    today = now.date()

    time_of_day = TimeOfDay.of(now.hour)
    match time_of_day:
        case TimeOfDay.MORNING:
            salutation = "Good morning"
        case TimeOfDay.AFTERNOON:
            salutation = "Good afternoon"
        case TimeOfDay.EVENING:
            salutation = "Good evening"

    greeting = Greeting("World", salutation)
    print(greeting.formatted(), end="")

    info = (
        f"Python version : {sys.version.split()[0]}\n"
        f"Today's date   : {today} ({season_of(today.month)})\n"
    )
    print(info, end="")


if __name__ == "__main__":
    main()
