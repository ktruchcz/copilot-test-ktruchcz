package support;

import java.math.BigDecimal;
import java.util.HashMap;
import java.util.Map;

/**
 * Fluent builder for constructing test-data payloads that mirror the data model
 * extracted from the COBOL FINMONOL copybook (ACCOUNTREC.cpy) and working-storage
 * transaction fields.
 */
public class TestDataBuilder {

    // ------------------------------------------------------------------
    // Account builder
    // ------------------------------------------------------------------

    public static AccountBuilder anAccount() {
        return new AccountBuilder();
    }

    public static class AccountBuilder {
        private String id;
        private String name;
        private String type = "CA";
        private BigDecimal balance = BigDecimal.ZERO;
        private BigDecimal limit = new BigDecimal("10000.00");
        private String status = "A";

        public AccountBuilder withId(String id) {
            this.id = id;
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
            this.balance = BigDecimal.valueOf(balance);
            return this;
        }

        public AccountBuilder withBalance(String balance) {
            this.balance = new BigDecimal(balance);
            return this;
        }

        public AccountBuilder withLimit(double limit) {
            this.limit = BigDecimal.valueOf(limit);
            return this;
        }

        public AccountBuilder withLimit(String limit) {
            this.limit = new BigDecimal(limit);
            return this;
        }

        public AccountBuilder withStatus(String status) {
            this.status = status;
            return this;
        }

        public Map<String, Object> build() {
            Map<String, Object> payload = new HashMap<>();
            if (id != null)     payload.put("id", id);
            if (name != null)   payload.put("name", name);
            payload.put("type", type);
            payload.put("balance", balance);
            payload.put("limit", limit);
            payload.put("status", status);
            return payload;
        }
    }

    // ------------------------------------------------------------------
    // Transaction builder
    // ------------------------------------------------------------------

    /** TXN-TYPE 'D' = Debit */
    public static TransactionBuilder aDebitTransaction() {
        return new TransactionBuilder("D");
    }

    /** TXN-TYPE 'C' = Credit */
    public static TransactionBuilder aCreditTransaction() {
        return new TransactionBuilder("C");
    }

    public static class TransactionBuilder {
        private final String type;
        private String accountId;
        private BigDecimal amount = BigDecimal.ZERO;
        private String code = "001";

        private TransactionBuilder(String type) {
            this.type = type;
        }

        public TransactionBuilder forAccount(String accountId) {
            this.accountId = accountId;
            return this;
        }

        public TransactionBuilder withAmount(double amount) {
            this.amount = BigDecimal.valueOf(amount);
            return this;
        }

        public TransactionBuilder withAmount(String amount) {
            this.amount = new BigDecimal(amount);
            return this;
        }

        /**
         * TXN-CODE: 3-character code. Code '999' triggers the legacy manual-review flag.
         */
        public TransactionBuilder withCode(String code) {
            this.code = code;
            return this;
        }

        public Map<String, Object> build() {
            Map<String, Object> payload = new HashMap<>();
            if (accountId != null) payload.put("accountId", accountId);
            payload.put("type", type);
            payload.put("amount", amount);
            payload.put("code", code);
            return payload;
        }
    }

    // ------------------------------------------------------------------
    // Helpers for table-driven scenarios
    // ------------------------------------------------------------------

    /**
     * Build an account payload from a Cucumber DataTable row map.
     * Expected keys: id, name, type, balance, limit, status.
     */
    public static Map<String, Object> accountFromRow(Map<String, String> row) {
        return anAccount()
                .withId(row.get("id"))
                .withName(row.get("name"))
                .withType(row.getOrDefault("type", "CA"))
                .withBalance(row.getOrDefault("balance", "0"))
                .withLimit(row.getOrDefault("limit", "10000.00"))
                .withStatus(row.getOrDefault("status", "A"))
                .build();
    }

    /**
     * Build a transaction payload from a Cucumber DataTable row map.
     * Expected keys: type, amount, code (accountId supplied separately).
     */
    public static Map<String, Object> transactionFromRow(String accountId, Map<String, String> row) {
        String type = row.getOrDefault("type", "D");
        TransactionBuilder builder = "C".equalsIgnoreCase(type)
                ? aCreditTransaction() : aDebitTransaction();
        return builder
                .forAccount(accountId)
                .withAmount(row.getOrDefault("amount", "0"))
                .withCode(row.getOrDefault("code", "001"))
                .build();
    }
}
