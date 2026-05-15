#!/usr/bin/env python3
"""Generate Markdown reports for portfolio modernization analysis."""

import json
from pathlib import Path

BASE_DIR = Path("/home/runner/work/copilot-test-ktruchcz/copilot-test-ktruchcz")
APPS_DIR = BASE_DIR / "output/applications/internal_app_model"
TECH_DIR = BASE_DIR / "output/technology_assessment"
COMPLEXITY_DIR = BASE_DIR / "output/complexity_results"
SCENARIO_DIR = BASE_DIR / "output/scenario_applicability_results"
BUSINESS_CASE_FILE = BASE_DIR / "output/business_case_results/business_case.json"
REPORTS_DIR = BASE_DIR / "output/reports"
APP_REPORTS_DIR = REPORTS_DIR / "apps"

REPORTS_DIR.mkdir(parents=True, exist_ok=True)
APP_REPORTS_DIR.mkdir(parents=True, exist_ok=True)

RETIRED_APPS = {"app005", "app007", "app009", "app029"}
IN_SCOPE = [f"app{str(i).zfill(3)}" for i in range(1, 31) if f"app{str(i).zfill(3)}" not in RETIRED_APPS]

# Load all data
apps = {}
tech_data = {}
complexity_data = {}
scenario_data = {}

for app_id in [f"app{str(i).zfill(3)}" for i in range(1, 31)]:
    with open(APPS_DIR / f"{app_id}.json") as f:
        apps[app_id] = json.load(f)

for app_id in IN_SCOPE:
    with open(TECH_DIR / f"technology_assessment_{app_id}.json") as f:
        tech_data[app_id] = json.load(f)
    with open(COMPLEXITY_DIR / f"complexity_{app_id}.json") as f:
        complexity_data[app_id] = json.load(f)
    with open(SCENARIO_DIR / f"scenario_assessment_{app_id}.json") as f:
        scenario_data[app_id] = json.load(f)

with open(BUSINESS_CASE_FILE) as f:
    business_case = json.load(f)

bc_by_app = {bc["application_identifier"]: bc for bc in business_case["application_business_cases"]}

SCENARIO_LABELS = {
    "os_update_security_patch": "OS Security Patch",
    "switch_to_standard_linux_os": "Switch to Linux",
    "switch_to_arm_cpu": "ARM CPU",
    "application_server_replacement": "App Server Replace",
    "app_deployment_to_cloud": "Cloud Deploy",
    "app_containerization": "Containerization",
    "app_refactor_decoupling": "Refactor/Decouple",
    "upgrade_legacy_databases": "DB Upgrade",
    "switch_db_engine_open_source": "Open Source DB",
    "update_outdated_components": "Update Components",
}

def complexity_class(score):
    if score <= 3:
        return "LOW"
    elif score <= 6:
        return "MEDIUM"
    else:
        return "HIGH"

def status_emoji(status):
    return {"CURRENT_VERSION": "✅", "OUTDATED": "⚠️", "EOL": "❌"}.get(status, "❓")

def scenario_emoji(status):
    return {"APPLICABLE": "🔧", "FULFILLED": "✅", "BLOCKED": "🚫", "NOT_APPLICABLE": "➖"}.get(status, "❓")

# ============================================================
# Per-app reports
# ============================================================
print("Generating per-app reports...")

for app_id in IN_SCOPE:
    app = apps[app_id]
    ta = tech_data[app_id]
    cd = complexity_data[app_id]
    sd = scenario_data[app_id]
    bc = bc_by_app.get(app_id, {})

    score = cd["complexity_score"]
    cls = complexity_class(score)

    # Count component statuses
    statuses = [c["component_status"] for c in ta["components_analyzed"]]
    cnt_current = statuses.count("CURRENT_VERSION")
    cnt_outdated = statuses.count("OUTDATED")
    cnt_eol = statuses.count("EOL")

    # Applicable scenarios
    applicable_scenarios = [s for s in sd["scenarios_detailed"] if s["status"] == "APPLICABLE"]

    lines = []
    lines.append(f"# {app['app_name']} ({app_id})\n")
    lines.append(f"> Analysis timestamp: 2025-07-15T00:00:00Z\n")

    # Overview table
    lines.append("## Application Overview\n")
    lines.append("| Attribute | Value |")
    lines.append("|-----------|-------|")
    lines.append(f"| **Name** | {app['app_name']} |")
    lines.append(f"| **Status** | {app['application_status']} |")
    lines.append(f"| **Criticality** | {app['business_criticality']} |")
    lines.append(f"| **Users** | {app['user_count']:,} |")
    lines.append(f"| **Solution Type** | {app['solution_type']} |")
    lines.append(f"| **Architecture** | {app.get('application_architecture') or 'Unknown'} |")
    lines.append(f"| **Containerized** | {app.get('is_containerized', 'No')} |")
    lines.append(f"| **CI/CD** | {app.get('ci_cd_present', 'No')} |")
    lines.append(f"| **Environments** | {app['environment_count']} |")
    lines.append(f"| **Servers** | {', '.join(app['server_instances'])} |")
    lines.append(f"| **External Interfaces** | {app['external_interface_count']} |")
    lines.append("")

    # Technology stack
    lines.append("## Technology Stack\n")
    lines.append("| Component | Value | Status |")
    lines.append("|-----------|-------|--------|")
    for comp in ta["components_analyzed"]:
        emoji = status_emoji(comp["component_status"])
        lines.append(f"| **{comp['component_type'].replace('_', ' ').title()}** | {comp['component_name']} | {emoji} {comp['component_status']} |")
    lines.append("")

    # Technology health chart
    lines.append("## Technology Health\n")
    lines.append("```mermaid")
    lines.append("pie title Technology Component Status")
    if cnt_current > 0:
        lines.append(f'    "Current" : {cnt_current}')
    if cnt_outdated > 0:
        lines.append(f'    "Outdated" : {cnt_outdated}')
    if cnt_eol > 0:
        lines.append(f'    "EOL" : {cnt_eol}')
    lines.append("```")
    lines.append("")

    # Complexity assessment
    lines.append("## Complexity Assessment\n")
    lines.append(f"**Score: {score}/10 — {cls}**\n")
    lines.append(cd["reasoning"])
    lines.append("")
    cf = cd["contributing_factors"]
    lines.append("| Factor | Value |")
    lines.append("|--------|-------|")
    lines.append(f"| Servers | {cf['number_of_servers']} |")
    lines.append(f"| Environments | {cf['number_of_environments']} |")
    lines.append(f"| External Interfaces | {cf['number_of_interfaces']} |")
    lines.append(f"| EOL Technologies | {cf['number_of_eol_technologies']} |")
    lines.append(f"| Outdated Technologies | {cf['number_of_outdated_technologies']} |")
    lines.append(f"| CI/CD Present | {cf['ci_cd_present']} |")
    lines.append(f"| Containerized | {cf['containerized']} |")
    lines.append("")

    # Modernization scenarios
    lines.append("## Modernization Scenarios\n")
    lines.append("| Scenario | Status | Reason |")
    lines.append("|----------|--------|--------|")
    for s in sd["scenarios_detailed"]:
        emoji = scenario_emoji(s["status"])
        lines.append(f"| {SCENARIO_LABELS.get(s['id'], s['id'])} | {emoji} {s['status']} | {s['reason'][:80]}{'...' if len(s['reason']) > 80 else ''} |")
    lines.append("")

    # Financial summary
    lines.append("## Financial Summary\n")
    if bc and bc.get("scenario_details"):
        lines.append(f"| Metric | Value |")
        lines.append(f"|--------|-------|")
        lines.append(f"| Total Implementation Cost | ${bc['total_implementation_cost']:,.2f} |")
        lines.append(f"| Total Annual Savings | ${bc['total_annual_savings']:,.2f} |")
        lines.append(f"| Payback Period | {bc['payback_period_years']} years |")
        lines.append(f"| 5-Year Net Benefit | ${bc['five_year_net_benefit']:,.2f} |")
        lines.append("")
        if applicable_scenarios:
            lines.append("### Applicable Scenario Costs\n")
            lines.append("| Scenario | Impl. Cost | Annual Savings | Payback |")
            lines.append("|----------|-----------|----------------|---------|")
            for sd_item in bc["scenario_details"]:
                lines.append(f"| {SCENARIO_LABELS.get(sd_item['scenario_id'], sd_item['scenario_id'])} | ${sd_item['implementation_cost']:,.2f} | ${sd_item['annual_savings']:,.2f} | {sd_item['payback_period_years']} yrs |")
            lines.append("")
    else:
        lines.append("_No applicable modernization scenarios with financial data._\n")

    report_path = APP_REPORTS_DIR / f"{app_id}.md"
    with open(report_path, "w") as f:
        f.write("\n".join(lines))

print(f"  Created {len(IN_SCOPE)} app reports")

# ============================================================
# Portfolio report
# ============================================================
print("Generating portfolio report...")

# Aggregate stats
status_counts = {}
criticality_counts = {}
eol_app_count = 0
outdated_app_count = 0

for app_id in IN_SCOPE:
    app = apps[app_id]
    status_counts[app["application_status"]] = status_counts.get(app["application_status"], 0) + 1
    criticality_counts[app["business_criticality"]] = criticality_counts.get(app["business_criticality"], 0) + 1
    ta = tech_data[app_id]
    if ta["has_eol_components"]:
        eol_app_count += 1
    elif ta["has_outdated_components"]:
        outdated_app_count += 1

current_app_count = len(IN_SCOPE) - eol_app_count - outdated_app_count

# Top modernization opportunities by total cost
sorted_apps = sorted(
    business_case["application_business_cases"],
    key=lambda x: x["total_implementation_cost"],
    reverse=True
)[:10]

ps = business_case["portfolio_summary"]

lines = []
lines.append("# Portfolio Modernization Report\n")
lines.append(f"> Analysis ID: portfolio_analysis_2025 | Timestamp: 2025-07-15T00:00:00Z\n")

# Executive Summary
lines.append("## Executive Summary\n")
lines.append(
    f"This portfolio modernization analysis covers **{len(IN_SCOPE)} in-scope applications** "
    f"(4 retired applications excluded) across multiple business units. "
    f"The assessment identifies significant technical debt: **{eol_app_count} applications** have at least one EOL component "
    f"and **{outdated_app_count} applications** have outdated components requiring attention. "
    f"The total estimated modernization investment is **${ps['total_implementation_cost']:,.0f}** "
    f"with projected annual savings of **${ps['total_annual_savings']:,.0f}**, "
    f"yielding a payback period of **{ps['payback_period_years']} years** and a 5-year net benefit of "
    f"**${ps['five_year_net_benefit']:,.0f}**. "
    f"Priority actions include containerizing eligible custom applications, migrating AIX-based legacy systems, "
    f"and upgrading EOL databases and application servers."
)
lines.append("")

# Portfolio Overview
lines.append("## Portfolio Overview\n")

lines.append("### Application Status Distribution\n")
lines.append("```mermaid")
lines.append("pie title Application Status (In-Scope)")
for k, v in status_counts.items():
    lines.append(f'    "{k}" : {v}')
lines.append("```")
lines.append("")

lines.append("### Business Criticality Distribution\n")
lines.append("```mermaid")
lines.append("pie title Business Criticality")
for k, v in criticality_counts.items():
    lines.append(f'    "{k}" : {v}')
lines.append("```")
lines.append("")

lines.append("### Technology Health Overview\n")
lines.append("```mermaid")
lines.append("pie title Application Tech Health")
lines.append(f'    "Has EOL Components" : {eol_app_count}')
lines.append(f'    "Has Outdated Components" : {outdated_app_count}')
lines.append(f'    "All Current" : {current_app_count}')
lines.append("```")
lines.append("")

# Summary table
lines.append("### Portfolio Statistics\n")
lines.append("| Metric | Value |")
lines.append("|--------|-------|")
lines.append(f"| Total Applications | 30 |")
lines.append(f"| In-Scope (Analyzed) | {len(IN_SCOPE)} |")
lines.append(f"| Retired (Out of Scope) | 4 |")
lines.append(f"| Applications with EOL Components | {eol_app_count} |")
lines.append(f"| Applications with Outdated Components | {outdated_app_count} |")
lines.append(f"| Total Modernization Cost | ${ps['total_implementation_cost']:,.2f} |")
lines.append(f"| Total Annual Savings | ${ps['total_annual_savings']:,.2f} |")
lines.append(f"| Payback Period | {ps['payback_period_years']} years |")
lines.append(f"| 5-Year Net Benefit | ${ps['five_year_net_benefit']:,.2f} |")
lines.append("")

# Top modernization opportunities
lines.append("## Top Modernization Opportunities\n")
lines.append("| App ID | Name | Complexity | Total Cost | Annual Savings | Payback |")
lines.append("|--------|------|-----------|-----------|----------------|---------|")
for bc_item in sorted_apps:
    aid = bc_item["application_identifier"]
    cls = complexity_class(bc_item["complexity_score"])
    lines.append(
        f"| {aid} | {bc_item['application_name']} | {bc_item['complexity_score']} ({cls}) | "
        f"${bc_item['total_implementation_cost']:,.0f} | ${bc_item['total_annual_savings']:,.0f} | "
        f"{bc_item['payback_period_years']} yrs |"
    )
lines.append("")

# Scenario applicability matrix
lines.append("## Scenario Applicability Matrix\n")
scenario_ids = list(SCENARIO_LABELS.keys())
header = "| App |" + "".join(f" {SCENARIO_LABELS[s][:8]} |" for s in scenario_ids)
sep = "|-----|" + "".join("---------:|" for _ in scenario_ids)
lines.append(header)
lines.append(sep)

for app_id in IN_SCOPE:
    sd = scenario_data[app_id]
    status_map = {s["id"]: s["status"] for s in sd["scenarios_detailed"]}
    row = f"| [{app_id}](apps/{app_id}.md) |"
    for sid in scenario_ids:
        emoji = scenario_emoji(status_map.get(sid, ""))
        row += f" {emoji} |"
    lines.append(row)
lines.append("")

# Financial summary table
lines.append("## Financial Summary by Application\n")
lines.append("| App ID | Name | Score | Total Cost | Annual Savings | 5-Yr Benefit |")
lines.append("|--------|------|-------|-----------|----------------|--------------|")
for bc_item in business_case["application_business_cases"]:
    lines.append(
        f"| [{bc_item['application_identifier']}](apps/{bc_item['application_identifier']}.md) | "
        f"{bc_item['application_name']} | {bc_item['complexity_score']} | "
        f"${bc_item['total_implementation_cost']:,.0f} | "
        f"${bc_item['total_annual_savings']:,.0f} | "
        f"${bc_item['five_year_net_benefit']:,.0f} |"
    )
lines.append("")

# Risk Applications
lines.append("## Risk Applications\n")

lines.append("### Applications with EOL Components\n")
lines.append("| App ID | Name | Criticality | EOL Components |")
lines.append("|--------|------|------------|----------------|")
for app_id in IN_SCOPE:
    ta = tech_data[app_id]
    eol_comps = [c["component_name"] for c in ta["components_analyzed"] if c["component_status"] == "EOL"]
    if eol_comps:
        app = apps[app_id]
        lines.append(f"| [{app_id}](apps/{app_id}.md) | {app['app_name']} | {app['business_criticality']} | {', '.join(eol_comps)} |")
lines.append("")

lines.append("### Critical Business Applications\n")
lines.append("| App ID | Name | EOL Components | Outdated Components |")
lines.append("|--------|------|---------------|---------------------|")
for app_id in IN_SCOPE:
    app = apps[app_id]
    if app["business_criticality"] == "Critical":
        ta = tech_data[app_id]
        eol_c = [c["component_name"] for c in ta["components_analyzed"] if c["component_status"] == "EOL"]
        out_c = [c["component_name"] for c in ta["components_analyzed"] if c["component_status"] == "OUTDATED"]
        lines.append(f"| [{app_id}](apps/{app_id}.md) | {app['app_name']} | {', '.join(eol_c) or 'None'} | {', '.join(out_c) or 'None'} |")
lines.append("")

# Per-app links
lines.append("## Per-Application Reports\n")
lines.append("| App ID | Name | Criticality | Complexity | Report |")
lines.append("|--------|------|------------|-----------|--------|")
for app_id in IN_SCOPE:
    app = apps[app_id]
    score = complexity_data[app_id]["complexity_score"]
    cls = complexity_class(score)
    lines.append(f"| {app_id} | {app['app_name']} | {app['business_criticality']} | {score} ({cls}) | [View Report](apps/{app_id}.md) |")

# Retired apps note
lines.append("")
lines.append("### Retired Applications (Out of Scope)\n")
lines.append("| App ID | Name |")
lines.append("|--------|------|")
for app_id in sorted(RETIRED_APPS):
    app = apps[app_id]
    lines.append(f"| {app_id} | {app['app_name']} |")
lines.append("")

report_path = REPORTS_DIR / "portfolio_report.md"
with open(report_path, "w") as f:
    f.write("\n".join(lines))

print(f"  Created portfolio_report.md")
print("\nAll reports generated!")
