package com.testapp.support;

import java.time.Instant;
import java.util.HashMap;
import java.util.Map;
import java.util.UUID;

/**
 * Fluent builder for constructing item request payloads used in tests.
 *
 * <p>Example usage:
 * <pre>{@code
 * Map<String, Object> payload = TestDataBuilder.anItem()
 *         .withName("Java 17 LTS")
 *         .withVersion("17.0.9")
 *         .withVendor("Eclipse Temurin")
 *         .withStatus("ACTIVE")
 *         .build();
 * }</pre>
 */
public class TestDataBuilder {

    private final Map<String, Object> fields = new HashMap<>();

    private TestDataBuilder() {}

    public static TestDataBuilder anItem() {
        return new TestDataBuilder();
    }

    /** Creates a builder pre-populated with valid defaults for quick smoke tests. */
    public static TestDataBuilder aValidItem() {
        return anItem()
                .withName("Java 17 LTS " + UUID.randomUUID().toString().substring(0, 8))
                .withDescription("Auto-generated test item")
                .withVersion("17.0.9")
                .withVendor("Eclipse Temurin")
                .withStatus("ACTIVE");
    }

    /** Creates a builder for an item that intentionally lacks required fields. */
    public static TestDataBuilder anInvalidItem() {
        return anItem()
                .withDescription("Item missing required name and version");
    }

    // ── Field setters ─────────────────────────────────────────────────────────

    public TestDataBuilder withName(String name) {
        fields.put("name", name);
        return this;
    }

    public TestDataBuilder withDescription(String description) {
        fields.put("description", description);
        return this;
    }

    public TestDataBuilder withVersion(String version) {
        fields.put("version", version);
        return this;
    }

    public TestDataBuilder withVendor(String vendor) {
        fields.put("vendor", vendor);
        return this;
    }

    public TestDataBuilder withStatus(String status) {
        fields.put("status", status);
        return this;
    }

    public TestDataBuilder withReleaseDate(Instant releaseDate) {
        fields.put("releaseDate", releaseDate.toString());
        return this;
    }

    public TestDataBuilder withMetadata(String key, Object value) {
        @SuppressWarnings("unchecked")
        Map<String, Object> metadata = (Map<String, Object>) fields.computeIfAbsent("metadata", k -> new HashMap<>());
        metadata.put(key, value);
        return this;
    }

    public TestDataBuilder withField(String key, Object value) {
        fields.put(key, value);
        return this;
    }

    public TestDataBuilder withoutField(String key) {
        fields.remove(key);
        return this;
    }

    // ── Build ─────────────────────────────────────────────────────────────────

    /** Returns an immutable copy of the accumulated fields. */
    public Map<String, Object> build() {
        return Map.copyOf(fields);
    }

    /**
     * Returns a mutable copy — useful when tests need to alter the map after building.
     */
    public Map<String, Object> buildMutable() {
        return new HashMap<>(fields);
    }

    // ── Pre-built payloads ────────────────────────────────────────────────────

    public static Map<String, Object> java17Item() {
        return anItem()
                .withName("Java 17 LTS")
                .withDescription("Long-term support release")
                .withVersion("17.0.9")
                .withVendor("Eclipse Temurin")
                .withStatus("ACTIVE")
                .build();
    }

    public static Map<String, Object> java21Item() {
        return anItem()
                .withName("Java 21 LTS")
                .withDescription("Latest LTS release")
                .withVersion("21.0.1")
                .withVendor("Eclipse Temurin")
                .withStatus("ACTIVE")
                .build();
    }

    public static Map<String, Object> java8DeprecatedItem() {
        return anItem()
                .withName("Java 8 EOL")
                .withDescription("End of life release")
                .withVersion("8.0.392")
                .withVendor("Eclipse Temurin")
                .withStatus("DEPRECATED")
                .build();
    }

    public static Map<String, Object> fromDataTable(Map<String, String> tableRow) {
        TestDataBuilder builder = anItem();
        tableRow.forEach((key, value) -> {
            if (!value.isBlank()) {
                builder.withField(key, value);
            }
        });
        return builder.build();
    }
}
