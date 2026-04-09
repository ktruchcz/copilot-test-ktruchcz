# Migration Requirements Checklist: Java 21 → Python 3

**Purpose**: Requirements quality audit for the Java 21 → Python 3 Hello World migration — validating completeness, clarity, consistency, measurability, and scenario coverage of the written specification.
**Created**: 2026-04-09
**Feature**: [specs/001-java-to-python-migration/spec.md](../specs/001-java-to-python-migration/spec.md)
**Actor / Timing**: Reviewer — pre-implementation gate

> **Scope**: Items below are *unit tests for the requirements themselves* — each asks whether a requirement is well-written, not whether the implementation is correct.  
> Check items off as you read the spec/plan artefacts: `[ ]` open · `[x]` satisfied · `[-]` intentionally excluded / N/A.

---

## 1 · Construct Mapping — Completeness & Clarity

*Are all Java → Python construct translations fully and unambiguously specified?*

- [ ] CHK001 — Is the `Greeting` Java record → Python `@dataclass(frozen=True)` mapping complete, covering field names (`recipient`, `message`), field types (`str`), and the exact validation behaviour at construction time? [Completeness, Spec §Key Entities]
- [ ] CHK002 — Is the immutability equivalence between Java `record` and `@dataclass(frozen=True)` explicitly stated, including what error (`FrozenInstanceError`) is raised on post-construction attribute assignment? [Clarity, Spec §Key Entities]
- [ ] CHK003 — Is `__post_init__` specified as the validation hook for `Greeting`, and does this align consistently between the spec's Key Entities section and the data model's validation pattern? [Consistency, Spec §Key Entities vs Plan §data-model.md]
- [ ] CHK004 — Is the Java sealed interface → Python ABC hierarchy mapping complete? Does the spec define that `TimeOfDay` must be non-instantiable and that `Morning`, `Afternoon`, `Evening` are the only three permitted concrete subclasses? [Completeness, Spec §FR-008]
- [ ] CHK005 — Is the naming convention change from Java `TimeOfDay.of(hour)` to Python `time_of_day(hour)` (camelCase → snake_case; static method → module-level function) explicitly documented rather than left as an assumed idiom? [Clarity, Plan §research.md Research Item 2]
- [ ] CHK006 — Is the `match/case` guard-pattern requirement specified for *both* `time_of_day()` and `season_of()` explicitly in FR-008 and FR-009, rather than only implied by comparison to the Java switch expression? [Clarity, Spec §FR-008, §FR-009]
- [ ] CHK007 — Is the Java text block (`"""…""".formatted()`) → Python multiline string / f-string translation documented, including the requirement that `Greeting.formatted()` must always end with a trailing newline (`\n`)? [Completeness, Spec §FR-004, Plan §contracts/python-module-contract.md]
- [ ] CHK008 — Is the Java `IllegalArgumentException` → Python `ValueError` exception-type mapping explicitly stated in the spec (not only in the research document), so it is authoritative for implementers? [Traceability, Spec §FR-005, §FR-006]
- [ ] CHK009 — Is the Python 3.10+ version constraint traceable to the `match/case` syntax requirement in FR-008 and FR-009, establishing the dependency chain: `match/case` → Python ≥ 3.10? [Traceability, Spec §Assumptions, §FR-008, §FR-009]
- [ ] CHK010 — Are the exact inner-padding rules for `Greeting.formatted()` (two spaces on each side of the content line: `║  {message}, {recipient}!  ║`) specified precisely enough to be objectively verified? [Clarity, Plan §data-model.md Box Format]

---

## 2 · Test Parity — Completeness & Coverage

*Are all 8 JUnit 5 test functions mapped 1-for-1 to pytest equivalents with no gaps?*

- [ ] CHK011 — Are all 8 JUnit 5 test functions individually named in the spec or plan with their direct pytest counterpart names, preventing accidental omission during migration? [Completeness, Spec §FR-011]
- [ ] CHK012 — Does the spec distinguish between 8 test *functions* and 19 total test *invocations* (7 regular + 12 parametrized)? Is "8 migrated test cases" in SC-001 unambiguously defined as 8 test functions rather than 8 individual assertions? [Clarity, Spec §SC-001, §FR-011]
- [ ] CHK013 — Is the `@ParameterizedTest` + `@CsvSource` (12 rows) → `@pytest.mark.parametrize` (12 cases) mapping specified for the season test, and does FR-012 require *exactly* 12 cases (one per calendar month) with no duplicates? [Completeness, Spec §FR-012, §SC-002]
- [ ] CHK014 — Is the pytest assertion idiom for type-checking specified? Specifically, is `assertInstanceOf(X.class, obj)` → `assert isinstance(obj, X)` documented to prevent use of equality assertions instead? [Clarity, Spec §FR-011]
- [ ] CHK015 — Is the translation of `assertThrows(IllegalArgumentException.class, lambda)` to `pytest.raises(ValueError)` explicitly required in the spec or plan, covering both the blank-recipient and blank-message test cases? [Clarity, Spec §FR-005, §FR-006, §FR-011]
- [ ] CHK016 — Is the use of `@pytest.fixture` for a shared `Greeting("World", "Hello")` instance specified in the plan, and is it clear which test functions are expected to use it vs. construct their own instances? [Completeness, Plan §Post-Phase-1 Re-check]
- [ ] CHK017 — Is the 100% coverage requirement (SC-004) specified with enough granularity? Does it explicitly include: all branches of `time_of_day()` (3 arms), all arms of `season_of()` (4 arms), both `__post_init__` validation branches, and `main()`? [Clarity, Spec §SC-004]
- [ ] CHK018 — Is there a requirement specifying the pytest test file naming convention (`test_hello_world.py`) so that test discovery works without any `conftest.py` or `pytest.ini` path manipulation? [Completeness, Spec §Assumptions]
- [ ] CHK019 — Does the spec define what "without modification to test logic" (SC-001) means in practice — i.e., are there any allowable differences (e.g., fixture usage, import style) or must the test logic be structurally identical to the JUnit original? [Clarity, Spec §SC-001]

---

## 3 · Output Layout — Completeness & Consistency

*Are the three required output files and their placement unambiguously specified?*

- [ ] CHK020 — Are all three required output files (`output/hello_world.py`, `output/test_hello_world.py`, `output/pyproject.toml`) listed as explicit mandatory deliverables in the spec, not only implied by the plan? [Completeness, Plan §Project Structure]
- [ ] CHK021 — Is there a requirement explicitly prohibiting Python source from being placed in `src/` (the Java source tree), ensuring the co-existence constraint is enforced? [Clarity, Plan §Project Structure]
- [ ] CHK022 — Is `output/README.md` specified as a mandatory or optional deliverable? If mandatory, are its required contents defined? [Completeness, Plan §Project Structure, Gap]
- [ ] CHK023 — Is the `output/` directory's role as an installable Python project (`pip install -e output/[dev]`) consistent with the `pyproject.toml` placement, and is this relationship documented in the spec or quickstart? [Consistency, Plan §Structure Decision, Plan §quickstart.md]
- [ ] CHK024 — Is the relationship between the flat `output/` layout and pytest discovery (`pytest output/ -v`) explicitly documented so that test path requirements are traceable to the project structure decision? [Traceability, Plan §quickstart.md]

---

## 4 · Validation Clarity — Specificity & Measurability

*Are the ValueError trigger conditions and error messages specified without ambiguity?*

- [ ] CHK025 — Are all three invalid-input categories — `None`, empty string `""`, and whitespace-only string `"   "` — individually enumerated in FR-005 and FR-006, with no ambiguity about what "blank" encompasses? [Clarity, Spec §FR-005, §FR-006]
- [ ] CHK026 — Is the exact `ValueError` message text ("recipient must not be blank" / "message must not be blank") specified in the spec, or are implementers free to choose any error message string? [Clarity, Plan §data-model.md Validation Rules]
- [ ] CHK027 — Is the validation order (recipient checked before message, or vice versa) either explicitly specified or intentionally left as an implementation detail? Is either choice traceable to a requirement? [Clarity, Spec §FR-005, §FR-006, Gap]
- [ ] CHK028 — Does the contract (Plan §contracts/python-module-contract.md) type-annotate `recipient` and `message` as `str`, and if so, is there a requirement clarifying that the type annotation does NOT prevent `None` from being passed at runtime (and must still be guarded against)? [Consistency, Plan §contracts/python-module-contract.md]
- [ ] CHK029 — Is the `not self.recipient or not self.recipient.strip()` guard pattern specified as the required validation logic, or is only the observable behaviour (raises `ValueError`) specified, leaving the implementation pattern open? [Clarity, Plan §research.md Research Item 1]

---

## 5 · Unicode Consistency — Completeness & Measurability

*Are box-drawing character requirements specified precisely enough to guarantee identical output?*

- [ ] CHK030 — Are the exact Unicode code points for all six box-drawing characters explicitly specified in the requirements? (╔ U+2554, ═ U+2550, ╗ U+2557, ║ U+2551, ╚ U+255A, ╝ U+255D) [Clarity, Spec §FR-004]
- [ ] CHK031 — Is the exact count of `═` characters in the top and bottom borders (30×) specified as a concrete requirement, rather than delegating "match the Java source" as the acceptance criterion? [Completeness, Plan §data-model.md Box Format]
- [ ] CHK032 — Is a UTF-8 file encoding requirement specified for `hello_world.py` to guarantee box-drawing characters are preserved when the file is read on non-UTF-8 default-encoding platforms? [Completeness, Spec §FR-004, Gap]
- [ ] CHK033 — Is there a requirement defining the expected behaviour of `Greeting.formatted()` when the combined content (`{message}, {recipient}!`) is longer than the fixed 30-character border — does it overflow, truncate, or wrap? [Edge Case, Spec §FR-004, Gap]
- [ ] CHK034 — Is "visually identical in structure" (SC-003) quantified beyond subjective assessment — e.g., does the spec require exact stdout string matching against a reference string, or only structural element presence? [Measurability, Spec §SC-003]

---

## 6 · Environment — Completeness & Traceability

*Are the Python version floor, packaging tool, and dependency constraints fully specified?*

- [ ] CHK035 — Is Python 3.10 stated as a *hard minimum* version requirement (not a recommendation), with the rationale (`match/case` syntax) explicitly traceable to FR-008 and FR-009? [Traceability, Spec §Assumptions, §FR-008, §FR-009]
- [ ] CHK036 — Is the `pyproject.toml`-only constraint specified as an *exclusive* requirement — explicitly prohibiting `setup.py`, `requirements.txt`, and `setup.cfg` — rather than only stating what is preferred? [Completeness, Spec §Assumptions]
- [ ] CHK037 — Is the `[project.optional-dependencies]` structure for pytest specified with a concrete key name (e.g., `dev = ["pytest>=7.0"]`) and a minimum pytest version, or is the structure left ambiguous? [Clarity, Spec §Assumptions, Plan §Technical Context]
- [ ] CHK038 — Is a `[build-system]` backend requirement specified for `pyproject.toml` (e.g., `hatchling`, `flit-core`, or `setuptools`)? Without it, `pip install -e output/[dev]` may behave differently across pip versions. [Gap, Plan §Technical Context]
- [ ] CHK039 — Is the stdlib-only runtime dependency constraint stated as a hard requirement, and are the consequences of adding a third-party runtime library explicitly defined (e.g., Constitution Principle V violation)? [Completeness, Spec §SC-005, §Assumptions]
- [ ] CHK040 — Is the acceptance criterion for "no errors or warnings on a clean Python 3 environment" (SC-005) measurable? Does it specify which Python version(s), which OS(es), and what constitutes a "clean" environment (e.g., fresh virtualenv)? [Measurability, Spec §SC-005]

---

## 7 · Scenario Coverage — Completeness & Boundary Precision

*Are all hour boundaries, all 12 month cases, and all edge paths present in the requirements?*

- [ ] CHK041 — Are requirements defined for all six `time_of_day()` boundary inputs (hours 0, 11, 12, 16, 17, 23) with the exact expected return type (`Morning`, `Afternoon`, `Evening`) specified for each? [Completeness, Spec §FR-007, §Edge Cases]
- [ ] CHK042 — Are the boundary transitions 11→12 (Morning→Afternoon) and 16→17 (Afternoon→Evening) explicitly described as *inclusive on the upper bound of Afternoon* (i.e., hour 16 → Afternoon, hour 17 → Evening), eliminating any off-by-one ambiguity? [Clarity, Spec §FR-007, §Edge Cases]
- [ ] CHK043 — Are all 12 month → season mappings individually tabulated in the spec (not just grouped by season), ensuring no month is accidentally omitted from the parametrized test? [Completeness, Spec §FR-009, §FR-012]
- [ ] CHK044 — Is the December (month 12) → "Winter" mapping explicitly called out as the non-obvious case where winter spans two calendar years (December–February), requiring the `12, 1, 2` grouping rather than a simple sequential range? [Clarity, Spec §FR-009]
- [ ] CHK045 — Is the `season_of()` parameter defined as 1-based integer (compatible with `datetime.date.today().month`) rather than zero-based or a `Month` enum, and is this type constraint explicit in both FR-009 and the module contract? [Clarity, Spec §FR-009, Plan §contracts/python-module-contract.md]
- [ ] CHK046 — Is the undefined behaviour for `time_of_day()` inputs outside 0–23 and `season_of()` inputs outside 1–12 explicitly documented as intentional non-requirements, preventing scope creep or silent incorrect output? [Coverage, Spec §Edge Cases]
- [ ] CHK047 — Are requirements defined for the three `main()` salutation scenarios at boundary hours (hour 0 → "Good morning", hour 12 → "Good afternoon", hour 17 → "Good evening") to verify the integration of `time_of_day()` with the greeting text? [Coverage, Spec §US-1 Acceptance Scenarios]
- [ ] CHK048 — Is the `main()` info-block output format (two lines: `Python version : …` and `Today's date   : YYYY-MM-DD (Season)`) specified with exact label text and spacing, so it can be verified against the quickstart's expected output without guesswork? [Clarity, Spec §FR-002, Plan §quickstart.md]

---

## 8 · Non-Functional Requirements — Measurability

*Are quality attributes quantified or explicitly scoped out?*

- [ ] CHK049 — Is the 100% test coverage goal (SC-004) paired with a specified measurement tool (e.g., `pytest-cov`) and coverage type (line coverage only, or branch coverage required too)? [Measurability, Spec §SC-004, Gap]
- [ ] CHK050 — Are performance requirements intentionally absent, and is this explicitly documented given that SC-005 implies "no errors or warnings" but makes no latency or throughput statement? [Completeness, Plan §Performance Goals]
- [ ] CHK051 — Is there a requirement specifying the expected exit code of `hello_world.py` on successful execution (exit code 0) and on any unhandled error, so SC-005 ("no errors") is verifiable? [Measurability, Spec §SC-005, Gap]

---

## 9 · Dependencies & Assumptions — Completeness & Consistency

*Are all assumptions documented, and do they align with each other and with the requirements?*

- [ ] CHK052 — Is the assumption that "Java source files are the authoritative reference" consistent with the plan's documented intentional divergence in `main()` (Python uses `datetime.datetime.now().hour` while Java uses `today.getDayOfMonth() % 24`)? Is it clear which source is authoritative for `main()` specifically? [Consistency, Spec §Assumptions vs Plan §Complexity Tracking]
- [ ] CHK053 — Is the assumption that Java source and Maven build files remain untouched backed by an explicit requirement (or prohibition) preventing modification to `HelloWorld.java`, `HelloWorldTest.java`, and `pom.xml`? [Completeness, Spec §Assumptions]
- [ ] CHK054 — Is the `platform.python_version()` output format in the info block (`Python version : {platform.python_version()}`) specified and consistent with the quickstart's expected output, so the test for FR-002 has a deterministic reference? [Completeness, Spec §FR-002, Plan §quickstart.md]
- [ ] CHK055 — Is there a requirement establishing a traceability ID scheme for acceptance criteria (SC-001 through SC-005) that maps each success criterion back to the specific functional requirements it validates? [Traceability, Spec §Success Criteria]

---

## 10 · Ambiguities & Conflicts

*Are there open questions in the spec that could lead to divergent implementations?*

- [ ] CHK056 — Does SC-003 ("visually identical in structure to the Java application's output") conflict with the plan's intentional divergence in hour derivation (`getDayOfMonth() % 24` vs `datetime.now().hour`)? Is this conflict explicitly resolved with a statement that SC-003 covers output *structure*, not the hour-selection mechanism? [Conflict, Spec §SC-003 vs Plan §Complexity Tracking]
- [ ] CHK057 — Is the traceability gap between FR-011 ("8 test cases") and the Java test file's actual method count (8 methods, 19 invocations) resolved? Could a reader interpret SC-001 as requiring 8 parametrized season invocations rather than 8 test function definitions? [Clarity, Spec §FR-011, §SC-001]
- [ ] CHK058 — Is the `Greeting.formatted()` fixed-width border (30× `═`) consistent with what the Java `formatted()` text block actually produces, and is this consistency explicitly stated as a requirement rather than assumed from the Java source? [Consistency, Spec §FR-004, Plan §data-model.md]
- [ ] CHK059 — Is the term "meteorological season" used in FR-009 and SC-002 defined unambiguously — i.e., is there a statement that it follows the Northern Hemisphere calendar convention (Dec–Feb = Winter) rather than astronomical seasons? [Clarity, Spec §FR-009, §Assumptions]

---

## Notes

- Check items off as completed: `[x]` satisfied, `[-]` intentionally excluded / N/A
- Add inline comments for findings: e.g., `[x] CHK003 — confirmed: spec §Key Entities and data-model.md use identical __post_init__ pattern`
- Items marked `[Gap]` indicate requirements that appear to be missing from the spec and should be added or explicitly excluded
- Items marked `[Conflict]` indicate potential inconsistencies between spec sections or between spec and plan that need resolution before implementation begins
- Total items: **59** across 10 categories
