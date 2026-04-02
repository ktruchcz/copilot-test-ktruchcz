package com.example.testapp.support;

import io.restassured.response.Response;

public class SharedContext {

    private static final SharedContext INSTANCE = new SharedContext();
    private static final ApiClient API_CLIENT = new ApiClient();

    private Response lastResponse;
    private Long lastItemId;
    private String lastItemName;
    private String lastItemStatus;
    private Integer lastItemVersion;

    private SharedContext() {}

    public static SharedContext getInstance() {
        return INSTANCE;
    }

    public static ApiClient getApiClient() {
        return API_CLIENT;
    }

    public void reset() {
        lastResponse = null;
        lastItemId = null;
        lastItemName = null;
        lastItemStatus = null;
        lastItemVersion = null;
    }

    public String resolvePath(String path) {
        if (path.contains("{id}") && lastItemId != null) {
            return path.replace("{id}", lastItemId.toString());
        }
        return path;
    }

    public Response getLastResponse() { return lastResponse; }
    public void setLastResponse(Response r) { this.lastResponse = r; }
    public Long getLastItemId() { return lastItemId; }
    public void setLastItemId(Long id) { this.lastItemId = id; }
    public String getLastItemName() { return lastItemName; }
    public void setLastItemName(String n) { this.lastItemName = n; }
    public String getLastItemStatus() { return lastItemStatus; }
    public void setLastItemStatus(String s) { this.lastItemStatus = s; }
    public Integer getLastItemVersion() { return lastItemVersion; }
    public void setLastItemVersion(Integer v) { this.lastItemVersion = v; }
}
