# AnalyticsApp-003 (app003) — Modernization Report

**Analysis Date:** 2025-01-01T00:00:00Z  
**Business Unit:** IT  
**Criticality:** Low  
**Status:** Production  
**Deployment:** AWS  
**Architecture:** 3-Tier  
**Containerized:** Yes  

## Technology Assessment

| Component | Version | Status |
|-----------|---------|--------|
| Operating System | RHEL 7 | 🔴 EOL |
| Programming Language | Python 3.9 | ⚠️ OUTDATED |
| Application Server | Apache Tomcat 6.1 | 🔴 EOL |
| Database Engine | PostgreSQL 13 | ⚠️ OUTDATED |

**Overall Risk:** `HIGH_RISK`

## Complexity Assessment

**Score:** 4/10 — **Medium** (Cost Multiplier: 1.2x)

| Factor | Value | Points |
|--------|-------|--------|
| Server Count | 1 | 1 |
| External Interfaces | 3 | 0 |
| Api Endpoints | 8 | 1 |
| Business Criticality | Low | 0 |
| Tech Debt Components | 4 | 3 |
| Deployment Type | AWS | 0 |
| Database Storage Gb | 200.0 | 1 |
| Ci Cd Present | Yes | 0 |
| Is Containerized | Yes | 0 |

## Scenario Applicability

| Scenario | Status |
|----------|--------|
| OS Security Patch | APPLICABLE |
| Switch to Linux | NOT_APPLICABLE |
| ARM CPU Migration | APPLICABLE |
| App Server Replacement | APPLICABLE |
| Cloud Deployment | FULFILLED |
| Containerization | FULFILLED |
| Refactor/Decouple | APPLICABLE |
| DB Upgrade | APPLICABLE |
| Managed DB | APPLICABLE |
| Managed ARM DB | APPLICABLE |
| Serverless DB | NOT_APPLICABLE |
| Switch to PostgreSQL | NOT_APPLICABLE |

## Business Case

| Metric | Value |
|--------|-------|
| Total Migration Cost | $343,200 |
| Total Yearly Savings | $188,500 |
| 3-Year ROI | 64.8% |
| Payback Period | 1.82 years |

### Applicable Scenarios Breakdown

| Scenario | Migration Cost | Yearly Savings |
|----------|----------------|----------------|
| OS Security Patch | $1,200 | $500 |
| ARM CPU Migration | $6,000 | $1,000 |
| App Server Replacement | $12,000 | $12,000 |
| Refactor/Decouple | $300,000 | $150,000 |
| DB Upgrade | $12,000 | $10,000 |
| Managed DB | $6,000 | $10,000 |
| Managed ARM DB | $6,000 | $5,000 |
