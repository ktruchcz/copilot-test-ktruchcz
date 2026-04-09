#pragma once

#include <string>
#include <stdexcept>

/**
 * Hello World application – C++ port of the Java 21 original.
 *
 * Mirrors the structure of the Java source:
 *  - Greeting  : immutable value type with input validation and formatted output
 *  - TimeOfDay : enum class with a factory function (equivalent to the sealed interface)
 *  - seasonOf  : free function mapping calendar month (1–12) to meteorological season
 */

// ---------------------------------------------------------------------------
// Greeting
// ---------------------------------------------------------------------------

/**
 * Immutable value object holding a greeting message.
 * Throws std::invalid_argument when either field is blank.
 */
struct Greeting {
    const std::string recipient;
    const std::string message;

    Greeting(std::string recipient, std::string message);

    /** Returns a box-framed greeting string. */
    std::string formatted() const;
};

// ---------------------------------------------------------------------------
// TimeOfDay
// ---------------------------------------------------------------------------

enum class TimeOfDay { Morning, Afternoon, Evening };

/** Maps an hour in [0, 23] to the appropriate TimeOfDay. */
TimeOfDay timeOfDayOf(int hour);

/** Returns the greeting salutation for the given TimeOfDay. */
std::string salutationFor(TimeOfDay tod);

// ---------------------------------------------------------------------------
// Season
// ---------------------------------------------------------------------------

/** Returns the meteorological season for a calendar month (1 = Jan … 12 = Dec). */
std::string seasonOf(int month);
