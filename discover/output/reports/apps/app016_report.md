# MobileApp-016 (app016) — Modernization Report

**Analysis Date:** 2025-01-01T00:00:00Z  
**Business Unit:** Operations  
**Criticality:** Medium  
**Status:** Production  
**Deployment:** AWS  
**Architecture:** 3-Tier  
**Containerized:** Yes  

## Technology Assessment

| Component | Version | Status |
|-----------|---------|--------|
| Operating System | RHEL 7 | 🔴 EOL |
| Programming Language | React Native | ✅ CURRENT_VERSION |
| Application Server | Payara 4.0 | 🔴 EOL |
| Database Engine | SQL Server 2019 | ✅ CURRENT_VERSION |

**Overall Risk:** `HIGH_RISK`

## Complexity Assessment

**Score:** 6/10 — **Medium** (Cost Multiplier: 1.2x)

| Factor | Value | Points |
|--------|-------|--------|
| Server Count | 2 | 2 |
| External Interfaces | 10 | 1 |
| Api Endpoints | 30 | 2 |
| Business Criticality | Medium | 1 |
| Tech Debt Components | 2 | 2 |
| Deployment Type | AWS | 0 |
| Database Storage Gb | 2000.0 | 2 |
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
| DB Upgrade | NOT_APPLICABLE |
| Managed DB | APPLICABLE |
| Managed ARM DB | APPLICABLE |
| Serverless DB | NOT_APPLICABLE |
| Switch to PostgreSQL | APPLICABLE |

## Business Case

| Metric | Value |
|--------|-------|
| Total Migration Cost | $361,200 |
| Total Yearly Savings | $193,500 |
| 3-Year ROI | 60.7% |
| Payback Period | 1.87 years |

### Applicable Scenarios Breakdown

| Scenario | Migration Cost | Yearly Savings |
|----------|----------------|----------------|
| OS Security Patch | $1,200 | $500 |
| ARM CPU Migration | $6,000 | $1,000 |
| App Server Replacement | $12,000 | $12,000 |
| Refactor/Decouple | $300,000 | $150,000 |
| Managed DB | $6,000 | $10,000 |
| Managed ARM DB | $6,000 | $5,000 |
| Switch to PostgreSQL | $30,000 | $15,000 |
