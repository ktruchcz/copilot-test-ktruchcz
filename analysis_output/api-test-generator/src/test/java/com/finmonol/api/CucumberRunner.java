package com.finmonol.api;

import org.junit.platform.suite.api.ConfigurationParameter;
import org.junit.platform.suite.api.IncludeEngines;
import org.junit.platform.suite.api.SelectClasspathResource;
import org.junit.platform.suite.api.Suite;

import static io.cucumber.junit.platform.engine.Constants.GLUE_PROPERTY_NAME;
import static io.cucumber.junit.platform.engine.Constants.PLUGIN_PROPERTY_NAME;

/**
 * JUnit 5 Cucumber test suite runner for the Finance Monolith API tests.
 * Run all scenarios with: mvn test
 * Run a specific tag: mvn test -Dcucumber.filter.tags="@smoke"
 */
@Suite
@IncludeEngines("cucumber")
@SelectClasspathResource("features")
@ConfigurationParameter(key = GLUE_PROPERTY_NAME,
        value = "com.finmonol.api.steps,com.finmonol.api.support")
@ConfigurationParameter(key = PLUGIN_PROPERTY_NAME,
        value = "pretty, json:target/cucumber-reports/cucumber.json, html:target/cucumber-reports/report.html")
public class CucumberRunner {
    // Entry-point; JUnit 5 Suite discovers and runs all feature files.
}
