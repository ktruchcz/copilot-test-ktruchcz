package com.finmonol.api.steps;

import com.finmonol.api.support.ApiClient;
import com.finmonol.api.support.TestContext;
import io.cucumber.java.en.And;
import io.cucumber.java.en.Then;
import io.cucumber.java.en.When;

import static org.assertj.core.api.Assertions.assertThat;

/**
 * Cucumber step definitions for day-end reporting scenarios.
 * Covers: total debits, total credits, over-limit counts, and manual review
 * sections in the day-end report — mapping to the COBOL 9000-WRITE-SUMMARY
 * and 3300-LEGACY-RISK-CHECK paragraphs.
 */
public class ReportingStepDefinitions {

    private final TestContext ctx;
    private final ApiClient api;

    public ReportingStepDefinitions(TestContext ctx) {
        this.ctx = ctx;
        this.api = new ApiClient();
    }

    @When("I request the day-end report")
    public void iRequestTheDayEndReport() {
        ctx.setLastResponse(api.getDayEndReport());
    }

    @When("I request the day-end report for date {string}")
    public void iRequestTheDayEndReportForDate(String date) {
        ctx.setLastResponse(api.getDayEndReport(date));
    }

    @When("I request the day-end summary")
    public void iRequestTheDayEndSummary() {
        ctx.setLastResponse(api.getDayEndSummary());
    }

    @And("the report total debits should be {double}")
    public void theReportTotalDebitsShouldBe(double expected) {
        double actual = ctx.getLastResponse().jsonPath().getDouble("totalDebits");
        assertThat(actual).isEqualTo(expected);
    }

    @And("the report total credits should be {double}")
    public void theReportTotalCreditsShouldBe(double expected) {
        double actual = ctx.getLastResponse().jsonPath().getDouble("totalCredits");
        assertThat(actual).isEqualTo(expected);
    }

    @And("the report over-limit account count should be at least {int}")
    public void theReportOverLimitAccountCountShouldBeAtLeast(int minCount) {
        int actual = ctx.getLastResponse().jsonPath().getInt("overLimitCount");
        assertThat(actual).isGreaterThanOrEqualTo(minCount);
    }

    @And("the report over-limit account count should be {int}")
    public void theReportOverLimitAccountCountShouldBe(int expected) {
        int actual = ctx.getLastResponse().jsonPath().getInt("overLimitCount");
        assertThat(actual).isEqualTo(expected);
    }

    @And("the summary should contain a total debits field")
    public void theSummaryShouldContainATotalDebitsField() {
        assertThat((Object) ctx.getLastResponse().jsonPath().get("totalDebits"))
                .as("totalDebits field should be present").isNotNull();
    }

    @And("the summary should contain a total credits field")
    public void theSummaryShouldContainATotalCreditsField() {
        assertThat((Object) ctx.getLastResponse().jsonPath().get("totalCredits"))
                .as("totalCredits field should be present").isNotNull();
    }

    @And("the summary should contain an over-limit count field")
    public void theSummaryShouldContainAnOverLimitCountField() {
        assertThat((Object) ctx.getLastResponse().jsonPath().get("overLimitCount"))
                .as("overLimitCount field should be present").isNotNull();
    }

    @And("the report should include a manual review section")
    public void theReportShouldIncludeAManualReviewSection() {
        assertThat((Object) ctx.getLastResponse().jsonPath().get("manualReviews"))
                .as("manualReviews section should be present").isNotNull();
    }

    @And("the manual review section should contain account {string}")
    public void theManualReviewSectionShouldContainAccount(String accountId) {
        String json = ctx.getLastResponse().asString();
        assertThat(json).contains(accountId);
    }
}
