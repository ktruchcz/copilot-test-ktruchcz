package com.example;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;

class HelloWorldTest {

    @Test
    void testGetGreeting() {
        String greeting = HelloWorld.getGreeting();
        assertNotNull(greeting);
        assertEquals("Hello World", greeting);
    }
}
