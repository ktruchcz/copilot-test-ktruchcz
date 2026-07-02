# InventoryApp-008 (app008) — Modernization Report

**Analysis Date:** 2025-01-01T00:00:00Z  
**Business Unit:** Operations  
**Criticality:** High  
**Status:** Production  
**Deployment:** On-Premise  
**Architecture:** 1-Tier  
**Containerized:** No  

## Technology Assessment

| Component | Version | Status |
|-----------|---------|--------|
| Operating System | AIX 6 | 🔴 EOL |
| Programming Language | COBOL-2014 | ⚠️ OUTDATED |
| Application Server | Oracle Weblogic 8.0 | 🔴 EOL |
| Database Engine | SQL Server 2019 | ✅ CURRENT_VERSION |

**Overall Risk:** `HIGH_RISK`

## Complexity Assessment

**Score:** 7/10 — **High** (Cost Multiplier: 1.5x)

| Factor | Value | Points |
|--------|-------|--------|
| Server Count | 2 | 2 |
| External Interfaces | 2 | 0 |
| Api Endpoints | 0 | 0 |
| Business Criticality | High | 2 |
| Tech Debt Components | 3 | 3 |
| Deployment Type | On-Premise | 2 |
| Database Storage Gb | 400.0 | 1 |
| Ci Cd Present | No | 1 |
| Is Containerized | No | 1 |

## Scenario Applicability

| Scenario | Status |
|----------|--------|
| OS Security Patch | APPLICABLE |
| Switch to Linux | APPLICABLE |
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
| Total Migration Cost | $601,950 |
| Total Yearly Savings | $295,900 |
| 3-Year ROI | 47.5% |
| Payback Period | 2.03 years |

### Applicable Scenarios Breakdown

| Scenario | Migration Cost | Yearly Savings |
|----------|----------------|----------------|
| OS Security Patch | $1,500 | $500 |
| Switch to Linux | $450 | $400 |
| App Server Replacement | $15,000 | $12,000 |
| Cloud Deployment | $7,500 | $3,000 |
| Containerization | $150,000 | $100,000 |
| Refactor/Decouple | $375,000 | $150,000 |
| Managed DB | $7,500 | $10,000 |
| Managed ARM DB | $7,500 | $5,000 |
| Switch to PostgreSQL | $37,500 | $15,000 |
