# ReportingApp-015 (app015)

**Status:** Production | **Criticality:** Low | **Solution Type:** Custom made

## Overview

| Field | Value |
|-------|-------|
| Description | Financial reporting tool for generating executive dashboards and regulatory compliance reports |
| Business Unit | Finance |
| Operating System | Windows Server 2019 |
| Programming Language | PHP 8.1 |
| Database | MongoDB |
| Architecture | 2-Tier |
| Containerized | No |
| CI/CD Present | Yes |
| Environments | 4 |
| Server Instances | sv21 |
| External Interfaces | 4 |
| Users | 340 |

## Technology Assessment

**Overall Status:** ❓ NO_KNOWLEDGE

| Component | Name | Status |
|-----------|------|--------|
| operating_system | Windows Server 2019 | ✅ CURRENT_VERSION |
| programming_language | PHP 8.1 | ✅ CURRENT_VERSION |
| database | MongoDB | ✅ CURRENT_VERSION |
| application_server | Microsoft IIS 10.0 | ❓ NO_KNOWLEDGE |

## Complexity Assessment

**Score:** 3/10 — **Classification:** LOW

| Factor | Score |
|--------|-------|
| Technology Age Eol | 0.5 |
| Integration Complexity | 0.4 |
| Infrastructure Scale | 0.9 |
| Business Criticality | 0.3 |
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
| Upgrade Legacy Databases | NOT_APPLICABLE | Database MongoDB is current; no immediate upgrade needed. |
| Switch to Open Source DB | NOT_APPLICABLE | Already using open source or managed database (MongoDB). |
| Update Outdated Components | NOT_APPLICABLE | All components are current; no immediate updates needed. |

## Business Case

**Total Implementation Cost:** $281,590.00
**Total Annual Savings:** $266,400.00
**3-Year ROI:** 183.8%

| Scenario | Impl. Cost | Annual Savings | 3-Yr ROI | Payback (mo) |
|----------|------------|----------------|----------|--------------|
| Switch to Standard Linux OS | $228.13 | $400.00 | 426.0% | 6.8 |
| Switch to ARM CPU | $3,802.19 | $1,000.00 | -21.1% | 45.6 |
| Application Server Replacement | $7,604.37 | $12,000.00 | 373.4% | 7.6 |
| Cloud Migration (Lift & Shift) | $3,802.19 | $3,000.00 | 136.7% | 15.2 |
| Containerization | $76,043.75 | $100,000.00 | 294.5% | 9.1 |
| Refactoring & Decoupling | $190,109.37 | $150,000.00 | 136.7% | 15.2 |
