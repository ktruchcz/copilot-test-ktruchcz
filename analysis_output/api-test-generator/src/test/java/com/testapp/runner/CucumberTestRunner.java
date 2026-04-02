package com.testapp.runner;

import org.junit.platform.suite.api.ConfigurationParameter;
import org.junit.platform.suite.api.IncludeEngines;
import org.junit.platform.suite.api.SelectClasspathResource;
import org.junit.platform.suite.api.Suite;

import static io.cucumber.junit.platform.engine.Constants.*;

/**
 * JUnit 5 Cucumber test suite runner.
 *
 * <p>Run all scenarios:
 * <pre>mvn test</pre>
 *
 * <p>Run by tag (e.g. smoke only):
 * <pre>mvn test -Dcucumber.filter.tags="@smoke"</pre>
 */
@Suite
@IncludeEngines("cucumber")
@SelectClasspathResource("features")
@ConfigurationParameter(key = PLUGIN_PROPERTY_NAME,
        value = "pretty, html:target/cucumber-reports/report.html, json:target/cucumber-reports/report.json")
@ConfigurationParameter(key = GLUE_PROPERTY_NAME, value = "com.testapp")
@ConfigurationParameter(key = FILTER_TAGS_PROPERTY_NAME, value = "${cucumber.filter.tags:}")
@ConfigurationParameter(key = EXECUTION_DRY_RUN_PROPERTY_NAME, value = "false")
@ConfigurationParameter(key = SNIPPET_TYPE_PROPERTY_NAME, value = "camelcase")
public class CucumberTestRunner {
    // Intentionally empty — JUnit Platform Suite drives execution.
}
