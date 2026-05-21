# Migrated from src/test/java/HelloWorldTest.java
from hello_world import main


def test_main_prints_hello_world_with_trailing_newline(capsys) -> None:
    main()
    captured = capsys.readouterr()
    assert captured.out == "Hello World\n"
