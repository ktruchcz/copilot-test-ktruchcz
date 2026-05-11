#!/usr/bin/env python3
"""Generate Markdown reports for all in-scope applications"""
import json
import os
from datetime import datetime
from pathlib import Path

BASE = Path("/home/runner/work/copilot-test-ktruchcz/copilot-test-ktruchcz")
OUT = BASE / "discover/output"

# Load data
def load_json(path):
    try:
        with open(path) as f:
            return json.load(f)
    except:
        return {}

# Get all in-scope apps
app_ids = []
for f in sorted((OUT / "out_of_scope_results").glob("out_of_scope_app*.json")):
    d = load_json(f)
    if not d.get("out_of_scope", False):
        app_ids.append(d["application_identifier"])

print(f"Generating reports for {len(app_ids)} in-scope applications")

# Load business case
bc = load_json(OUT / "business_case_results/business_case.json")
app_bc_map = {a["app_id"]: a for a in bc.get("application_details", [])}

# Load scenario metadata
with open(BASE / ".github/skills/scenario-analysis/references/modernization_scenarios_list.json") as f:
    scenarios_list = json.load(f)
scenario_meta = {s["scenario_id"]: s for s in scenarios_list}

STATUS_EMOJI = {
    "CURRENT_VERSION": "🟢",
    "OUTDATED": "🟡",
    "EOL": "🔴",
    "NO_KNOWLEDGE": "⚪"
}

SCENARIO_STATUS_EMOJI = {
    "APPLICABLE": "✅",
    "FULFILLED": "✔️",
    "PARTIALLY_FULFILLED": "🔶",
    "NOT_APPLICABLE": "❌",
    "BLOCKED": "🚫",
    "LACK_OF_DATA": "❓"
}

def generate_app_report(app_id):
    schema = load_json(OUT / f"applications/consolidated_schema/consolidated_schema_application_{app_id}.json")
    internal = load_json(OUT / f"applications/internal_app_model/internal_app_model_application_{app_id}.json")
    tech = load_json(OUT / f"technology_assessment/technology_assessment_{app_id}.json")
    compl = load_json(OUT / f"complexity_results/complexity_{app_id}.json")
    scen = load_json(OUT / f"scenario_applicability_results/scenario_assessment_{app_id}.json")
    app_bc = app_bc_map.get(app_id, {})
    
    app_name = schema.get("name", app_id)
    today = datetime.now().strftime("%Y-%m-%d")
    
    # Complexity level
    cs = compl.get("complexity_score", 5)
    if cs <= 3: clevel = "LOW"
    elif cs <= 6: clevel = "MEDIUM"
    else: clevel = "HIGH"
    
    # Technology health counts
    comps = tech.get("components_analyzed", [])
    current_count = sum(1 for c in comps if c["component_status"] == "CURRENT_VERSION")
    outdated_count = sum(1 for c in comps if c["component_status"] == "OUTDATED")
    eol_count = sum(1 for c in comps if c["component_status"] == "EOL")
    missing_count = sum(1 for c in comps if c["component_status"] == "NO_KNOWLEDGE")
    
    # Server count
    servers = schema.get("Physical servers instances", "")
    if isinstance(servers, list): srv_count = len(servers)
    elif isinstance(servers, str) and servers: srv_count = len([s for s in servers.split(",") if s.strip()])
    else: srv_count = "N/A"
    
    lines = []
    lines.append(f"# Application Report: {app_name}")
    lines.append(f"")
    lines.append(f"**ID:** {app_id}  ")
    lines.append(f"**Generated:** {today}")
    lines.append(f"")
    lines.append(f"## Overview")
    lines.append(f"")
    lines.append(f"| Attribute | Value |")
    lines.append(f"|-----------|-------|")
    lines.append(f"| Business Unit | {schema.get('business unit', 'N/A')} |")
    lines.append(f"| Solution Type | {schema.get('Solution type', 'N/A')} |")
    lines.append(f"| Deployment Type | {schema.get('Deployment type', 'N/A')} |")
    lines.append(f"| Business Criticality | {schema.get('criticality', 'N/A')} |")
    lines.append(f"| Users | {schema.get('number of users', 'N/A')} |")
    lines.append(f"| Servers | {srv_count} |")
    lines.append(f"| Architecture | {schema.get('Application Architecture', 'N/A')} |")
    lines.append(f"| Containerized | {schema.get('Application is containerized', 'N/A')} |")
    lines.append(f"| CI/CD | {schema.get('CI_CD present', 'N/A')} |")
    lines.append(f"| Data Classification | {schema.get('data classification', 'N/A')} |")
    lines.append(f"")
    lines.append(f"## Technology Stack")
    lines.append(f"")
    lines.append(f"| Component | Technology | Status |")
    lines.append(f"|-----------|-----------|--------|")
    
    for comp in comps:
        badge = STATUS_EMOJI.get(comp["component_status"], "⚪")
        lines.append(f"| {comp['component_type'].replace('_',' ').title()} | {comp['component_name']} | {badge} {comp['component_status']} |")
    
    lines.append(f"")
    lines.append(f"```mermaid")
    lines.append(f"pie title Technology Health")
    if current_count: lines.append(f'    "Current" : {current_count}')
    if outdated_count: lines.append(f'    "Outdated" : {outdated_count}')
    if eol_count: lines.append(f'    "End of Life" : {eol_count}')
    if missing_count: lines.append(f'    "Missing Version" : {missing_count}')
    lines.append(f"```")
    lines.append(f"")
    lines.append(f"## Complexity Assessment")
    lines.append(f"")
    lines.append(f"**Score:** {cs}/10 — **{clevel}**  ")
    lines.append(f"**Confidence:** {compl.get('confidence', 7)}")
    lines.append(f"")
    lines.append(f"> {compl.get('reasoning', '')}")
    lines.append(f"")
    
    # Contributing factors
    cf = compl.get("contributing_factors", {})
    lines.append(f"| Factor | Value |")
    lines.append(f"|--------|-------|")
    lines.append(f"| Servers | {cf.get('number_of_servers', 'N/A')} |")
    lines.append(f"| Interfaces | {cf.get('number_of_interfaces', 'N/A')} |")
    lines.append(f"| Environments | {cf.get('number_of_environments', 'N/A')} |")
    lines.append(f"| EOL Technologies | {cf.get('number_of_eol_technologies', 0)} |")
    lines.append(f"| Outdated Technologies | {cf.get('number_of_outdated_technologies', 0)} |")
    lines.append(f"| CI/CD Present | {cf.get('ci_cd_present', 'N/A')} |")
    lines.append(f"| Containerized | {cf.get('containerized', 'N/A')} |")
    lines.append(f"")
    lines.append(f"## Modernization Scenarios")
    lines.append(f"")
    
    # Scenario details
    scen_details = scen.get("scenarios_detailed", [])
    applicable = [s for s in scen_details if s["status"] == "APPLICABLE"]
    other = [s for s in scen_details if s["status"] != "APPLICABLE"]
    
    # Map scenario costs
    bc_scens = {s["scenario_id"]: s for s in app_bc.get("scenarios", [])}
    
    if applicable:
        lines.append(f"### Applicable Scenarios")
        lines.append(f"")
        for s in applicable:
            sid = s["id"]
            meta = scenario_meta.get(sid, {})
            sbc = bc_scens.get(sid, {})
            lines.append(f"#### ✅ {meta.get('scenario_name', sid)}")
            lines.append(f"")
            lines.append(f"- **Priority:** {meta.get('priority', 'N/A')}")
            lines.append(f"- **Effort:** {meta.get('effort', 'N/A')}")
            lines.append(f"- **Effects:** {', '.join(meta.get('modernization_effects', []))}")
            if sbc:
                lines.append(f"- **Cost:** €{sbc.get('adjusted_cost', 0):,} (one-time)")
                lines.append(f"- **Annual Savings:** €{sbc.get('adjusted_yearly_savings', 0):,}/year")
            lines.append(f"- **Reasoning:** {s.get('reason', '')}")
            lines.append(f"")
    
    if other:
        lines.append(f"### Other Scenarios")
        lines.append(f"")
        lines.append(f"| Scenario | Status | Reason |")
        lines.append(f"|----------|--------|--------|")
        for s in other:
            sid = s["id"]
            meta = scenario_meta.get(sid, {})
            emoji = SCENARIO_STATUS_EMOJI.get(s["status"], "")
            reason = s.get("reason", "")[:100]
            lines.append(f"| {meta.get('scenario_name', sid)} | {emoji} {s['status']} | {reason} |")
        lines.append(f"")
    
    # Financial summary
    if app_bc:
        lines.append(f"## Financial Summary")
        lines.append(f"")
        lines.append(f"| Metric | Value |")
        lines.append(f"|--------|-------|")
        lines.append(f"| Total One-Time Cost | €{app_bc.get('total_cost', 0):,} |")
        lines.append(f"| Total Yearly Savings | €{app_bc.get('total_yearly_savings', 0):,} |")
        roi = app_bc.get('roi_years')
        lines.append(f"| Break-Even | {f'{roi} years' if roi else 'N/A'} |")
        lines.append(f"")
    
    return "\n".join(lines)

# Generate per-app reports
for app_id in app_ids:
    report = generate_app_report(app_id)
    path = OUT / f"reports/apps/{app_id}_report.md"
    with open(path, "w") as f:
        f.write(report)

print(f"Generated {len(app_ids)} app reports")

# ============================================================
# Portfolio report
# ============================================================

# Load all data for portfolio
all_schemas = {app_id: load_json(OUT / f"applications/consolidated_schema/consolidated_schema_application_{app_id}.json") for app_id in app_ids}
all_tech = {app_id: load_json(OUT / f"technology_assessment/technology_assessment_{app_id}.json") for app_id in app_ids}
all_compl = {app_id: load_json(OUT / f"complexity_results/complexity_{app_id}.json") for app_id in app_ids}
all_scen = {app_id: load_json(OUT / f"scenario_applicability_results/scenario_assessment_{app_id}.json") for app_id in app_ids}

today = datetime.now().strftime("%Y-%m-%d")
ps = bc["portfolio_summary"]

# Complexity distribution
low_c = sum(1 for a in app_ids if all_compl[a].get("complexity_score",5) <= 3)
med_c = sum(1 for a in app_ids if 4 <= all_compl[a].get("complexity_score",5) <= 6)
high_c = sum(1 for a in app_ids if all_compl[a].get("complexity_score",5) >= 7)

# Tech health totals
total_current = sum(sum(1 for c in all_tech[a].get("components_analyzed",[]) if c["component_status"]=="CURRENT_VERSION") for a in app_ids)
total_outdated = sum(sum(1 for c in all_tech[a].get("components_analyzed",[]) if c["component_status"]=="OUTDATED") for a in app_ids)
total_eol = sum(sum(1 for c in all_tech[a].get("components_analyzed",[]) if c["component_status"]=="EOL") for a in app_ids)
total_missing = sum(sum(1 for c in all_tech[a].get("components_analyzed",[]) if c["component_status"]=="NO_KNOWLEDGE") for a in app_ids)

# Top scenarios
scen_summary = sorted(bc["scenarios_summary"], key=lambda x: x["applicable_count"], reverse=True)

# Scenario applicability matrix
all_scenario_ids = [s["scenario_id"] for s in scenarios_list]
matrix_scenarios = all_scenario_ids[:7]  # limit for readability

lines = []
lines.append("# Portfolio Modernization Report")
lines.append("")
lines.append(f"**Generated:** {today}  ")
lines.append(f"**Applications Analyzed:** {len(app_ids)} in-scope ({len(app_ids)+5} total, 5 out-of-scope)")
lines.append("")
lines.append("## Executive Summary")
lines.append("")
lines.append(f"This portfolio analysis covers {len(app_ids)} in-scope applications across multiple business units. "
             f"Technology assessment reveals significant modernization needs: {total_eol} EOL components and "
             f"{total_outdated} outdated components were identified. "
             f"{high_c} applications scored HIGH complexity and {med_c} scored MEDIUM, indicating substantial "
             f"transformation effort is required. "
             f"A total of {ps['total_applicable_scenarios']} modernization scenarios are applicable across the portfolio, "
             f"with an estimated total investment of €{ps['total_one_time_costs']:,} yielding annual savings of "
             f"€{ps['total_yearly_savings']:,} and a portfolio break-even of {ps['roi_years']} years.")
lines.append("")
lines.append("## Portfolio Overview")
lines.append("")
lines.append("```mermaid")
lines.append("pie title Complexity Distribution")
if low_c: lines.append(f'    "Low (1-3)" : {low_c}')
if med_c: lines.append(f'    "Medium (4-6)" : {med_c}')
if high_c: lines.append(f'    "High (7-10)" : {high_c}')
lines.append("```")
lines.append("")
lines.append("```mermaid")
lines.append("pie title Technology Health")
if total_current: lines.append(f'    "Current" : {total_current}')
if total_outdated: lines.append(f'    "Outdated" : {total_outdated}')
if total_eol: lines.append(f'    "End of Life" : {total_eol}')
if total_missing: lines.append(f'    "Unknown" : {total_missing}')
lines.append("```")
lines.append("")
lines.append("## Top Modernization Opportunities")
lines.append("")
lines.append("```mermaid")
lines.append("graph LR")
high_prio = [s for s in scen_summary if scenario_meta.get(s["scenario_id"],{}).get("priority","") == "High"][:4]
med_prio = [s for s in scen_summary if scenario_meta.get(s["scenario_id"],{}).get("priority","") == "Medium"][:4]
if high_prio:
    lines.append('    subgraph "High Priority"')
    for s in high_prio:
        nid = s["scenario_id"].replace("_","")
        lines.append(f'        {nid}["{scenario_meta.get(s["scenario_id"],{}).get("scenario_name",s["scenario_id"])} ({s["applicable_count"]} apps)"]')
    lines.append("    end")
if med_prio:
    lines.append('    subgraph "Medium Priority"')
    for s in med_prio:
        nid = s["scenario_id"].replace("_","")
        lines.append(f'        {nid}["{scenario_meta.get(s["scenario_id"],{}).get("scenario_name",s["scenario_id"])} ({s["applicable_count"]} apps)"]')
    lines.append("    end")
lines.append("```")
lines.append("")
lines.append("| Scenario | Applicable Apps | Priority | Total Cost | Yearly Savings | ROI |")
lines.append("|----------|----------------|----------|------------|---------------|-----|")
for s in scen_summary[:8]:
    meta = scenario_meta.get(s["scenario_id"], {})
    roi = f"{s['roi_years']}y" if s['roi_years'] else "N/A"
    lines.append(f"| {meta.get('scenario_name',s['scenario_id'])} | {s['applicable_count']} | {meta.get('priority','N/A')} | €{s['total_cost']:,} | €{s['total_yearly_savings']:,} | {roi} |")
lines.append("")

# Scenario applicability matrix  
lines.append("## Scenario Applicability Matrix")
lines.append("")
header_scenarios = scen_summary[:6]
header_ids = [s["scenario_id"] for s in header_scenarios]
header_names = [scenario_meta.get(sid,{}).get("scenario_name",sid)[:20] for sid in header_ids]

lines.append("| Application | " + " | ".join(header_names) + " |")
lines.append("|-------------|" + "|".join([":---:"] * len(header_ids)) + "|")

for app_id in app_ids:
    schema = all_schemas[app_id]
    app_name = schema.get("name", app_id)[:25]
    scen_d = {s["id"]: s["status"] for s in all_scen[app_id].get("scenarios_detailed", [])}
    cells = []
    for sid in header_ids:
        status = scen_d.get(sid, "LACK_OF_DATA")
        cells.append(SCENARIO_STATUS_EMOJI.get(status, "❓"))
    lines.append(f"| {app_name} | " + " | ".join(cells) + " |")

lines.append("")
lines.append("Legend: ✅ Applicable | ❌ Not Applicable | ✔️ Fulfilled | 🔶 Partially Fulfilled | 🚫 Blocked | ❓ Unknown")
lines.append("")
lines.append("## Financial Summary")
lines.append("")
lines.append("| Metric | Value |")
lines.append("|--------|-------|")
lines.append(f"| Total One-Time Investment | €{ps['total_one_time_costs']:,} |")
lines.append(f"| Total Annual Savings | €{ps['total_yearly_savings']:,} |")
lines.append(f"| Portfolio Break-Even | {ps['roi_years']} years |")
lines.append(f"| Applications with Opportunities | {ps['applications_with_opportunities']} / {ps['total_applications_assessed']} |")
lines.append(f"| Total Applicable Scenarios | {ps['total_applicable_scenarios']} |")
lines.append("")
lines.append("```mermaid")
lines.append("graph TD")
lines.append(f'    A["💰 Investment: €{ps["total_one_time_costs"]:,}"] --> B["📈 Annual Savings: €{ps["total_yearly_savings"]:,}"]')
lines.append(f'    B --> C["⏱️ Break-Even: {ps["roi_years"]} years"]')
lines.append("```")
lines.append("")

# Risk applications - top by complexity
risk_apps = sorted(app_ids, key=lambda a: all_compl[a].get("complexity_score",5), reverse=True)[:10]
lines.append("## Risk Applications")
lines.append("")
lines.append("| Application | Complexity | EOL Components | Applicable Scenarios |")
lines.append("|-------------|-----------|---------------|---------------------|")
for app_id in risk_apps:
    schema = all_schemas[app_id]
    app_name = schema.get("name", app_id)
    cs = all_compl[app_id].get("complexity_score", 5)
    if cs <= 3: lvl = "LOW"
    elif cs <= 6: lvl = "MEDIUM"
    else: lvl = "HIGH"
    eol_c = sum(1 for c in all_tech[app_id].get("components_analyzed",[]) if c["component_status"]=="EOL")
    appl_c = sum(1 for s in all_scen[app_id].get("scenarios_detailed",[]) if s["status"]=="APPLICABLE")
    lines.append(f"| {app_name} | {cs}/10 ({lvl}) | {eol_c} | {appl_c} |")
lines.append("")
lines.append("## Per-Application Reports")
lines.append("")
lines.append("| Application | ID | Complexity | Report |")
lines.append("|-------------|-----|-----------|--------|")
for app_id in app_ids:
    schema = all_schemas[app_id]
    app_name = schema.get("name", app_id)
    cs = all_compl[app_id].get("complexity_score", 5)
    if cs <= 3: lvl = "LOW"
    elif cs <= 6: lvl = "MEDIUM"
    else: lvl = "HIGH"
    lines.append(f"| {app_name} | {app_id} | {cs}/10 ({lvl}) | [View Report](apps/{app_id}_report.md) |")

portfolio_report = "\n".join(lines)
with open(OUT / "reports/portfolio_report.md", "w") as f:
    f.write(portfolio_report)

print("Portfolio report generated")
print("All markdown reports complete!")
