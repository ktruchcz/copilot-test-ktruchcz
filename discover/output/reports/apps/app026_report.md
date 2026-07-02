# LegacyFinApp-026 (app026) — Modernization Report

**Analysis Date:** 2025-01-01T00:00:00Z  
**Business Unit:** Finance  
**Criticality:** Critical  
**Status:** Production  
**Deployment:** On-Premise  
**Architecture:** 1-Tier  
**Containerized:** No  

## Technology Assessment

| Component | Version | Status |
|-----------|---------|--------|
| Operating System | AIX 7.2 | ✅ CURRENT_VERSION |
| Programming Language | FORTRAN 2018 | ⚠️ OUTDATED |
| Database Engine | DB2 | ⚠️ OUTDATED |

**Overall Risk:** `MEDIUM_RISK`

## Complexity Assessment

**Score:** 7/10 — **High** (Cost Multiplier: 1.5x)

| Factor | Value | Points |
|--------|-------|--------|
| Server Count | 1 | 1 |
| External Interfaces | 1 | 0 |
| Api Endpoints | 0 | 0 |
| Business Criticality | Critical | 3 |
| Tech Debt Components | 2 | 2 |
| Deployment Type | On-Premise | 2 |
| Database Storage Gb | 1500.0 | 2 |
| Ci Cd Present | No | 1 |
| Is Containerized | No | 1 |

## Scenario Applicability

| Scenario | Status |
|----------|--------|
| OS Security Patch | NOT_APPLICABLE |
| Switch to Linux | APPLICABLE |
| ARM CPU Migration | NOT_APPLICABLE |
| App Server Replacement | NOT_APPLICABLE |
| Cloud Deployment | APPLICABLE |
| Containerization | APPLICABLE |
| Refactor/Decouple | APPLICABLE |
| DB Upgrade | APPLICABLE |
| Managed DB | APPLICABLE |
| Managed ARM DB | APPLICABLE |
| Serverless DB | NOT_APPLICABLE |
| Switch to PostgreSQL | APPLICABLE |

## Business Case

| Metric | Value |
|--------|-------|
| Total Migration Cost | $600,450 |
| Total Yearly Savings | $293,400 |
| 3-Year ROI | 46.6% |
| Payback Period | 2.05 years |

### Applicable Scenarios Breakdown

| Scenario | Migration Cost | Yearly Savings |
|----------|----------------|----------------|
| Switch to Linux | $450 | $400 |
| Cloud Deployment | $7,500 | $3,000 |
| Containerization | $150,000 | $100,000 |
| Refactor/Decouple | $375,000 | $150,000 |
| DB Upgrade | $15,000 | $10,000 |
| Managed DB | $7,500 | $10,000 |
| Managed ARM DB | $7,500 | $5,000 |
| Switch to PostgreSQL | $37,500 | $15,000 |
