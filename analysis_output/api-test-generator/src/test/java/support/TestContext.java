package support;

import io.restassured.response.Response;
import java.util.HashMap;
import java.util.Map;

/**
 * Shared test context that holds state across Cucumber step definitions.
 * Each scenario gets a fresh instance via dependency injection.
 */
public class TestContext {

    private Response lastResponse;
    private long lastResponseTimeMs;
    private final Map<String, Object> scenarioData = new HashMap<>();

    public Response getLastResponse() {
        return lastResponse;
    }

    public void setLastResponse(Response response) {
        this.lastResponse = response;
    }

    public long getLastResponseTimeMs() {
        return lastResponseTimeMs;
    }

    public void setLastResponseTimeMs(long ms) {
        this.lastResponseTimeMs = ms;
    }

    public void put(String key, Object value) {
        scenarioData.put(key, value);
    }

    public Object get(String key) {
        return scenarioData.get(key);
    }

    public String getString(String key) {
        return (String) scenarioData.get(key);
    }
}
