# Application Report: AuditApp-024

**ID:** app024  
**Generated:** 2026-05-11

## Overview

| Attribute | Value |
|-----------|-------|
| Business Unit | Finance |
| Solution Type | Custom made |
| Deployment Type | On-Premise |
| Business Criticality | High |
| Users | 95 |
| Servers | 1 |
| Architecture | 2-Tier |
| Containerized | No |
| CI/CD | No |
| Data Classification | Confidential |

## Technology Stack

| Component | Technology | Status |
|-----------|-----------|--------|
| Os | Windows Server 2019 | 🟢 CURRENT_VERSION |
| Database | SQL Server 2014 | 🔴 EOL |
| Language | VB.NET | 🔴 EOL |
| Application Server | Microsoft IIS 10.0 | 🟢 CURRENT_VERSION |

```mermaid
pie title Technology Health
    "Current" : 2
    "End of Life" : 2
```

## Complexity Assessment

**Score:** 7/10 — **HIGH**  
**Confidence:** 7

> Score 7/10 (HIGH): 2 EOL component(s), 0 outdated, 3 external interfaces, 1 server(s), criticality=High, architecture=2-Tier.

| Factor | Value |
|--------|-------|
| Servers | 1 |
| Interfaces | 3 |
| Environments | 2 |
| EOL Technologies | 2 |
| Outdated Technologies | 0 |
| CI/CD Present | No |
| Containerized | No |

## Modernization Scenarios

### Applicable Scenarios

#### ✅ Switch to ARM-based CPU

- **Priority:** Medium
- **Effort:** Medium
- **Effects:** cost, sustainability
- **Cost:** €6,650 (one-time)
- **Annual Savings:** €1,000/year
- **Reasoning:** Application on on-premise x86 infrastructure could benefit from ARM migration for cost savings.

#### ✅ Application Migration to Cloud Infrastructure (Lift & Shift)

- **Priority:** High
- **Effort:** Low
- **Effects:** security, agility
- **Cost:** €6,650 (one-time)
- **Annual Savings:** €2,400/year
- **Reasoning:** Application runs on-premise and is a candidate for cloud migration.

#### ✅ Application Containerization

- **Priority:** High
- **Effort:** High
- **Effects:** agility, cost, sustainability
- **Cost:** €133,001 (one-time)
- **Annual Savings:** €80,000/year
- **Reasoning:** Application is not containerized; containerization is applicable for improved portability and scalability.

#### ✅ Application Refactoring and De-coupling

- **Priority:** High
- **Effort:** High
- **Effects:** agility, cost, sustainability
- **Cost:** €332,502 (one-time)
- **Annual Savings:** €120,000/year
- **Reasoning:** Application has 2-Tier architecture - refactoring to microservices would improve scalability.

#### ✅ Upgrade Legacy Databases

- **Priority:** High
- **Effort:** Medium
- **Effects:** security, agility
- **Cost:** €13,300 (one-time)
- **Annual Savings:** €10,000/year
- **Reasoning:** Database (SQL Server 2014) is EOL and requires upgrade.

#### ✅ Switch DB Engine to open-source database solution

- **Priority:** High
- **Effort:** Medium
- **Effects:** cost
- **Reasoning:** Application uses commercial database (SQL Server 2014) with license cost; migration to open-source is recommended.

#### ✅ Update outdated components

- **Priority:** High
- **Effort:** High
- **Effects:** security, agility, cost
- **Reasoning:** EOL components found: SQL Server 2014, VB.NET. Update required.

### Other Scenarios

| Scenario | Status | Reason |
|----------|--------|--------|
| Operating System Update | ✔️ FULFILLED | Operating system is on a current, supported version. |
| Switch to standard Linux Operating System | ❌ NOT_APPLICABLE | Application runs on Windows or is SaaS; switching to standard Linux OS is not applicable. |
| Applications Server replacement | ✔️ FULFILLED | Application server appears to be on a supported version. |

## Financial Summary

| Metric | Value |
|--------|-------|
| Total One-Time Cost | €492,103 |
| Total Yearly Savings | €213,400 |
| Break-Even | 2.3 years |
