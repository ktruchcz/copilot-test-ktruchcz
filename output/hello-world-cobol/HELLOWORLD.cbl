       IDENTIFICATION DIVISION.
       PROGRAM-ID. HELLOWORLD.
      *> ============================================================
      *> HelloWorld -- GnuCOBOL migration of Java 21 HelloWorld
      *>
      *> Original Java features migrated:
      *>   record Greeting          -> WORKING-STORAGE + DISPLAY-GREETING paragraph
      *>   sealed TimeOfDay         -> EVALUATE TRUE in DETERMINE-TIME-OF-DAY
      *>   LocalDate.now()          -> FUNCTION CURRENT-DATE
      *>   getDayOfMonth() % 24     -> FUNCTION MOD(WS-DAY, 24)
      *>   seasonOf(Month)          -> EVALUATE WS-MONTH in DETERMINE-SEASON
      *>   Unicode box drawing      -> ASCII +--+ box art
      *>
      *> Compile : cobc -x -free -o helloworld HELLOWORLD.cbl
      *> Run     : ./helloworld
      *> ============================================================

       ENVIRONMENT DIVISION.

       DATA DIVISION.
       WORKING-STORAGE SECTION.

      *> ---- Date / time --------------------------------------------------
      *> Raw 21-character string returned by FUNCTION CURRENT-DATE:
      *>   Chars  1- 4  YYYY
      *>   Chars  5- 6  MM
      *>   Chars  7- 8  DD
      *>   Chars  9-10  hh
      *>   Chars 11-12  mm
      *>   Chars 13-14  ss
      *>   Chars 15-16  cc  (centiseconds)
      *>   Char  17     +/- (UTC offset sign)
      *>   Chars 18-19  UTC offset hours
      *>   Chars 20-21  UTC offset minutes
       01 WS-CURRENT-DATE              PIC X(21).
       01 WS-DATE-PARTS REDEFINES WS-CURRENT-DATE.
          05 WS-YEAR                   PIC 9(4).
          05 WS-MONTH                  PIC 9(2).
          05 WS-DAY                    PIC 9(2).
          05 WS-HOUR                   PIC 9(2).
          05 WS-MINUTE                 PIC 9(2).
          05 WS-SECOND                 PIC 9(2).
          05 WS-CENTISECOND            PIC 9(2).
          05 WS-TZ-SIGN                PIC X.
          05 WS-TZ-HOURS               PIC 9(2).
          05 WS-TZ-MINS                PIC 9(2).

      *> ---- Computed fields ----------------------------------------------
      *> Replicates Java: today.getDayOfMonth() % 24
       01 WS-HOUR-MOD                  PIC 9(2).

      *> ---- Greeting fields ----------------------------------------------
      *> "Good morning" / "Good afternoon" / "Good evening"  (max 14 chars)
       01 WS-SALUTATION                PIC X(15).

      *> ---- Season -------------------------------------------------------
      *> "Winter" / "Spring" / "Summer" / "Autumn"
       01 WS-SEASON                    PIC X(10).

      *> ---- Formatted date YYYY-MM-DD ------------------------------------
       01 WS-DATE-DISPLAY              PIC X(10).

      *> ---- Box inner content (32 chars fills between | ... | = 34 wide) -
       01 WS-GREETING-MSG              PIC X(32).

      *> ---- Info output line ---------------------------------------------
       01 WS-INFO-LINE                 PIC X(50).

      *> ===================================================================
       PROCEDURE DIVISION.
      *> ===================================================================

      *> -------------------------------------------------------------------
       MAIN-LOGIC.
      *> Entry point -- calls all paragraphs in order then stops.
      *> Mirrors Java main(): get date, determine time/season,
      *>                      format, display.
      *> -------------------------------------------------------------------
           PERFORM GET-CURRENT-DATE
           PERFORM DETERMINE-TIME-OF-DAY
           PERFORM DETERMINE-SEASON
           PERFORM BUILD-DATE-STRING
           PERFORM DISPLAY-GREETING
           PERFORM DISPLAY-INFO
           STOP RUN.

      *> -------------------------------------------------------------------
       GET-CURRENT-DATE.
      *> Mirrors: var today = LocalDate.now()
      *> FUNCTION CURRENT-DATE returns a 21-char string; WS-DATE-PARTS
      *> REDEFINES it to expose individual numeric subfields.
      *> -------------------------------------------------------------------
           MOVE FUNCTION CURRENT-DATE TO WS-CURRENT-DATE.

      *> -------------------------------------------------------------------
       DETERMINE-TIME-OF-DAY.
      *> Mirrors: TimeOfDay.of(today.getDayOfMonth() % 24)
      *>          then switch(timeOfDay) -> salutation string
      *>
      *> NOTE: Java uses getDayOfMonth() % 24 (NOT the actual clock hour).
      *>       This is intentional quirky demo logic -- replicated exactly.
      *>   day MOD 24 < 12          -> "Good morning"
      *>   day MOD 24 12..16        -> "Good afternoon"
      *>   day MOD 24 17..23        -> "Good evening"
      *> -------------------------------------------------------------------
           COMPUTE WS-HOUR-MOD = FUNCTION MOD(WS-DAY, 24)
           EVALUATE TRUE
               WHEN WS-HOUR-MOD < 12
                   MOVE "Good morning"   TO WS-SALUTATION
               WHEN WS-HOUR-MOD < 17
                   MOVE "Good afternoon" TO WS-SALUTATION
               WHEN OTHER
                   MOVE "Good evening"   TO WS-SALUTATION
           END-EVALUATE.

      *> -------------------------------------------------------------------
       DETERMINE-SEASON.
      *> Mirrors: seasonOf(today.getMonth())
      *>   12 / 1 / 2  -> Winter
      *>    3 / 4 / 5  -> Spring
      *>    6 / 7 / 8  -> Summer
      *>   9 / 10 / 11 -> Autumn
      *> Stacked WHEN clauses act as OR (fall-through to shared action).
      *> -------------------------------------------------------------------
           EVALUATE WS-MONTH
               WHEN 12
               WHEN 1
               WHEN 2
                   MOVE "Winter" TO WS-SEASON
               WHEN 3
               WHEN 4
               WHEN 5
                   MOVE "Spring" TO WS-SEASON
               WHEN 6
               WHEN 7
               WHEN 8
                   MOVE "Summer" TO WS-SEASON
               WHEN OTHER
                   MOVE "Autumn" TO WS-SEASON
           END-EVALUATE.

      *> -------------------------------------------------------------------
       BUILD-DATE-STRING.
      *> Mirrors: today.toString()  (ISO 8601: YYYY-MM-DD)
      *> Uses reference modification on WS-CURRENT-DATE to extract
      *> the YYYY, MM, DD substrings and assembles them with hyphens.
      *> -------------------------------------------------------------------
           MOVE SPACES TO WS-DATE-DISPLAY
           STRING WS-CURRENT-DATE(1:4) DELIMITED SIZE
                  "-"                  DELIMITED SIZE
                  WS-CURRENT-DATE(5:2) DELIMITED SIZE
                  "-"                  DELIMITED SIZE
                  WS-CURRENT-DATE(7:2) DELIMITED SIZE
             INTO WS-DATE-DISPLAY.

      *> -------------------------------------------------------------------
       DISPLAY-GREETING.
      *> Mirrors: System.out.print(greeting.formatted())
      *>
      *> Java original used Unicode box drawing characters (╔ ═ ╗ ║ ╚ ╝).
      *> GnuCOBOL output is ASCII-safe, so we use +, -, | instead.
      *>
      *> Box design (34 chars wide):
      *>   +--------------------------------+
      *>   |  <salutation>, World!          |
      *>   +--------------------------------+
      *>
      *> WS-GREETING-MSG is 32 chars -- MOVE SPACES pre-fills it, then
      *> STRING fills from the left; trailing spaces stay as padding.
      *> The final DISPLAY line is: | (1) + 32-char field + | (1) = 34.
      *> -------------------------------------------------------------------
           MOVE SPACES TO WS-GREETING-MSG
           STRING "  "                         DELIMITED SIZE
                  FUNCTION TRIM(WS-SALUTATION) DELIMITED SIZE
                  ", World!"                   DELIMITED SIZE
             INTO WS-GREETING-MSG
           DISPLAY "+--------------------------------+"
           DISPLAY "|" WS-GREETING-MSG "|"
           DISPLAY "+--------------------------------+".

      *> -------------------------------------------------------------------
       DISPLAY-INFO.
      *> Mirrors: System.out.print(info)
      *>   Java version : <java.version>   -> COBOL version : GnuCOBOL
      *>   Today's date : <date> (<season>) -> same pattern, ASCII date
      *>
      *> WS-SEASON is DELIMITED SPACE so trailing spaces are stripped
      *> before the closing ")" is appended.
      *> -------------------------------------------------------------------
           DISPLAY "COBOL version : GnuCOBOL"
           MOVE SPACES TO WS-INFO-LINE
           STRING "Today's date  : "  DELIMITED SIZE
                  WS-DATE-DISPLAY     DELIMITED SIZE
                  " ("                DELIMITED SIZE
                  WS-SEASON           DELIMITED SPACE
                  ")"                 DELIMITED SIZE
             INTO WS-INFO-LINE
           DISPLAY WS-INFO-LINE.
