#include "HelloWorld.hpp"

#include <chrono>
#include <ctime>
#include <iostream>
#include <string>

int main() {
    // Get current local date
    auto now = std::chrono::system_clock::now();
    std::time_t now_t = std::chrono::system_clock::to_time_t(now);
    std::tm* local = std::localtime(&now_t);

    int hour  = local->tm_hour;
    int month = local->tm_mon + 1;  // tm_mon is 0-based

    // Determine time-of-day salutation
    auto tod       = timeOfDayOf(hour);
    auto salutation = salutationFor(tod);

    // Build and print greeting
    Greeting greeting("World", salutation);
    std::cout << greeting.formatted();

    // Print runtime info
    char dateBuf[32];
    std::strftime(dateBuf, sizeof(dateBuf), "%Y-%m-%d", local);

    std::cout << "C++ standard : C++17\n"
              << "Today's date : " << dateBuf
              << " (" << seasonOf(month) << ")\n";

    return 0;
}
