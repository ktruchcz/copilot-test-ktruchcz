package com.example;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;

class HelloWorldTest {

    @Test
    void getGreeting_returnsExpectedMessage() {
        var app = new HelloWorld();
        assertEquals("Hello, World!", app.getGreeting());
    }
}
