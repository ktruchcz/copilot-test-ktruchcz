package com.example;

import org.junit.jupiter.api.Test;

import java.io.ByteArrayOutputStream;
import java.io.PrintStream;

import static org.junit.jupiter.api.Assertions.assertEquals;

class HelloWorldTest {

    @Test
    void getMessage_returnsHelloWorld() {
        assertEquals("Hello World", HelloWorld.getMessage());
    }

    @Test
    void main_printsHelloWorld() {
        ByteArrayOutputStream outputStream = new ByteArrayOutputStream();
        PrintStream originalOut = System.out;
        System.setOut(new PrintStream(outputStream));

        try {
            HelloWorld.main(new String[]{});
        } finally {
            System.setOut(originalOut);
        }

        assertEquals("Hello World", outputStream.toString().trim());
    }
}
