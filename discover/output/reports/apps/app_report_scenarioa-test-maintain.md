# Application Report - COBOL maintain

**Application ID:** scenarioa-test-maintain  
**Business Unit:** Finance  
**Criticality:** High  
**Status:** Production  
**Analysis Date:** 2026-06-25

This application is a core ERP system handling financial transactions, general ledger, and regulatory reporting. Like its counterpart, it is a custom-made COBOL application on IBM AIX with Oracle Database. It is designated for maintenance-mode operation but retains identical modernization needs and risks as the transform variant.

## Application Overview

| Attribute | Value |
|-----------|-------|
| Solution Type | Custom made |
| Deployment Type | On-Premise |
| Architecture | 1-Tier (Monolith) |
| Containerized | No |
| CI/CD Pipeline | No |
| Users | 350 |
| Environments | 2 |
| Servers | sv01, sv02 |
| CPU Cores | 4 |
| Memory | 16 GB |
| API Endpoints | 0 |
| External Interfaces | 5 |
| Data Classification | Confidential |
| Decommission Date | 2027 |

## Technology Assessment

| Component | Type | Version | Status | EOL Date | Notes |
|-----------|------|---------|--------|----------|-------|
| IBM AIX | Operating System | 7.2 | 🔴 EOL | 2023-04-30 | Standard support ended April 2023; proprietary UNIX, no container support |
| COBOL | Programming Language | 2014 | 🟡 OUTDATED | — | Legacy language standard; scarce developer talent; superseded by COBOL 2023 |
| Oracle Database | Database | 19c | 🟡 OUTDATED | 2027-01-31 | In Extended Support (Premier ended Jan 2024); commercial license at extra cost |

```mermaid
pie title Technology Health
    "EOL" : 1
    "OUTDATED" : 2
    "CURRENT" : 0
```

## Complexity Assessment

**Complexity Score: 7 / 10 (High)**  
**Cost Multiplier: 1.4×**

| Factor | Impact |
|--------|--------|
| Legacy COBOL language | High — scarce talent, limited tooling |
| IBM AIX proprietary OS | High — no cloud/container support |
| 1-Tier monolithic architecture | High — tight coupling, hard to decompose |
| Oracle 1TB database + license | Medium — data migration risk, license cost |
| No CI/CD pipeline | Medium — deployment automation needed |
| High criticality / Finance | Medium — testing, compliance overhead |

## Scenario Applicability

```mermaid
pie title Modernization Scenarios
    "Applicable" : 6
    "Partially Fulfilled" : 1
    "Blocked" : 1
    "Not Applicable" : 2
```

| Scenario | Status | Priority | Effort |
|----------|--------|----------|--------|
| Operating System Update | ✅ APPLICABLE | High | Low |
| Switch to Standard Linux OS | ✅ APPLICABLE | Medium | Medium |
| Switch to ARM CPU | ⚪ NOT_APPLICABLE | Medium | Medium |
| Application Server Replacement | ⚪ NOT_APPLICABLE | Medium | Medium |
| Cloud Migration (Lift & Shift) | 🔶 PARTIALLY_FULFILLED | High | Low |
| Application Containerization | 🚫 BLOCKED | High | High |
| Application Refactoring & De-coupling | ✅ APPLICABLE | High | High |
| Upgrade Legacy Databases | ✅ APPLICABLE | High | Medium |
| Switch DB to Open-Source | ✅ APPLICABLE | High | Medium |
| Update Outdated Components | ✅ APPLICABLE | High | High |

### Key Scenario Details

**Operating System Update** — AIX 7.2 standard support ended April 2023. Immediate action required to address the EOL operating system risk.

**Switch to Standard Linux OS** — IBM AIX imposes licensing, operational, and cloud portability constraints. Migration to standard Linux is a foundational prerequisite for most other modernization scenarios.

**Cloud Migration (Lift & Shift)** — Partially applicable via IBM Power Virtual Server. Standard hyperscaler cloud not available for AIX workloads.

**Application Containerization** — Blocked until OS and language modernization is completed.

**Application Refactoring & De-coupling** — The 1-Tier monolith is a key modernization target. Even in maintenance mode, decomposing the application into services would enable lower-cost, lower-risk incremental changes.

**Upgrade Legacy Databases / Switch to Open-Source** — Oracle 19c license costs and extended support fees represent actionable savings. These scenarios can be pursued independently of the OS modernization.

**Update Outdated Components** — COBOL maintenance risk is high. With decommission target 2027, a comprehensive COBOL modernization effort should be initiated now.

## Business Case (3-Year Horizon)

| Scenario | Migration Cost | Annual Savings | 3-Yr Net |
|----------|---------------|----------------|----------|
| OS Update | $1,400 | $500 | $100 |
| Switch to Linux OS | $420 | $400 | $780 |
| Cloud Migration | $7,000 | $3,000 | $2,000 |
| App Refactoring | $350,000 | $150,000 | $100,000 |
| DB Upgrade | $14,000 | $10,000 | $16,000 |
| Switch to Open-Source DB | $35,000 | $15,000 | $10,000 |
| **Total** | **$407,820** | **$178,900/yr** | **$128,880** |

> Costs adjusted with complexity multiplier 1.4×.

## Modernization Roadmap

```mermaid
gantt
    title Modernization Roadmap — COBOL maintain
    dateFormat YYYY-MM
    section Quick Wins (0-6 months)
    OS Security Patch / Planning    :2026-07, 2026-09
    Switch to Linux OS (Planning)   :2026-07, 2026-10
    section Medium-Term (6-18 months)
    DB Upgrade (Oracle 19c → 21c)   :2026-10, 2027-04
    Switch DB to PostgreSQL         :2027-01, 2027-07
    Cloud Migration (IBM Power VS)  :2027-01, 2027-06
    section Long-Term (18-36 months)
    COBOL Component Modernization   :2027-06, 2028-06
    App Refactoring & De-coupling   :2027-09, 2028-12
```

### Recommended Priority Order

1. **Immediate:** OS security patch evaluation; plan AIX extended support or Linux migration
2. **Short-term:** Linux OS migration to remove AIX dependency
3. **Medium-term:** Oracle DB upgrade or PostgreSQL migration
4. **Medium-term:** Cloud migration via IBM Power Virtual Server
5. **Long-term:** COBOL modernization (given 2027 decommission target, fast-track this)

