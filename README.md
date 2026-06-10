# Legacy Finance COBOL Monolith

This repository contains a deliberately old-styled COBOL finance application intended for future modernization exercises.

## Layout

- `/src/cobol/FINMONOL.cbl` - monolithic finance application
- `/src/copybooks/ACCOUNTREC.cpy` - shared record definition
- `/docs/MODERNIZATION_PATH.md` - modernization directions

## Characteristics

- Single large procedural program
- File-based data access and hard-coded rules
- Tight coupling between input, business rules, and output
- Outdated component markers (`LEDGER-ENGINE-V1`, `BATCH-RUNNER-1988`)
