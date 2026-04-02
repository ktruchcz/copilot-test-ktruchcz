package com.testapp.runner;

import org.junit.platform.suite.api.ConfigurationParameter;
import org.junit.platform.suite.api.IncludeEngines;
import org.junit.platform.suite.api.SelectClasspathResource;
import org.junit.platform.suite.api.Suite;

import static io.cucumber.junit.platform.engine.Constants.*;

/**
 * JUnit 5 Platform Suite runner for the Cucumber test suite.
 *
 * <p>Tag filtering can be applied at build time via the system property
 * {@code cucumber.filter.tags}, e.g.:
 * <pre>{@code
 *   mvn test -Dcucumber.filter.tags="@smoke"
 *   mvn test -Dcucumber.filter.tags="@regression and not @wip"
 * }</pre>
 */
@Suite
@IncludeEngines("cucumber")
@SelectClasspathResource("features")
@ConfigurationParameter(key = PLUGIN_PROPERTY_NAME,
        value = "pretty,html:target/cucumber-reports/index.html," +
                "json:target/cucumber-reports/cucumber.json," +
                "junit:target/cucumber-reports/cucumber.xml")
@ConfigurationParameter(key = GLUE_PROPERTY_NAME,
        value = "com.testapp.steps,com.testapp.support")
@ConfigurationParameter(key = JUNIT_PLATFORM_NAMING_STRATEGY_PROPERTY_NAME,
        value = "long")
@ConfigurationParameter(key = PUBLISH_QUIET_PROPERTY_NAME,
        value = "true")
public class CucumberTestRunner {
    // Intentionally empty — the JUnit Platform Suite engine drives execution.
}
