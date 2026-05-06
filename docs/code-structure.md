# Code Structure

The entire application is contained in a single Java source file: `src/main/java/HelloWorld.java`.

## Component Diagram

```mermaid
classDiagram
    class HelloWorld {
        +main(String[] args)
        +seasonOf(Month month) String
    }

    class Greeting {
        +String recipient
        +String message
        +formatted() String
    }

    class TimeOfDay {
        <<sealed interface>>
        +of(int hour) TimeOfDay
    }

    class Morning {
        <<record>>
    }

    class Afternoon {
        <<record>>
    }

    class Evening {
        <<record>>
    }

    HelloWorld ..> Greeting : creates
    HelloWorld ..> TimeOfDay : uses
    TimeOfDay <|-- Morning
    TimeOfDay <|-- Afternoon
    TimeOfDay <|-- Evening
```

## Classes and Types

### `HelloWorld`

Top-level class and application entry point. Contains two static members:

| Member | Type | Description |
|--------|------|-------------|
| `main(String[])` | Method | Entry point; orchestrates greeting output and metadata printing |
| `seasonOf(Month)` | Method | Maps a `java.time.Month` to a meteorological season string |

### `HelloWorld.Greeting`

A Java 16 **record** that holds a recipient name and a salutation message.

| Member | Description |
|--------|-------------|
| `recipient` | Name of the person being greeted |
| `message` | Salutation string (e.g., `Good morning`) |
| Compact constructor | Validates that neither field is blank; throws `IllegalArgumentException` otherwise |
| `formatted()` | Returns a Unicode box-drawing banner containing the message and recipient |

### `HelloWorld.TimeOfDay`

A **sealed interface** with three permitted record subtypes, used to classify an hour of the day.

| Subtype | Hour range | Salutation |
|---------|-----------|------------|
| `Morning` | 0 – 11 | Good morning |
| `Afternoon` | 12 – 16 | Good afternoon |
| `Evening` | 17 – 23 | Good evening |

The factory method `TimeOfDay.of(int hour)` uses a guarded pattern-matching switch to construct the correct subtype.

## Execution Flow

```mermaid
flowchart TD
    A[main called] --> B[Get current LocalDate]
    B --> C[Compute hour = dayOfMonth mod 24]
    C --> D[TimeOfDay.of hour]
    D --> E{Pattern match}
    E -->|hour lt 12| F[Morning → Good morning]
    E -->|12 le hour lt 17| G[Afternoon → Good afternoon]
    E -->|hour ge 17| H[Evening → Good evening]
    F & G & H --> I[new Greeting World salutation]
    I --> J[Print greeting.formatted]
    J --> K[Print Java version and date + season]
    K --> L[Exit]
```

## Key Java 21 Features Used

| Feature | Where |
|---------|-------|
| Record (`Greeting`) | Immutable value object with compact constructor |
| Sealed interface (`TimeOfDay`) | Exhaustive type hierarchy |
| Guarded pattern switch | `TimeOfDay.of` — `case Integer h when h < 12` |
| Pattern matching switch | `main` — `case TimeOfDay.Morning ignored` |
| Text block | `Greeting.formatted()` and the `info` variable in `main` |
| `var` inference | All local variables in `main` |

*Last updated: 2026-05-06*
