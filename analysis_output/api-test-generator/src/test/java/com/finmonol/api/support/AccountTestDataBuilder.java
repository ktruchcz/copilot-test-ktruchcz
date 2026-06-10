package com.finmonol.api.support;

import java.util.HashMap;
import java.util.Map;

/**
 * Builder for Account request payloads.
 * Field names match the modernised REST API JSON contract derived from the
 * COBOL ACCOUNT-RECORD / ACCOUNTREC copybook.
 */
public class AccountTestDataBuilder {

    private String accountId;
    private String accountName;
    private String accountType;
    private double balance;
    private double creditLimit;
    private String status = "A";

    public static AccountTestDataBuilder anAccount() {
        return new AccountTestDataBuilder();
    }

    public AccountTestDataBuilder withId(String accountId) {
        this.accountId = accountId;
        return this;
    }

    public AccountTestDataBuilder withName(String accountName) {
        this.accountName = accountName;
        return this;
    }

    public AccountTestDataBuilder withType(String accountType) {
        this.accountType = accountType;
        return this;
    }

    public AccountTestDataBuilder withBalance(double balance) {
        this.balance = balance;
        return this;
    }

    public AccountTestDataBuilder withCreditLimit(double creditLimit) {
        this.creditLimit = creditLimit;
        return this;
    }

    public AccountTestDataBuilder withStatus(String status) {
        this.status = status;
        return this;
    }

    public Map<String, Object> build() {
        Map<String, Object> payload = new HashMap<>();
        payload.put("accountId", accountId);
        payload.put("accountName", accountName);
        payload.put("accountType", accountType);
        payload.put("balance", balance);
        payload.put("creditLimit", creditLimit);
        payload.put("status", status);
        return payload;
    }

    // ── Pre-built realistic test accounts ────────────────────────────────────

    /** Standard active checking account, balance well within limit. */
    public static Map<String, Object> defaultCheckingAccount(String id) {
        return anAccount()
                .withId(id)
                .withName("Test Account Holder")
                .withType("CH")
                .withBalance(5000.00)
                .withCreditLimit(10000.00)
                .withStatus("A")
                .build();
    }

    /** Savings account. */
    public static Map<String, Object> defaultSavingsAccount(String id) {
        return anAccount()
                .withId(id)
                .withName("Savings Account Holder")
                .withType("SV")
                .withBalance(12500.00)
                .withCreditLimit(20000.00)
                .withStatus("A")
                .build();
    }

    /** Account whose balance already exceeds its credit limit (over-limit). */
    public static Map<String, Object> overLimitAccount(String id) {
        return anAccount()
                .withId(id)
                .withName("Over Limit Account")
                .withType("CH")
                .withBalance(12000.00)
                .withCreditLimit(10000.00)
                .withStatus("A")
                .build();
    }

    /** Inactive account. */
    public static Map<String, Object> inactiveAccount(String id) {
        return anAccount()
                .withId(id)
                .withName("Inactive Account Holder")
                .withType("CH")
                .withBalance(0.00)
                .withCreditLimit(1000.00)
                .withStatus("I")
                .build();
    }
}
