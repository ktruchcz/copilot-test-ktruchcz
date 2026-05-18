import java.time.LocalDate;
import java.time.Month;

/**
 * Hello World application modernized for Java 17.
 *
 * <p>Demonstrates modern Java features:
 * <ul>
 *   <li>Records (Java 16+)</li>
 *   <li>Text blocks (Java 15+)</li>
 *   <li>Local-variable type inference via {@code var} (Java 10+)</li>
 *   <li>Switch expressions (Java 14+)</li>
 *   <li>Sealed interfaces (Java 17)</li>
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

    /** Simple sealed hierarchy used in time-of-day handling. */
    sealed interface TimeOfDay permits TimeOfDay.Morning, TimeOfDay.Afternoon, TimeOfDay.Evening {
        record Morning() implements TimeOfDay {}
        record Afternoon() implements TimeOfDay {}
        record Evening() implements TimeOfDay {}

        /** Factory – maps an hour (0-23) to the appropriate {@link TimeOfDay}. */
        static TimeOfDay of(int hour) {
            if (hour < 12) {
                return new Morning();
            }
            if (hour < 17) {
                return new Afternoon();
            }
            return new Evening();
        }
    }

    public static void main(String[] args) {
        // var – local-variable type inference (Java 10+)
        var today = LocalDate.now();

        // Java 17-compatible salutation mapping
        var timeOfDay = TimeOfDay.of(today.getDayOfMonth() % 24);
        var salutation = timeOfDay instanceof TimeOfDay.Morning
                ? "Good morning"
                : timeOfDay instanceof TimeOfDay.Afternoon
                ? "Good afternoon"
                : "Good evening";

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
}
