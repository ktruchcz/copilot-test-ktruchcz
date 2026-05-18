import java.time.LocalDate;
import java.time.Month;
import java.util.Arrays;
import java.util.List;
import java.util.stream.Gatherers;

/**
 * Hello World application modernized for Java 25.
 *
 * <p>Demonstrates modern Java features:
 * <ul>
 *   <li>Records (Java 16+)</li>
 *   <li>Text blocks (Java 15+)</li>
 *   <li>Local-variable type inference via {@code var} (Java 10+)</li>
 *   <li>Switch expressions (Java 14+)</li>
 *   <li>Sealed interfaces &amp; pattern matching (Java 21)</li>
 *   <li>Stream Gatherers – {@link Gatherers#windowFixed} (Java 24+, finalised Java 25)</li>
 * </ul>
 */
public class HelloWorld {

    /** Immutable value object holding a greeting message – uses a Java 16 record. */
    record Greeting(String recipient, String message) {

        /** Compact canonical constructor – validates inputs. */
        Greeting {
            if (recipient == null || recipient.isBlank()) {
                throw new IllegalArgumentException("recipient must not be blank");
            }
            if (message == null || message.isBlank()) {
                throw new IllegalArgumentException("message must not be blank");
            }
        }

        /** Returns a fully-formatted greeting string using a Java 15 text block. */
        String formatted() {
            return """
                    ╔══════════════════════════════╗
                    ║  %s, %s!  ║
                    ╚══════════════════════════════╝
                    """.formatted(message, recipient);
        }
    }

    /** Simple sealed hierarchy used to show Java 21 pattern matching in a switch. */
    sealed interface TimeOfDay permits TimeOfDay.Morning, TimeOfDay.Afternoon, TimeOfDay.Evening {
        record Morning() implements TimeOfDay {}
        record Afternoon() implements TimeOfDay {}
        record Evening() implements TimeOfDay {}

        /** Factory – maps an hour (0-23) to the appropriate {@link TimeOfDay}. */
        static TimeOfDay of(int hour) {
            // Box to Integer so the switch can use guarded pattern matching (Java 21)
            return switch ((Integer) hour) {
                case Integer h when h < 12 -> new Morning();
                case Integer h when h < 17 -> new Afternoon();
                default                    -> new Evening();
            };
        }
    }

    public static void main(String[] args) {
        // var – local-variable type inference (Java 10+)
        var today = LocalDate.now();

        // Switch expression with pattern matching (Java 21)
        var timeOfDay = TimeOfDay.of(today.getDayOfMonth() % 24);
        var salutation = switch (timeOfDay) {
            case TimeOfDay.Morning   ignored -> "Good morning";
            case TimeOfDay.Afternoon ignored -> "Good afternoon";
            case TimeOfDay.Evening   ignored -> "Good evening";
        };

        var greeting = new Greeting("World", salutation);

        // Text block output
        System.out.print(greeting.formatted());

        // Multi-line text block with runtime values interpolated via formatted()
        var info = """
                Java version : %s
                Today's date : %s (%s)
                """.formatted(
                System.getProperty("java.version"),
                today,
                seasonOf(today.getMonth()));

        System.out.print(info);

        // Stream Gatherers (Java 24+, finalised Java 25) – group months into seasonal windows
        var windows = monthsBySeason();
        var seasonWindows = new StringBuilder("Seasonal month windows (Stream Gatherers):\n");
        for (var window : windows) {
            var season = seasonOf(window.get(1)); // middle month is representative
            seasonWindows.append("  ").append(season).append(": ").append(window).append("\n");
        }
        System.out.print(seasonWindows);
    }

    /** Returns the meteorological season for the given {@link Month}. */
    static String seasonOf(Month month) {
        return switch (month) {
            case DECEMBER, JANUARY, FEBRUARY -> "Winter";
            case MARCH, APRIL, MAY           -> "Spring";
            case JUNE, JULY, AUGUST          -> "Summer";
            case SEPTEMBER, OCTOBER, NOVEMBER -> "Autumn";
        };
    }

    /**
     * Groups all 12 calendar months into fixed windows of 3 (one per meteorological season)
     * using the Java 24+ {@link Gatherers#windowFixed} Stream Gatherer.
     *
     * <p>The resulting list contains four windows:
     * <ol>
     *   <li>JAN–MAR (Winter/Spring transition)</li>
     *   <li>APR–JUN (Spring/Summer transition)</li>
     *   <li>JUL–SEP (Summer/Autumn transition)</li>
     *   <li>OCT–DEC (Autumn/Winter transition)</li>
     * </ol>
     *
     * @return an unmodifiable list of four 3-month windows
     */
    static List<List<Month>> monthsBySeason() {
        return Arrays.stream(Month.values())
                .gather(Gatherers.windowFixed(3))
                .toList();
    }
}
