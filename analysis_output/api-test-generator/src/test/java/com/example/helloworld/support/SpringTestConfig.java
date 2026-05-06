package com.example.helloworld.support;

import com.example.helloworld.HelloWorldApplication;
import io.cucumber.spring.CucumberContextConfiguration;
import org.springframework.boot.test.context.SpringBootTest;

/**
 * Binds the Cucumber execution context to the Spring Boot test context.
 *
 * <p>Each scenario runs against a real Spring Boot server started on a random
 * port. The actual port is injected into {@link ApiClient} via the
 * {@code local.server.port} property.
 */
@CucumberContextConfiguration
@SpringBootTest(
        classes = HelloWorldApplication.class,
        webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT
)
public class SpringTestConfig {
}
