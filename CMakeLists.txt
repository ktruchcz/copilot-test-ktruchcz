cmake_minimum_required(VERSION 3.14)
project(HelloWorld LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# ---------------------------------------------------------------------------
# Library (shared logic – no main)
# ---------------------------------------------------------------------------
add_library(hello_world_lib STATIC
    src/cpp/HelloWorld.cpp
)
target_include_directories(hello_world_lib PUBLIC src/cpp)

# ---------------------------------------------------------------------------
# Main executable
# ---------------------------------------------------------------------------
add_executable(hello_world src/cpp/main.cpp)
target_link_libraries(hello_world PRIVATE hello_world_lib)

# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------
enable_testing()

add_executable(hello_world_test tests/HelloWorldTest.cpp)
target_link_libraries(hello_world_test PRIVATE hello_world_lib)
target_include_directories(hello_world_test PRIVATE src/cpp)

add_test(NAME HelloWorldTest COMMAND hello_world_test)
