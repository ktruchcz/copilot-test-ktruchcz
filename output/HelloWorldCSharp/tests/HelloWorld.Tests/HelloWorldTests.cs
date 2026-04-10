using Xunit;
using static HelloWorld;

/// <summary>
/// Unit tests for <see cref="HelloWorld"/> migrated from JUnit 5 to xUnit 2.x.
///
/// Migration map:
///   @Test                        → [Fact]
///   @ParameterizedTest @CsvSource → [Theory] [InlineData(…)]
///   assertEquals(exp, act)       → Assert.Equal(exp, act)
///   assertTrue(cond, msg)        → Assert.True(cond, msg)
///   assertThrows(T.class, () →)  → Assert.Throws&lt;T&gt;(() =&gt; …)
///   assertInstanceOf(T.class, o) → Assert.IsType&lt;T&gt;(o)
///   g.recipient() / g.message()  → g.Recipient / g.Message  (PascalCase)
/// </summary>
public class HelloWorldTests
{
    // -----------------------------------------------------------------------
    // Greeting record
    // -----------------------------------------------------------------------

    [Fact]
    public void GreetingRecordStoresFields()
    {
        var g = new Greeting("World", "Hello");
        Assert.Equal("World", g.Recipient);
        Assert.Equal("Hello", g.Message);
    }

    [Fact]
    public void GreetingFormattedContainsRecipientAndMessage()
    {
        var g      = new Greeting("Alice", "Hi");
        var result = g.Formatted();
        Assert.True(result.Contains("Alice"), "formatted output should contain recipient");
        Assert.True(result.Contains("Hi"),    "formatted output should contain message");
    }

    [Fact]
    public void GreetingRejectsBlankRecipient()
    {
        Assert.Throws<ArgumentException>(() => new Greeting("", "Hello"));
    }

    [Fact]
    public void GreetingRejectsBlankMessage()
    {
        Assert.Throws<ArgumentException>(() => new Greeting("World", "  "));
    }

    // -----------------------------------------------------------------------
    // TimeOfDay sealed hierarchy
    // -----------------------------------------------------------------------

    [Fact]
    public void TimeOfDayMorningForHourLessThan12()
    {
        Assert.IsType<TimeOfDay.Morning>(TimeOfDay.Of(0));
        Assert.IsType<TimeOfDay.Morning>(TimeOfDay.Of(11));
    }

    [Fact]
    public void TimeOfDayAfternoonForHour12To16()
    {
        Assert.IsType<TimeOfDay.Afternoon>(TimeOfDay.Of(12));
        Assert.IsType<TimeOfDay.Afternoon>(TimeOfDay.Of(16));
    }

    [Fact]
    public void TimeOfDayEveningForHour17AndAbove()
    {
        Assert.IsType<TimeOfDay.Evening>(TimeOfDay.Of(17));
        Assert.IsType<TimeOfDay.Evening>(TimeOfDay.Of(23));
    }

    // -----------------------------------------------------------------------
    // SeasonOf  (@ParameterizedTest @CsvSource → [Theory] [InlineData(…)])
    // -----------------------------------------------------------------------

    [Theory]
    [InlineData(Month.December,  "Winter")]
    [InlineData(Month.January,   "Winter")]
    [InlineData(Month.February,  "Winter")]
    [InlineData(Month.March,     "Spring")]
    [InlineData(Month.April,     "Spring")]
    [InlineData(Month.May,       "Spring")]
    [InlineData(Month.June,      "Summer")]
    [InlineData(Month.July,      "Summer")]
    [InlineData(Month.August,    "Summer")]
    [InlineData(Month.September, "Autumn")]
    [InlineData(Month.October,   "Autumn")]
    [InlineData(Month.November,  "Autumn")]
    public void SeasonOfReturnsCorrectSeason(Month month, string expected)
    {
        Assert.Equal(expected, HelloWorld.SeasonOf(month));
    }
}
