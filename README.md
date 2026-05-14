# copilot-test-ktruchcz

A Hello World application migrated from Java 21 to Python 3.10+.

## Running

```bash
python src/hello_world.py
```

## Testing

```bash
pip install -e .[test]
pytest tests/
```

## Architecture

### System Context

```mermaid
flowchart TD
    User([User]) -->|runs| App[hello_world.py]
    App -->|reads| SysDate[System Date]
    App -->|reads| SysVer[Python Version]
    App -->|prints| Output[Console Output]
```

### Module Structure

```mermaid
classDiagram
    class Greeting {
        +str recipient
        +str message
        +__post_init__() None
        +formatted() str
    }
    class TimeOfDay {
        <<enumeration>>
        MORNING
        AFTERNOON
        EVENING
        +of(hour: int) TimeOfDay
    }
    class hello_world {
        +season_of(month: int) str
        +main() None
    }
    hello_world --> Greeting : creates
    hello_world --> TimeOfDay : uses
```

### Runtime Flow

```mermaid
sequenceDiagram
    participant main
    participant TimeOfDay
    participant Greeting
    main->>TimeOfDay: of(today.day % 24)
    TimeOfDay-->>main: MORNING | AFTERNOON | EVENING
    main->>Greeting: Greeting("World", salutation)
    Greeting-->>main: greeting instance
    main->>Greeting: formatted()
    Greeting-->>main: banner string
    main->>main: print banner + version/date info
```