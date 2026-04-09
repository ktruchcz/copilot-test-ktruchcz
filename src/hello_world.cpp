/**
 * hello_world.cpp
 *
 * C++17 port of the Java 21 HelloWorld application.
 *
 * Mirrors the original structure:
 *  - Greeting  : immutable value struct with validation and formatted()
 *  - TimeOfDay : scoped enum + factory function timeOfDayOf(hour)
 *  - seasonOf  : maps month numbers (1-12) to season strings
 *  - main()    : assembles everything and prints the greeting + info block
 */

#include "hello_world.hpp"

#include <chrono>
#include <ctime>
#include <iomanip>
#include <iostream>
#include <sstream>
#include <stdexcept>
#include <string>

// ── Greeting ────────────────────────────────────────────────────────────────

namespace {
/// Returns true if the string is empty or contains only whitespace.
bool isBlank(const std::string& s) {
    return s.find_first_not_of(" \t\n\r\f\v") == std::string::npos;
}
} // anonymous namespace

Greeting::Greeting(std::string recipient, std::string message)
    : recipient(std::move(recipient)), message(std::move(message))
{
    if (this->recipient.empty() || isBlank(this->recipient)) {
        throw std::invalid_argument("recipient must not be blank");
    }
    if (this->message.empty() || isBlank(this->message)) {
        throw std::invalid_argument("message must not be blank");
    }
}

std::string Greeting::formatted() const {
    // Build the centre line: "  <message>, <recipient>!  "
    std::string centre = "  " + message + ", " + recipient + "!  ";

    // The box is 32 characters wide (matching the Java original's
    // ╔══════════════════════════════╗  which spans 32 '═' chars).
    const int boxWidth = 32;
    std::string top    = "╔" + std::string(boxWidth, static_cast<char>(0)) + "╗";
    std::string bottom = "╚" + std::string(boxWidth, static_cast<char>(0)) + "╝";

    // Build proper UTF-8 box lines using the actual Unicode characters.
    top    = "╔══════════════════════════════╗";
    bottom = "╚══════════════════════════════╝";

    // Pad / truncate centre line to exactly boxWidth characters.
    if (static_cast<int>(centre.size()) < boxWidth) {
        centre.resize(boxWidth, ' ');
    }

    return top    + "\n"
         + "║" + centre + "║\n"
         + bottom + "\n";
}

// ── TimeOfDay ────────────────────────────────────────────────────────────────

TimeOfDay timeOfDayOf(int hour) {
    if (hour < 12)  return TimeOfDay::Morning;
    if (hour < 17)  return TimeOfDay::Afternoon;
    return TimeOfDay::Evening;
}

// ── seasonOf ─────────────────────────────────────────────────────────────────

std::string seasonOf(int month) {
    switch (month) {
        case 12: case 1: case 2:  return "Winter";
        case 3:  case 4: case 5:  return "Spring";
        case 6:  case 7: case 8:  return "Summer";
        case 9:  case 10: case 11: return "Autumn";
        default:
            throw std::invalid_argument("month must be between 1 and 12");
    }
}

// ── main ──────────────────────────────────────────────────────────────────────
// Excluded when this translation unit is compiled into a shared library
// or the test binary (both define HELLO_WORLD_LIBRARY_BUILD).
#ifndef HELLO_WORLD_LIBRARY_BUILD
int main() {
    // Obtain today's local date via the C standard library.
    const std::time_t now     = std::time(nullptr);
    const std::tm*    local   = std::localtime(&now);

    const int day   = local->tm_mday;          // 1-31
    const int month = local->tm_mon + 1;       // tm_mon is 0-based
    const int year  = local->tm_year + 1900;

    // Mirror Java: TimeOfDay.of(today.getDayOfMonth() % 24)
    TimeOfDay tod = timeOfDayOf(day % 24);

    std::string salutation;
    switch (tod) {
        case TimeOfDay::Morning:   salutation = "Good morning";   break;
        case TimeOfDay::Afternoon: salutation = "Good afternoon"; break;
        case TimeOfDay::Evening:   salutation = "Good evening";   break;
    }

    Greeting greeting("World", salutation);
    std::cout << greeting.formatted();

    // Format date as YYYY-MM-DD to match Java's LocalDate::toString.
    std::ostringstream dateBuf;
    dateBuf << year
            << '-' << std::setw(2) << std::setfill('0') << month
            << '-' << std::setw(2) << std::setfill('0') << day;

    std::cout << "C++ standard   : C++17\n"
              << "Today's date   : " << dateBuf.str()
              << " (" << seasonOf(month) << ")\n";

    return 0;
}
#endif // HELLO_WORLD_LIBRARY_BUILD
