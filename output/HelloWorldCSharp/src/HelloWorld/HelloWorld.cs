using System;

/// <summary>
/// Hello World application migrated from Java 21 to C# (.NET 9).
///
/// Demonstrates equivalent C# features:
/// <list type="bullet">
///   <item>Records (C# 9+)</item>
///   <item>Raw interpolated string literals (C# 11+)</item>
///   <item>Local-variable type inference via <c>var</c></item>
///   <item>Switch expressions (C# 8+) with <c>or</c> pattern combinator</item>
///   <item>Abstract records modelling sealed type hierarchies</item>
/// </list>
/// </summary>
public class HelloWorld
{
    // -----------------------------------------------------------------------
    // Month enum  (mirrors java.time.Month imported in the original source)
    // -----------------------------------------------------------------------

    /// <summary>Calendar months – integer values match java.time.Month ordinals (1-based).</summary>
    public enum Month
    {
        January = 1, February, March, April, May, June,
        July, August, September, October, November, December
    }

    // -----------------------------------------------------------------------
    // Greeting record  (Java 16 record → C# 9 record)
    // -----------------------------------------------------------------------

    /// <summary>
    /// Immutable value object holding a greeting message.
    /// Mirrors the Java record with a compact-constructor-style validation.
    /// </summary>
    public sealed record Greeting
    {
        /// <summary>The person (or entity) being greeted.</summary>
        public string Recipient { get; init; }

        /// <summary>The greeting text (e.g. "Hello", "Good morning").</summary>
        public string Message { get; init; }

        /// <summary>
        /// Constructs a <see cref="Greeting"/>, validating that neither argument is blank.
        /// Mirrors the Java compact canonical constructor.
        /// </summary>
        /// <exception cref="ArgumentException">
        /// Thrown when <paramref name="recipient"/> or <paramref name="message"/> is null/blank.
        /// </exception>
        public Greeting(string recipient, string message)
        {
            if (string.IsNullOrWhiteSpace(recipient))
                throw new ArgumentException("recipient must not be blank", nameof(recipient));
            if (string.IsNullOrWhiteSpace(message))
                throw new ArgumentException("message must not be blank", nameof(message));

            Recipient = recipient;
            Message   = message;
        }

        /// <summary>
        /// Returns a fully-formatted greeting string using a C# 11 raw interpolated string literal.
        /// Mirrors the Java text-block + <c>String.formatted()</c> pattern.
        /// </summary>
        public string Formatted() =>
            $"""
            ╔══════════════════════════════╗
            ║  {Message}, {Recipient}!  ║
            ╚══════════════════════════════╝
            """;
    }

    // -----------------------------------------------------------------------
    // TimeOfDay sealed hierarchy  (Java sealed interface → C# abstract record)
    // -----------------------------------------------------------------------

    /// <summary>
    /// Simple sealed hierarchy used to demonstrate C# pattern matching in a switch.
    /// The <c>private protected</c> constructor prevents external subclassing,
    /// mirroring Java's <c>sealed interface … permits …</c> declaration.
    /// </summary>
    public abstract record TimeOfDay
    {
        // Prevent external subclassing – equivalent to Java's sealed permits list.
        private protected TimeOfDay() { }

        /// <summary>Represents the morning period (before 12:00).</summary>
        public sealed record Morning   : TimeOfDay;

        /// <summary>Represents the afternoon period (12:00–16:59).</summary>
        public sealed record Afternoon : TimeOfDay;

        /// <summary>Represents the evening period (17:00 and later).</summary>
        public sealed record Evening   : TimeOfDay;

        /// <summary>
        /// Factory – maps an hour (0–23) to the appropriate <see cref="TimeOfDay"/>.
        /// Uses a C# relational pattern switch instead of Java guarded-pattern matching.
        /// </summary>
        public static TimeOfDay Of(int hour) => hour switch
        {
            < 12 => new Morning(),
            < 17 => new Afternoon(),
            _    => new Evening()
        };
    }

    // -----------------------------------------------------------------------
    // Entry point
    // -----------------------------------------------------------------------

    public static void Main(string[] args)
    {
        // var – local-variable type inference (identical in both languages)
        // LocalDate.now() → DateOnly.FromDateTime(DateTime.Now)
        var today = DateOnly.FromDateTime(DateTime.Now);

        // Switch expression with type-pattern matching
        // today.getDayOfMonth() → today.Day
        var timeOfDay  = TimeOfDay.Of(today.Day % 24);
        var salutation = timeOfDay switch
        {
            TimeOfDay.Morning   => "Good morning",
            TimeOfDay.Afternoon => "Good afternoon",
            TimeOfDay.Evening   => "Good evening",
            _                   => throw new InvalidOperationException("Unknown time of day")
        };

        var greeting = new Greeting("World", salutation);

        // Raw interpolated string literal output  (System.out.print → Console.Write)
        Console.Write(greeting.Formatted());

        // Multi-line raw interpolated string with runtime values
        // System.getProperty("java.version") → Environment.Version.ToString()
        // today.getMonth()                   → (Month)today.Month
        var info = $"""
                .NET version : {Environment.Version}
                Today's date : {today} ({SeasonOf((Month)today.Month)})
                """;

        Console.Write(info);
    }

    // -----------------------------------------------------------------------
    // SeasonOf  (package-private static → public static)
    // -----------------------------------------------------------------------

    /// <summary>
    /// Returns the meteorological season for the given <see cref="Month"/>.
    /// Java multi-case switch arms (<c>case A, B, C -></c>) become C# <c>A or B or C =></c>.
    /// </summary>
    public static string SeasonOf(Month month) => month switch
    {
        Month.December or Month.January  or Month.February  => "Winter",
        Month.March    or Month.April    or Month.May       => "Spring",
        Month.June     or Month.July     or Month.August    => "Summer",
        Month.September or Month.October or Month.November  => "Autumn",
        _ => throw new InvalidOperationException($"Unknown month: {month}")
    };
}
