import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvSource;

import java.time.Month;
import java.util.List;

import static org.junit.jupiter.api.Assertions.*;

class HelloWorldTest {

    // -----------------------------------------------------------------------
    // Greeting record
    // -----------------------------------------------------------------------

    @Test
    void greetingRecordStoresFields() {
        var g = new HelloWorld.Greeting("World", "Hello");
        assertEquals("World", g.recipient());
        assertEquals("Hello", g.message());
    }

    @Test
    void greetingFormattedContainsRecipientAndMessage() {
        var g = new HelloWorld.Greeting("Alice", "Hi");
        var result = g.formatted();
        assertTrue(result.contains("Alice"), "formatted output should contain recipient");
        assertTrue(result.contains("Hi"),    "formatted output should contain message");
    }

    @Test
    void greetingRejectsBlankRecipient() {
        assertThrows(IllegalArgumentException.class,
                () -> new HelloWorld.Greeting("", "Hello"));
    }

    @Test
    void greetingRejectsBlankMessage() {
        assertThrows(IllegalArgumentException.class,
                () -> new HelloWorld.Greeting("World", "  "));
    }

    // -----------------------------------------------------------------------
    // TimeOfDay sealed hierarchy
    // -----------------------------------------------------------------------

    @Test
    void timeOfDayMorningForHourLessThan12() {
        assertInstanceOf(HelloWorld.TimeOfDay.Morning.class, HelloWorld.TimeOfDay.of(0));
        assertInstanceOf(HelloWorld.TimeOfDay.Morning.class, HelloWorld.TimeOfDay.of(11));
    }

    @Test
    void timeOfDayAfternoonForHour12To16() {
        assertInstanceOf(HelloWorld.TimeOfDay.Afternoon.class, HelloWorld.TimeOfDay.of(12));
        assertInstanceOf(HelloWorld.TimeOfDay.Afternoon.class, HelloWorld.TimeOfDay.of(16));
    }

    @Test
    void timeOfDayEveningForHour17AndAbove() {
        assertInstanceOf(HelloWorld.TimeOfDay.Evening.class, HelloWorld.TimeOfDay.of(17));
        assertInstanceOf(HelloWorld.TimeOfDay.Evening.class, HelloWorld.TimeOfDay.of(23));
    }

    // -----------------------------------------------------------------------
    // seasonOf
    // -----------------------------------------------------------------------

    @ParameterizedTest
    @CsvSource({
        "DECEMBER, Winter",
        "JANUARY,  Winter",
        "FEBRUARY, Winter",
        "MARCH,    Spring",
        "APRIL,    Spring",
        "MAY,      Spring",
        "JUNE,     Summer",
        "JULY,     Summer",
        "AUGUST,   Summer",
        "SEPTEMBER, Autumn",
        "OCTOBER,  Autumn",
        "NOVEMBER, Autumn"
    })
    void seasonOfReturnsCorrectSeason(Month month, String expected) {
        assertEquals(expected, HelloWorld.seasonOf(month));
    }

    // -----------------------------------------------------------------------
    // monthsBySeason – Stream Gatherers (Java 24+, finalised Java 25)
    // -----------------------------------------------------------------------

    @Test
    void monthsBySeasonReturnsFourWindows() {
        var windows = HelloWorld.monthsBySeason();
        assertEquals(4, windows.size(), "should produce exactly 4 windows of 3 months each");
    }

    @Test
    void monthsBySeasonEachWindowHasThreeMonths() {
        for (var window : HelloWorld.monthsBySeason()) {
            assertEquals(3, window.size(), "each window must contain exactly 3 months");
        }
    }

    @Test
    void monthsBySeasonFirstWindowIsJanFebMar() {
        var first = HelloWorld.monthsBySeason().getFirst();
        assertEquals(List.of(Month.JANUARY, Month.FEBRUARY, Month.MARCH), first);
    }

    @Test
    void monthsBySeasonLastWindowIsOctNovDec() {
        var windows = HelloWorld.monthsBySeason();
        var last = windows.getLast();
        assertEquals(List.of(Month.OCTOBER, Month.NOVEMBER, Month.DECEMBER), last);
    }

    @Test
    void monthsBySeasonCoversAllTwelveMonths() {
        var allMonths = HelloWorld.monthsBySeason().stream()
                .flatMap(List::stream)
                .toList();
        assertEquals(12, allMonths.size(), "all 12 months must appear across the windows");
    }
}
