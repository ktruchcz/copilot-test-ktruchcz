package com.finmonol.api.tests.builders;

import java.util.HashMap;
import java.util.Map;

/**
 * Fluent builder for transaction request payloads.
 *
 * <p>Mirrors the FINMONOL COBOL WS-PARSED-TXN layout:
 * <ul>
 *   <li>TXN-ACCT-ID  – PIC X(10)</li>
 *   <li>TXN-TYPE     – PIC X(01)  (D = debit, C = credit)</li>
 *   <li>TXN-AMOUNT   – PIC S9(11)V99</li>
 *   <li>TXN-CODE     – PIC X(03)  (999 triggers MANUAL_REVIEW)</li>
 * </ul>
 */
public class TransactionBuilder {

    private String accountId     = "ACC-TEST-01";
    private String type          = "D";
    private double amount        = 100.00;
    private String code          = "001";

    public TransactionBuilder withAccountId(String accountId) {
        this.accountId = accountId;
        return this;
    }

    public TransactionBuilder withType(String type) {
        this.type = type;
        return this;
    }

    public TransactionBuilder withAmount(double amount) {
        this.amount = amount;
        return this;
    }

    public TransactionBuilder withCode(String code) {
        this.code = code;
        return this;
    }

    /** Marks this transaction with risk code 999 (triggers MANUAL_REVIEW). */
    public TransactionBuilder riskCode() {
        this.code = "999";
        return this;
    }

    public Map<String, Object> build() {
        Map<String, Object> payload = new HashMap<>();
        payload.put("accountId", accountId);
        payload.put("type", type);
        payload.put("amount", amount);
        payload.put("code", code);
        return payload;
    }

    // -----------------------------------------------------------------------
    // Static factory helpers
    // -----------------------------------------------------------------------

    public static TransactionBuilder debit(String accountId, double amount) {
        return new TransactionBuilder()
                .withAccountId(accountId)
                .withType("D")
                .withAmount(amount);
    }

    public static TransactionBuilder credit(String accountId, double amount) {
        return new TransactionBuilder()
                .withAccountId(accountId)
                .withType("C")
                .withAmount(amount);
    }

    public static TransactionBuilder riskTransaction(String accountId) {
        return new TransactionBuilder()
                .withAccountId(accountId)
                .withType("D")
                .withAmount(5000.00)
                .riskCode();
    }
}
