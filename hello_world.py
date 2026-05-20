from dataclasses import dataclass
from datetime import date
import sys


@dataclass(frozen=True)
class Greeting:
    recipient: str
    message: str

    def __post_init__(self) -> None:
        if not self.recipient or not self.recipient.strip():
            raise ValueError("recipient must not be blank")
        if not self.message or not self.message.strip():
            raise ValueError("message must not be blank")

    def formatted(self) -> str:
        return (
            "╔══════════════════════════════╗\n"
            f"║  {self.message}, {self.recipient}!  ║\n"
            "╚══════════════════════════════╝\n"
        )


def time_of_day(hour: int) -> str:
    if hour < 12:
        return "morning"
    if hour < 17:
        return "afternoon"
    return "evening"


def season_of(month: int) -> str:
    if month in (12, 1, 2):
        return "Winter"
    if month in (3, 4, 5):
        return "Spring"
    if month in (6, 7, 8):
        return "Summer"
    return "Autumn"


def main() -> None:
    today = date.today()
    salutation = f"Good {time_of_day(today.day % 24)}"
    greeting = Greeting("World", salutation)
    print(greeting.formatted(), end="")
    print(f"Python version : {sys.version.split()[0]}", end="")
    print(f"\nToday's date : {today} ({season_of(today.month)})")


if __name__ == "__main__":
    main()
