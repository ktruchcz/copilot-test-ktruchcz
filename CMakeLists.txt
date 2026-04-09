cmake_minimum_required(VERSION 3.16)
project(HelloWorld VERSION 1.0.0 LANGUAGES CXX)

# ── Global settings ────────────────────────────────────────────────────────────
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# ── Shared library (logic only, no main) ──────────────────────────────────────
# We compile the implementation once into a static library so that both the
# main executable and the test executable can link against it without
# recompiling hello_world.cpp twice.
add_library(hello_world_lib STATIC
    src/hello_world.cpp
)
target_include_directories(hello_world_lib PUBLIC src)

# Exclude main() from the library build by defining a preprocessor guard.
# The CPP file uses this guard around main() so that the library build skips it.
target_compile_definitions(hello_world_lib PRIVATE HELLO_WORLD_LIBRARY_BUILD)

# ── Main executable ────────────────────────────────────────────────────────────
add_executable(hello_world src/hello_world.cpp)
target_include_directories(hello_world PRIVATE src)

# ── Tests via doctest ─────────────────────────────────────────────────────────
# Download doctest header automatically if it is not already present.
include(FetchContent)

FetchContent_Declare(
    doctest
    GIT_REPOSITORY https://github.com/doctest/doctest.git
    GIT_TAG        v2.4.11
)
FetchContent_MakeAvailable(doctest)

add_executable(hello_world_test
    src/hello_world_test.cpp
    src/hello_world.cpp          # compile the impl directly into the test binary
)
target_include_directories(hello_world_test PRIVATE src)
target_link_libraries(hello_world_test PRIVATE doctest::doctest)

# Suppress main() in hello_world.cpp when building the test binary.
target_compile_definitions(hello_world_test PRIVATE HELLO_WORLD_LIBRARY_BUILD)

# Register with CTest so `ctest` / `cmake --build . --target test` works.
enable_testing()
add_test(NAME HelloWorldTests COMMAND hello_world_test)
