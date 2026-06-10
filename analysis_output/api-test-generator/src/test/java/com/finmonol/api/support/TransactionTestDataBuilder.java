package com.finmonol.api.support;

import java.util.HashMap;
import java.util.Map;

/**
 * Builder for Transaction request payloads.
 * Field names match the modernised REST API JSON contract derived from the
 * COBOL WS-PARSED-TXN structure: TXN-ACCT-ID, TXN-TYPE (D/C), TXN-AMOUNT, TXN-CODE.
 */
public class TransactionTestDataBuilder {

    private String accountId;
    private String transactionType;
    private double amount;
    private String code;

    public static TransactionTestDataBuilder aTransaction() {
        return new TransactionTestDataBuilder();
    }

    public TransactionTestDataBuilder forAccount(String accountId) {
        this.accountId = accountId;
        return this;
    }

    public TransactionTestDataBuilder ofType(String transactionType) {
        this.transactionType = transactionType;
        return this;
    }

    public TransactionTestDataBuilder withAmount(double amount) {
        this.amount = amount;
        return this;
    }

    public TransactionTestDataBuilder withCode(String code) {
        this.code = code;
        return this;
    }

    public Map<String, Object> build() {
        Map<String, Object> payload = new HashMap<>();
        payload.put("accountId", accountId);
        payload.put("transactionType", transactionType);
        payload.put("amount", amount);
        payload.put("code", code);
        return payload;
    }

    // ── Pre-built realistic transactions ──────────────────────────────────────

    /** Standard debit transaction with a normal risk code. */
    public static Map<String, Object> standardDebit(String accountId, double amount) {
        return aTransaction()
                .forAccount(accountId)
                .ofType("D")
                .withAmount(amount)
                .withCode("100")
                .build();
    }

    /** Standard credit transaction with a normal risk code. */
    public static Map<String, Object> standardCredit(String accountId, double amount) {
        return aTransaction()
                .forAccount(accountId)
                .ofType("C")
                .withAmount(amount)
                .withCode("200")
                .build();
    }

    /**
     * High-risk debit transaction using code 999, which maps to the COBOL
     * MANUAL REVIEW path (TXN-CODE = '999').
     */
    public static Map<String, Object> highRiskDebit(String accountId, double amount) {
        return aTransaction()
                .forAccount(accountId)
                .ofType("D")
                .withAmount(amount)
                .withCode("999")
                .build();
    }
}
