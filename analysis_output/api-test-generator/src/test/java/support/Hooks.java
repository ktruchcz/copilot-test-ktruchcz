package support;

import io.cucumber.java.After;
import io.cucumber.java.Before;
import io.cucumber.java.Scenario;

/**
 * Cucumber lifecycle hooks.
 * Wires up any per-scenario setup / teardown that all step definition classes need.
 */
public class Hooks {

    private final TestContext ctx;

    public Hooks(TestContext ctx) {
        this.ctx = ctx;
    }

    @Before
    public void beforeScenario(Scenario scenario) {
        // TestContext is created fresh per scenario by PicoContainer DI.
        // Add any global pre-scenario setup here (e.g., auth token retrieval).
    }

    @After
    public void afterScenario(Scenario scenario) {
        if (scenario.isFailed() && ctx.getLastResponse() != null) {
            String body = ctx.getLastResponse().getBody().asPrettyString();
            scenario.attach(body.getBytes(), "application/json", "Last API Response");
        }
    }
}
