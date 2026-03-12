package com.example;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;

class GreeterTest {

    private final Greeter greeter = new Greeter();

    @Test
    void greetWithName() {
        assertEquals("Hello, Alice!", greeter.greet("Alice"));
    }

    @Test
    void greetWithNullName() {
        assertEquals("Hello, World!", greeter.greet(null));
    }

    @Test
    void greetWithBlankName() {
        assertEquals("Hello, World!", greeter.greet("   "));
    }

    @Test
    void greetWithEmptyName() {
        assertEquals("Hello, World!", greeter.greet(""));
    }
}
