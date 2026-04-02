package com.testapp.support;

import io.restassured.response.Response;

import java.util.HashMap;
import java.util.Map;

/**
 * Holds scenario-scoped state that must be shared across multiple step
 * definition classes within a single Cucumber scenario.
 *
 * <p>Cucumber-PicoContainer injects a single instance of this class into every
 * step definition class that declares it as a constructor parameter, so all
 * steps in the same scenario operate on the same context object.
 */
public class TestContext {

    /** Shared API client instance — one per scenario. */
    private final ApiClient apiClient;

    /** The most recent HTTP response received during the scenario. */
    private Response lastResponse;

    /** Generic property bag for arbitrary scenario state. */
    private final Map<String, Object> scenarioData = new HashMap<>();

    public TestContext() {
        this.apiClient = new ApiClient();
    }

    // -------------------------------------------------------------------------
    // ApiClient access
    // -------------------------------------------------------------------------

    public ApiClient getApiClient() {
        return apiClient;
    }

    // -------------------------------------------------------------------------
    // Last response
    // -------------------------------------------------------------------------

    public Response getLastResponse() {
        return lastResponse;
    }

    public void setLastResponse(Response response) {
        this.lastResponse = response;
    }

    /**
     * Convenience: return the HTTP status code of the last response.
     *
     * @return status code, or -1 if no response has been set
     */
    public int getLastStatusCode() {
        return lastResponse != null ? lastResponse.getStatusCode() : -1;
    }

    /**
     * Convenience: return the response body as a plain string.
     *
     * @return response body string, or empty string if no response has been set
     */
    public String getLastResponseBody() {
        return lastResponse != null ? lastResponse.getBody().asString() : "";
    }

    // -------------------------------------------------------------------------
    // Generic scenario data bag
    // -------------------------------------------------------------------------

    /**
     * Store an arbitrary value under a named key for the duration of the scenario.
     *
     * @param key   key name
     * @param value value to store
     */
    public void set(String key, Object value) {
        scenarioData.put(key, value);
    }

    /**
     * Retrieve a previously stored value.
     *
     * @param key key name
     * @return stored value, or {@code null} if not present
     */
    public Object get(String key) {
        return scenarioData.get(key);
    }

    /**
     * Retrieve a previously stored value, cast to the specified type.
     *
     * @param key        key name
     * @param targetType target class
     * @param <T>        type parameter
     * @return stored value cast to T, or {@code null}
     */
    @SuppressWarnings("unchecked")
    public <T> T get(String key, Class<T> targetType) {
        return (T) scenarioData.get(key);
    }

    /**
     * Check whether a key exists in the scenario data bag.
     *
     * @param key key name
     * @return {@code true} if the key is present
     */
    public boolean has(String key) {
        return scenarioData.containsKey(key);
    }

    /**
     * Remove a key from the scenario data bag.
     *
     * @param key key name
     */
    public void remove(String key) {
        scenarioData.remove(key);
    }

    /** Clear all stored scenario data. */
    public void clearScenarioData() {
        scenarioData.clear();
    }

    // -------------------------------------------------------------------------
    // Auth convenience
    // -------------------------------------------------------------------------

    /**
     * Set a valid bearer token on the underlying {@link ApiClient}.
     *
     * @param token JWT or opaque bearer token
     */
    public void setAuthToken(String token) {
        apiClient.setAuthToken(token);
        set("authToken", token);
    }

    /** Remove the bearer token from the underlying {@link ApiClient}. */
    public void clearAuthToken() {
        apiClient.clearAuthToken();
        remove("authToken");
    }
}
