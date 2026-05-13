# DocumentApp-014 (app014)

**Status:** Production | **Criticality:** Medium | **Solution Type:** Open Source

## Overview

| Field | Value |
|-------|-------|
| Description | Document management system for handling shipping documents, contracts, and regulatory paperwork |
| Business Unit | Operations |
| Operating System | Windows Server 2019 |
| Programming Language | C# .NET 6 |
| Database | MySQL 8.0 |
| Architecture | 2-Tier |
| Containerized | No |
| CI/CD Present | Yes |
| Environments | 2 |
| Server Instances | sv19, sv20 |
| External Interfaces | 9 |
| Users | 890 |

## Technology Assessment

**Overall Status:** ⚠️ OUTDATED

| Component | Name | Status |
|-----------|------|--------|
| operating_system | Windows Server 2019 | ✅ CURRENT_VERSION |
| programming_language | C# .NET 6 | ⚠️ OUTDATED |
| database | MySQL 8.0 | ✅ CURRENT_VERSION |
| application_server | Microsoft IIS 10.0 | ❓ NO_KNOWLEDGE |

## Complexity Assessment

**Score:** 5/10 — **Classification:** MEDIUM

| Factor | Score |
|--------|-------|
| Technology Age Eol | 1.5 |
| Integration Complexity | 0.8 |
| Infrastructure Scale | 0.9 |
| Business Criticality | 0.6 |
| Code And Architecture | 0.75 |
| Data Complexity | 0.5 |

## Scenario Analysis

| Scenario | Status | Reasoning |
|----------|--------|-----------|
| OS Update / Security Patch | NOT_APPLICABLE | OS Windows Server 2019 is current; no immediate patch needed. |
| Switch to Standard Linux OS | APPLICABLE | Running on Windows Server 2019; migrating to standard Linux would reduce licensing costs. |
| Switch to ARM CPU | APPLICABLE | ARM CPU migration is possible with recompilation/containerization effort. |
| Application Server Replacement | APPLICABLE | Uses application server Microsoft IIS 10.0; replacement/upgrade may be beneficial. |
| Cloud Migration (Lift & Shift) | APPLICABLE | Application can be migrated to cloud (lift & shift). |
| Containerization | APPLICABLE | Application can be containerized to improve portability and scalability. |
| Refactoring & Decoupling | APPLICABLE | Refactoring would improve maintainability and reduce technical debt. |
| Upgrade Legacy Databases | NOT_APPLICABLE | Database MySQL 8.0 is current; no immediate upgrade needed. |
| Switch to Open Source DB | NOT_APPLICABLE | Already using open source or managed database (MySQL 8.0). |
| Update Outdated Components | APPLICABLE | Multiple outdated components detected (OS: CURRENT_VERSION, Lang: OUTDATED, DB: CURRENT_VERSION). |

## Business Case

**Total Implementation Cost:** $372,402.78
**Total Annual Savings:** $239,760.00
**3-Year ROI:** 93.1%

| Scenario | Impl. Cost | Annual Savings | 3-Yr ROI | Payback (mo) |
|----------|------------|----------------|----------|--------------|
| Switch to Standard Linux OS | $301.70 | $360.00 | 258.0% | 10.1 |
| Switch to ARM CPU | $5,028.39 | $900.00 | -46.3% | 67.0 |
| Application Server Replacement | $10,056.79 | $10,800.00 | 222.2% | 11.2 |
| Cloud Migration (Lift & Shift) | $5,028.39 | $2,700.00 | 61.1% | 22.3 |
| Containerization | $100,567.86 | $90,000.00 | 168.5% | 13.4 |
| Refactoring & Decoupling | $251,419.65 | $135,000.00 | 61.1% | 22.3 |
