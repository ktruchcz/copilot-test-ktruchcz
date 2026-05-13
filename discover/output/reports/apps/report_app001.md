# ERPApp-001 (app001)

**Status:** Production | **Criticality:** High | **Solution Type:** Custom made

## Overview

| Field | Value |
|-------|-------|
| Description | Core ERP system handling financial transactions, general ledger, and regulatory reporting |
| Business Unit | Finance |
| Operating System | AIX 7.2 |
| Programming Language | COBOL-2014 |
| Database | Oracle 19c |
| Architecture | 1-Tier |
| Containerized | No |
| CI/CD Present | No |
| Environments | 2 |
| Server Instances | sv01, sv02 |
| External Interfaces | 5 |
| Users | 350 |

## Technology Assessment

**Overall Status:** ⚠️ OUTDATED

| Component | Name | Status |
|-----------|------|--------|
| operating_system | AIX 7.2 | ⚠️ OUTDATED |
| programming_language | COBOL-2014 | ⚠️ OUTDATED |
| database | Oracle 19c | ✅ CURRENT_VERSION |

## Complexity Assessment

**Score:** 6/10 — **Classification:** MEDIUM

| Factor | Score |
|--------|-------|
| Technology Age Eol | 1.5 |
| Integration Complexity | 0.8 |
| Infrastructure Scale | 0.9 |
| Business Criticality | 1.05 |
| Code And Architecture | 1.35 |
| Data Complexity | 0.7 |

## Scenario Analysis

| Scenario | Status | Reasoning |
|----------|--------|-----------|
| OS Update / Security Patch | APPLICABLE | OS AIX 7.2 is outdated; update recommended. |
| Switch to Standard Linux OS | APPLICABLE | Running on AIX 7.2 (UNIX); migrating to standard Linux would modernize infrastructure. |
| Switch to ARM CPU | APPLICABLE | ARM CPU migration is possible with recompilation/containerization effort. |
| Application Server Replacement | NOT_APPLICABLE | No dedicated application server identified; scenario not applicable. |
| Cloud Migration (Lift & Shift) | APPLICABLE | Application can be migrated to cloud (lift & shift). |
| Containerization | PARTIALLY_FULFILLED | Legacy architecture/language (COBOL-2014); containerization is complex but possible with effort. |
| Refactoring & Decoupling | APPLICABLE | Monolithic/legacy architecture with COBOL-2014; refactoring and decoupling recommended. |
| Upgrade Legacy Databases | NOT_APPLICABLE | Database Oracle 19c is current; no immediate upgrade needed. |
| Switch to Open Source DB | APPLICABLE | Uses proprietary database Oracle 19c; switching to PostgreSQL/MySQL would reduce licensing costs. |
| Update Outdated Components | APPLICABLE | Multiple outdated components detected (OS: OUTDATED, Lang: OUTDATED, DB: CURRENT_VERSION). |

## Business Case

**Total Implementation Cost:** $331,114.65
**Total Annual Savings:** $135,920.00
**3-Year ROI:** 23.1%

| Scenario | Impl. Cost | Annual Savings | 3-Yr ROI | Payback (mo) |
|----------|------------|----------------|----------|--------------|
| OS Update / Security Patch | $1,156.53 | $400.00 | 3.8% | 34.7 |
| Switch to Standard Linux OS | $346.96 | $320.00 | 176.7% | 13.0 |
| Switch to ARM CPU | $5,782.65 | $800.00 | -58.5% | 86.7 |
| Cloud Migration (Lift & Shift) | $5,782.65 | $2,400.00 | 24.5% | 28.9 |
| Refactoring & Decoupling | $289,132.60 | $120,000.00 | 24.5% | 28.9 |
| Switch to Open Source DB | $28,913.26 | $12,000.00 | 24.5% | 28.9 |
