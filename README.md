# copilot-test-ktruchcz

A Hello World application – originally written in Java 21, now also available as a C++ 17 port.

## C++ Build & Run

Requirements: **CMake ≥ 3.14** and a **C++17-capable compiler** (e.g. GCC 7+, Clang 5+).

```bash
# Configure & build
cmake -S . -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build

# Run the application
./build/hello_world

# Run tests (all 24 assertions)
./build/hello_world_test
# or via CTest
ctest --test-dir build --output-on-failure
```

## Java Build & Run

Requirements: **Java 21** and **Maven**.

```bash
export JAVA_HOME=/usr/lib/jvm/temurin-21-jdk-amd64
mvn clean verify
```