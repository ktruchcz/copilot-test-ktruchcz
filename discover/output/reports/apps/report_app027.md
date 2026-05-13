# DataWarehouseApp-027 (app027)

**Status:** Production | **Criticality:** High | **Solution Type:** Custom made

## Overview

| Field | Value |
|-------|-------|
| Description | Enterprise data warehouse for consolidating business data from multiple sources |
| Business Unit | BI |
| Operating System | RHEL 7 |
| Programming Language | Java 11 |
| Database | SQL Server 2022 |
| Architecture | 3-Tier |
| Containerized | No |
| CI/CD Present | Yes |
| Environments | 3 |
| Server Instances | sv39, sv40 |
| External Interfaces | 20 |
| Users | 320 |

## Technology Assessment

**Overall Status:** 🔴 EOL

| Component | Name | Status |
|-----------|------|--------|
| operating_system | RHEL 7 | 🔴 EOL |
| programming_language | Java 11 | ⚠️ OUTDATED |
| database | SQL Server 2022 | ✅ CURRENT_VERSION |
| application_server | Websphere 8.5 | ❓ NO_KNOWLEDGE |

## Complexity Assessment

**Score:** 8/10 — **Classification:** HIGH

| Factor | Score |
|--------|-------|
| Technology Age Eol | 2.5 |
| Integration Complexity | 2.0 |
| Infrastructure Scale | 1.05 |
| Business Criticality | 1.05 |
| Code And Architecture | 0.45 |
| Data Complexity | 1.0 |

## Scenario Analysis

| Scenario | Status | Reasoning |
|----------|--------|-----------|
| OS Update / Security Patch | APPLICABLE | OS RHEL 7 is EOL; security patch update is needed. |
| Switch to Standard Linux OS | FULFILLED | Already running on standard Linux (RHEL 7). |
| Switch to ARM CPU | APPLICABLE | ARM CPU migration is possible with recompilation/containerization effort. |
| Application Server Replacement | APPLICABLE | Uses application server Websphere 8.5; replacement/upgrade may be beneficial. |
| Cloud Migration (Lift & Shift) | APPLICABLE | Application can be migrated to cloud (lift & shift). |
| Containerization | APPLICABLE | Application can be containerized to improve portability and scalability. |
| Refactoring & Decoupling | APPLICABLE | High complexity (8/10); refactoring would reduce technical debt. |
| Upgrade Legacy Databases | NOT_APPLICABLE | Database SQL Server 2022 is current; no immediate upgrade needed. |
| Switch to Open Source DB | APPLICABLE | Uses proprietary database SQL Server 2022; switching to PostgreSQL/MySQL would reduce licensing costs. |
| Update Outdated Components | APPLICABLE | Multiple outdated components detected (OS: EOL, Lang: OUTDATED, DB: CURRENT_VERSION). |

## Business Case

**Total Implementation Cost:** $605,686.53
**Total Annual Savings:** $225,200.00
**3-Year ROI:** 11.5%

| Scenario | Impl. Cost | Annual Savings | 3-Yr ROI | Payback (mo) |
|----------|------------|----------------|----------|--------------|
| OS Update / Security Patch | $1,529.51 | $400.00 | -21.5% | 45.9 |
| Switch to ARM CPU | $7,647.56 | $800.00 | -68.6% | 114.7 |
| Application Server Replacement | $15,295.11 | $9,600.00 | 88.3% | 19.1 |
| Cloud Migration (Lift & Shift) | $7,647.56 | $2,400.00 | -5.9% | 38.2 |
| Containerization | $152,951.14 | $80,000.00 | 56.9% | 22.9 |
| Refactoring & Decoupling | $382,377.86 | $120,000.00 | -5.9% | 38.2 |
| Switch to Open Source DB | $38,237.79 | $12,000.00 | -5.9% | 38.2 |
