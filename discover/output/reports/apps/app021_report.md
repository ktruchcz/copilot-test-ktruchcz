# FleetApp-021 (app021) — Modernization Report

**Analysis Date:** 2025-01-01T00:00:00Z  
**Business Unit:** Operations  
**Criticality:** High  
**Status:** Production  
**Deployment:** On-Premise  
**Architecture:** 2-Tier  
**Containerized:** No  

## Technology Assessment

| Component | Version | Status |
|-----------|---------|--------|
| Operating System | Windows Server 2022 | ✅ CURRENT_VERSION |
| Programming Language | C++ 17 | ✅ CURRENT_VERSION |
| Application Server | Microsoft IIS 10.0 | ✅ CURRENT_VERSION |
| Database Engine | Oracle 11g | 🔴 EOL |

**Overall Risk:** `HIGH_RISK`

## Complexity Assessment

**Score:** 6/10 — **Medium** (Cost Multiplier: 1.2x)

| Factor | Value | Points |
|--------|-------|--------|
| Server Count | 2 | 2 |
| External Interfaces | 4 | 0 |
| Api Endpoints | 3 | 0 |
| Business Criticality | High | 2 |
| Tech Debt Components | 1 | 1 |
| Deployment Type | On-Premise | 2 |
| Database Storage Gb | 400.0 | 1 |
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
| Refactor/Decouple | NOT_APPLICABLE |
| DB Upgrade | APPLICABLE |
| Managed DB | APPLICABLE |
| Managed ARM DB | APPLICABLE |
| Serverless DB | NOT_APPLICABLE |
| Switch to PostgreSQL | APPLICABLE |

## Business Case

| Metric | Value |
|--------|-------|
| Total Migration Cost | $180,360 |
| Total Yearly Savings | $143,400 |
| 3-Year ROI | 138.5% |
| Payback Period | 1.26 years |

### Applicable Scenarios Breakdown

| Scenario | Migration Cost | Yearly Savings |
|----------|----------------|----------------|
| Switch to Linux | $360 | $400 |
| Cloud Deployment | $6,000 | $3,000 |
| Containerization | $120,000 | $100,000 |
| DB Upgrade | $12,000 | $10,000 |
| Managed DB | $6,000 | $10,000 |
| Managed ARM DB | $6,000 | $5,000 |
| Switch to PostgreSQL | $30,000 | $15,000 |
