#!/usr/bin/env bash
# =============================================================================
# test.sh — compile, run, and assert HelloWorld GnuCOBOL program
#
# Usage:
#   cd output/hello-world-cobol
#   bash test.sh
#
# Exit codes:
#   0 — all assertions passed
#   1 — one or more assertions failed or compilation error
# =============================================================================
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CBL="$SCRIPT_DIR/HELLOWORLD.cbl"
EXE="$SCRIPT_DIR/helloworld"

# ---- Compile ----------------------------------------------------------------
echo "==> Compiling HELLOWORLD.cbl ..."
cobc -x -free -o "$EXE" "$CBL"
echo "    Compile OK"

# ---- Run --------------------------------------------------------------------
echo ""
echo "==> Running ./helloworld ..."
OUTPUT="$("$EXE")"
echo "$OUTPUT"
echo ""

# ---- Assertions -------------------------------------------------------------
echo "==> Running assertions ..."
PASS=0
FAIL=0

assert_contains() {
    local desc="$1"
    local pattern="$2"
    if echo "$OUTPUT" | grep -qE "$pattern"; then
        echo "    PASS: $desc"
        ((PASS++)) || true
    else
        echo "    FAIL: $desc  [pattern: '$pattern' not found in output]"
        ((FAIL++)) || true
    fi
}

# Box borders
assert_contains "Top border line"       '^\+--------------------------------\+$'
assert_contains "Bottom border line"    '^\+--------------------------------\+$'

# Inner greeting line: starts with | and ends with |, exactly 34 chars
assert_contains "Greeting line format"  '^\|.{32}\|$'

# The word "Good" appears in the greeting
assert_contains "Salutation 'Good'"     'Good'

# "World" appears in the greeting
assert_contains "Recipient 'World'"     'World'

# One of the three salutations is present
assert_contains "Valid salutation"      'Good (morning|afternoon|evening), World'

# COBOL version line
assert_contains "COBOL version label"   'COBOL version : GnuCOBOL'

# Date label
assert_contains "Date label present"    "Today's date"

# Date in YYYY-MM-DD format
assert_contains "Date format YYYY-MM-DD" '[0-9]{4}-[0-9]{2}-[0-9]{2}'

# Season name
assert_contains "Season present"        '(Winter|Spring|Summer|Autumn)'

# Season appears inside parentheses on the date line
assert_contains "Season in parentheses" '\((Winter|Spring|Summer|Autumn)\)'

# ---- Summary ----------------------------------------------------------------
echo ""
echo "==> Results: ${PASS} passed, ${FAIL} failed"
if [ "$FAIL" -gt 0 ]; then
    echo "==> FAILED"
    exit 1
fi
echo "==> All assertions passed!"
exit 0
