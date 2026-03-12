package com.example;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;

/**
 * Unit tests for {@link HelloWorld}.
 */
class HelloWorldTest {

    @Test
    void getGreeting_returnsHelloWorld() {
        HelloWorld app = new HelloWorld();
        assertEquals("Hello World", app.getGreeting());
    }
}
