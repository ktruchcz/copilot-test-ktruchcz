package com.finmonol.api.test.support;

import io.restassured.response.Response;
import lombok.Getter;
import lombok.Setter;

import java.util.HashMap;
import java.util.Map;

/**
 * Shared test context injected by PicoContainer into step definition classes.
 *
 * <p>Holds state that needs to be shared across step definition files within a
 * single Cucumber scenario, such as the last HTTP response, the last created
 * resource IDs, and any accumulated totals.
 */
@Getter
@Setter
public class TestContext {

    /** Last HTTP response received from the API. */
    private Response lastResponse;

    /** The account ID created or used in the most recent step. */
    private String lastAccountId;

    /** The transaction ID created or used in the most recent step. */
    private String lastTransactionId;

    /**
     * Arbitrary key-value store for storing ad-hoc values between steps
     * (e.g. captured field values for later assertion).
     */
    private final Map<String, Object> store = new HashMap<>();

    /**
     * Convenience method to stash an arbitrary value.
     *
     * @param key   identifier
     * @param value value to stash
     */
    public void put(String key, Object value) {
        store.put(key, value);
    }

    /**
     * Convenience method to retrieve a stashed value.
     *
     * @param key identifier
     * @return value, or {@code null} if not present
     */
    public Object get(String key) {
        return store.get(key);
    }

    /** Clears all transient state – called between scenarios if needed. */
    public void reset() {
        lastResponse = null;
        lastAccountId = null;
        lastTransactionId = null;
        store.clear();
    }
}
