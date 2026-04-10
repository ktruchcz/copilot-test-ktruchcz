# Migration Report

**Source:** Java 21 (Maven) → **Target:** C# (.NET 9)
**Date:** 2025
**Status:** ✅ Complete

---

## Files Created

| Output Path | Source | Notes |
|---|---|---|
| `output/analysis-report.md` | _(new)_ | Analysis report (required by workflow) |
| `output/HelloWorldCSharp/HelloWorld.sln` | `pom.xml` | Visual Studio solution; two projects wired up |
| `output/HelloWorldCSharp/src/HelloWorld/HelloWorld.csproj` | `pom.xml` | `net9.0`, `OutputType=Exe`, version `1.0.0` |
| `output/HelloWorldCSharp/src/HelloWorld/HelloWorld.cs` | `src/main/java/HelloWorld.java` | Full production migration (see decisions below) |
| `output/HelloWorldCSharp/tests/HelloWorld.Tests/HelloWorld.Tests.csproj` | `pom.xml` | `net9.0`, xUnit 2.x, references main project |
| `output/HelloWorldCSharp/tests/HelloWorld.Tests/HelloWorldTests.cs` | `src/test/java/HelloWorldTest.java` | Full test migration (see decisions below) |

---

## Migration Decisions

### 1. `record Greeting` — Validation via explicit constructor
Java uses a *compact canonical constructor* (body inside the record definition with no `()`)
which re-assigns and validates the components. C# positional records do not have an exact
equivalent when property-level validation is required, so the record was migrated to a
**non-positional record with an explicit constructor**:

```csharp
public sealed record Greeting
{
    public string Recipient { get; init; }
    public string Message   { get; init; }

    public Greeting(string recipient, string message)
    {
        if (string.IsNullOrWhiteSpace(recipient))
            throw new ArgumentException("recipient must not be blank", nameof(recipient));
        ...
    }
}
```

Property names are **PascalCase** (`Recipient`, `Message`) per C# convention;
all call-sites updated accordingly.

### 2. `sealed interface TimeOfDay` → `public abstract record TimeOfDay`
Java sealed interfaces cannot be directly represented in C#.  
The chosen idiom is an **abstract record** with a `private protected` no-arg constructor,
which prevents any external class from extending it (only nested types `Morning`,
`Afternoon`, `Evening` declared inside the same class can do so).

```csharp
public abstract record TimeOfDay
{
    private protected TimeOfDay() { }
    public sealed record Morning   : TimeOfDay;
    public sealed record Afternoon : TimeOfDay;
    public sealed record Evening   : TimeOfDay;
    ...
}
```

### 3. Pattern-matching switch in `TimeOfDay.Of`
Java used guarded integer patterns (`case Integer h when h < 12`).  
C# uses **relational patterns** directly, which is cleaner:

```csharp
public static TimeOfDay Of(int hour) => hour switch
{
    < 12 => new Morning(),
    < 17 => new Afternoon(),
    _    => new Evening()
};
```

### 4. Text blocks + `String.formatted()` → raw interpolated string literals
Java:
```java
"""...\n%s...""".formatted(arg)
```
C# 11:
```csharp
$"""...\n{arg}..."""
```
Applied to both `Greeting.Formatted()` and the `info` block in `Main`.

### 5. `LocalDate.now()` → `DateOnly.FromDateTime(DateTime.Now)`
`DateOnly` is the direct .NET equivalent of `java.time.LocalDate`.  
`.getDayOfMonth()` → `.Day`; `.getMonth()` → `(Month)today.Month`.

### 6. `Month` enum defined locally
Java imports `java.time.Month`.  
C# has no built-in calendar-month enum, so a matching `public enum Month` (1-based)
was declared inside the `HelloWorld` class:

```csharp
public enum Month { January = 1, February, ..., December }
```

### 7. Multi-case switch arms → `or` pattern combinator
Java `case DECEMBER, JANUARY, FEBRUARY -> "Winter"` becomes:

```csharp
Month.December or Month.January or Month.February => "Winter",
```

A catch-all `_ => throw new InvalidOperationException(...)` arm was added as required
by exhaustive C# switch expressions.

### 8. `System.getProperty("java.version")` → `Environment.Version`
`Environment.Version` returns the .NET runtime version as a `Version` object;
used directly in the interpolated string (`.ToString()` called implicitly).

### 9. `System.out.print` → `Console.Write`
No newline appended — exact semantic match.

### 10. `IllegalArgumentException` → `ArgumentException`
Standard .NET mapping.

---

## Test Migration Decisions

| JUnit 5 | xUnit 2 |
|---|---|
| `@Test` | `[Fact]` |
| `@ParameterizedTest` + `@CsvSource({…})` | `[Theory]` + one `[InlineData(…)]` per row |
| `assertEquals(exp, act)` | `Assert.Equal(exp, act)` |
| `assertTrue(cond, msg)` | `Assert.True(cond, msg)` |
| `assertThrows(T.class, λ)` | `Assert.Throws<T>(λ)` |
| `assertInstanceOf(T.class, obj)` | `Assert.IsType<T>(obj)` |
| `g.recipient()` / `g.message()` | `g.Recipient` / `g.Message` |

The `@CsvSource` rows used string month names (`"DECEMBER"`, etc.).  
In xUnit `[InlineData]`, the C# enum values (`Month.December`, etc.) are used directly —
they are compile-time constants and are fully supported as attribute arguments.

Test method names were converted from `camelCase` to `PascalCase` per C# conventions.

---

## What Was NOT Changed
- Application logic and output format are semantically identical to the Java original.
- The Unicode box-drawing characters in `Greeting.Formatted()` are preserved verbatim.
- No third-party production dependencies were added (Java source had none either).
