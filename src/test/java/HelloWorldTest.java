import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvSource;

import java.io.ByteArrayOutputStream;
import java.io.PrintStream;
import java.time.Month;
import java.nio.charset.StandardCharsets;

import static org.junit.jupiter.api.Assertions.*;

class HelloWorldTest {

    @Test
    void mainPrintsExpectedSections() {
        var originalOut = System.out;
        var output = new ByteArrayOutputStream();

        try {
            System.setOut(new PrintStream(output, true, StandardCharsets.UTF_8));
            HelloWorld.main(new String[0]);
        } finally {
            System.setOut(originalOut);
        }

        var printed = output.toString(StandardCharsets.UTF_8);
        assertTrue(printed.contains("World"));
        assertTrue(printed.contains("Java version"));
        assertTrue(printed.contains("Today's date"));
    }

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
}
