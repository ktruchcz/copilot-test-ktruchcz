package com.example;

import org.junit.jupiter.api.Test;

import java.io.ByteArrayOutputStream;
import java.io.PrintStream;

import static org.junit.jupiter.api.Assertions.*;

/**
 * Unit tests for {@link HelloWorld} using JUnit 5.
 */
class HelloWorldTest {

    // --- Record tests ---------------------------------------------------------

    @Test
    void greetingMessage_formatsCorrectly() {
        var greeting = new HelloWorld.Greeting("Hello", "World");
        assertEquals("Hello, World!", greeting.message());
    }

    @Test
    void person_withoutTitle_returnsNameOnly() {
        var person = new HelloWorld.Person("Alice");
        assertEquals("Alice", person.displayName());
    }

    @Test
    void person_withTitle_returnsTitleAndName() {
        var person = new HelloWorld.Person("Duke", "Dr.");
        assertEquals("Dr. Duke", person.displayName());
    }

    @Test
    void person_withBlankTitle_treatedAsNoTitle() {
        var person = new HelloWorld.Person("Bob", "  ");
        assertEquals("Bob", person.displayName());
    }

    // --- OutputTarget tests ---------------------------------------------------

    @Test
    void silentTarget_doesNotThrow() {
        var silent = new HelloWorld.OutputTarget.Silent();
        assertDoesNotThrow(() -> HelloWorld.run(silent));
    }

    @Test
    void consoleTarget_writesExpectedOutput() {
        // Capture System.out to verify the Console target writes output
        PrintStream original = System.out;
        ByteArrayOutputStream buffer = new ByteArrayOutputStream();
        System.setOut(new PrintStream(buffer));
        try {
            HelloWorld.run(new HelloWorld.OutputTarget.Console());
        } finally {
            System.setOut(original);
        }

        String output = buffer.toString();
        assertTrue(output.contains("Hello, World!"),   "Output should contain the greeting");
        assertTrue(output.contains("Welcome, Modern Java!"), "Output should contain the second greeting");
    }
}
