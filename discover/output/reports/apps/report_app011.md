# RouteOptApp-011 (app011)

**Status:** Production | **Criticality:** Medium | **Solution Type:** Custom made

## Overview

| Field | Value |
|-------|-------|
| Description | Advanced route optimization system using machine learning algorithms for delivery planning |
| Business Unit | R&D |
| Operating System | CentOS 7 |
| Programming Language | Python 3.11 |
| Database | PostgreSQL 14 |
| Architecture | 3-Tier |
| Containerized | Yes |
| CI/CD Present | Yes |
| Environments | 1 |
| Server Instances | sv14 |
| External Interfaces | 5 |
| Users | 125 |

## Technology Assessment

**Overall Status:** 🔴 EOL

| Component | Name | Status |
|-----------|------|--------|
| operating_system | CentOS 7 | 🔴 EOL |
| programming_language | Python 3.11 | ✅ CURRENT_VERSION |
| database | PostgreSQL 14 | ✅ CURRENT_VERSION |
| application_server | Glassfish 4.0 | ❓ NO_KNOWLEDGE |

## Complexity Assessment

**Score:** 5/10 — **Classification:** MEDIUM

| Factor | Score |
|--------|-------|
| Technology Age Eol | 2.5 |
| Integration Complexity | 0.8 |
| Infrastructure Scale | 0.45 |
| Business Criticality | 0.6 |
| Code And Architecture | 0.15 |
| Data Complexity | 0.5 |

## Scenario Analysis

| Scenario | Status | Reasoning |
|----------|--------|-----------|
| OS Update / Security Patch | APPLICABLE | OS CentOS 7 is EOL; security patch update is needed. |
| Switch to Standard Linux OS | FULFILLED | Already running on standard Linux (CentOS 7). |
| Switch to ARM CPU | APPLICABLE | Application is containerized; ARM CPU adoption is feasible with image rebuilds. |
| Application Server Replacement | APPLICABLE | Uses application server Glassfish 4.0; replacement/upgrade may be beneficial. |
| Cloud Migration (Lift & Shift) | APPLICABLE | Application can be migrated to cloud (lift & shift). |
| Containerization | FULFILLED | Application is already containerized. |
| Refactoring & Decoupling | PARTIALLY_FULFILLED | Already uses multi-tier architecture; further decomposition may be beneficial. |
| Upgrade Legacy Databases | NOT_APPLICABLE | Database PostgreSQL 14 is current; no immediate upgrade needed. |
| Switch to Open Source DB | NOT_APPLICABLE | Already using open source or managed database (PostgreSQL 14). |
| Update Outdated Components | APPLICABLE | Multiple outdated components detected (OS: EOL, Lang: CURRENT_VERSION, DB: CURRENT_VERSION). |

## Business Case

**Total Implementation Cost:** $21,119.25
**Total Annual Savings:** $14,850.00
**3-Year ROI:** 110.9%

| Scenario | Impl. Cost | Annual Savings | 3-Yr ROI | Payback (mo) |
|----------|------------|----------------|----------|--------------|
| OS Update / Security Patch | $1,005.68 | $450.00 | 34.2% | 26.8 |
| Switch to ARM CPU | $5,028.39 | $900.00 | -46.3% | 67.0 |
| Application Server Replacement | $10,056.79 | $10,800.00 | 222.2% | 11.2 |
| Cloud Migration (Lift & Shift) | $5,028.39 | $2,700.00 | 61.1% | 22.3 |
