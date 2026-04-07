package com.example;

/**
 * A modernized Hello World application showcasing Java 21 features:
 * <ul>
 *   <li>Records (JEP 395) – immutable data carriers</li>
 *   <li>Sealed interfaces (JEP 409) – restricted type hierarchies</li>
 *   <li>Pattern matching for switch (JEP 441) – concise type dispatch</li>
 *   <li>Text blocks (JEP 378) – readable multi-line strings</li>
 * </ul>
 */
public class HelloWorld {

    // --- Records: concise, immutable data carriers ----------------------------

    /** Represents a greeting composed of a salutation and a subject. */
    record Greeting(String salutation, String subject) {
        /** Renders the greeting as a single sentence. */
        String message() {
            return "%s, %s!".formatted(salutation, subject);
        }
    }

    /** A person with a name and an optional title. */
    record Person(String name, String title) {
        /** Convenience constructor for a person without a title. */
        Person(String name) {
            this(name, null);
        }

        /** Returns the display name, incorporating the title when present. */
        String displayName() {
            return (title != null && !title.isBlank())
                    ? "%s %s".formatted(title, name)
                    : name;
        }
    }

    // --- Sealed interface + pattern-matching switch ---------------------------

    /** Models different kinds of output targets. */
    sealed interface OutputTarget permits OutputTarget.Console, OutputTarget.Silent {
        /** Writes {@code text} to the target. */
        void write(String text);

        /** Writes to standard output. */
        record Console() implements OutputTarget {
            @Override
            public void write(String text) {
                System.out.println(text);
            }
        }

        /** Discards output (useful for testing). */
        record Silent() implements OutputTarget {
            @Override
            public void write(String text) {
                // intentionally silent
            }
        }
    }

    // --- Text block: application banner ---------------------------------------

    private static final String BANNER = """
            ╔══════════════════════════════════╗
            ║   Hello World – Java 21 Edition  ║
            ╚══════════════════════════════════╝
            """;

    // --- Entry point ----------------------------------------------------------

    /**
     * Application entry point.
     *
     * @param args command-line arguments (unused)
     */
    public static void main(String[] args) {
        var target = new OutputTarget.Console();
        run(target);
    }

    /**
     * Core application logic, separated from {@code main} to enable testing
     * with a {@link OutputTarget.Silent} target.
     *
     * @param target the output target to write messages to
     */
    static void run(OutputTarget target) {
        target.write(BANNER);

        var world  = new Person("World");
        var greet  = new Greeting("Hello", world.displayName());
        target.write(greet.message());

        var titled = new Person("Java", "Modern");
        var greet2 = new Greeting("Welcome", titled.displayName());
        target.write(greet2.message());

        // Pattern-matching switch over the sealed OutputTarget hierarchy
        String description = switch (target) {
            case OutputTarget.Console c -> "Writing to the console";
            case OutputTarget.Silent  s -> "Running silently";
        };
        target.write("\n[Info] " + description);
    }
}
