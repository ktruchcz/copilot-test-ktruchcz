# HelloWorld — GnuCOBOL

A GnuCOBOL (free-format) migration of the Java 21 `HelloWorld` application.

## Prerequisites

| Tool | Version | Install |
|------|---------|---------|
| GnuCOBOL | 3.x or later | `sudo apt-get install -y gnucobol` |
| bash | any | pre-installed |

Verify your installation:

```bash
cobc --version
```

## Source file

```
HELLOWORLD.cbl   — single COBOL source, free format
```

## Build

```bash
# From the repo root:
cobc -x -free -o output/hello-world-cobol/helloworld \
     output/hello-world-cobol/HELLOWORLD.cbl

# Or from within output/hello-world-cobol/:
cobc -x -free -o helloworld HELLOWORLD.cbl
```

Flags explained:

| Flag    | Meaning |
|---------|---------|
| `-x`    | Produce a native executable (links the GnuCOBOL runtime) |
| `-free` | Compile in free-format mode (no fixed-column restrictions) |
| `-o`    | Output binary name |

## Run

```bash
./output/hello-world-cobol/helloworld
```

### Example output

```
+--------------------------------+
|  Good morning, World!          |
+--------------------------------+
COBOL version : GnuCOBOL
Today's date  : 2025-06-15 (Summer)
```

The greeting (`Good morning` / `Good afternoon` / `Good evening`) is determined
by `day-of-month MOD 24` — replicating the original Java demo logic exactly.

## Compile + run + test in one step

```bash
bash output/hello-world-cobol/test.sh
```

`test.sh` will:
1. Compile `HELLOWORLD.cbl` with `cobc -x -free`
2. Run the resulting binary and capture stdout
3. Assert the following invariants:
   - Box borders `+--------------------------------+` are present
   - Inner box line is exactly 34 characters (`| ... |`)
   - A valid salutation (`Good morning/afternoon/evening`) is displayed
   - `COBOL version : GnuCOBOL` is present
   - A date in `YYYY-MM-DD` format is present
   - A season name (`Winter/Spring/Summer/Autumn`) is present in parentheses
4. Report pass/fail counts and exit `0` on success, `1` on failure

## Program structure

```
PROCEDURE DIVISION paragraphs
│
├── MAIN-LOGIC            entry point; PERFORM chain; STOP RUN
├── GET-CURRENT-DATE      MOVE FUNCTION CURRENT-DATE TO WS-CURRENT-DATE
├── DETERMINE-TIME-OF-DAY COMPUTE WS-HOUR-MOD = MOD(WS-DAY,24)
│                         EVALUATE TRUE / WHEN < 12 / < 17 / OTHER
├── DETERMINE-SEASON      EVALUATE WS-MONTH with stacked WHEN clauses
├── BUILD-DATE-STRING     STRING YYYY "-" MM "-" DD INTO WS-DATE-DISPLAY
├── DISPLAY-GREETING      ASCII box art with salutation + ", World!"
└── DISPLAY-INFO          COBOL version label + date + season
```

## Java → COBOL feature mapping

| Java (21) | COBOL (GnuCOBOL) |
|-----------|------------------|
| `record Greeting` | `WORKING-STORAGE` fields + `DISPLAY-GREETING` paragraph |
| `sealed interface TimeOfDay` | `WS-SALUTATION PIC X(15)` + `EVALUATE TRUE` |
| `LocalDate.now()` | `FUNCTION CURRENT-DATE` → `WS-CURRENT-DATE PIC X(21)` |
| `getDayOfMonth() % 24` | `COMPUTE WS-HOUR-MOD = FUNCTION MOD(WS-DAY, 24)` |
| `switch (timeOfDay)` pattern match | `EVALUATE TRUE / WHEN WS-HOUR-MOD < 12 …` |
| `seasonOf(Month)` switch | `EVALUATE WS-MONTH` with stacked `WHEN` clauses |
| `today.toString()` ISO date | `STRING` reference-modification on `WS-CURRENT-DATE` |
| Unicode box `╔══╗ ║ ╚══╝` | ASCII box `+--+ \| +--+` |
| `System.getProperty("java.version")` | Literal `"GnuCOBOL"` |
| `System.out.print(...)` | `DISPLAY` statement |

## Known limitations

- **No exception handling** — COBOL has no `throw`/`catch`. Input validation
  from the Java `Greeting` compact constructor is omitted (the program always
  passes `"World"` and a computed salutation, so validation is unnecessary).
- **Unicode box art** — The original Java program used `╔ ═ ╗ ║ ╚ ╝` Unicode
  glyphs. These are replaced with portable ASCII art (`+`, `-`, `|`) because
  GnuCOBOL terminal output may not render UTF-8 box-drawing characters
  reliably in all environments.
- **No OOP** — Java records, sealed interfaces, and pattern-matching are all
  flattened into `WORKING-STORAGE` variables and paragraph calls.
- **Day-mod-24 time logic** — Both Java and COBOL versions use
  `day-of-month MOD 24` (not the actual wall-clock hour) to select the
  greeting, because that is what the original Java demo does.
