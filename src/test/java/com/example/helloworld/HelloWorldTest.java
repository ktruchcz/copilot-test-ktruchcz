package com.example.helloworld;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertDoesNotThrow;

/**
 * Smoke tests for the {@link HelloWorld} entry-point class.
 *
 * <p>The main method is exercised without assertion on stdout; its primary
 * purpose is to verify that the program runs to completion without exceptions.
 */
@DisplayName("HelloWorld main method")
class HelloWorldTest {

    @Test
    @DisplayName("main() runs without throwing when no arguments are passed")
    void main_noArgs_doesNotThrow() {
        assertDoesNotThrow(() -> HelloWorld.main(new String[]{}));
    }

    @Test
    @DisplayName("main() runs without throwing when arguments are passed")
    void main_withArgs_doesNotThrow() {
        assertDoesNotThrow(() -> HelloWorld.main(new String[]{"foo", "bar"}));
    }
}
