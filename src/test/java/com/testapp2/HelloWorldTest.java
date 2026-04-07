package com.testapp2;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Nested;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.NullAndEmptySource;
import org.junit.jupiter.params.provider.ValueSource;

import java.time.LocalDateTime;
import java.util.List;
import java.util.Map;

import static org.assertj.core.api.Assertions.*;

@DisplayName("HelloWorld")
class HelloWorldTest {

    private final HelloWorld app = new HelloWorld();

    // ── Greeting record ────────────────────────────────────────────────────────

    @Nested
    @DisplayName("Greeting record")
    class GreetingRecordTests {

        @Test
        @DisplayName("creates a valid Greeting with correct field values")
        void shouldCreateGreetingWithCorrectFields() {
            var now = LocalDateTime.now();
            var greeting = new HelloWorld.Greeting("Alice", "Hello!", now);

            assertThat(greeting.recipient()).isEqualTo("Alice");
            assertThat(greeting.message()).isEqualTo("Hello!");
            assertThat(greeting.timestamp()).isEqualTo(now);
        }

        @Test
        @DisplayName("format() includes recipient and message")
        void formatShouldContainRecipientAndMessage() {
            var greeting = new HelloWorld.Greeting("Bob", "Hi there!", LocalDateTime.now());
            var formatted = greeting.format();

            assertThat(formatted).contains("Bob").contains("Hi there!");
        }

        @ParameterizedTest(name = "recipient=''{0}''")
        @NullAndEmptySource
        @ValueSource(strings = {" ", "\t", "\n"})
        @DisplayName("compact constructor rejects blank/null recipient")
        void shouldRejectBlankRecipient(String badRecipient) {
            assertThatIllegalArgumentException()
                    .isThrownBy(() -> new HelloWorld.Greeting(badRecipient, "msg", LocalDateTime.now()))
                    .withMessageContaining("Recipient");
        }

        @ParameterizedTest(name = "message=''{0}''")
        @NullAndEmptySource
        @ValueSource(strings = {" ", "\t"})
        @DisplayName("compact constructor rejects blank/null message")
        void shouldRejectBlankMessage(String badMessage) {
            assertThatIllegalArgumentException()
                    .isThrownBy(() -> new HelloWorld.Greeting("Alice", badMessage, LocalDateTime.now()))
                    .withMessageContaining("Message");
        }

        @Test
        @DisplayName("two Greetings with same values are equal (record equality)")
        void recordEqualityShouldWork() {
            var ts = LocalDateTime.of(2024, 1, 1, 0, 0);
            var g1 = new HelloWorld.Greeting("X", "Y", ts);
            var g2 = new HelloWorld.Greeting("X", "Y", ts);

            assertThat(g1).isEqualTo(g2).hasSameHashCodeAs(g2);
        }
    }

    // ── greet() ────────────────────────────────────────────────────────────────

    @Nested
    @DisplayName("greet()")
    class GreetTests {

        @Test
        @DisplayName("returns Success for a valid recipient")
        void shouldReturnSuccessForValidRecipient() {
            var result = app.greet("World");

            assertThat(result).isInstanceOf(HelloWorld.GreetingResult.Success.class);
            var success = (HelloWorld.GreetingResult.Success) result;
            assertThat(success.greeting().recipient()).isEqualTo("World");
        }

        @ParameterizedTest(name = "recipient=''{0}''")
        @NullAndEmptySource
        @ValueSource(strings = {" ", "  "})
        @DisplayName("returns Failure for blank/null recipient")
        void shouldReturnFailureForBlankRecipient(String badRecipient) {
            var result = app.greet(badRecipient);

            assertThat(result).isInstanceOf(HelloWorld.GreetingResult.Failure.class);
            var failure = (HelloWorld.GreetingResult.Failure) result;
            assertThat(failure.reason()).isNotBlank();
        }
    }

    // ── describe() ────────────────────────────────────────────────────────────

    @Nested
    @DisplayName("describe()")
    class DescribeTests {

        @Test
        @DisplayName("describes a Success result")
        void shouldDescribeSuccess() {
            var result = app.greet("Charlie");
            var description = app.describe(result);

            assertThat(description).contains("Charlie").contains("TestApp2");
        }

        @Test
        @DisplayName("describes a Failure result with reason")
        void shouldDescribeFailure() {
            var failure = new HelloWorld.GreetingResult.Failure("test error");
            var description = app.describe(failure);

            assertThat(description)
                    .containsIgnoringCase("failed")
                    .contains("test error");
        }
    }

    // ── greetAll() ────────────────────────────────────────────────────────────

    @Nested
    @DisplayName("greetAll()")
    class GreetAllTests {

        @Test
        @DisplayName("returns greetings for all valid recipients")
        void shouldGreetAllValidRecipients() {
            var names = List.of("Alice", "Bob", "Charlie");
            Map<String, String> result = app.greetAll(names);

            assertThat(result).containsOnlyKeys("Alice", "Bob", "Charlie");
            assertThat(result.values()).allSatisfy(v -> assertThat(v).isNotBlank());
        }

        @Test
        @DisplayName("silently skips blank/null entries")
        void shouldSkipBlankEntries() {
            var names = List.of("Alice", "", " ", "Bob");
            Map<String, String> result = app.greetAll(names);

            assertThat(result).containsOnlyKeys("Alice", "Bob");
        }

        @Test
        @DisplayName("returns empty map for all-blank input")
        void shouldReturnEmptyMapForAllBlankInput() {
            var names = List.of("", " ", "  ");
            Map<String, String> result = app.greetAll(names);

            assertThat(result).isEmpty();
        }

        @Test
        @DisplayName("returns empty map for empty list")
        void shouldReturnEmptyMapForEmptyList() {
            Map<String, String> result = app.greetAll(List.of());

            assertThat(result).isEmpty();
        }
    }
}
