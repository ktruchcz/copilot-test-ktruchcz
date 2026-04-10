# Migration Analysis Report

**Source Technology:** Java 21  
**Target Technology:** COBOL (GnuCOBOL, free-format)  
**Source Application:** HelloWorld  
**Target Output Path:** `output/hello-world-cobol/`  
**Date:** 2025

---

## 1. Feature Inventory — Java → COBOL Mapping

| Java Feature | Java Construct | COBOL Equivalent |
|---|---|---|
| `Greeting` record | `record Greeting(String recipient, String message)` | WORKING-STORAGE items `WS-RECIPIENT`, `WS-MESSAGE`, `WS-SALUTATION`; paragraph `DISPLAY-GREETING` |
| `Greeting.formatted()` | Returns decorated box string | Paragraph `DISPLAY-GREETING` using DISPLAY statements with +/- ASCII box art |
| `TimeOfDay` sealed interface | `Morning`, `Afternoon`, `Evening` sub-records | WORKING-STORAGE `WS-TIME-OF-DAY PIC X(15)`; EVALUATE logic in `DETERMINE-TIME-OF-DAY` |
| `TimeOfDay.of(hour)` | switch on hour | `EVALUATE TRUE` with `WHEN WS-HOUR < 12` etc. in paragraph `DETERMINE-TIME-OF-DAY` |
| `seasonOf(Month)` | switch on Month enum | `EVALUATE WS-MONTH` with WHEN clauses in paragraph `DETERMINE-SEASON` |
| `LocalDate.now()` | Java time API | `MOVE FUNCTION CURRENT-DATE TO WS-CURRENT-DATE` |
| `today.getDayOfMonth()` | day-of-month int | Extract from `WS-CURRENT-DATE(7:2)` |
| `today.getMonth()` | Month enum | Extract from `WS-CURRENT-DATE(5:2)` as numeric |
| `System.out.print(...)` | Console output | `DISPLAY` statement |
| Java version string | `System.getProperty("java.version")` | Replaced by literal `"GnuCOBOL"` version string or omit |
| Decorative Unicode box | `╔══╗ ║ ╚══╝` | ASCII fallback: `+--+  |  +--+` — GnuCOBOL terminals may not render UTF-8 box chars reliably; use ASCII art |
| Input validation | `IllegalArgumentException` | EVALUATE / IF checks with DISPLAY error and STOP RUN |
| `today.toString()` | ISO date string | Construct from WS-CURRENT-DATE subfields: YYYY-MM-DD |

---

## 2. Architecture Plan

The COBOL program will be a single source file `HELLOWORLD.cbl` structured as follows:

### IDENTIFICATION DIVISION
- `PROGRAM-ID. HELLOWORLD.`
- Author, date comments

### ENVIRONMENT DIVISION
- Minimal — no file I/O needed

### DATA DIVISION — WORKING-STORAGE SECTION

| Variable | PIC Clause | Purpose |
|---|---|---|
| `WS-CURRENT-DATE` | `PIC X(21)` | Raw output of FUNCTION CURRENT-DATE |
| `WS-YEAR` | `PIC 9(4)` | Current year |
| `WS-MONTH` | `PIC 9(2)` | Current month (01-12) |
| `WS-DAY` | `PIC 9(2)` | Current day of month |
| `WS-HOUR` | `PIC 9(2)` | Current hour (00-23) |
| `WS-DATE-DISPLAY` | `PIC X(10)` | Formatted date YYYY-MM-DD |
| `WS-TIME-OF-DAY` | `PIC X(15)` | "MORNING", "AFTERNOON", "EVENING" |
| `WS-SALUTATION` | `PIC X(20)` | "Good morning" / "Good afternoon" / "Good evening" |
| `WS-SEASON` | `PIC X(10)` | "Winter" / "Spring" / "Summer" / "Autumn" |
| `WS-RECIPIENT` | `PIC X(20)` | "World" |
| `WS-GREETING-LINE` | `PIC X(50)` | Assembled greeting line for box |
| `WS-HOUR-MOD` | `PIC 9(2)` | day-of-month MOD 24 (replicates Java logic) |

### PROCEDURE DIVISION Paragraphs

1. **MAIN-LOGIC** — entry point, calls all paragraphs in order, STOP RUN
2. **GET-CURRENT-DATE** — uses FUNCTION CURRENT-DATE, extracts year/month/day/hour
3. **DETERMINE-TIME-OF-DAY** — EVALUATE on WS-HOUR-MOD to set WS-SALUTATION
4. **DETERMINE-SEASON** — EVALUATE on WS-MONTH to set WS-SEASON
5. **BUILD-DATE-STRING** — assembles WS-DATE-DISPLAY as YYYY-MM-DD
6. **DISPLAY-GREETING** — prints the ASCII decorative box with salutation + "World"
7. **DISPLAY-INFO** — prints COBOL version label, date, and season

---

## 3. Data Mapping Detail

### CURRENT-DATE function layout (21 chars)
```
Positions  1- 4 : YYYY
Positions  5- 6 : MM
Positions  7- 8 : DD
Positions  9-10 : hh
Positions 11-12 : mm
Positions 13-14 : ss
Positions 15-16 : ss/100
Positions 17    : +/-
Positions 18-19 : offset hours
Positions 20-21 : offset minutes
```

### Box art design (ASCII, 34 chars wide)
```
+--------------------------------+
|  Good morning, World!          |
+--------------------------------+
```

The greeting line content is `WS-SALUTATION + ", " + WS-RECIPIENT + "!"` — padded / trimmed to fit the fixed-width box line.

---

## 4. Build Plan

### Compiler
**GnuCOBOL** (package `gnucobol` on Debian/Ubuntu, `open-cobol` on some distros).

```bash
# Install (if needed)
sudo apt-get install -y gnucobol

# Compile
cobc -x -free -o output/hello-world-cobol/helloworld \
     output/hello-world-cobol/HELLOWORLD.cbl

# Run
./output/hello-world-cobol/helloworld
```

### Test script
A shell script `output/hello-world-cobol/test.sh` will:
1. Compile the program
2. Run it and capture output
3. Assert output contains "Good", "World", a season name, and date pattern YYYY-MM-DD
4. Exit 0 on pass, 1 on failure

---

## 5. Risks & Notes

| Risk | Mitigation |
|---|---|
| Unicode box-drawing chars (╔ ╗ ║ ╚ ╝ ═) may not display correctly in all COBOL environments | Use ASCII art (`+`, `-`, `\|`) for portability |
| COBOL has no OOP — no records, interfaces, or sealed types | Flatten all state into WORKING-STORAGE; use paragraphs for behaviour |
| Java's `LocalDate.now()` — COBOL `FUNCTION CURRENT-DATE` returns a 21-char string, not structured | Parse subfields explicitly |
| Java uses `getDayOfMonth() % 24` to derive time-of-day (quirky demo logic) | Replicate exactly: `WS-HOUR-MOD = WS-DAY MOD 24` |
| COBOL string concatenation is verbose | Use STRING / MOVE / INSPECT or pre-build display lines in WS |
| No exception handling in COBOL | Use IF checks with DISPLAY + STOP RUN |
| GnuCOBOL free-format requires `-free` flag | Document in build script |

---

## 6. Target File Layout

```
output/
  analysis-report.md          ← this file
  hello-world-cobol/
    HELLOWORLD.cbl             ← main COBOL source
    test.sh                    ← compile + run + assert script
    README.md                  ← how to build & run
```
