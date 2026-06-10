package com.finmonol.api.steps;

import com.finmonol.api.support.ApiClient;
import com.finmonol.api.support.TestContext;
import io.cucumber.java.en.And;
import io.cucumber.java.en.Then;
import io.cucumber.java.en.When;

import java.util.HashMap;
import java.util.Map;

import static org.assertj.core.api.Assertions.assertThat;

/**
 * Cucumber step definitions for risk management scenarios.
 * Covers: code-999 manual review flagging, over-limit risk, and
 * high-value enhanced review, mapping to the COBOL 3300-LEGACY-RISK-CHECK
 * and 2200-CHECK-ACCOUNT-LIMIT paragraphs.
 */
public class RiskManagementStepDefinitions {

    private final TestContext ctx;
    private final ApiClient api;

    public RiskManagementStepDefinitions(TestContext ctx) {
        this.ctx = ctx;
        this.api = new ApiClient();
    }

    @When("I assess risk for account {string} transaction with amount {double} and code {string}")
    public void iAssessRisk(String accountId, double amount, String code) {
        Map<String, Object> payload = new HashMap<>();
        payload.put("accountId", accountId);
        payload.put("amount", amount);
        payload.put("code", code);
        ctx.setLastResponse(api.assessRisk(payload));
    }

    @Then("the risk assessment result should be {string}")
    public void theRiskAssessmentResultShouldBe(String expected) {
        String actual = ctx.getLastResponse().jsonPath().getString("result");
        assertThat(actual).isEqualTo(expected);
    }

    @And("the transaction should require manual review")
    public void theTransactionShouldRequireManualReview() {
        Boolean required = ctx.getLastResponse().jsonPath().getBoolean("manualReview");
        assertThat(required).as("Risk assessment should require manual review").isTrue();
    }

    @And("the transaction should not require manual review")
    public void theTransactionShouldNotRequireManualReview() {
        Boolean required = ctx.getLastResponse().jsonPath().getBoolean("manualReview");
        assertThat(required).as("Risk assessment should NOT require manual review").isFalse();
    }

    @And("the risk reason should contain {string}")
    public void theRiskReasonShouldContain(String text) {
        String reason = ctx.getLastResponse().jsonPath().getString("reason");
        assertThat(reason).containsIgnoringCase(text);
    }
}
