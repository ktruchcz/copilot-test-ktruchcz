# ERPApp-001 (app001) — Modernization Report

**Analysis Date:** 2025-01-01T00:00:00Z  
**Business Unit:** Finance  
**Criticality:** High  
**Status:** Production  
**Deployment:** On-Premise  
**Architecture:** 1-Tier  
**Containerized:** No  

## Technology Assessment

| Component | Version | Status |
|-----------|---------|--------|
| Operating System | AIX 7.2 | ✅ CURRENT_VERSION |
| Programming Language | COBOL-2014 | ⚠️ OUTDATED |
| Database Engine | Oracle 19c | ✅ CURRENT_VERSION |

**Overall Risk:** `MEDIUM_RISK`

## Complexity Assessment

**Score:** 6/10 — **Medium** (Cost Multiplier: 1.2x)

| Factor | Value | Points |
|--------|-------|--------|
| Server Count | 2 | 2 |
| External Interfaces | 5 | 1 |
| Api Endpoints | 0 | 0 |
| Business Criticality | High | 2 |
| Tech Debt Components | 1 | 1 |
| Deployment Type | On-Premise | 2 |
| Database Storage Gb | 1000.0 | 1 |
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
| DB Upgrade | NOT_APPLICABLE |
| Managed DB | APPLICABLE |
| Managed ARM DB | APPLICABLE |
| Serverless DB | NOT_APPLICABLE |
| Switch to PostgreSQL | APPLICABLE |

## Business Case

| Metric | Value |
|--------|-------|
| Total Migration Cost | $468,360 |
| Total Yearly Savings | $283,400 |
| 3-Year ROI | 81.5% |
| Payback Period | 1.65 years |

### Applicable Scenarios Breakdown

| Scenario | Migration Cost | Yearly Savings |
|----------|----------------|----------------|
| Switch to Linux | $360 | $400 |
| Cloud Deployment | $6,000 | $3,000 |
| Containerization | $120,000 | $100,000 |
| Refactor/Decouple | $300,000 | $150,000 |
| Managed DB | $6,000 | $10,000 |
| Managed ARM DB | $6,000 | $5,000 |
| Switch to PostgreSQL | $30,000 | $15,000 |
