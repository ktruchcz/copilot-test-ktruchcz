# LegacyFinApp-026 (app026)

**Status:** Production | **Criticality:** Critical | **Solution Type:** Custom made

## Overview

| Field | Value |
|-------|-------|
| Description | Legacy financial modeling system for complex calculations and risk assessments |
| Business Unit | Finance |
| Operating System | AIX 7.2 |
| Programming Language | FORTRAN 2018 |
| Database | DB2 |
| Architecture | 1-Tier |
| Containerized | No |
| CI/CD Present | No |
| Environments | 2 |
| Server Instances | sv38 |
| External Interfaces | 1 |
| Users | 150 |

## Technology Assessment

**Overall Status:** ⚠️ OUTDATED

| Component | Name | Status |
|-----------|------|--------|
| operating_system | AIX 7.2 | ⚠️ OUTDATED |
| programming_language | FORTRAN 2018 | ⚠️ OUTDATED |
| database | DB2 | ⚠️ OUTDATED |

## Complexity Assessment

**Score:** 6/10 — **Classification:** MEDIUM

| Factor | Score |
|--------|-------|
| Technology Age Eol | 1.5 |
| Integration Complexity | 0.4 |
| Infrastructure Scale | 0.6 |
| Business Criticality | 1.5 |
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
| Containerization | PARTIALLY_FULFILLED | Legacy architecture/language (FORTRAN 2018); containerization is complex but possible with effort. |
| Refactoring & Decoupling | APPLICABLE | Monolithic/legacy architecture with FORTRAN 2018; refactoring and decoupling recommended. |
| Upgrade Legacy Databases | APPLICABLE | Database DB2 is outdated; upgrade recommended. |
| Switch to Open Source DB | APPLICABLE | Uses proprietary database DB2; switching to PostgreSQL/MySQL would reduce licensing costs. |
| Update Outdated Components | APPLICABLE | Multiple outdated components detected (OS: OUTDATED, Lang: OUTDATED, DB: OUTDATED). |

## Business Case

**Total Implementation Cost:** $342,679.95
**Total Annual Savings:** $143,920.00
**3-Year ROI:** 26.0%

| Scenario | Impl. Cost | Annual Savings | 3-Yr ROI | Payback (mo) |
|----------|------------|----------------|----------|--------------|
| OS Update / Security Patch | $1,156.53 | $400.00 | 3.8% | 34.7 |
| Switch to Standard Linux OS | $346.96 | $320.00 | 176.7% | 13.0 |
| Switch to ARM CPU | $5,782.65 | $800.00 | -58.5% | 86.7 |
| Cloud Migration (Lift & Shift) | $5,782.65 | $2,400.00 | 24.5% | 28.9 |
| Refactoring & Decoupling | $289,132.60 | $120,000.00 | 24.5% | 28.9 |
| Upgrade Legacy Databases | $11,565.30 | $8,000.00 | 107.5% | 17.3 |
| Switch to Open Source DB | $28,913.26 | $12,000.00 | 24.5% | 28.9 |
