package com.example;

/**
 * Provides greeting functionality.
 */
public class Greeter {

    /**
     * Returns a greeting message for the given name.
     *
     * @param name the name to greet
     * @return a greeting string
     */
    public String greet(String name) {
        if (name == null || name.isBlank()) {
            return "Hello, World!";
        }
        return "Hello, " + name + "!";
    }
}
