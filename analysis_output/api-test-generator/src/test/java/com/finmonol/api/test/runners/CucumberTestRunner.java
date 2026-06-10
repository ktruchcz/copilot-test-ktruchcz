package com.finmonol.api.test.runners;

import org.junit.platform.suite.api.ConfigurationParameter;
import org.junit.platform.suite.api.IncludeEngines;
import org.junit.platform.suite.api.SelectClasspathResource;
import org.junit.platform.suite.api.Suite;

import static io.cucumber.junit.platform.engine.Constants.GLUE_PROPERTY_NAME;
import static io.cucumber.junit.platform.engine.Constants.PLUGIN_PROPERTY_NAME;
import static io.cucumber.junit.platform.engine.Constants.FILTER_TAGS_PROPERTY_NAME;

/**
 * JUnit 5 test suite runner for the FINMONOL upgrade_legacy_databases
 * Cucumber BDD scenarios.
 *
 * <p>Run all scenarios:
 * <pre>mvn test</pre>
 *
 * <p>Run a specific tag:
 * <pre>mvn test -Dcucumber.filter.tags="@account_management"</pre>
 */
@Suite
@IncludeEngines("cucumber")
@SelectClasspathResource("features")
@ConfigurationParameter(
        key = GLUE_PROPERTY_NAME,
        value = "com.finmonol.api.test.stepdefs,com.finmonol.api.test.support")
@ConfigurationParameter(
        key = PLUGIN_PROPERTY_NAME,
        value = "pretty, json:target/cucumber-reports/cucumber.json, html:target/cucumber-reports/cucumber.html")
public class CucumberTestRunner {
}
