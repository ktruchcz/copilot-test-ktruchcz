package com.example.helloworld;

/**
 * Immutable record representing a greeting message.
 *
 * <p>Records are a modern Java 16+ feature that provide a compact,
 * transparent carrier for immutable data without boilerplate.
 *
 * @param recipient the name of the person (or thing) being greeted
 * @param message   the greeting text
 */
public record Greeting(String recipient, String message) {

    /** Compact canonical constructor — validates inputs. */
    public Greeting {
        if (recipient == null || recipient.isBlank()) {
            throw new IllegalArgumentException("recipient must not be blank");
        }
        if (message == null || message.isBlank()) {
            throw new IllegalArgumentException("message must not be blank");
        }
        recipient = recipient.strip();
        message   = message.strip();
    }

    /**
     * Factory method that creates a standard "Hello" greeting.
     *
     * @param recipient the name to greet
     * @return a new {@link Greeting}
     */
    public static Greeting hello(String recipient) {
        return new Greeting(recipient, "Hello, " + recipient + "!");
    }

    /**
     * Returns a formatted, multi-line representation using a <em>text block</em>
     * (Java 15+ standard feature).
     *
     * @return pretty-printed greeting
     */
    public String format() {
        return """
                ┌─────────────────────────────┐
                │  %s
                └─────────────────────────────┘
                """.formatted(message);
    }
}
