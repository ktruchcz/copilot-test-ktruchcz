package com.testapp.support;

import java.util.HashMap;
import java.util.Map;
import java.util.concurrent.atomic.AtomicLong;

/**
 * Fluent builder for {@code User} request payloads used in test scenarios.
 *
 * <p>Provides sensible defaults so individual tests only need to override the
 * fields relevant to the scenario under test.
 */
public class TestDataBuilder {

    /** Auto-incrementing ID seed — keeps generated IDs unique within a test run. */
    private static final AtomicLong ID_SEED = new AtomicLong(2000L);

    // -------------------------------------------------------------------------
    // User builder
    // -------------------------------------------------------------------------

    /**
     * Returns a new {@link UserBuilder} pre-populated with valid default values.
     *
     * @return builder instance
     */
    public static UserBuilder aUser() {
        long id = ID_SEED.getAndIncrement();
        return new UserBuilder()
                .withId(id)
                .withUsername("user_" + id)
                .withEmail("user_" + id + "@example.com")
                .withFirstName("First")
                .withLastName("Last")
                .withAge(25)
                .withStatus("ACTIVE");
    }

    /**
     * Returns a {@link UserBuilder} that mirrors the Background user (id=1001, johndoe).
     *
     * @return builder pre-set to the Background fixture
     */
    public static UserBuilder theBackgroundUser() {
        return new UserBuilder()
                .withId(1001L)
                .withUsername("johndoe")
                .withEmail("johndoe@example.com")
                .withFirstName("John")
                .withLastName("Doe")
                .withAge(30)
                .withStatus("ACTIVE");
    }

    /**
     * Converts a Cucumber {@link io.cucumber.datatable.DataTable}-style list of
     * two-element rows into a mutable {@link Map} suitable for use as a request body.
     *
     * @param rows list of [field, value] pairs
     * @return mutable map of field → value
     */
    public static Map<String, Object> fromRows(java.util.List<java.util.List<String>> rows) {
        Map<String, Object> map = new HashMap<>();
        for (java.util.List<String> row : rows) {
            if (row.size() >= 2) {
                String key = row.get(0);
                String raw = row.get(1);
                map.put(key, coerce(key, raw));
            }
        }
        return map;
    }

    /**
     * Coerces a raw string value from a DataTable into the correct Java type
     * based on known field names.
     */
    private static Object coerce(String field, String raw) {
        return switch (field) {
            case "id"  -> parseLongOrNull(raw);
            case "age" -> parseIntOrNull(raw);
            default    -> raw;
        };
    }

    private static Long parseLongOrNull(String s) {
        if (s == null || s.isBlank()) return null;
        try { return Long.parseLong(s.trim()); } catch (NumberFormatException e) { return null; }
    }

    private static Integer parseIntOrNull(String s) {
        if (s == null || s.isBlank()) return null;
        try { return Integer.parseInt(s.trim()); } catch (NumberFormatException e) { return null; }
    }

    // -------------------------------------------------------------------------
    // Inner builder class
    // -------------------------------------------------------------------------

    public static final class UserBuilder {

        private Long   id;
        private String username;
        private String email;
        private String firstName;
        private String lastName;
        private Integer age;
        private String status;

        private UserBuilder() {}

        public UserBuilder withId(Long id)             { this.id = id;             return this; }
        public UserBuilder withUsername(String u)      { this.username = u;        return this; }
        public UserBuilder withEmail(String e)         { this.email = e;           return this; }
        public UserBuilder withFirstName(String fn)    { this.firstName = fn;      return this; }
        public UserBuilder withLastName(String ln)     { this.lastName = ln;       return this; }
        public UserBuilder withAge(int age)            { this.age = age;           return this; }
        public UserBuilder withStatus(String status)   { this.status = status;     return this; }

        /** Produce an invalid email to trigger validation errors. */
        public UserBuilder withInvalidEmail()          { this.email = "not-an-email"; return this; }

        /** Produce a blank username to trigger validation errors. */
        public UserBuilder withBlankUsername()         { this.username = ""; return this; }

        /** Produce a negative age to trigger validation errors. */
        public UserBuilder withNegativeAge()           { this.age = -1; return this; }

        /**
         * Build a full {@link Map} suitable as the body for a PUT (full update) request.
         * The {@code id} field is intentionally excluded from the body — it lives in the URL.
         *
         * @return request body map
         */
        public Map<String, Object> buildPutBody() {
            Map<String, Object> body = new HashMap<>();
            body.put("username",  username);
            body.put("email",     email);
            body.put("firstName", firstName);
            body.put("lastName",  lastName);
            body.put("age",       age);
            body.put("status",    status);
            return body;
        }

        /**
         * Build a partial {@link Map} containing only the fields that are non-null,
         * suitable as the body for a PATCH (partial update) request.
         *
         * @return partial request body map
         */
        public Map<String, Object> buildPatchBody() {
            Map<String, Object> body = new HashMap<>();
            if (username  != null) body.put("username",  username);
            if (email     != null) body.put("email",     email);
            if (firstName != null) body.put("firstName", firstName);
            if (lastName  != null) body.put("lastName",  lastName);
            if (age       != null) body.put("age",       age);
            if (status    != null) body.put("status",    status);
            return body;
        }

        /**
         * Build the complete user representation (including {@code id}),
         * suitable for setting up mock server stubs or asserting responses.
         *
         * @return full user map
         */
        public Map<String, Object> buildFullRepresentation() {
            Map<String, Object> body = buildPutBody();
            if (id != null) body.put("id", id);
            return body;
        }

        // Getters
        public Long    getId()        { return id; }
        public String  getUsername()  { return username; }
        public String  getEmail()     { return email; }
        public String  getFirstName() { return firstName; }
        public String  getLastName()  { return lastName; }
        public Integer getAge()       { return age; }
        public String  getStatus()    { return status; }
    }
}
