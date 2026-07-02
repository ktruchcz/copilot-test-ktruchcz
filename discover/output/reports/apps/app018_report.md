# VendorApp-018 (app018) — Modernization Report

**Analysis Date:** 2025-01-01T00:00:00Z  
**Business Unit:** Procurement  
**Criticality:** Medium  
**Status:** Production  
**Deployment:** On-Premise  
**Architecture:** 3-Tier  
**Containerized:** No  

## Technology Assessment

| Component | Version | Status |
|-----------|---------|--------|
| Operating System | RHEL 7 | 🔴 EOL |
| Programming Language | Java 8 | 🔴 EOL |
| Application Server | Glassfish 4.5 | 🔴 EOL |
| Database Engine | PostgreSQL 13 | ⚠️ OUTDATED |

**Overall Risk:** `HIGH_RISK`

## Complexity Assessment

**Score:** 7/10 — **High** (Cost Multiplier: 1.5x)

| Factor | Value | Points |
|--------|-------|--------|
| Server Count | 2 | 2 |
| External Interfaces | 6 | 1 |
| Api Endpoints | 5 | 0 |
| Business Criticality | Medium | 1 |
| Tech Debt Components | 4 | 3 |
| Deployment Type | On-Premise | 2 |
| Database Storage Gb | 250.0 | 1 |
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
| Refactor/Decouple | APPLICABLE |
| DB Upgrade | APPLICABLE |
| Managed DB | APPLICABLE |
| Managed ARM DB | APPLICABLE |
| Serverless DB | NOT_APPLICABLE |
| Switch to PostgreSQL | NOT_APPLICABLE |

## Business Case

| Metric | Value |
|--------|-------|
| Total Migration Cost | $579,000 |
| Total Yearly Savings | $290,500 |
| 3-Year ROI | 50.5% |
| Payback Period | 1.99 years |

### Applicable Scenarios Breakdown

| Scenario | Migration Cost | Yearly Savings |
|----------|----------------|----------------|
| OS Security Patch | $1,500 | $500 |
| App Server Replacement | $15,000 | $12,000 |
| Cloud Deployment | $7,500 | $3,000 |
| Containerization | $150,000 | $100,000 |
| Refactor/Decouple | $375,000 | $150,000 |
| DB Upgrade | $15,000 | $10,000 |
| Managed DB | $7,500 | $10,000 |
| Managed ARM DB | $7,500 | $5,000 |
