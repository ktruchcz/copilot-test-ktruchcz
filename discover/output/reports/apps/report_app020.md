# TrainingApp-020 (app020)

**Status:** Production | **Criticality:** Low | **Solution Type:** 3rd party software

## Overview

| Field | Value |
|-------|-------|
| Description | Learning management system for employee training programs and professional development tracking |
| Business Unit | HR |
| Operating System | Windows Server 2012 |
| Programming Language | Angular 15 |
| Database | SQL Server 2016 |
| Architecture | 2-Tier |
| Containerized | No |
| CI/CD Present | Yes |
| Environments | 3 |
| Server Instances | sv29 |
| External Interfaces | 7 |
| Users | 750 |

## Technology Assessment

**Overall Status:** 🔴 EOL

| Component | Name | Status |
|-----------|------|--------|
| operating_system | Windows Server 2012 | 🔴 EOL |
| programming_language | Angular 15 | ⚠️ OUTDATED |
| database | SQL Server 2016 | ⚠️ OUTDATED |
| application_server | Microsoft IIS 8.5 | ❓ NO_KNOWLEDGE |

## Complexity Assessment

**Score:** 6/10 — **Classification:** MEDIUM

| Factor | Score |
|--------|-------|
| Technology Age Eol | 2.5 |
| Integration Complexity | 0.8 |
| Infrastructure Scale | 0.75 |
| Business Criticality | 0.3 |
| Code And Architecture | 0.75 |
| Data Complexity | 0.5 |

## Scenario Analysis

| Scenario | Status | Reasoning |
|----------|--------|-----------|
| OS Update / Security Patch | APPLICABLE | OS Windows Server 2012 is EOL; security patch update is needed. |
| Switch to Standard Linux OS | PARTIALLY_FULFILLED | Running on Windows Server 2012; switch to Linux may require vendor support confirmation for 3rd party software. |
| Switch to ARM CPU | BLOCKED | 3rd party software; ARM support depends on vendor roadmap. |
| Application Server Replacement | APPLICABLE | Uses application server Microsoft IIS 8.5; replacement/upgrade may be beneficial. |
| Cloud Migration (Lift & Shift) | APPLICABLE | 3rd party software; cloud-hosted or SaaS version likely available. |
| Containerization | BLOCKED | 3rd party software; containerization depends on vendor support. |
| Refactoring & Decoupling | BLOCKED | 3rd party software; source code refactoring is not feasible. |
| Upgrade Legacy Databases | APPLICABLE | Database SQL Server 2016 is outdated; upgrade recommended. |
| Switch to Open Source DB | PARTIALLY_FULFILLED | 3rd party software using proprietary database SQL Server 2016; switch feasibility depends on vendor. |
| Update Outdated Components | PARTIALLY_FULFILLED | 3rd party software with outdated components; updates depend on vendor release schedule. |

## Business Case

**Total Implementation Cost:** $30,069.78
**Total Annual Savings:** $25,500.00
**3-Year ROI:** 154.4%

| Scenario | Impl. Cost | Annual Savings | 3-Yr ROI | Payback (mo) |
|----------|------------|----------------|----------|--------------|
| OS Update / Security Patch | $1,156.53 | $500.00 | 29.7% | 27.8 |
| Application Server Replacement | $11,565.30 | $12,000.00 | 211.3% | 11.6 |
| Cloud Migration (Lift & Shift) | $5,782.65 | $3,000.00 | 55.6% | 23.1 |
| Upgrade Legacy Databases | $11,565.30 | $10,000.00 | 159.4% | 13.9 |
