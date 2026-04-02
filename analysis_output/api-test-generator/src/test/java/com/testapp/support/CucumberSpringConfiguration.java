package com.testapp.support;

import io.cucumber.spring.CucumberContextConfiguration;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.ActiveProfiles;

/**
 * Bootstraps the Spring application context for Cucumber tests.
 *
 * <p>{@code @CucumberContextConfiguration} bridges Cucumber's step-definition
 * glue code with Spring's dependency-injection container, so that
 * {@code @Autowired} fields in step definitions are resolved correctly.
 *
 * <p>The {@code webEnvironment = NONE} setting avoids starting an embedded
 * servlet container — the tests call an external API via RestAssured.
 * Switch to {@code RANDOM_PORT} and add {@code @LocalServerPort} if you want
 * to spin up the application under test in-process.
 */
@CucumberContextConfiguration
@SpringBootTest(
        classes = TestAppTestConfiguration.class,
        webEnvironment = SpringBootTest.WebEnvironment.NONE
)
@ActiveProfiles("test")
public class CucumberSpringConfiguration {
    // Intentionally empty — Spring wiring is handled by the annotations above.
}
