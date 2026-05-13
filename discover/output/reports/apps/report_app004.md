# HRApp-004 (app004)

**Status:** Production | **Criticality:** High | **Solution Type:** Custom made

## Overview

| Field | Value |
|-------|-------|
| Description | Human resources management system handling employee records, benefits, and HR workflows |
| Business Unit | HR |
| Operating System | Windows Server 2012 |
| Programming Language | .NET Core |
| Database | SQL Server 2019 |
| Architecture | 2-Tier |
| Containerized | Yes |
| CI/CD Present | Yes |
| Environments | 2 |
| Server Instances | sv06, sv02 |
| External Interfaces | 6 |
| Users | 670 |

## Technology Assessment

**Overall Status:** 🔴 EOL

| Component | Name | Status |
|-----------|------|--------|
| operating_system | Windows Server 2012 | 🔴 EOL |
| programming_language | .NET Core | ⚠️ OUTDATED |
| database | SQL Server 2019 | ✅ CURRENT_VERSION |
| application_server | Microsoft IIS 8.0 | ❓ NO_KNOWLEDGE |

## Complexity Assessment

**Score:** 6/10 — **Classification:** MEDIUM

| Factor | Score |
|--------|-------|
| Technology Age Eol | 2.5 |
| Integration Complexity | 0.8 |
| Infrastructure Scale | 0.9 |
| Business Criticality | 1.05 |
| Code And Architecture | 0.45 |
| Data Complexity | 0.5 |

## Scenario Analysis

| Scenario | Status | Reasoning |
|----------|--------|-----------|
| OS Update / Security Patch | APPLICABLE | OS Windows Server 2012 is EOL; security patch update is needed. |
| Switch to Standard Linux OS | APPLICABLE | Running on Windows Server 2012; migrating to standard Linux would reduce licensing costs. |
| Switch to ARM CPU | APPLICABLE | Application is containerized; ARM CPU adoption is feasible with image rebuilds. |
| Application Server Replacement | APPLICABLE | Uses application server Microsoft IIS 8.0; replacement/upgrade may be beneficial. |
| Cloud Migration (Lift & Shift) | APPLICABLE | Application can be migrated to cloud (lift & shift). |
| Containerization | FULFILLED | Application is already containerized. |
| Refactoring & Decoupling | APPLICABLE | Refactoring would improve maintainability and reduce technical debt. |
| Upgrade Legacy Databases | NOT_APPLICABLE | Database SQL Server 2019 is current; no immediate upgrade needed. |
| Switch to Open Source DB | APPLICABLE | Uses proprietary database SQL Server 2019; switching to PostgreSQL/MySQL would reduce licensing costs. |
| Update Outdated Components | APPLICABLE | Multiple outdated components detected (OS: EOL, Lang: OUTDATED, DB: CURRENT_VERSION). |

## Business Case

**Total Implementation Cost:** $342,679.95
**Total Annual Savings:** $145,520.00
**3-Year ROI:** 27.4%

| Scenario | Impl. Cost | Annual Savings | 3-Yr ROI | Payback (mo) |
|----------|------------|----------------|----------|--------------|
| OS Update / Security Patch | $1,156.53 | $400.00 | 3.8% | 34.7 |
| Switch to Standard Linux OS | $346.96 | $320.00 | 176.7% | 13.0 |
| Switch to ARM CPU | $5,782.65 | $800.00 | -58.5% | 86.7 |
| Application Server Replacement | $11,565.30 | $9,600.00 | 149.0% | 14.5 |
| Cloud Migration (Lift & Shift) | $5,782.65 | $2,400.00 | 24.5% | 28.9 |
| Refactoring & Decoupling | $289,132.60 | $120,000.00 | 24.5% | 28.9 |
| Switch to Open Source DB | $28,913.26 | $12,000.00 | 24.5% | 28.9 |
