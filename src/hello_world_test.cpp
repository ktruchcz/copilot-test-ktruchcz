/**
 * hello_world_test.cpp
 *
 * Unit tests for the C++17 HelloWorld port.
 * Uses the header-only doctest framework (fetched automatically by CMake).
 *
 * Test coverage mirrors HelloWorldTest.java:
 *  - Greeting field storage
 *  - Greeting::formatted() contains recipient + message
 *  - Greeting rejects blank recipient
 *  - Greeting rejects blank message
 *  - TimeOfDay classification (Morning / Afternoon / Evening)
 *  - seasonOf() for all 12 months
 */

#define DOCTEST_CONFIG_IMPLEMENT_WITH_MAIN
#include <doctest/doctest.h>

#include "hello_world.hpp"

// ── Greeting tests ────────────────────────────────────────────────────────────

TEST_CASE("Greeting stores recipient and message fields") {
    Greeting g("World", "Hello");
    CHECK(g.recipient == "World");
    CHECK(g.message   == "Hello");
}

TEST_CASE("Greeting::formatted() contains recipient and message") {
    Greeting g("Alice", "Hi");
    std::string result = g.formatted();
    CHECK(result.find("Alice") != std::string::npos);
    CHECK(result.find("Hi")    != std::string::npos);
}

TEST_CASE("Greeting rejects blank recipient") {
    CHECK_THROWS_AS(Greeting("", "Hello"),       std::invalid_argument);
    CHECK_THROWS_AS(Greeting("   ", "Hello"),    std::invalid_argument);
}

TEST_CASE("Greeting rejects blank message") {
    CHECK_THROWS_AS(Greeting("World", ""),       std::invalid_argument);
    CHECK_THROWS_AS(Greeting("World", "  "),     std::invalid_argument);
}

// ── TimeOfDay tests ───────────────────────────────────────────────────────────

TEST_CASE("timeOfDayOf returns Morning for hours 0-11") {
    CHECK(timeOfDayOf(0)  == TimeOfDay::Morning);
    CHECK(timeOfDayOf(11) == TimeOfDay::Morning);
}

TEST_CASE("timeOfDayOf returns Afternoon for hours 12-16") {
    CHECK(timeOfDayOf(12) == TimeOfDay::Afternoon);
    CHECK(timeOfDayOf(16) == TimeOfDay::Afternoon);
}

TEST_CASE("timeOfDayOf returns Evening for hours 17-23") {
    CHECK(timeOfDayOf(17) == TimeOfDay::Evening);
    CHECK(timeOfDayOf(23) == TimeOfDay::Evening);
}

// ── seasonOf tests ────────────────────────────────────────────────────────────

TEST_CASE("seasonOf returns correct season for every month") {
    // Winter
    CHECK(seasonOf(12) == "Winter");
    CHECK(seasonOf(1)  == "Winter");
    CHECK(seasonOf(2)  == "Winter");

    // Spring
    CHECK(seasonOf(3)  == "Spring");
    CHECK(seasonOf(4)  == "Spring");
    CHECK(seasonOf(5)  == "Spring");

    // Summer
    CHECK(seasonOf(6)  == "Summer");
    CHECK(seasonOf(7)  == "Summer");
    CHECK(seasonOf(8)  == "Summer");

    // Autumn
    CHECK(seasonOf(9)  == "Autumn");
    CHECK(seasonOf(10) == "Autumn");
    CHECK(seasonOf(11) == "Autumn");
}

TEST_CASE("seasonOf throws for out-of-range month") {
    CHECK_THROWS_AS(seasonOf(0),  std::invalid_argument);
    CHECK_THROWS_AS(seasonOf(13), std::invalid_argument);
}
