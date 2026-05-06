package com.example.helloworld.runner;

import org.junit.platform.suite.api.ConfigurationParameter;
import org.junit.platform.suite.api.IncludeEngines;
import org.junit.platform.suite.api.SelectClasspathResource;
import org.junit.platform.suite.api.Suite;

/**
 * JUnit Platform Suite that runs all Cucumber feature files.
 *
 * <p>Execute with:
 * <pre>
 *   mvn test
 * </pre>
 *
 * <p>Reports are generated in {@code target/cucumber-reports/}.
 */
@Suite
@IncludeEngines("cucumber")
@SelectClasspathResource("features")
@ConfigurationParameter(
        key = "cucumber.plugin",
        value = "pretty, "
                + "html:target/cucumber-reports/cucumber.html, "
                + "json:target/cucumber-reports/cucumber.json"
)
@ConfigurationParameter(
        key = "cucumber.glue",
        value = "com.example.helloworld.steps,com.example.helloworld.support"
)
@ConfigurationParameter(key = "cucumber.publish.quiet", value = "true")
public class CucumberRunner {
}
