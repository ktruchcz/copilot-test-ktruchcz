#pragma once
/**
 * hello_world.hpp
 *
 * Public interface shared by hello_world.cpp and hello_world_test.cpp.
 */

#include <string>
#include <stdexcept>

// ── Greeting ─────────────────────────────────────────────────────────────────

struct Greeting {
    const std::string recipient;
    const std::string message;

    /// Constructs a Greeting; throws std::invalid_argument for blank inputs.
    Greeting(std::string recipient, std::string message);

    /// Returns a box-framed greeting string.
    std::string formatted() const;
};

// ── TimeOfDay ────────────────────────────────────────────────────────────────

enum class TimeOfDay { Morning, Afternoon, Evening };

/// Maps an hour value (0-23) to the appropriate TimeOfDay.
TimeOfDay timeOfDayOf(int hour);

// ── seasonOf ─────────────────────────────────────────────────────────────────

/// Returns the meteorological season for month numbers 1-12.
std::string seasonOf(int month);
