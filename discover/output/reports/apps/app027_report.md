# DataWarehouseApp-027 (app027) — Modernization Report

**Analysis Date:** 2025-01-01T00:00:00Z  
**Business Unit:** BI  
**Criticality:** High  
**Status:** Production  
**Deployment:** AWS, On-premise  
**Architecture:** 3-Tier  
**Containerized:** No  

## Technology Assessment

| Component | Version | Status |
|-----------|---------|--------|
| Operating System | RHEL 7 | 🔴 EOL |
| Programming Language | Java 11 | ⚠️ OUTDATED |
| Application Server | Websphere 8.5 | ⚠️ OUTDATED |
| Database Engine | SQL Server 2022 | ✅ CURRENT_VERSION |

**Overall Risk:** `HIGH_RISK`

## Complexity Assessment

**Score:** 7/10 — **High** (Cost Multiplier: 1.5x)

| Factor | Value | Points |
|--------|-------|--------|
| Server Count | 2 | 2 |
| External Interfaces | 20 | 2 |
| Api Endpoints | 5 | 0 |
| Business Criticality | High | 2 |
| Tech Debt Components | 3 | 3 |
| Deployment Type | AWS, On-premise | 1 |
| Database Storage Gb | 5000.0 | 2 |
| Ci Cd Present | Yes | 0 |
| Is Containerized | No | 1 |

## Scenario Applicability

| Scenario | Status |
|----------|--------|
| OS Security Patch | APPLICABLE |
| Switch to Linux | NOT_APPLICABLE |
| ARM CPU Migration | APPLICABLE |
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
| Total Migration Cost | $609,000 |
| Total Yearly Savings | $296,500 |
| 3-Year ROI | 46.1% |
| Payback Period | 2.05 years |

### Applicable Scenarios Breakdown

| Scenario | Migration Cost | Yearly Savings |
|----------|----------------|----------------|
| OS Security Patch | $1,500 | $500 |
| ARM CPU Migration | $7,500 | $1,000 |
| App Server Replacement | $15,000 | $12,000 |
| Cloud Deployment | $7,500 | $3,000 |
| Containerization | $150,000 | $100,000 |
| Refactor/Decouple | $375,000 | $150,000 |
| Managed DB | $7,500 | $10,000 |
| Managed ARM DB | $7,500 | $5,000 |
| Switch to PostgreSQL | $37,500 | $15,000 |
