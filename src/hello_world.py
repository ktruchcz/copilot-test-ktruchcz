"""Hello World application – Python port of HelloWorld.java."""

from __future__ import annotations

import datetime
from dataclasses import dataclass
from enum import Enum, auto


@dataclass(frozen=True)
class Greeting:
    """Immutable value object holding a greeting message."""

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
    """Simple enumeration used to represent the time of day."""

    MORNING = auto()
    AFTERNOON = auto()
    EVENING = auto()

    @staticmethod
    def of(hour: int) -> TimeOfDay:
        """Map an hour (0-23) to the appropriate TimeOfDay."""
        if hour < 12:
            return TimeOfDay.MORNING
        if hour < 17:
            return TimeOfDay.AFTERNOON
        return TimeOfDay.EVENING


def season_of(month: int) -> str:
    """Return the meteorological season for the given month (1=January … 12=December)."""
    if month in (12, 1, 2):
        return "Winter"
    if month in (3, 4, 5):
        return "Spring"
    if month in (6, 7, 8):
        return "Summer"
    return "Autumn"


def main() -> None:
    """Entry point: print a time-appropriate greeting and date information."""
    today = datetime.date.today()

    time_of_day = TimeOfDay.of(datetime.datetime.now().hour)
    salutation_map = {
        TimeOfDay.MORNING: "Good morning",
        TimeOfDay.AFTERNOON: "Good afternoon",
        TimeOfDay.EVENING: "Good evening",
    }
    salutation = salutation_map[time_of_day]

    greeting = Greeting(recipient="World", message=salutation)
    print(greeting.formatted(), end="")

    info = (
        f"Python version : {__import__('sys').version.split()[0]}\n"
        f"Today's date   : {today} ({season_of(today.month)})\n"
    )
    print(info, end="")


if __name__ == "__main__":
    main()
