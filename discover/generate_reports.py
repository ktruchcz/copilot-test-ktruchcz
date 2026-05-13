#!/usr/bin/env python3
"""Generate all markdown reports for the portfolio modernization analysis (Step 7)."""

import json
from pathlib import Path
from collections import defaultdict

BASE = Path("/home/runner/work/copilot-test-ktruchcz/copilot-test-ktruchcz/discover/output")
REPORTS_DIR = BASE / "reports"
APPS_DIR = REPORTS_DIR / "apps"
APPS_DIR.mkdir(parents=True, exist_ok=True)

RETIRED = {"app005", "app007", "app009", "app029"}
ALL_IDS = [f"app{str(i).zfill(3)}" for i in range(1, 31)]
IN_SCOPE = [a for a in ALL_IDS if a not in RETIRED]

STATUS_EMOJI = {
    "CURRENT_VERSION": "🟢",
    "OUTDATED": "🟡",
    "EOL": "🔴",
    "NO_KNOWLEDGE": "⚪",
}

# ── Load all data ──────────────────────────────────────────────────────────────
apps = {}
for aid in ALL_IDS:
    with open(BASE / "applications" / "internal_app_model" / f"{aid}.json") as f:
        apps[aid] = json.load(f)

tech_assessments = {}
complexities = {}
scenario_assessments = {}

for aid in IN_SCOPE:
    with open(BASE / "applications" / "technology_assessment" / f"technology_assessment_{aid}.json") as f:
        tech_assessments[aid] = json.load(f)
    with open(BASE / "applications" / "complexity" / f"complexity_{aid}.json") as f:
        complexities[aid] = json.load(f)
    with open(BASE / "applications" / "scenario_assessment" / f"scenario_assessment_{aid}.json") as f:
        scenario_assessments[aid] = json.load(f)

with open(BASE / "business_case.json") as f:
    business_case = json.load(f)

bc_by_app = {a["application_identifier"]: a for a in business_case["applications"]}

FINANCE_INFO = {
    "os_update_security_patch": {"cost_once": 1000, "savings_annual": 500},
    "switch_to_standard_linux_os": {"cost_once": 300, "savings_annual": 400},
    "switch_to_arm_cpu": {"cost_once": 5000, "savings_annual": 1000},
    "application_server_replacement": {"cost_once": 10000, "savings_annual": 12000},
    "app_deployment_to_cloud": {"cost_once": 5000, "savings_annual": 3000},
    "app_containerization": {"cost_once": 100000, "savings_annual": 100000},
    "app_refactor_decoupling": {"cost_once": 250000, "savings_annual": 150000},
    "upgrade_legacy_databases": {"cost_once": 10000, "savings_annual": 10000},
    "switch_to_managed_db": {"cost_once": 5000, "savings_annual": 10000},
    "managed_arm_db": {"cost_once": 5000, "savings_annual": 5000},
    "serverless_db_migration": {"cost_once": 5000, "savings_annual": 15000},
    "switch_db_engine_postgresql": {"cost_once": 25000, "savings_annual": 15000},
    "switch_db_engine_open_source": {"cost_once": 25000, "savings_annual": 15000},
}

SCENARIO_LABELS = {
    "os_update_security_patch": "OS Security Patch",
    "switch_to_standard_linux_os": "Switch to Standard Linux",
    "switch_to_arm_cpu": "Switch to ARM CPU",
    "application_server_replacement": "App Server Replacement",
    "app_deployment_to_cloud": "Cloud Deployment",
    "app_containerization": "Containerization",
    "app_refactor_decoupling": "Refactor & Decouple",
    "upgrade_legacy_databases": "Upgrade Legacy DB",
    "switch_db_engine_open_source": "Switch to OSS DB",
    "update_outdated_components": "Update Outdated Components",
    "switch_to_managed_db": "Switch to Managed DB",
    "managed_arm_db": "Managed ARM DB",
    "serverless_db_migration": "Serverless DB Migration",
    "switch_db_engine_postgresql": "Switch to PostgreSQL",
}

# ── Per-app markdown ───────────────────────────────────────────────────────────
def app_report(aid):
    app = apps[aid]
    ta = tech_assessments[aid]
    cx = complexities[aid]
    sa = scenario_assessments[aid]
    bc_app = bc_by_app.get(aid, {})

    name = app.get("app_name", aid)
    os_val = app.get("operating_system", "")
    db_val = app.get("database_engine", "")
    lang_val = app.get("programming_language", "")
    appserver = app.get("application_server", "N/A") or "N/A"
    arch = app.get("application_architecture", "unknown")
    deploy = app.get("deployment_type", "")
    containerized = app.get("is_containerized", "No")
    cicd = app.get("ci_cd_present", "No")
    users = app.get("user_count", 0)
    bu = app.get("business_unit", "")
    crit = app.get("business_criticality", "")
    envs = app.get("environment_count", 0)
    interfaces = app.get("external_interface_count", 0)
    servers = app.get("server_instances", [])
    db_gb = app.get("database_storage_gb", 0)
    db_lic = app.get("database_license_required", "No")

    lines = []
    lines.append(f"# {name} — Application Modernization Report\n")
    lines.append(f"> **Application ID:** {aid}  \n> **Business Unit:** {bu}  \n> **Criticality:** {crit}\n")

    lines.append("## Application Overview\n")
    lines.append("| Attribute | Value |")
    lines.append("|-----------|-------|")
    lines.append(f"| Application ID | {aid} |")
    lines.append(f"| Name | {name} |")
    lines.append(f"| Business Unit | {bu} |")
    lines.append(f"| Criticality | {crit} |")
    lines.append(f"| Status | {app.get('application_status', '')} |")
    lines.append(f"| Deployment Type | {deploy} |")
    lines.append(f"| Architecture | {arch} |")
    lines.append(f"| Containerized | {containerized} |")
    lines.append(f"| CI/CD | {cicd} |")
    lines.append(f"| Users | {users:,} |")
    lines.append(f"| Environments | {envs} |")
    lines.append(f"| External Interfaces | {interfaces} |")
    lines.append(f"| Servers | {', '.join(servers) if servers else 'N/A'} |")
    lines.append(f"| DB Storage (GB) | {db_gb} |")
    lines.append(f"| DB License Required | {db_lic} |")
    lines.append("")

    lines.append("## Technology Stack Assessment\n")
    lines.append("| Component | Name | Status |")
    lines.append("|-----------|------|--------|")
    for comp in ta["components"]:
        emoji = STATUS_EMOJI.get(comp["status"], "⚪")
        lines.append(f"| {comp['component_type']} | {comp['component_name']} | {emoji} {comp['status']} |")
    lines.append("")

    # Tech health pie chart
    counts = {
        "CURRENT_VERSION": ta["current_component_count"],
        "OUTDATED": ta["outdated_component_count"],
        "EOL": ta["eol_component_count"],
        "NO_KNOWLEDGE": ta["no_knowledge_component_count"],
    }
    has_data = any(v > 0 for v in counts.values())
    if has_data:
        lines.append("### Technology Health Distribution\n")
        lines.append("```mermaid")
        lines.append("pie title Technology Component Health")
        for k, v in counts.items():
            if v > 0:
                lines.append(f'    "{k}" : {v}')
        lines.append("```\n")

    lines.append("## Complexity Assessment\n")
    cx_level = cx["complexity_level"]
    cx_score = cx["complexity_score"]
    level_emoji = {"LOW": "🟢", "MEDIUM": "🟡", "HIGH": "🔴"}.get(cx_level, "⚪")
    lines.append(f"**Overall Complexity:** {level_emoji} **{cx_level}** (Score: {cx_score}/10)\n")
    lines.append("| Factor | Score | Weight |")
    lines.append("|--------|-------|--------|")
    cf = cx["contributing_factors"]
    w = cx["weights"]
    lines.append(f"| Technology Age | {cf['tech_age_score']} | {w['tech_age']*100:.0f}% |")
    lines.append(f"| Integration Complexity | {cf['integration_score']} | {w['integration']*100:.0f}% |")
    lines.append(f"| Infrastructure | {cf['infrastructure_score']} | {w['infrastructure']*100:.0f}% |")
    lines.append(f"| Business Criticality | {cf['criticality_score']} | {w['criticality']*100:.0f}% |")
    lines.append(f"| Architecture | {cf['architecture_score']} | {w['architecture']*100:.0f}% |")
    lines.append(f"| Data Complexity | {cf['data_score']} | {w['data']*100:.0f}% |")
    lines.append("")

    lines.append("## Modernization Scenarios\n")
    applicable = [s for s in sa["scenarios"] if s["status"] == "APPLICABLE"]
    if applicable:
        lines.append("### Applicable Scenarios\n")
        lines.append("| Scenario | Reasoning |")
        lines.append("|----------|-----------|")
        for s in applicable:
            label = SCENARIO_LABELS.get(s["scenario_id"], s["scenario_id"])
            lines.append(f"| {label} | {s['reasoning']} |")
        lines.append("")
    else:
        lines.append("*No applicable scenarios identified.*\n")

    lines.append("### All Scenario Statuses\n")
    lines.append("| Scenario | Status |")
    lines.append("|----------|--------|")
    for s in sa["scenarios"]:
        label = SCENARIO_LABELS.get(s["scenario_id"], s["scenario_id"])
        status = s["status"]
        s_emoji = {"APPLICABLE": "✅", "FULFILLED": "🔵", "NOT_APPLICABLE": "⬜", "BLOCKED": "🚫",
                   "PARTIALLY_FULFILLED": "🔷", "LACK_OF_DATA": "❓"}.get(status, "⬜")
        lines.append(f"| {label} | {s_emoji} {status} |")
    lines.append("")

    lines.append("## Financial Summary\n")
    if bc_app:
        total_cost = bc_app.get("total_estimated_cost", 0)
        total_savings = bc_app.get("total_estimated_annual_savings", 0)
        lines.append(f"| Metric | Value |")
        lines.append("|--------|-------|")
        lines.append(f"| Total Estimated Implementation Cost | ${total_cost:,.2f} |")
        lines.append(f"| Total Estimated Annual Savings | ${total_savings:,.2f} |")
        roi = round(total_cost / total_savings, 1) if total_savings > 0 else "N/A"
        lines.append(f"| Estimated ROI Payback Period | {roi} years |")
        lines.append("")

        if bc_app.get("scenarios"):
            lines.append("### Cost/Savings Breakdown by Scenario\n")
            lines.append("| Scenario | Est. Cost | Est. Annual Savings | ROI (years) |")
            lines.append("|----------|-----------|---------------------|-------------|")
            for s in bc_app["scenarios"]:
                label = SCENARIO_LABELS.get(s["scenario_id"], s["scenario_id"])
                cost = f"${s['estimated_cost']:,.2f}" if s.get("estimated_cost") is not None else "N/A"
                sav = f"${s['estimated_annual_savings']:,.2f}" if s.get("estimated_annual_savings") is not None else "N/A"
                roi_y = str(s["roi_years"]) if s.get("roi_years") is not None else "N/A"
                lines.append(f"| {label} | {cost} | {sav} | {roi_y} |")
            lines.append("")
    else:
        lines.append("*No financial data available.*\n")

    return "\n".join(lines)

for aid in IN_SCOPE:
    content = app_report(aid)
    out = APPS_DIR / f"{aid}.md"
    with open(out, "w") as f:
        f.write(content)
print(f"Per-app markdown: {len(IN_SCOPE)} files created")

# ── Portfolio report ───────────────────────────────────────────────────────────
def portfolio_report():
    lines = []
    lines.append("# Application Portfolio Modernization Report\n")
    lines.append("> Comprehensive analysis of the application portfolio modernization opportunities.\n")

    # Executive summary
    lines.append("## Executive Summary\n")
    total_apps = 30
    in_scope = len(IN_SCOPE)
    retired = len(RETIRED)
    ps = business_case["portfolio_summary"]

    lines.append(f"This report covers a portfolio of **{total_apps} applications**, of which **{in_scope} are in-scope** "
                 f"for modernization analysis. {retired} applications are retired and excluded from assessment.\n")
    lines.append(f"| Portfolio Metric | Value |")
    lines.append("|------------------|-------|")
    lines.append(f"| Total Applications | {total_apps} |")
    lines.append(f"| In-Scope Applications | {in_scope} |")
    lines.append(f"| Retired / Out-of-Scope | {retired} |")
    lines.append(f"| Total Estimated Modernization Cost | ${ps['total_estimated_cost']:,.2f} |")
    lines.append(f"| Total Estimated Annual Savings | ${ps['total_estimated_annual_savings']:,.2f} |")
    roi_y = f"{ps['estimated_roi_years']:.1f} years" if ps.get('estimated_roi_years') else "N/A"
    lines.append(f"| Portfolio ROI Payback | {roi_y} |")
    lines.append("")

    # Complexity distribution
    cx_levels = defaultdict(int)
    for aid in IN_SCOPE:
        cx_levels[complexities[aid]["complexity_level"]] += 1
    lines.append("## Complexity Distribution\n")
    lines.append("```mermaid")
    lines.append("pie title Application Complexity Distribution")
    for k in ["LOW", "MEDIUM", "HIGH"]:
        if cx_levels[k]:
            lines.append(f'    "{k}" : {cx_levels[k]}')
    lines.append("```\n")

    lines.append("| Complexity Level | Count | Description |")
    lines.append("|-----------------|-------|-------------|")
    lines.append(f"| 🟢 LOW (1-3) | {cx_levels['LOW']} | Minimal modernization effort required |")
    lines.append(f"| 🟡 MEDIUM (4-6) | {cx_levels['MEDIUM']} | Moderate effort with clear modernization path |")
    lines.append(f"| 🔴 HIGH (7-10) | {cx_levels['HIGH']} | Significant effort, legacy components |")
    lines.append("")

    # Tech health distribution
    tech_counts = defaultdict(int)
    for aid in IN_SCOPE:
        ta = tech_assessments[aid]
        tech_counts["CURRENT_VERSION"] += ta["current_component_count"]
        tech_counts["OUTDATED"] += ta["outdated_component_count"]
        tech_counts["EOL"] += ta["eol_component_count"]
        tech_counts["NO_KNOWLEDGE"] += ta["no_knowledge_component_count"]
    total_comps = sum(tech_counts.values())

    lines.append("## Portfolio Technology Health\n")
    lines.append("```mermaid")
    lines.append("pie title Portfolio Technology Component Health")
    for k in ["CURRENT_VERSION", "OUTDATED", "EOL", "NO_KNOWLEDGE"]:
        if tech_counts[k]:
            lines.append(f'    "{k}" : {tech_counts[k]}')
    lines.append("```\n")

    lines.append(f"Total technology components assessed: **{total_comps}** across {in_scope} applications.\n")
    lines.append("| Status | Count | Percentage |")
    lines.append("|--------|-------|-----------|")
    for k in ["CURRENT_VERSION", "OUTDATED", "EOL", "NO_KNOWLEDGE"]:
        pct = round(tech_counts[k] / total_comps * 100, 1) if total_comps else 0
        emoji = STATUS_EMOJI.get(k, "⚪")
        lines.append(f"| {emoji} {k} | {tech_counts[k]} | {pct}% |")
    lines.append("")

    # Scenario popularity
    scenario_counts = defaultdict(int)
    for aid in IN_SCOPE:
        for s in scenario_assessments[aid]["scenarios"]:
            if s["status"] == "APPLICABLE":
                scenario_counts[s["scenario_id"]] += 1

    sorted_scenarios = sorted(scenario_counts.items(), key=lambda x: x[1], reverse=True)
    lines.append("## Top Modernization Scenarios\n")
    lines.append("```mermaid")
    lines.append("xychart-beta")
    lines.append('    title "Top Applicable Scenarios (Count of Apps)"')
    labels = [f'"{SCENARIO_LABELS.get(s, s)[:20]}"' for s, _ in sorted_scenarios[:8]]
    vals = [str(c) for _, c in sorted_scenarios[:8]]
    lines.append(f"    x-axis [{', '.join(labels)}]")
    lines.append(f"    bar [{', '.join(vals)}]")
    lines.append("```\n")

    lines.append("| Scenario | Applicable Apps | Description |")
    lines.append("|----------|----------------|-------------|")
    for sid, count in sorted_scenarios:
        label = SCENARIO_LABELS.get(sid, sid)
        lines.append(f"| {label} | {count} | — |")
    lines.append("")

    # Scenario matrix
    lines.append("## Scenario Applicability Matrix\n")
    scenario_ids = [s["scenario_id"] for s in scenario_assessments[IN_SCOPE[0]]["scenarios"]]
    header_labels = [SCENARIO_LABELS.get(s, s)[:18] for s in scenario_ids]

    STATUS_SHORT = {
        "APPLICABLE": "✅",
        "FULFILLED": "🔵",
        "NOT_APPLICABLE": "⬜",
        "BLOCKED": "🚫",
        "PARTIALLY_FULFILLED": "🔷",
        "LACK_OF_DATA": "❓",
    }

    lines.append("| App ID | " + " | ".join(header_labels[:7]) + " |")
    lines.append("|--------|" + "|".join(["---"] * 7) + "|")
    for aid in IN_SCOPE:
        sa = scenario_assessments[aid]
        row_parts = []
        for s in sa["scenarios"][:7]:
            row_parts.append(STATUS_SHORT.get(s["status"], "⬜"))
        lines.append(f"| {aid} | " + " | ".join(row_parts) + " |")
    lines.append("")

    lines.append("| App ID | " + " | ".join(header_labels[7:]) + " |")
    lines.append("|--------|" + "|".join(["---"] * len(header_labels[7:])) + "|")
    for aid in IN_SCOPE:
        sa = scenario_assessments[aid]
        row_parts = []
        for s in sa["scenarios"][7:]:
            row_parts.append(STATUS_SHORT.get(s["status"], "⬜"))
        lines.append(f"| {aid} | " + " | ".join(row_parts) + " |")
    lines.append("")

    # Legend
    lines.append("**Legend:** ✅ APPLICABLE | 🔵 FULFILLED | ⬜ NOT_APPLICABLE | 🚫 BLOCKED | 🔷 PARTIALLY_FULFILLED | ❓ LACK_OF_DATA\n")

    # Financial summary
    lines.append("## Portfolio Financial Summary\n")
    lines.append("| Application | Name | Complexity | Est. Cost | Est. Annual Savings | ROI (yrs) |")
    lines.append("|-------------|------|-----------|-----------|---------------------|-----------|")
    for a in business_case["applications"]:
        aid = a["application_identifier"]
        name = apps[aid].get("app_name", "")
        cx_lvl = a["complexity_level"]
        cost = f"${a['total_estimated_cost']:,.0f}"
        sav = f"${a['total_estimated_annual_savings']:,.0f}"
        roi = f"{round(a['total_estimated_cost']/a['total_estimated_annual_savings'],1)}" if a['total_estimated_annual_savings'] > 0 else "N/A"
        lines.append(f"| {aid} | {name} | {cx_lvl} | {cost} | {sav} | {roi} |")
    lines.append("")
    lines.append(f"**Portfolio Total:** ${ps['total_estimated_cost']:,.2f} implementation cost | "
                 f"${ps['total_estimated_annual_savings']:,.2f} annual savings | {roi_y} payback\n")

    # Per-app complexity table
    lines.append("## Application Complexity Details\n")
    lines.append("| App ID | Name | OS Status | DB Status | Lang Status | Score | Level |")
    lines.append("|--------|------|-----------|-----------|-------------|-------|-------|")
    for aid in IN_SCOPE:
        app = apps[aid]
        ta = tech_assessments[aid]
        cx = complexities[aid]
        comps_by_type = {c["component_type"]: c["status"] for c in ta["components"]}
        os_s = STATUS_EMOJI.get(comps_by_type.get("Operating System", "NO_KNOWLEDGE"), "⚪")
        db_s = STATUS_EMOJI.get(comps_by_type.get("Database", "NO_KNOWLEDGE"), "⚪")
        lang_s = STATUS_EMOJI.get(comps_by_type.get("Programming Language", "NO_KNOWLEDGE"), "⚪")
        cx_emoji = {"LOW": "🟢", "MEDIUM": "🟡", "HIGH": "🔴"}.get(cx["complexity_level"], "⚪")
        lines.append(f"| {aid} | {app.get('app_name','')} | {os_s} | {db_s} | {lang_s} | {cx['complexity_score']} | {cx_emoji} {cx['complexity_level']} |")
    lines.append("")

    return "\n".join(lines)

content = portfolio_report()
out = REPORTS_DIR / "portfolio_report.md"
with open(out, "w") as f:
    f.write(content)
print("Portfolio report created: discover/output/reports/portfolio_report.md")

print("\nAll markdown reports generated!")
