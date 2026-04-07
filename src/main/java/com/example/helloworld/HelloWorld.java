package com.example.helloworld;

import java.util.List;

/**
 * Entry point for the Hello World application.
 *
 * <p>Demonstrates several modern Java features:
 * <ul>
 *   <li><strong>Records</strong> ({@link Greeting}) – compact immutable data carriers (Java 16+)</li>
 *   <li><strong>Text blocks</strong> – multi-line string literals (Java 15+)</li>
 *   <li><strong>Enhanced switch expressions</strong> – concise pattern-based dispatch (Java 14+)</li>
 *   <li><strong>Local variable type inference</strong> ({@code var}) – (Java 10+)</li>
 *   <li><strong>Stream API &amp; collection factories</strong> – (Java 9+)</li>
 * </ul>
 */
public class HelloWorld {

    public static void main(String[] args) {
        // --- Text block: banner ---
        var banner = """
                ╔══════════════════════════════╗
                ║   Hello World  –  Java 21    ║
                ╚══════════════════════════════╝
                """;
        System.out.print(banner);

        // --- Records: create typed greeting objects ---
        var recipients = List.of("World", "Java 21", "Records", "Text Blocks");

        recipients.stream()
                  .map(Greeting::hello)
                  .map(Greeting::format)
                  .forEach(System.out::print);

        // --- Enhanced switch expression ---
        int argCount = args.length;
        String summary = switch (argCount) {
            case 0  -> "No arguments provided – running with defaults.";
            case 1  -> "One argument provided: " + args[0];
            default -> "Multiple arguments provided (" + argCount + " total).";
        };
        System.out.println(summary);
    }
}
