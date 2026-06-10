package runners;

import io.cucumber.junit.Cucumber;
import io.cucumber.junit.CucumberOptions;
import org.junit.runner.RunWith;

/**
 * JUnit 4 Cucumber runner.
 *
 * Tags can be overridden at runtime:
 *   mvn test -Dcucumber.filter.tags="@smoke"
 */
@RunWith(Cucumber.class)
@CucumberOptions(
        features  = "src/test/resources/features",
        glue      = {"steps", "support"},
        plugin    = {
                "pretty",
                "html:target/cucumber-reports/cucumber.html",
                "json:target/cucumber-reports/cucumber.json",
                "junit:target/cucumber-reports/cucumber.xml"
        },
        tags      = "not @wip",
        monochrome = true
)
public class CucumberRunner {
}
