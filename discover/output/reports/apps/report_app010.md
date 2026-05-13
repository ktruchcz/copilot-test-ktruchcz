# PayrollApp-010 (app010)

**Status:** Production | **Criticality:** Medium | **Solution Type:** 3rd party software

## Overview

| Field | Value |
|-------|-------|
| Description | Payroll processing system handling salary calculations, tax deductions, and compensation reporting |
| Business Unit | HR |
| Operating System | Windows Server 2019 |
| Programming Language | Ruby 2.7 |
| Database | MySQL 8.0 |
| Architecture | unknown |
| Containerized | No |
| CI/CD Present | Yes |
| Environments | 1 |
| Server Instances | sv13 |
| External Interfaces | 4 |
| Users | 315 |

## Technology Assessment

**Overall Status:** 🔴 EOL

| Component | Name | Status |
|-----------|------|--------|
| operating_system | Windows Server 2019 | ✅ CURRENT_VERSION |
| programming_language | Ruby 2.7 | 🔴 EOL |
| database | MySQL 8.0 | ✅ CURRENT_VERSION |
| application_server | Microsoft IIS 10.0 | ❓ NO_KNOWLEDGE |

## Complexity Assessment

**Score:** 5/10 — **Classification:** MEDIUM

| Factor | Score |
|--------|-------|
| Technology Age Eol | 2.5 |
| Integration Complexity | 0.4 |
| Infrastructure Scale | 0.45 |
| Business Criticality | 0.6 |
| Code And Architecture | 0.75 |
| Data Complexity | 0.5 |

## Scenario Analysis

| Scenario | Status | Reasoning |
|----------|--------|-----------|
| OS Update / Security Patch | NOT_APPLICABLE | OS Windows Server 2019 is current; no immediate patch needed. |
| Switch to Standard Linux OS | PARTIALLY_FULFILLED | Running on Windows Server 2019; switch to Linux may require vendor support confirmation for 3rd party software. |
| Switch to ARM CPU | BLOCKED | 3rd party software; ARM support depends on vendor roadmap. |
| Application Server Replacement | APPLICABLE | Uses application server Microsoft IIS 10.0; replacement/upgrade may be beneficial. |
| Cloud Migration (Lift & Shift) | APPLICABLE | 3rd party software; cloud-hosted or SaaS version likely available. |
| Containerization | BLOCKED | 3rd party software; containerization depends on vendor support. |
| Refactoring & Decoupling | BLOCKED | 3rd party software; source code refactoring is not feasible. |
| Upgrade Legacy Databases | NOT_APPLICABLE | Database MySQL 8.0 is current; no immediate upgrade needed. |
| Switch to Open Source DB | NOT_APPLICABLE | Already using open source or managed database (MySQL 8.0). |
| Update Outdated Components | PARTIALLY_FULFILLED | 3rd party software with outdated components; updates depend on vendor release schedule. |

## Business Case

**Total Implementation Cost:** $15,085.18
**Total Annual Savings:** $13,500.00
**3-Year ROI:** 168.5%

| Scenario | Impl. Cost | Annual Savings | 3-Yr ROI | Payback (mo) |
|----------|------------|----------------|----------|--------------|
| Application Server Replacement | $10,056.79 | $10,800.00 | 222.2% | 11.2 |
| Cloud Migration (Lift & Shift) | $5,028.39 | $2,700.00 | 61.1% | 22.3 |
