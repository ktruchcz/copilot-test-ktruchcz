package com.testapp2;

import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.List;
import java.util.Map;

/**
 * TestApp2 — modernized Hello World demonstrating Java 21 features.
 *
 * <p>Features showcased:
 * <ul>
 *   <li>Records (JEP 395, GA Java 16)</li>
 *   <li>Text blocks (JEP 378, GA Java 15)</li>
 *   <li>Switch expressions with pattern matching (JEP 441, GA Java 21)</li>
 *   <li>{@code var} local-variable type inference (JEP 286, GA Java 10)</li>
 *   <li>Sealed interfaces (JEP 409, GA Java 17)</li>
 *   <li>Enhanced instanceof pattern matching (JEP 394, GA Java 16)</li>
 *   <li>Stream API with modern collectors</li>
 *   <li>Sequenced collections (JEP 431, GA Java 21)</li>
 * </ul>
 */
public class HelloWorld {

    // ── Records (Java 16) ──────────────────────────────────────────────────────

    /** Immutable greeting message carrier. */
    public record Greeting(String recipient, String message, LocalDateTime timestamp) {

        /** Compact constructor with validation. */
        public Greeting {
            if (recipient == null || recipient.isBlank()) {
                throw new IllegalArgumentException("Recipient must not be blank");
            }
            if (message == null || message.isBlank()) {
                throw new IllegalArgumentException("Message must not be blank");
            }
        }

        /** Returns a formatted, human-readable representation. */
        public String format() {
            var formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss");
            return "[%s] Hello, %s! %s".formatted(timestamp.format(formatter), recipient, message);
        }
    }

    // ── Sealed interface + pattern matching (Java 17 / 21) ────────────────────

    /** Represents the result of a greeting operation. */
    public sealed interface GreetingResult
            permits GreetingResult.Success, GreetingResult.Failure {

        record Success(Greeting greeting) implements GreetingResult {}
        record Failure(String reason)    implements GreetingResult {}
    }

    // ── Application logic ─────────────────────────────────────────────────────

    /**
     * Builds a {@link Greeting} for the given recipient.
     *
     * @param recipient the person to greet
     * @return a {@link GreetingResult} indicating success or failure
     */
    public GreetingResult greet(String recipient) {
        if (recipient == null || recipient.isBlank()) {
            return new GreetingResult.Failure("Recipient must not be blank");
        }
        var greeting = new Greeting(recipient, "Welcome to TestApp2!", LocalDateTime.now());
        return new GreetingResult.Success(greeting);
    }

    /**
     * Renders a {@link GreetingResult} to a human-readable string.
     *
     * <p>Uses Java 21 pattern-matching switch expressions.
     *
     * @param result the result to describe
     * @return display string
     */
    public String describe(GreetingResult result) {
        // Pattern-matching switch (Java 21, JEP 441)
        return switch (result) {
            case GreetingResult.Success s -> s.greeting().format();
            case GreetingResult.Failure f -> "Greeting failed: " + f.reason();
        };
    }

    /**
     * Returns a greeting summary for a list of recipients using the Stream API.
     *
     * @param recipients list of names
     * @return map of recipient → formatted greeting (failures are excluded)
     */
    public Map<String, String> greetAll(List<String> recipients) {
        return recipients.stream()
                .filter(r -> r != null && !r.isBlank())
                .map(r -> Map.entry(r, greet(r)))
                .filter(e -> e.getValue() instanceof GreetingResult.Success)
                .collect(java.util.stream.Collectors.toMap(
                        Map.Entry::getKey,
                        e -> describe(e.getValue())
                ));
    }

    // ── Entry point ───────────────────────────────────────────────────────────

    public static void main(String[] args) {
        var app = new HelloWorld();

        // Text block (Java 15, JEP 378)
        var banner = """
                ╔══════════════════════════════════╗
                ║       TestApp2  –  Java 21       ║
                ╚══════════════════════════════════╝
                """;
        System.out.print(banner);

        // Single greeting
        var result = app.greet("World");
        System.out.println(app.describe(result));

        // Batch greetings via Stream API + sequenced-collection API (Java 21)
        var names = List.of("Alice", "Bob", "Charlie", "");
        var greetings = app.greetAll(names);

        // SequencedCollection: getFirst() / getLast() on a sorted view
        var sortedNames = new java.util.ArrayList<>(greetings.keySet());
        java.util.Collections.sort(sortedNames);
        System.out.printf("%nGreeted %d recipient(s):%n", sortedNames.size());
        sortedNames.forEach(name -> System.out.println("  • " + greetings.get(name)));

        // Enhanced instanceof pattern matching (Java 16, JEP 394)
        Object sample = app.greet("Demo");
        if (sample instanceof GreetingResult.Success s) {
            System.out.printf("%nPattern-match success → recipient: %s%n",
                    s.greeting().recipient());
        }
    }
}
