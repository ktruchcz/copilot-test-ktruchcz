#include "HelloWorld.hpp"

#include <algorithm>
#include <stdexcept>
#include <string>

// ---------------------------------------------------------------------------
// Greeting
// ---------------------------------------------------------------------------

static bool isBlank(const std::string& s) {
    return std::all_of(s.begin(), s.end(), [](unsigned char c){ return std::isspace(c); });
}

Greeting::Greeting(std::string recipient_, std::string message_)
    : recipient(std::move(recipient_)), message(std::move(message_))
{
    if (recipient.empty() || isBlank(recipient)) {
        throw std::invalid_argument("recipient must not be blank");
    }
    if (message.empty() || isBlank(message)) {
        throw std::invalid_argument("message must not be blank");
    }
}

std::string Greeting::formatted() const {
    return
        "\u2554\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550"
        "\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550"
        "\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2557\n"
        "\u2551  " + message + ", " + recipient + "!  \u2551\n"
        "\u255a\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550"
        "\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550"
        "\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u255d\n";
}

// ---------------------------------------------------------------------------
// TimeOfDay
// ---------------------------------------------------------------------------

TimeOfDay timeOfDayOf(int hour) {
    if (hour < 12)  return TimeOfDay::Morning;
    if (hour < 17)  return TimeOfDay::Afternoon;
    return TimeOfDay::Evening;
}

std::string salutationFor(TimeOfDay tod) {
    switch (tod) {
        case TimeOfDay::Morning:   return "Good morning";
        case TimeOfDay::Afternoon: return "Good afternoon";
        case TimeOfDay::Evening:   return "Good evening";
    }
    return "Hello"; // defensive fallback for out-of-range enum values (e.g. via a cast)
}

// ---------------------------------------------------------------------------
// Season
// ---------------------------------------------------------------------------

std::string seasonOf(int month) {
    switch (month) {
        case 12: case 1: case 2:  return "Winter";
        case 3:  case 4: case 5:  return "Spring";
        case 6:  case 7: case 8:  return "Summer";
        case 9:  case 10: case 11: return "Autumn";
        default: throw std::invalid_argument("month must be in [1, 12]");
    }
}
