import unittest

from hello_world import Greeting, season_of, time_of_day


class HelloWorldTest(unittest.TestCase):
    def test_greeting_stores_fields(self) -> None:
        greeting = Greeting("World", "Hello")
        self.assertEqual("World", greeting.recipient)
        self.assertEqual("Hello", greeting.message)

    def test_greeting_formatted_contains_recipient_and_message(self) -> None:
        result = Greeting("Alice", "Hi").formatted()
        self.assertIn("Alice", result)
        self.assertIn("Hi", result)

    def test_greeting_rejects_blank_recipient(self) -> None:
        with self.assertRaises(ValueError):
            Greeting("", "Hello")

    def test_greeting_rejects_blank_message(self) -> None:
        with self.assertRaises(ValueError):
            Greeting("World", "  ")

    def test_time_of_day(self) -> None:
        self.assertEqual("morning", time_of_day(0))
        self.assertEqual("morning", time_of_day(11))
        self.assertEqual("afternoon", time_of_day(12))
        self.assertEqual("afternoon", time_of_day(16))
        self.assertEqual("evening", time_of_day(17))
        self.assertEqual("evening", time_of_day(23))

    def test_season_of(self) -> None:
        expected = {
            12: "Winter",
            1: "Winter",
            2: "Winter",
            3: "Spring",
            4: "Spring",
            5: "Spring",
            6: "Summer",
            7: "Summer",
            8: "Summer",
            9: "Autumn",
            10: "Autumn",
            11: "Autumn",
        }
        for month, season in expected.items():
            with self.subTest(month=month):
                self.assertEqual(season, season_of(month))


if __name__ == "__main__":
    unittest.main()
