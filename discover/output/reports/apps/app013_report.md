# SecurityApp-013 (app013) — Modernization Report

**Analysis Date:** 2025-01-01T00:00:00Z  
**Business Unit:** Security  
**Criticality:** Critical  
**Status:** Production  
**Deployment:** On-Premise  
**Architecture:** 3-Tier  
**Containerized:** No  

## Technology Assessment

| Component | Version | Status |
|-----------|---------|--------|
| Operating System | Debian 7 | 🔴 EOL |
| Programming Language | Java 17 | ✅ CURRENT_VERSION |
| Application Server | Websphere 8.0 | 🔴 EOL |
| Database Engine | SQL Server 2022 | ✅ CURRENT_VERSION |

**Overall Risk:** `HIGH_RISK`

## Complexity Assessment

**Score:** 8/10 — **High** (Cost Multiplier: 1.5x)

| Factor | Value | Points |
|--------|-------|--------|
| Server Count | 2 | 2 |
| External Interfaces | 15 | 2 |
| Api Endpoints | 8 | 1 |
| Business Criticality | Critical | 3 |
| Tech Debt Components | 2 | 2 |
| Deployment Type | On-Premise | 2 |
| Database Storage Gb | 600.0 | 1 |
| Ci Cd Present | Yes | 0 |
| Is Containerized | No | 1 |

## Scenario Applicability

| Scenario | Status |
|----------|--------|
| OS Security Patch | APPLICABLE |
| Switch to Linux | NOT_APPLICABLE |
| ARM CPU Migration | NOT_APPLICABLE |
| App Server Replacement | APPLICABLE |
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
| Total Migration Cost | $601,500 |
| Total Yearly Savings | $295,500 |
| 3-Year ROI | 47.4% |
| Payback Period | 2.04 years |

### Applicable Scenarios Breakdown

| Scenario | Migration Cost | Yearly Savings |
|----------|----------------|----------------|
| OS Security Patch | $1,500 | $500 |
| App Server Replacement | $15,000 | $12,000 |
| Cloud Deployment | $7,500 | $3,000 |
| Containerization | $150,000 | $100,000 |
| Refactor/Decouple | $375,000 | $150,000 |
| Managed DB | $7,500 | $10,000 |
| Managed ARM DB | $7,500 | $5,000 |
| Switch to PostgreSQL | $37,500 | $15,000 |
