import io
import unittest
from contextlib import redirect_stdout

import hello_world


class HelloWorldTest(unittest.TestCase):
    def test_main_prints_hello_world_with_trailing_newline(self) -> None:
        output = io.StringIO()
        with redirect_stdout(output):
            hello_world.main()
        self.assertEqual(f"Hello World{'\n'}", output.getvalue())


if __name__ == "__main__":
    unittest.main()
