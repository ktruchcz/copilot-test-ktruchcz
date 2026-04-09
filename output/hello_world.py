"""Hello World application – Python 3.10+ port of the Java 21 original.

Demonstrates idiomatic Python equivalents of modern Java features:
- frozen dataclass  (≈ Java record)
- ABC hierarchy     (≈ sealed interface)
- match/case        (≈ switch expression with guarded patterns)
- f-strings         (≈ text blocks with .formatted())
- datetime / platform (≈ LocalDate / System.getProperty)
"""

from __future__ import annotations

import datetime
import platform
from abc import ABC
from dataclasses import dataclass


# ---------------------------------------------------------------------------
# Greeting – immutable value object (Java record → frozen dataclass)
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class Greeting:
    """Immutable greeting holding a recipient and a message."""

    recipient: str
    message: str

    def __post_init__(self) -> None:
        if not self.recipient or not self.recipient.strip():
            raise ValueError("recipient must not be blank")
        if not self.message or not self.message.strip():
            raise ValueError("message must not be blank")

    def formatted(self) -> str:
        """Return a Unicode box-framed greeting string."""
        return (
            "╔══════════════════════════════╗\n"
            f"║  {self.message}, {self.recipient}!  ║\n"
            "╚══════════════════════════════╝\n"
        )


# ---------------------------------------------------------------------------
# TimeOfDay – sealed hierarchy (Java sealed interface → ABC + subclasses)
# ---------------------------------------------------------------------------

class TimeOfDay(ABC):
    """Abstract base for time-of-day categories."""

    @staticmethod
    def of(hour: int) -> "TimeOfDay":
        """Map an hour (0-23) to the appropriate TimeOfDay instance."""
        match hour:
            case h if h < 12:
                return Morning()
            case h if h < 17:
                return Afternoon()
            case _:
                return Evening()


class Morning(TimeOfDay):
    pass


class Afternoon(TimeOfDay):
    pass


class Evening(TimeOfDay):
    pass


# ---------------------------------------------------------------------------
# season_of – meteorological season (Java Month enum → int 1-12)
# ---------------------------------------------------------------------------

def season_of(month: int) -> str:
    """Return the meteorological season for a month number (1-12)."""
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


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------

def main() -> None:
    today = datetime.date.today()
    time_of_day = TimeOfDay.of(datetime.datetime.now().hour)

    match time_of_day:
        case Morning():
            salutation = "Good morning"
        case Afternoon():
            salutation = "Good afternoon"
        case Evening():
            salutation = "Good evening"

    greeting = Greeting("World", salutation)
    print(greeting.formatted(), end="")

    info = (
        f"Python version : {platform.python_version()}\n"
        f"Today's date   : {today} ({season_of(today.month)})\n"
    )
    print(info, end="")


if __name__ == "__main__":
    main()
