# Planned Modernization Directions

This codebase is intentionally legacy and monolithic.

## 1) Application Refactoring and De-coupling

- Split one large program into bounded business modules (accounts, transactions, risk, reporting).
- Isolate file I/O from business rules.
- Extract transaction processing into callable services.
- Replace direct shared working-storage coupling with explicit data contracts.

## 2) Update Outdated Components

- Replace `LEDGER-ENGINE-V1` with a maintained ledger service.
- Replace `BATCH-RUNNER-1988` with modern batch orchestration.
- Replace flat-file processing with managed storage/database access.
- Add automated tests and CI checks around refactored modules.
