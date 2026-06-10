package com.finmonol.api.test.support;

import java.math.BigDecimal;
import java.util.HashMap;
import java.util.Map;

/**
 * Fluent builder for constructing well-formed test-data payloads.
 *
 * <p>Data shapes are derived from the COBOL FINMONOL working-storage layout:
 * <ul>
 *   <li>Account: ACCT-ID (10), ACCT-NAME (30), ACCT-TYPE (2), ACCT-BALANCE,
 *       ACCT-LIMIT, ACCT-STATUS (1)</li>
 *   <li>Transaction: TXN-ACCT-ID (10), TXN-TYPE (1) [D/C], TXN-AMOUNT,
 *       TXN-CODE (3)</li>
 * </ul>
 */
public class TestDataBuilder {

    // ------------------------------------------------------------------
    // AccountBuilder
    // ------------------------------------------------------------------

    /**
     * Creates a new {@link AccountBuilder} pre-populated with safe default
     * values so that callers only need to override what is relevant for their
     * scenario.
     *
     * @return new builder instance
     */
    public static AccountBuilder anAccount() {
        return new AccountBuilder();
    }

    public static class AccountBuilder {
        private String accountId   = "ACCT000001";
        private String accountName = "Default Test Account";
        private String accountType = "CA";
        private BigDecimal balance     = BigDecimal.ZERO;
        private BigDecimal creditLimit = new BigDecimal("10000.00");
        private String status      = "A";

        public AccountBuilder withAccountId(String accountId) {
            this.accountId = accountId;
            return this;
        }

        public AccountBuilder withAccountName(String accountName) {
            this.accountName = accountName;
            return this;
        }

        public AccountBuilder withAccountType(String accountType) {
            this.accountType = accountType;
            return this;
        }

        public AccountBuilder withBalance(double balance) {
            this.balance = BigDecimal.valueOf(balance);
            return this;
        }

        public AccountBuilder withCreditLimit(double creditLimit) {
            this.creditLimit = BigDecimal.valueOf(creditLimit);
            return this;
        }

        public AccountBuilder withStatus(String status) {
            this.status = status;
            return this;
        }

        /** Builds the account over its credit limit (balance = limit + 1). */
        public AccountBuilder overLimit() {
            this.balance = this.creditLimit.add(BigDecimal.ONE);
            return this;
        }

        /** Builds the request payload as a {@link Map} ready for JSON serialisation. */
        public Map<String, Object> build() {
            Map<String, Object> payload = new HashMap<>();
            payload.put("accountId",   accountId);
            payload.put("accountName", accountName);
            payload.put("accountType", accountType);
            payload.put("balance",     balance);
            payload.put("creditLimit", creditLimit);
            payload.put("status",      status);
            return payload;
        }
    }

    // ------------------------------------------------------------------
    // TransactionBuilder
    // ------------------------------------------------------------------

    /**
     * Creates a new {@link TransactionBuilder} pre-populated with safe default
     * values.
     *
     * @return new builder instance
     */
    public static TransactionBuilder aTransaction() {
        return new TransactionBuilder();
    }

    public static class TransactionBuilder {
        private String accountId       = "ACCT000001";
        private String transactionType = "D";
        private BigDecimal amount      = new BigDecimal("100.00");
        private String transactionCode = "001";

        public TransactionBuilder forAccount(String accountId) {
            this.accountId = accountId;
            return this;
        }

        /** Sets type to {@code "D"} (debit). */
        public TransactionBuilder asDebit() {
            this.transactionType = "D";
            return this;
        }

        /** Sets type to {@code "C"} (credit). */
        public TransactionBuilder asCredit() {
            this.transactionType = "C";
            return this;
        }

        public TransactionBuilder withAmount(double amount) {
            this.amount = BigDecimal.valueOf(amount);
            return this;
        }

        public TransactionBuilder withCode(String code) {
            this.transactionCode = code;
            return this;
        }

        /**
         * Sets the transaction code to {@code "999"}, triggering the legacy
         * MANUAL REVIEW risk-check rule (3300-LEGACY-RISK-CHECK).
         */
        public TransactionBuilder requiresManualReview() {
            this.transactionCode = "999";
            return this;
        }

        /** Builds the request payload as a {@link Map} ready for JSON serialisation. */
        public Map<String, Object> build() {
            Map<String, Object> payload = new HashMap<>();
            payload.put("accountId",       accountId);
            payload.put("transactionType", transactionType);
            payload.put("amount",          amount);
            payload.put("transactionCode", transactionCode);
            return payload;
        }
    }

    // ------------------------------------------------------------------
    // Convenience factory helpers
    // ------------------------------------------------------------------

    /**
     * Convenience method: builds a standard debit transaction payload.
     *
     * @param accountId account identifier
     * @param amount    transaction amount
     * @param code      transaction code (3 characters)
     * @return payload map
     */
    public static Map<String, Object> debitTransaction(
            String accountId, double amount, String code) {
        return aTransaction()
                .forAccount(accountId)
                .asDebit()
                .withAmount(amount)
                .withCode(code)
                .build();
    }

    /**
     * Convenience method: builds a standard credit transaction payload.
     *
     * @param accountId account identifier
     * @param amount    transaction amount
     * @param code      transaction code (3 characters)
     * @return payload map
     */
    public static Map<String, Object> creditTransaction(
            String accountId, double amount, String code) {
        return aTransaction()
                .forAccount(accountId)
                .asCredit()
                .withAmount(amount)
                .withCode(code)
                .build();
    }

    /**
     * Convenience method: builds an account payload from a Cucumber data-table row.
     *
     * @param row map of column name → value
     * @return payload map
     */
    public static Map<String, Object> accountFromRow(Map<String, String> row) {
        return anAccount()
                .withAccountId(row.get("accountId"))
                .withAccountName(row.get("accountName"))
                .withAccountType(row.get("accountType"))
                .withBalance(Double.parseDouble(row.get("balance")))
                .withCreditLimit(Double.parseDouble(row.get("creditLimit")))
                .withStatus(row.get("status"))
                .build();
    }

    /**
     * Convenience method: builds a transaction payload from a Cucumber data-table row.
     *
     * @param row map of column name → value
     * @return payload map
     */
    public static Map<String, Object> transactionFromRow(Map<String, String> row) {
        return aTransaction()
                .forAccount(row.get("accountId"))
                .withCode(row.get("transactionCode"))
                .withAmount(Double.parseDouble(row.get("amount")))
                .asDebit() // default; overridden below if needed
                .build();
    }
}
