# SupportApp-006 (app006)

**Status:** Production | **Criticality:** Medium | **Solution Type:** 3rd party software

## Overview

| Field | Value |
|-------|-------|
| Description | IT service desk application for handling internal support tickets and IT service requests |
| Business Unit | IT |
| Operating System | Debian 6 |
| Programming Language | Java 11 |
| Database | PostgreSQL 13 |
| Architecture | unknown |
| Containerized | No |
| CI/CD Present | Yes |
| Environments | 2 |
| Server Instances | sv10 |
| External Interfaces | 4 |
| Users | 290 |

## Technology Assessment

**Overall Status:** 🔴 EOL

| Component | Name | Status |
|-----------|------|--------|
| operating_system | Debian 6 | 🔴 EOL |
| programming_language | Java 11 | ⚠️ OUTDATED |
| database | PostgreSQL 13 | ⚠️ OUTDATED |
| application_server | Glassfish 5.0 | ❓ NO_KNOWLEDGE |

## Complexity Assessment

**Score:** 5/10 — **Classification:** MEDIUM

| Factor | Score |
|--------|-------|
| Technology Age Eol | 2.5 |
| Integration Complexity | 0.4 |
| Infrastructure Scale | 0.6 |
| Business Criticality | 0.6 |
| Code And Architecture | 0.75 |
| Data Complexity | 0.5 |

## Scenario Analysis

| Scenario | Status | Reasoning |
|----------|--------|-----------|
| OS Update / Security Patch | APPLICABLE | OS Debian 6 is EOL; security patch update is needed. |
| Switch to Standard Linux OS | FULFILLED | Already running on standard Linux (Debian 6). |
| Switch to ARM CPU | BLOCKED | 3rd party software; ARM support depends on vendor roadmap. |
| Application Server Replacement | APPLICABLE | Uses application server Glassfish 5.0; replacement/upgrade may be beneficial. |
| Cloud Migration (Lift & Shift) | APPLICABLE | 3rd party software; cloud-hosted or SaaS version likely available. |
| Containerization | BLOCKED | 3rd party software; containerization depends on vendor support. |
| Refactoring & Decoupling | BLOCKED | 3rd party software; source code refactoring is not feasible. |
| Upgrade Legacy Databases | APPLICABLE | Database PostgreSQL 13 is outdated; upgrade recommended. |
| Switch to Open Source DB | NOT_APPLICABLE | Already using open source or managed database (PostgreSQL 13). |
| Update Outdated Components | PARTIALLY_FULFILLED | 3rd party software with outdated components; updates depend on vendor release schedule. |

## Business Case

**Total Implementation Cost:** $26,147.65
**Total Annual Savings:** $22,950.00
**3-Year ROI:** 163.3%

| Scenario | Impl. Cost | Annual Savings | 3-Yr ROI | Payback (mo) |
|----------|------------|----------------|----------|--------------|
| OS Update / Security Patch | $1,005.68 | $450.00 | 34.2% | 26.8 |
| Application Server Replacement | $10,056.79 | $10,800.00 | 222.2% | 11.2 |
| Cloud Migration (Lift & Shift) | $5,028.39 | $2,700.00 | 61.1% | 22.3 |
| Upgrade Legacy Databases | $10,056.79 | $9,000.00 | 168.5% | 13.4 |
