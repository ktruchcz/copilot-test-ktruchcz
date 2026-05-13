# MobileApp-016 (app016)

**Status:** Production | **Criticality:** Medium | **Solution Type:** Custom made

## Overview

| Field | Value |
|-------|-------|
| Description | Mobile application for drivers and customers to track shipments and manage delivery operations |
| Business Unit | Operations |
| Operating System | RHEL 7 |
| Programming Language | React Native |
| Database | SQL Server 2019 |
| Architecture | 3-Tier |
| Containerized | Yes |
| CI/CD Present | Yes |
| Environments | 3 |
| Server Instances | sv22, sv23 |
| External Interfaces | 10 |
| Users | 1580 |

## Technology Assessment

**Overall Status:** 🔴 EOL

| Component | Name | Status |
|-----------|------|--------|
| operating_system | RHEL 7 | 🔴 EOL |
| programming_language | React Native | ✅ CURRENT_VERSION |
| database | SQL Server 2019 | ✅ CURRENT_VERSION |
| application_server | Payara 4.0 | ❓ NO_KNOWLEDGE |

## Complexity Assessment

**Score:** 6/10 — **Classification:** MEDIUM

| Factor | Score |
|--------|-------|
| Technology Age Eol | 2.5 |
| Integration Complexity | 1.4 |
| Infrastructure Scale | 1.05 |
| Business Criticality | 0.6 |
| Code And Architecture | 0.15 |
| Data Complexity | 0.7 |

## Scenario Analysis

| Scenario | Status | Reasoning |
|----------|--------|-----------|
| OS Update / Security Patch | APPLICABLE | OS RHEL 7 is EOL; security patch update is needed. |
| Switch to Standard Linux OS | FULFILLED | Already running on standard Linux (RHEL 7). |
| Switch to ARM CPU | APPLICABLE | Application is containerized; ARM CPU adoption is feasible with image rebuilds. |
| Application Server Replacement | APPLICABLE | Uses application server Payara 4.0; replacement/upgrade may be beneficial. |
| Cloud Migration (Lift & Shift) | APPLICABLE | Application can be migrated to cloud (lift & shift). |
| Containerization | FULFILLED | Application is already containerized. |
| Refactoring & Decoupling | PARTIALLY_FULFILLED | Already uses multi-tier architecture; further decomposition may be beneficial. |
| Upgrade Legacy Databases | NOT_APPLICABLE | Database SQL Server 2019 is current; no immediate upgrade needed. |
| Switch to Open Source DB | APPLICABLE | Uses proprietary database SQL Server 2019; switching to PostgreSQL/MySQL would reduce licensing costs. |
| Update Outdated Components | APPLICABLE | Multiple outdated components detected (OS: EOL, Lang: CURRENT_VERSION, DB: CURRENT_VERSION). |

## Business Case

**Total Implementation Cost:** $53,200.39
**Total Annual Savings:** $28,350.00
**3-Year ROI:** 59.9%

| Scenario | Impl. Cost | Annual Savings | 3-Yr ROI | Payback (mo) |
|----------|------------|----------------|----------|--------------|
| OS Update / Security Patch | $1,156.53 | $450.00 | 16.7% | 30.8 |
| Switch to ARM CPU | $5,782.65 | $900.00 | -53.3% | 77.1 |
| Application Server Replacement | $11,565.30 | $10,800.00 | 180.1% | 12.9 |
| Cloud Migration (Lift & Shift) | $5,782.65 | $2,700.00 | 40.1% | 25.7 |
| Switch to Open Source DB | $28,913.26 | $13,500.00 | 40.1% | 25.7 |
