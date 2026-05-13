# AnalyticsApp-003 (app003)

**Status:** Production | **Criticality:** Low | **Solution Type:** Open Source

## Overview

| Field | Value |
|-------|-------|
| Description | Analytics platform for generating operational reports and business insights from logistics data |
| Business Unit | IT |
| Operating System | RHEL 7 |
| Programming Language | Python 3.9 |
| Database | PostgreSQL 13 |
| Architecture | 3-Tier |
| Containerized | Yes |
| CI/CD Present | Yes |
| Environments | 1 |
| Server Instances | sv03 |
| External Interfaces | 3 |
| Users | 480 |

## Technology Assessment

**Overall Status:** 🔴 EOL

| Component | Name | Status |
|-----------|------|--------|
| operating_system | RHEL 7 | 🔴 EOL |
| programming_language | Python 3.9 | ⚠️ OUTDATED |
| database | PostgreSQL 13 | ⚠️ OUTDATED |
| application_server | Apache Tomcat 6.1 | ❓ NO_KNOWLEDGE |

## Complexity Assessment

**Score:** 4/10 — **Classification:** MEDIUM

| Factor | Score |
|--------|-------|
| Technology Age Eol | 2.5 |
| Integration Complexity | 0.4 |
| Infrastructure Scale | 0.45 |
| Business Criticality | 0.3 |
| Code And Architecture | 0.15 |
| Data Complexity | 0.5 |

## Scenario Analysis

| Scenario | Status | Reasoning |
|----------|--------|-----------|
| OS Update / Security Patch | APPLICABLE | OS RHEL 7 is EOL; security patch update is needed. |
| Switch to Standard Linux OS | FULFILLED | Already running on standard Linux (RHEL 7). |
| Switch to ARM CPU | APPLICABLE | Application is containerized; ARM CPU adoption is feasible with image rebuilds. |
| Application Server Replacement | APPLICABLE | Uses application server Apache Tomcat 6.1; replacement/upgrade may be beneficial. |
| Cloud Migration (Lift & Shift) | APPLICABLE | Application can be migrated to cloud (lift & shift). |
| Containerization | FULFILLED | Application is already containerized. |
| Refactoring & Decoupling | PARTIALLY_FULFILLED | Already uses multi-tier architecture; further decomposition may be beneficial. |
| Upgrade Legacy Databases | APPLICABLE | Database PostgreSQL 13 is outdated; upgrade recommended. |
| Switch to Open Source DB | NOT_APPLICABLE | Already using open source or managed database (PostgreSQL 13). |
| Update Outdated Components | APPLICABLE | Multiple outdated components detected (OS: EOL, Lang: OUTDATED, DB: OUTDATED). |

## Business Case

**Total Implementation Cost:** $27,109.60
**Total Annual Savings:** $26,500.00
**3-Year ROI:** 193.3%

| Scenario | Impl. Cost | Annual Savings | 3-Yr ROI | Payback (mo) |
|----------|------------|----------------|----------|--------------|
| OS Update / Security Patch | $874.50 | $500.00 | 71.5% | 21.0 |
| Switch to ARM CPU | $4,372.52 | $1,000.00 | -31.4% | 52.5 |
| Application Server Replacement | $8,745.03 | $12,000.00 | 311.7% | 8.7 |
| Cloud Migration (Lift & Shift) | $4,372.52 | $3,000.00 | 105.8% | 17.5 |
| Upgrade Legacy Databases | $8,745.03 | $10,000.00 | 243.1% | 10.5 |
