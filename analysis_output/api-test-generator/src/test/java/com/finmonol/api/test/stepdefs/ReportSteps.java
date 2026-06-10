package com.finmonol.api.test.stepdefs;

import com.finmonol.api.test.support.ApiClient;
import com.finmonol.api.test.support.TestContext;
import io.cucumber.java.en.Then;
import io.cucumber.java.en.When;
import io.restassured.response.Response;

import static org.assertj.core.api.Assertions.assertThat;

/**
 * Cucumber step definitions covering day-end report and totals scenarios.
 *
 * <p>These steps replace the COBOL FINMONOL paragraph:
 * <ul>
 *   <li>9000-WRITE-SUMMARY (TOTAL DEBITS, TOTAL CREDITS, OVERLIMIT CNT,
 *       ENGINE, RUNNER)</li>
 * </ul>
 * and the working-storage accumulators:
 * <ul>
 *   <li>WS-TOTAL-DEBITS</li>
 *   <li>WS-TOTAL-CREDITS</li>
 *   <li>WS-OVERLIMIT-COUNT</li>
 *   <li>WS-LEDGER-ENGINE</li>
 *   <li>WS-BATCH-RUNNER</li>
 * </ul>
 */
public class ReportSteps {

    private final TestContext ctx;
    private final ApiClient   api;

    public ReportSteps(TestContext ctx) {
        this.ctx = ctx;
        this.api = new ApiClient();
    }

    // ------------------------------------------------------------------
    // When – action steps
    // ------------------------------------------------------------------

    @When("I generate the day-end report")
    public void iGenerateTheDayEndReport() {
        Response response = api.getDayEndReport();
        ctx.setLastResponse(response);
    }

    @When("I retrieve the totals summary")
    public void iRetrieveTheTotalsSummary() {
        Response response = api.getTotalsSummary();
        ctx.setLastResponse(response);
    }

    // ------------------------------------------------------------------
    // Then – assertion steps
    // ------------------------------------------------------------------

    @Then("the report should contain a {string} field")
    public void theReportShouldContainAField(String fieldName) {
        Object value = ctx.getLastResponse().jsonPath().get(fieldName);
        assertThat(value)
                .as("Report should contain field '%s'", fieldName)
                .isNotNull();
    }

    @Then("the report field {string} should be greater than {int}")
    public void theReportFieldShouldBeGreaterThan(String field, int threshold) {
        double actual = ctx.getLastResponse().jsonPath().getDouble(field);
        assertThat(actual)
                .as("Report field '%s'", field)
                .isGreaterThan(threshold);
    }

    @Then("the report field {string} should be at least {int}")
    public void theReportFieldShouldBeAtLeast(String field, int minimum) {
        double actual = ctx.getLastResponse().jsonPath().getDouble(field);
        assertThat(actual)
                .as("Report field '%s'", field)
                .isGreaterThanOrEqualTo(minimum);
    }

    @Then("the total debits should be at least {double}")
    public void theTotalDebitsShouldBeAtLeast(double minimum) {
        double actual = ctx.getLastResponse().jsonPath().getDouble("totalDebits");
        assertThat(actual)
                .as("totalDebits")
                .isGreaterThanOrEqualTo(minimum);
    }

    @Then("the total credits should be at least {double}")
    public void theTotalCreditsShouldBeAtLeast(double minimum) {
        double actual = ctx.getLastResponse().jsonPath().getDouble("totalCredits");
        assertThat(actual)
                .as("totalCredits")
                .isGreaterThanOrEqualTo(minimum);
    }
}
