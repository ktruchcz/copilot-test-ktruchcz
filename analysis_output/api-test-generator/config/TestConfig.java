package com.example.testapp.config;

import com.example.testapp.support.ApiClient;

public class TestConfig {

    public static ApiClient createApiClient() {
        return new ApiClient(
                System.getProperty("api.base.uri", "http://localhost"),
                Integer.parseInt(System.getProperty("api.port", "8080"))
        );
    }
}
