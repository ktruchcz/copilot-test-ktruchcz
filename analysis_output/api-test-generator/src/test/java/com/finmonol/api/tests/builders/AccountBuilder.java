package com.finmonol.api.tests.builders;

import java.util.HashMap;
import java.util.Map;

/**
 * Fluent builder for constructing account request payloads used in tests.
 *
 * <p>Default values mirror the FINMONOL COBOL data layout derived from
 * {@code ACCOUNTREC.cpy}:
 * <ul>
 *   <li>ACCT-ID      – PIC X(10)</li>
 *   <li>ACCT-NAME    – PIC X(30)</li>
 *   <li>ACCT-TYPE    – PIC X(02)  (e.g. CH = checking, SA = savings)</li>
 *   <li>ACCT-BALANCE – PIC S9(11)V99</li>
 *   <li>ACCT-LIMIT   – PIC S9(11)V99</li>
 *   <li>ACCT-STATUS  – PIC X(01)  (A = active, I = inactive)</li>
 * </ul>
 */
public class AccountBuilder {

    private String accountId = "ACC-TEST-01";
    private String name      = "Test Account";
    private String type      = "CH";
    private double balance   = 1000.00;
    private double limit     = 5000.00;
    private String status    = "A";

    public AccountBuilder withAccountId(String accountId) {
        this.accountId = accountId;
        return this;
    }

    public AccountBuilder withName(String name) {
        this.name = name;
        return this;
    }

    public AccountBuilder withType(String type) {
        this.type = type;
        return this;
    }

    public AccountBuilder withBalance(double balance) {
        this.balance = balance;
        return this;
    }

    public AccountBuilder withLimit(double limit) {
        this.limit = limit;
        return this;
    }

    public AccountBuilder withStatus(String status) {
        this.status = status;
        return this;
    }

    /** Returns an account whose balance is deliberately over the limit. */
    public AccountBuilder overLimit() {
        this.balance = this.limit + 1.00;
        return this;
    }

    /** Builds a {@code Map<String, Object>} suitable for serialising to JSON. */
    public Map<String, Object> build() {
        Map<String, Object> payload = new HashMap<>();
        payload.put("accountId", accountId);
        payload.put("name", name);
        payload.put("type", type);
        payload.put("balance", balance);
        payload.put("limit", limit);
        payload.put("status", status);
        return payload;
    }

    // -----------------------------------------------------------------------
    // Static factory helpers
    // -----------------------------------------------------------------------

    public static AccountBuilder defaultAccount() {
        return new AccountBuilder();
    }

    public static AccountBuilder overLimitAccount() {
        return new AccountBuilder()
                .withAccountId("ACC-OVERLIMIT")
                .withBalance(99000.00)
                .withLimit(10000.00);
    }

    public static AccountBuilder inactiveAccount() {
        return new AccountBuilder().withStatus("I");
    }
}
