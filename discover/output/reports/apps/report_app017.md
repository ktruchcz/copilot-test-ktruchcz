# BackupApp-017 (app017)

**Status:** Production | **Criticality:** High | **Solution Type:** 3rd party software

## Overview

| Field | Value |
|-------|-------|
| Description | Automated backup and disaster recovery system for critical business applications and data |
| Business Unit | IT |
| Operating System | RHEL 7 |
| Programming Language | PowerShell |
| Database | Oracle 12c |
| Architecture | unknown |
| Containerized | No |
| CI/CD Present | No |
| Environments | 5 |
| Server Instances | sv24, sv25 |
| External Interfaces | 8 |
| Users | 45 |

## Technology Assessment

**Overall Status:** 🔴 EOL

| Component | Name | Status |
|-----------|------|--------|
| operating_system | RHEL 7 | 🔴 EOL |
| programming_language | PowerShell | ✅ CURRENT_VERSION |
| database | Oracle 12c | 🔴 EOL |
| application_server | Payara 5.0 | ❓ NO_KNOWLEDGE |

## Complexity Assessment

**Score:** 7/10 — **Classification:** HIGH

| Factor | Score |
|--------|-------|
| Technology Age Eol | 2.5 |
| Integration Complexity | 0.8 |
| Infrastructure Scale | 1.35 |
| Business Criticality | 1.05 |
| Code And Architecture | 0.9 |
| Data Complexity | 0.5 |

## Scenario Analysis

| Scenario | Status | Reasoning |
|----------|--------|-----------|
| OS Update / Security Patch | APPLICABLE | OS RHEL 7 is EOL; security patch update is needed. |
| Switch to Standard Linux OS | FULFILLED | Already running on standard Linux (RHEL 7). |
| Switch to ARM CPU | BLOCKED | 3rd party software; ARM support depends on vendor roadmap. |
| Application Server Replacement | APPLICABLE | Uses application server Payara 5.0; replacement/upgrade may be beneficial. |
| Cloud Migration (Lift & Shift) | APPLICABLE | 3rd party software; cloud-hosted or SaaS version likely available. |
| Containerization | BLOCKED | 3rd party software; containerization depends on vendor support. |
| Refactoring & Decoupling | BLOCKED | 3rd party software; source code refactoring is not feasible. |
| Upgrade Legacy Databases | APPLICABLE | Database Oracle 12c is EOL; upgrade is critical for security. |
| Switch to Open Source DB | PARTIALLY_FULFILLED | 3rd party software using proprietary database Oracle 12c; switch feasibility depends on vendor. |
| Update Outdated Components | PARTIALLY_FULFILLED | 3rd party software with outdated components; updates depend on vendor release schedule. |

## Business Case

**Total Implementation Cost:** $34,580.26
**Total Annual Savings:** $20,400.00
**3-Year ROI:** 77.0%

| Scenario | Impl. Cost | Annual Savings | 3-Yr ROI | Payback (mo) |
|----------|------------|----------------|----------|--------------|
| OS Update / Security Patch | $1,330.01 | $400.00 | -9.8% | 39.9 |
| Application Server Replacement | $13,300.10 | $9,600.00 | 116.5% | 16.6 |
| Cloud Migration (Lift & Shift) | $6,650.05 | $2,400.00 | 8.3% | 33.3 |
| Upgrade Legacy Databases | $13,300.10 | $8,000.00 | 80.4% | 20.0 |
