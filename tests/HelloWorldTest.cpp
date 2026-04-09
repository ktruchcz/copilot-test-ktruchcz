#include "../src/cpp/HelloWorld.hpp"

#include <iostream>
#include <stdexcept>
#include <string>

// ---------------------------------------------------------------------------
// Minimal test framework
// ---------------------------------------------------------------------------

static int total = 0;
static int passed = 0;

static void assertEqual(const std::string& expected, const std::string& actual,
                        const std::string& label) {
    ++total;
    if (expected == actual) {
        ++passed;
        std::cout << "[PASS] " << label << "\n";
    } else {
        std::cout << "[FAIL] " << label
                  << "\n  expected: " << expected
                  << "\n  actual  : " << actual << "\n";
    }
}

static void assertTrue(bool condition, const std::string& label) {
    ++total;
    if (condition) {
        ++passed;
        std::cout << "[PASS] " << label << "\n";
    } else {
        std::cout << "[FAIL] " << label << "\n";
    }
}

template<typename Fn>
static void assertThrows(Fn fn, const std::string& label) {
    ++total;
    try {
        fn();
        std::cout << "[FAIL] " << label << " (no exception thrown)\n";
    } catch (const std::exception&) {
        ++passed;
        std::cout << "[PASS] " << label << "\n";
    }
}

// ---------------------------------------------------------------------------
// Greeting tests
// ---------------------------------------------------------------------------

static void greetingStoresFields() {
    Greeting g("World", "Hello");
    assertEqual("World", g.recipient, "greetingStoresFields – recipient");
    assertEqual("Hello", g.message,   "greetingStoresFields – message");
}

static void greetingFormattedContainsRecipientAndMessage() {
    Greeting g("Alice", "Hi");
    auto result = g.formatted();
    assertTrue(result.find("Alice") != std::string::npos,
               "greetingFormattedContainsRecipient");
    assertTrue(result.find("Hi") != std::string::npos,
               "greetingFormattedContainsMessage");
}

static void greetingRejectsBlankRecipient() {
    assertThrows([]{ Greeting("", "Hello"); },
                 "greetingRejectsBlankRecipient");
}

static void greetingRejectsBlankMessage() {
    assertThrows([]{ Greeting("World", "   "); },
                 "greetingRejectsBlankMessage");
}

// ---------------------------------------------------------------------------
// TimeOfDay tests
// ---------------------------------------------------------------------------

static void timeOfDayMorningForHourLessThan12() {
    assertTrue(timeOfDayOf(0)  == TimeOfDay::Morning, "timeOfDay_Morning_hour0");
    assertTrue(timeOfDayOf(11) == TimeOfDay::Morning, "timeOfDay_Morning_hour11");
}

static void timeOfDayAfternoonForHour12To16() {
    assertTrue(timeOfDayOf(12) == TimeOfDay::Afternoon, "timeOfDay_Afternoon_hour12");
    assertTrue(timeOfDayOf(16) == TimeOfDay::Afternoon, "timeOfDay_Afternoon_hour16");
}

static void timeOfDayEveningForHour17AndAbove() {
    assertTrue(timeOfDayOf(17) == TimeOfDay::Evening, "timeOfDay_Evening_hour17");
    assertTrue(timeOfDayOf(23) == TimeOfDay::Evening, "timeOfDay_Evening_hour23");
}

// ---------------------------------------------------------------------------
// seasonOf tests
// ---------------------------------------------------------------------------

static void seasonOfReturnsCorrectSeason() {
    // Winter
    assertEqual("Winter", seasonOf(12), "seasonOf_December");
    assertEqual("Winter", seasonOf(1),  "seasonOf_January");
    assertEqual("Winter", seasonOf(2),  "seasonOf_February");
    // Spring
    assertEqual("Spring", seasonOf(3),  "seasonOf_March");
    assertEqual("Spring", seasonOf(4),  "seasonOf_April");
    assertEqual("Spring", seasonOf(5),  "seasonOf_May");
    // Summer
    assertEqual("Summer", seasonOf(6),  "seasonOf_June");
    assertEqual("Summer", seasonOf(7),  "seasonOf_July");
    assertEqual("Summer", seasonOf(8),  "seasonOf_August");
    // Autumn
    assertEqual("Autumn", seasonOf(9),  "seasonOf_September");
    assertEqual("Autumn", seasonOf(10), "seasonOf_October");
    assertEqual("Autumn", seasonOf(11), "seasonOf_November");
}

// ---------------------------------------------------------------------------
// main
// ---------------------------------------------------------------------------

int main() {
    greetingStoresFields();
    greetingFormattedContainsRecipientAndMessage();
    greetingRejectsBlankRecipient();
    greetingRejectsBlankMessage();

    timeOfDayMorningForHourLessThan12();
    timeOfDayAfternoonForHour12To16();
    timeOfDayEveningForHour17AndAbove();

    seasonOfReturnsCorrectSeason();

    std::cout << "\n" << passed << " / " << total << " tests passed.\n";
    return (passed == total) ? 0 : 1;
}
