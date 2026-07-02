# BackupApp-017 (app017) — Modernization Report

**Analysis Date:** 2025-01-01T00:00:00Z  
**Business Unit:** IT  
**Criticality:** High  
**Status:** Production  
**Deployment:** On-Premise  
**Architecture:** unknown  
**Containerized:** No  

## Technology Assessment

| Component | Version | Status |
|-----------|---------|--------|
| Operating System | RHEL 7 | 🔴 EOL |
| Programming Language | PowerShell | ✅ CURRENT_VERSION |
| Application Server | Payara 5.0 | ⚠️ OUTDATED |
| Database Engine | Oracle 12c | 🔴 EOL |

**Overall Risk:** `HIGH_RISK`

## Complexity Assessment

**Score:** 7/10 — **High** (Cost Multiplier: 1.5x)

| Factor | Value | Points |
|--------|-------|--------|
| Server Count | 2 | 2 |
| External Interfaces | 8 | 1 |
| Api Endpoints | 2 | 0 |
| Business Criticality | High | 2 |
| Tech Debt Components | 3 | 3 |
| Deployment Type | On-Premise | 2 |
| Database Storage Gb | 350.0 | 1 |
| Ci Cd Present | No | 1 |
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
| Refactor/Decouple | LACK_OF_DATA |
| DB Upgrade | APPLICABLE |
| Managed DB | APPLICABLE |
| Managed ARM DB | APPLICABLE |
| Serverless DB | NOT_APPLICABLE |
| Switch to PostgreSQL | APPLICABLE |

## Business Case

| Metric | Value |
|--------|-------|
| Total Migration Cost | $241,500 |
| Total Yearly Savings | $155,500 |
| 3-Year ROI | 93.2% |
| Payback Period | 1.55 years |

### Applicable Scenarios Breakdown

| Scenario | Migration Cost | Yearly Savings |
|----------|----------------|----------------|
| OS Security Patch | $1,500 | $500 |
| App Server Replacement | $15,000 | $12,000 |
| Cloud Deployment | $7,500 | $3,000 |
| Containerization | $150,000 | $100,000 |
| DB Upgrade | $15,000 | $10,000 |
| Managed DB | $7,500 | $10,000 |
| Managed ARM DB | $7,500 | $5,000 |
| Switch to PostgreSQL | $37,500 | $15,000 |
