# VendorApp-018 (app018)

**Status:** Production | **Criticality:** Medium | **Solution Type:** Custom made

## Overview

| Field | Value |
|-------|-------|
| Description | Vendor management platform for handling supplier relationships, contracts, and procurement processes |
| Business Unit | Procurement |
| Operating System | RHEL 7 |
| Programming Language | Java 8 |
| Database | PostgreSQL 13 |
| Architecture | 3-Tier |
| Containerized | No |
| CI/CD Present | No |
| Environments | 6 |
| Server Instances | sv26, sv27 |
| External Interfaces | 6 |
| Users | 260 |

## Technology Assessment

**Overall Status:** 🔴 EOL

| Component | Name | Status |
|-----------|------|--------|
| operating_system | RHEL 7 | 🔴 EOL |
| programming_language | Java 8 | ⚠️ OUTDATED |
| database | PostgreSQL 13 | ⚠️ OUTDATED |
| application_server | Glassfish 4.5 | ❓ NO_KNOWLEDGE |

## Complexity Assessment

**Score:** 6/10 — **Classification:** MEDIUM

| Factor | Score |
|--------|-------|
| Technology Age Eol | 2.5 |
| Integration Complexity | 0.8 |
| Infrastructure Scale | 1.5 |
| Business Criticality | 0.6 |
| Code And Architecture | 0.6 |
| Data Complexity | 0.5 |

## Scenario Analysis

| Scenario | Status | Reasoning |
|----------|--------|-----------|
| OS Update / Security Patch | APPLICABLE | OS RHEL 7 is EOL; security patch update is needed. |
| Switch to Standard Linux OS | FULFILLED | Already running on standard Linux (RHEL 7). |
| Switch to ARM CPU | APPLICABLE | ARM CPU migration is possible with recompilation/containerization effort. |
| Application Server Replacement | APPLICABLE | Uses application server Glassfish 4.5; replacement/upgrade may be beneficial. |
| Cloud Migration (Lift & Shift) | APPLICABLE | Application can be migrated to cloud (lift & shift). |
| Containerization | APPLICABLE | Application can be containerized to improve portability and scalability. |
| Refactoring & Decoupling | PARTIALLY_FULFILLED | Already uses multi-tier architecture; further decomposition may be beneficial. |
| Upgrade Legacy Databases | APPLICABLE | Database PostgreSQL 13 is outdated; upgrade recommended. |
| Switch to Open Source DB | NOT_APPLICABLE | Already using open source or managed database (PostgreSQL 13). |
| Update Outdated Components | APPLICABLE | Multiple outdated components detected (OS: EOL, Lang: OUTDATED, DB: OUTDATED). |

## Business Case

**Total Implementation Cost:** $151,505.47
**Total Annual Savings:** $113,850.00
**3-Year ROI:** 125.4%

| Scenario | Impl. Cost | Annual Savings | 3-Yr ROI | Payback (mo) |
|----------|------------|----------------|----------|--------------|
| OS Update / Security Patch | $1,156.53 | $450.00 | 16.7% | 30.8 |
| Switch to ARM CPU | $5,782.65 | $900.00 | -53.3% | 77.1 |
| Application Server Replacement | $11,565.30 | $10,800.00 | 180.1% | 12.9 |
| Cloud Migration (Lift & Shift) | $5,782.65 | $2,700.00 | 40.1% | 25.7 |
| Containerization | $115,653.04 | $90,000.00 | 133.5% | 15.4 |
| Upgrade Legacy Databases | $11,565.30 | $9,000.00 | 133.5% | 15.4 |
