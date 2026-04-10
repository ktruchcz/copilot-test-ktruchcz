# Migration Report

**Source technology :** Java 21  
**Target technology :** COBOL (GnuCOBOL, free format)  
**Source application:** HelloWorld  
**Output path       :** `output/hello-world-cobol/`

---

## Summary

The Java 21 `HelloWorld` application was migrated to a single GnuCOBOL source
file (`HELLOWORLD.cbl`) in free format.  All runtime behaviour is preserved:

- The current date is obtained via `FUNCTION CURRENT-DATE` (mirrors
  `LocalDate.now()`).
- The time-of-day greeting is derived from `day-of-month MOD 24` (exactly
  replicating Java's `today.getDayOfMonth() % 24` demo logic).
- The meteorological season is determined from the numeric month.
- Output is a decorated ASCII box followed by a version/date/season info block.

No third-party libraries are required; the program compiles with the standard
GnuCOBOL toolchain (`cobc -x -free`).

---

## Migrated files

| File | Description |
|------|-------------|
| `output/hello-world-cobol/HELLOWORLD.cbl` | Complete GnuCOBOL program (free format) — single source file containing all divisions, working-storage, and procedure paragraphs |
| `output/hello-world-cobol/test.sh` | Shell script: compiles the program, runs it, and asserts expected output patterns; exits `0` on pass, `1` on failure |
| `output/hello-world-cobol/README.md` | Build & run instructions, paragraph structure reference, Java→COBOL feature mapping table, known limitations |

---

## Key mapping decisions — Java feature → COBOL construct

### 1. `record Greeting` → WORKING-STORAGE + `DISPLAY-GREETING` paragraph

Java records are immutable value objects with auto-generated accessors.  COBOL
has no equivalent construct.  The `recipient` and `message` fields become
implicit constants ("World" and the computed `WS-SALUTATION`), and the
`formatted()` method becomes the `DISPLAY-GREETING` paragraph.

### 2. `sealed interface TimeOfDay` (Morning / Afternoon / Evening)  
→ `WS-SALUTATION PIC X(15)` + `EVALUATE TRUE` in `DETERMINE-TIME-OF-DAY`

Sealed interfaces and pattern-matching `switch` have no COBOL equivalent.  The
three subtypes are replaced by a single string field holding the corresponding
salutation text.  The factory `TimeOfDay.of(hour)` logic becomes an
`EVALUATE TRUE / WHEN WS-HOUR-MOD < 12 / WHEN WS-HOUR-MOD < 17 / WHEN OTHER`
block, which is the idiomatic COBOL way to write guarded if-else chains.

### 3. `LocalDate.now()` → `FUNCTION CURRENT-DATE`

`FUNCTION CURRENT-DATE` returns a 21-character string
(`YYYYMMDDhhmmssccZhhmm`).  A `REDEFINES` group (`WS-DATE-PARTS`) overlays it
with named numeric subfields (`WS-YEAR`, `WS-MONTH`, `WS-DAY`, …), giving
structured access without any parsing code.

### 4. `today.getDayOfMonth() % 24` → `COMPUTE WS-HOUR-MOD = FUNCTION MOD(WS-DAY, 24)`

The Java code deliberately uses the day-of-month (not the clock hour) to
pick a greeting — a quirky demo choice.  This is replicated verbatim in COBOL
using `FUNCTION MOD`, the standard GnuCOBOL intrinsic function for modulo.

### 5. `seasonOf(Month)` switch → `EVALUATE WS-MONTH` with stacked `WHEN` clauses

Java's `switch` on an enum with multi-label cases maps naturally to COBOL's
`EVALUATE` with consecutive `WHEN` clauses acting as logical OR:
```
WHEN 12
WHEN 1
WHEN 2
    MOVE "Winter" TO WS-SEASON
```

### 6. Unicode box drawing → ASCII art

Java's `╔══════════════════════════════╗ / ║ / ╚══════════════════════════════╝`
are replaced with `+--------------------------------+ / | / +--------------------------------+`
(34 characters wide).  The content area between the pipes is exactly 32
characters: `MOVE SPACES` pre-fills the field, then `STRING` fills it
left-to-right; trailing spaces provide the padding automatically.

### 7. `today.toString()` (ISO date) → `STRING` with reference modification

COBOL reference modification (`WS-CURRENT-DATE(1:4)`) extracts substrings
directly from the raw `FUNCTION CURRENT-DATE` string.  The year, month, and
day parts are concatenated with hyphens using `STRING … INTO WS-DATE-DISPLAY`.

### 8. `System.getProperty("java.version")` → literal `"GnuCOBOL"`

Java system properties have no COBOL equivalent.  The version string is
replaced with the literal `"GnuCOBOL"` to preserve the informational intent of
the output line.

### 9. `System.out.print(…)` → `DISPLAY`

Every console output statement becomes a `DISPLAY` statement.  COBOL `DISPLAY`
automatically appends a newline (matching Java's `println` behaviour); the
original Java code uses `print` with embedded newlines in text blocks, which
produces the same visible result.

### 10. Input validation (`IllegalArgumentException`) → omitted

The Java `Greeting` compact constructor validates that `recipient` and
`message` are non-blank.  Since the COBOL program always passes the constants
`"World"` and a computed salutation (never empty), this validation is
structurally unnecessary and is omitted.

---

## Build command

```bash
# Install GnuCOBOL if not already present
sudo apt-get install -y gnucobol

# Compile (from repo root)
cobc -x -free \
     -o output/hello-world-cobol/helloworld \
     output/hello-world-cobol/HELLOWORLD.cbl

# Run
./output/hello-world-cobol/helloworld

# Compile + run + assert (all-in-one)
bash output/hello-world-cobol/test.sh
```

---

## Known limitations

| Limitation | Detail |
|------------|--------|
| No OOP | Java records, sealed interfaces, and switch pattern-matching are all flattened into `WORKING-STORAGE` variables and paragraph calls.  Behaviour is equivalent; structure is imperative. |
| No exception handling | COBOL has no `throw`/`catch` equivalent.  The `IllegalArgumentException` guards from `Greeting`'s compact constructor are omitted because the program never passes invalid values. |
| Unicode box art | The original Unicode glyphs (`╔ ═ ╗ ║ ╚ ╝`) are replaced with ASCII art (`+`, `-`, `|`) for portability.  GnuCOBOL terminal output may not correctly render UTF-8 box-drawing characters in all COBOL runtime environments. |
| Day-mod-24 time-of-day | Both versions use `day-of-month MOD 24` (not the actual wall-clock hour) to select the greeting — preserving the original Java demo logic exactly, even though it produces the same greeting all day long on a given date. |
| No runtime type safety | COBOL `PIC X` fields and `PIC 9` fields are untyped at the language level; out-of-range values in WORKING-STORAGE are not detected at compile time. |
| Single-file flat structure | COBOL has no package, class, or module system.  All logic resides in one `.cbl` file, which is idiomatic for a program of this size. |
