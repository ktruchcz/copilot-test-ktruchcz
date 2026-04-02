package com.testapp.support;

import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.ComponentScan;
import org.springframework.context.annotation.Configuration;

/**
 * Minimal Spring Boot application configuration for the test harness.
 *
 * <p>This class acts as the application entry-point for
 * {@link CucumberSpringConfiguration}. It component-scans the
 * {@code com.testapp} package so that support beans ({@link TestContext},
 * {@link ApiClient}) are discovered and wired automatically.
 */
@SpringBootApplication
@ComponentScan(basePackages = "com.testapp")
public class TestAppTestConfiguration {

    @Bean
    public com.fasterxml.jackson.databind.ObjectMapper objectMapper() {
        return TestContext.getObjectMapper();
    }
}
