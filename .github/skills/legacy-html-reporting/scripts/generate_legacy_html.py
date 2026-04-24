#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
from datetime import datetime, timezone
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
REFERENCES_DIR = SCRIPT_DIR.parent / "references"
LOGO_SVG = (REFERENCES_DIR / "logo.svg").read_text(encoding="utf-8").strip()


def slugify(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-") or "section"


def parse_markdown(markdown_text: str) -> dict:
    lines = markdown_text.splitlines()
    title = ""
    lead = ""
    sections: list[dict] = []
    current: dict | None = None
    intro: list[str] = []

    for raw_line in lines:
        line = raw_line.rstrip()
        if line.startswith("# ") and not title:
            title = line[2:].strip()
            continue
        if line.startswith("## "):
            current = {
                "title": line[3:].strip(),
                "blocks": [],
            }
            sections.append(current)
            continue
        if current is None:
            intro.append(line)
        else:
            current["blocks"].append(line)

    intro_lines = [line.strip() for line in intro if line.strip()]
    if intro_lines:
        lead = intro_lines[0]

    normalized_sections = []
    for section in sections:
        normalized_sections.append(
            {
                "title": section["title"],
                "slug": slugify(section["title"]),
                "html": render_markdown_blocks(section["blocks"]),
            }
        )

    return {
        "title": title,
        "lead": lead,
        "sections": normalized_sections,
    }


def render_markdown_blocks(lines: list[str]) -> str:
    blocks: list[str] = []
    buffer: list[str] = []
    list_items: list[str] = []
    in_code = False
    code_buffer: list[str] = []

    def flush_paragraph() -> None:
        nonlocal buffer
        if not buffer:
            return
        text = " ".join(part.strip() for part in buffer if part.strip())
        if text:
            blocks.append(f"<p>{inline_markdown(text)}</p>")
        buffer = []

    def flush_list() -> None:
        nonlocal list_items
        if not list_items:
            return
        items = "".join(f"<li>{inline_markdown(item)}</li>" for item in list_items)
        blocks.append(f"<ul>{items}</ul>")
        list_items = []

    def flush_code() -> None:
        nonlocal code_buffer
        code = "\n".join(code_buffer)
        blocks.append(f"<pre><code>{html.escape(code)}</code></pre>")
        code_buffer = []

    for raw_line in lines:
        line = raw_line.rstrip("\n")
        if line.startswith("```"):
            flush_paragraph()
            flush_list()
            if in_code:
                flush_code()
                in_code = False
            else:
                in_code = True
            continue
        if in_code:
            code_buffer.append(line)
            continue
        if not line.strip():
            flush_paragraph()
            flush_list()
            continue
        if line.startswith("### "):
            flush_paragraph()
            flush_list()
            blocks.append(f"<h3>{inline_markdown(line[4:].strip())}</h3>")
            continue
        if re.match(r"^[-*] ", line):
            flush_paragraph()
            list_items.append(line[2:].strip())
            continue
        if "|" in line and line.strip().startswith("|") and line.strip().endswith("|"):
            flush_paragraph()
            flush_list()
            table_html = render_pipe_table([line])
            if table_html:
                blocks.append(table_html)
            continue
        buffer.append(line)

    flush_paragraph()
    flush_list()
    if in_code:
        flush_code()
    return "\n".join(blocks)


def render_pipe_table(lines: list[str]) -> str | None:
    rows = []
    for line in lines:
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if cells and not all(re.fullmatch(r":?-{3,}:?", cell) for cell in cells):
            rows.append(cells)
    if not rows:
        return None
    if len(rows) == 1:
        return f"<p>{inline_markdown(' | '.join(rows[0]))}</p>"
    header = "".join(f"<th>{inline_markdown(cell)}</th>" for cell in rows[0])
    body = "".join(
        "<tr>" + "".join(f"<td>{inline_markdown(cell)}</td>" for cell in row) + "</tr>"
        for row in rows[1:]
    )
    return f"<table><thead><tr>{header}</tr></thead><tbody>{body}</tbody></table>"


def inline_markdown(text: str) -> str:
    escaped = html.escape(text)
    escaped = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", escaped)
    escaped = re.sub(r"`([^`]+)`", r"<code>\1</code>", escaped)
    escaped = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2" target="_blank">\1</a>', escaped)
    return escaped


def extract_app_id(path: Path) -> str:
    match = re.search(r"(app\d+)", path.stem)
    return match.group(1) if match else path.stem


def normalize_application_name(title: str, app_id: str) -> str:
    if not title:
        return app_id
    normalized = title.strip()
    normalized = re.sub(r"^Application Report\s*[-:]\s*", "", normalized, flags=re.IGNORECASE)
    return normalized.strip() or app_id


def analysis_id(*parts: str) -> str:
    digest = hashlib.md5()
    for part in parts:
        digest.update(part.encode("utf-8"))
    return digest.hexdigest()


def build_payload(kind: str, title: str, lead: str, sections: list[dict], extra: dict | None = None) -> dict:
    payload = {
        "kind": kind,
        "title": title,
        "lead": lead,
        "customer_name": "Client",
        "subtitle": "Application modernization with Agentic AI powered by Capgemini GenSuite",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "sections": sections,
    }
    if extra:
        payload.update(extra)
    payload["analysis_id"] = analysis_id(kind, title, payload["generated_at"])
    return payload


def read_json_file(path: Path) -> dict | list | None:
        if not path.exists():
                return None
        return json.loads(path.read_text(encoding="utf-8"))


def scenario_label(scenario_id: str) -> str:
        labels = {
                "app_refactor_decoupling": "Application Refactoring",
                "app_containerization": "Application Containerization",
                "upgrade_legacy_databases": "Upgrade Legacy Databases",
                "application_server_replacement": "Application Server Replacement",
                "app_deployment_to_cloud": "Application Deployment to Public Cloud",
                "os_update_security_patch": "Operating System Update",
                "switch_to_standard_linux_os": "Switch to Standard Linux OS",
                "switch_db_engine_open_source": "Switch DB Engine to Open Source",
                "update_outdated_components": "Update Outdated Components",
                "switch_to_arm_cpu": "Switch to ARM-Based CPU",
        }
        if scenario_id in labels:
                return labels[scenario_id]
        return scenario_id.replace("_", " ").title()


def format_compact_eur(value: float | int) -> str:
        amount = float(value)
        if abs(amount) >= 1_000_000:
                formatted = f"{amount / 1_000_000:.2f}".rstrip("0").rstrip(".")
                return f"{formatted}MEUR"
        if abs(amount) >= 1_000:
                formatted = f"{amount / 1_000:.1f}".rstrip("0").rstrip(".")
                return f"{formatted}kEUR"
        return f"EUR{int(round(amount))}"


def format_roi_label(years: float | int | None) -> tuple[str, str]:
        if years is None:
                return "n/a", "Until positive ROI"
        years_float = float(years)
        if years_float < 1:
                months = max(1, int(round(years_float * 12)))
                return str(months), "months"
        return f"{years_float:.1f}".rstrip("0").rstrip("."), "years"


def format_percent(value: float) -> str:
        return f"{round(value * 100)}%"


def extract_markdown_number(markdown_text: str, pattern: str) -> int | None:
        match = re.search(pattern, markdown_text, flags=re.IGNORECASE)
        if not match:
                return None
        return int(match.group(1))


def load_portfolio_dashboard_data(markdown_text: str, output_dir: Path, app_reports: list[dict]) -> dict:
        business_case = read_json_file(output_dir.parent / "business_case_results" / "business_case.json") or {}
        portfolio_summary = business_case.get("portfolio_summary", {})
        finance_scenarios = business_case.get("scenarios_summary", [])

        total_in_scope = portfolio_summary.get("total_applications_assessed", len(app_reports))
        total_portfolio = extract_markdown_number(markdown_text, r"Total Portfolio:\s*(\d+)") or total_in_scope
        out_of_scope = extract_markdown_number(markdown_text, r"\((\d+) out-of-scope")
        if out_of_scope is None:
                out_of_scope = max(total_portfolio - total_in_scope, 0)

        technology_dir = output_dir.parent / "technology_assessment"
        technology_files = sorted(technology_dir.glob("technology_assessment_*.json"))
        apps_with_eol = 0
        apps_with_outdated = 0
        apps_with_missing_versions = 0
        for tech_file in technology_files:
                technology = read_json_file(tech_file) or {}
                if technology.get("has_eol_components"):
                        apps_with_eol += 1
                if technology.get("has_outdated_components"):
                        apps_with_outdated += 1
                if technology.get("has_missing_version_data"):
                        apps_with_missing_versions += 1

        scenario_dir = output_dir.parent / "scenario_applicability_results"
        scenario_files = sorted(scenario_dir.glob("scenario_assessment_*.json"))
        applicable_statuses = {"APPLICABLE", "PARTIALLY_FULFILLED", "FULFILLED"}
        scenario_counts: dict[str, dict] = {}
        app_scenario_counts: dict[str, int] = {}
        unknown_scenarios = 0
        total_scenarios = 0
        for scenario_file in scenario_files:
                scenario_data = read_json_file(scenario_file) or {}
                app_id = scenario_data.get("application_identifier", extract_app_id(scenario_file))
                detailed = scenario_data.get("scenarios_detailed", [])
                total_scenarios += len(detailed)
                app_scenario_counts[app_id] = 0
                for scenario in detailed:
                        status = scenario.get("status")
                        total_scenarios += 0
                        if status == "LACK_OF_DATA":
                                unknown_scenarios += 1
                        if status not in applicable_statuses:
                                continue
                        scenario_id = scenario.get("id", "unknown")
                        scenario_counts.setdefault(
                                scenario_id,
                                {"scenario_id": scenario_id, "scenario_name": scenario_label(scenario_id), "applicable_count": 0, "app_ids": []},
                        )
                        scenario_counts[scenario_id]["applicable_count"] += 1
                        scenario_counts[scenario_id]["app_ids"].append(app_id)
                        app_scenario_counts[app_id] += 1

        data_completeness = 1.0
        if total_scenarios:
                data_completeness = (total_scenarios - unknown_scenarios) / total_scenarios

        app_name_by_id = {app["app_id"]: app["title"] for app in app_reports}
        complexity_by_app = {
                detail.get("app_id"): detail.get("complexity_score", 0)
                for detail in business_case.get("application_details", [])
        }
        priority_apps = []
        for tech_file in technology_files:
                technology = read_json_file(tech_file) or {}
                app_id = technology.get("application_identifier", extract_app_id(tech_file))
                priority_apps.append(
                        {
                                "app_id": app_id,
                                "title": app_name_by_id.get(app_id, app_id),
                                "status": "EOL" if technology.get("has_eol_components") else "OUTDATED",
                                "scenario_count": app_scenario_counts.get(app_id, 0),
                                "complexity": complexity_by_app.get(app_id, 0),
                                "score": (
                                        10 if technology.get("has_eol_components") else 0,
                                        5 if technology.get("has_outdated_components") else 0,
                                        app_scenario_counts.get(app_id, 0),
                                        complexity_by_app.get(app_id, 0),
                                ),
                        }
                )
        priority_apps.sort(key=lambda item: item["score"], reverse=True)
        priority_apps = priority_apps[:5]

        category_map = {
                "cost_reduction": {
                        "title": "Cost Reduction",
                        "description": "Lower operational costs, reduced licensing fees",
                        "accent": "orange",
                        "scenario_ids": {
                                "switch_db_engine_open_source",
                                "upgrade_legacy_databases",
                                "switch_to_standard_linux_os",
                                "application_server_replacement",
                        },
                },
                "agility": {
                        "title": "Agility",
                        "description": "Faster deployment, improved scalability, enhanced flexibility",
                        "accent": "blue",
                        "scenario_ids": {
                                "app_deployment_to_cloud",
                                "app_containerization",
                                "app_refactor_decoupling",
                                "application_server_replacement",
                        },
                },
                "security": {
                        "title": "Security",
                        "description": "Better compliance, reduced vulnerabilities, enhanced protection",
                        "accent": "red",
                        "scenario_ids": {
                                "os_update_security_patch",
                                "update_outdated_components",
                                "application_server_replacement",
                                "upgrade_legacy_databases",
                        },
                },
                "sustainability": {
                        "title": "Sustainability",
                        "description": "Reduced energy consumption, greener infrastructure",
                        "accent": "teal",
                        "scenario_ids": {
                                "app_deployment_to_cloud",
                                "app_containerization",
                                "switch_to_arm_cpu",
                                "switch_to_standard_linux_os",
                        },
                },
        }
        opportunity_cards = []
        for config in category_map.values():
                items = [scenario_counts[scenario_id] for scenario_id in config["scenario_ids"] if scenario_id in scenario_counts]
                app_ids = sorted({app_id for item in items for app_id in item["app_ids"]})
                opportunity_cards.append(
                        {
                                "title": config["title"],
                                "description": config["description"],
                                "accent": config["accent"],
                                "app_count": len(app_ids),
                                "scenario_count": len(items),
                                "items": sorted(items, key=lambda item: item["applicable_count"], reverse=True)[:6],
                        }
                )

        phase_configs = [
                {
                        "title": "Phase 1: Quick Wins",
                        "subtitle": "High Priority • Low/Medium Effort",
                        "accent": "teal",
                        "match": lambda scenario: float(scenario.get("roi_years", 99)) <= 1.2 or float(scenario.get("total_cost", 0)) <= 50_000,
                },
                {
                        "title": "Phase 2: Tactical Improvements",
                        "subtitle": "Medium/Low Priority • Low/Medium/High Effort",
                        "accent": "maroon",
                        "match": lambda scenario: 1.2 < float(scenario.get("roi_years", 99)) <= 2.0,
                },
                {
                        "title": "Phase 3: Strategic Initiatives",
                        "subtitle": "High Priority • High Effort",
                        "accent": "blue",
                        "match": lambda scenario: float(scenario.get("roi_years", 99)) > 2.0,
                },
        ]
        roadmap_cards = []
        unassigned = list(finance_scenarios)
        for phase in phase_configs:
                matched = [scenario for scenario in unassigned if phase["match"](scenario)]
                unassigned = [scenario for scenario in unassigned if scenario not in matched]
                total_cost = sum(float(scenario.get("total_cost", 0)) for scenario in matched)
                total_savings = sum(float(scenario.get("total_yearly_savings", 0)) for scenario in matched)
                roi_years = round(total_cost / total_savings, 1) if total_cost and total_savings else None
                roadmap_cards.append(
                        {
                                "title": phase["title"],
                                "subtitle": phase["subtitle"],
                                "accent": phase["accent"],
                                "total_cost": total_cost,
                                "total_savings": total_savings,
                                "roi_years": roi_years,
                                "items": matched,
                        }
                )
        if unassigned:
                roadmap_cards[-1]["items"].extend(unassigned)
                roadmap_cards[-1]["total_cost"] += sum(float(scenario.get("total_cost", 0)) for scenario in unassigned)
                roadmap_cards[-1]["total_savings"] += sum(float(scenario.get("total_yearly_savings", 0)) for scenario in unassigned)
                total_cost = roadmap_cards[-1]["total_cost"]
                total_savings = roadmap_cards[-1]["total_savings"]
                roadmap_cards[-1]["roi_years"] = round(total_cost / total_savings, 1) if total_cost and total_savings else None

        return {
                "summary": {
                        "total_portfolio": total_portfolio,
                        "in_scope": total_in_scope,
                        "out_of_scope": out_of_scope,
                        "modernization_potential": (
                                float(portfolio_summary.get("applications_with_opportunities", 0)) / total_in_scope if total_in_scope else 0
                        ),
                        "data_completeness": data_completeness,
                        "annual_savings": float(portfolio_summary.get("total_yearly_savings", 0)),
                        "migration_costs": float(portfolio_summary.get("total_one_time_costs", 0)),
                        "roi_years": portfolio_summary.get("roi_years"),
                        "apps_with_eol": apps_with_eol,
                        "apps_with_outdated": apps_with_outdated,
                        "apps_with_missing_versions": apps_with_missing_versions,
                        "priority_apps": priority_apps,
                },
                "opportunities": opportunity_cards,
                "roadmap": roadmap_cards,
        }


def render_summary_section(summary: dict) -> str:
        roi_value, roi_unit = format_roi_label(summary.get("roi_years"))
        priority_items = []
        for app in summary.get("priority_apps", []):
                priority_items.append(
                        f"""
<a href="application_reports/application_report_{html.escape(app['app_id'])}.html" class="pill-row" data-testid="summary-priority-{html.escape(app['app_id'])}">
    <span class="pill-title">{html.escape(app['title'])}</span>
    <span class="pill-badge pill-badge-danger">{html.escape(app['status'])}</span>
    <span class="pill-badge pill-badge-accent">{app['scenario_count']} scenarios</span>
</a>
""".strip()
                )
        priority_html = "\n".join(priority_items) if priority_items else '<div class="empty-state">No priority applications identified.</div>'
        return f"""
<details open class="section-panel" data-testid="section-summary">
    <summary>
        <div>
            <h2>Summary</h2>
            <p>Summary of portfolio modernization assessment</p>
        </div>
        <span class="chevron">⌃</span>
    </summary>
    <div class="section-panel-body summary-grid">
        <article class="metric-card metric-card-scope" data-testid="summary-scope-card">
            <h3>Scope</h3>
            <div class="ring-card">
                <div class="ring ring-blue"><span>{summary['total_portfolio']}</span><small>Total Apps</small></div>
            </div>
            <div class="mini-stats two-up">
                <div><strong>{summary['in_scope']}</strong><span>Apps in Scope</span></div>
                <div><strong>{summary['out_of_scope']}</strong><span>Apps out of Scope</span></div>
            </div>
        </article>
        <article class="metric-card" data-testid="summary-quality-card">
            <h3>Potential &amp; Data Quality</h3>
            <div class="dual-ring-block">
                <div class="ring-row">
                    <div class="mini-ring ring-teal"></div>
                    <div class="ring-copy"><strong>{format_percent(summary['modernization_potential'])}</strong><span>Apps with Modernization Potential</span></div>
                </div>
                <div class="ring-row">
                    <div class="mini-ring ring-orange"></div>
                    <div class="ring-copy"><strong>{format_percent(summary['data_completeness'])}</strong><span>Average Data Completeness Across All Scenarios</span></div>
                </div>
            </div>
        </article>
        <article class="metric-card metric-card-roi" data-testid="summary-roi-card">
            <h3>Return on Investment</h3>
            <div class="value-stack">
                <div class="stat-chip stat-chip-teal"><strong>{format_compact_eur(summary['annual_savings'])}</strong><span>Annual Savings</span></div>
                <div class="stat-chip stat-chip-maroon"><strong>{format_compact_eur(summary['migration_costs'])}</strong><span>Migration Costs</span></div>
                <div class="stat-chip stat-chip-blue stat-chip-large"><strong>{roi_value}</strong><span>{roi_unit}<br>Until positive ROI</span></div>
            </div>
        </article>
        <article class="metric-card" data-testid="summary-eol-card">
            <h3>End of Life</h3>
            <div class="signal-list">
                <div class="signal-row"><strong>{summary['apps_with_eol']}</strong><span>Apps with EOL Components</span><div class="signal-bar signal-red"><span></span></div></div>
                <div class="signal-row"><strong>{summary['apps_with_outdated']}</strong><span>Apps with Outdated Components</span><div class="signal-bar signal-orange"><span></span></div></div>
                <div class="signal-row"><strong>{summary['apps_with_missing_versions']}</strong><span>Apps with Missing Version Details</span><div class="signal-bar signal-teal"><span></span></div></div>
            </div>
        </article>
        <article class="metric-card" data-testid="summary-priority-card">
            <h3>Priority Apps for Modernization</h3>
            <div class="scroll-list">{priority_html}</div>
        </article>
    </div>
</details>
""".strip()


def render_opportunities_section(opportunities: list[dict]) -> str:
        cards = []
        for card in opportunities:
                items_html = "\n".join(
                        f"""
<div class="pill-row" data-testid="opportunity-{html.escape(card['title'].lower().replace(' ', '-'))}-{html.escape(item['scenario_id'])}">
    <span class="pill-title">{html.escape(item['scenario_name'])}</span>
    <span class="pill-badge pill-badge-accent">{item['applicable_count']} Apps</span>
</div>
""".strip()
                        for item in card.get("items", [])
                )
                if not items_html:
                        items_html = '<div class="empty-state">No applicable scenarios available.</div>'
                cards.append(
                        f"""
<article class="opportunity-card" data-testid="opportunity-card-{html.escape(card['title'].lower().replace(' ', '-'))}">
    <h3>{html.escape(card['title'])}</h3>
    <p>{html.escape(card['description'])}</p>
    <div class="opportunity-number">{card['app_count']}</div>
    <div class="opportunity-label">Applicable Apps</div>
    <div class="signal-bar signal-{html.escape(card['accent'])}"><span></span></div>
    <div class="scenario-count">{card['scenario_count']} scenarios</div>
    <div class="scroll-list">{items_html}</div>
</article>
""".strip()
                )
        return f"""
<details open class="section-panel" data-testid="section-opportunities">
    <summary>
        <div>
            <h2>Modernization Opportunities</h2>
            <p>Key opportunities for portfolio modernization</p>
        </div>
        <span class="chevron">⌃</span>
    </summary>
    <div class="section-panel-body opportunity-grid">
        {'\n'.join(cards)}
    </div>
</details>
""".strip()


def render_roadmap_section(roadmap: list[dict]) -> str:
        cards = []
        for phase in roadmap:
                roi_value, roi_unit = format_roi_label(phase.get("roi_years"))
                items_html = "\n".join(
                        f"""
<div class="pill-row" data-testid="roadmap-{html.escape(phase['title'].lower().replace(' ', '-').replace(':', ''))}-{html.escape(item['scenario_id'])}">
    <span class="pill-title">{html.escape(item['scenario_name'])}</span>
    <span class="pill-badge pill-badge-accent">{item['applicable_count']} Apps</span>
</div>
""".strip()
                        for item in phase.get("items", [])
                )
                if not items_html:
                        items_html = '<div class="empty-state">No scenarios assigned.</div>'
                cards.append(
                        f"""
<article class="roadmap-card" data-testid="roadmap-card-{html.escape(phase['title'].lower().replace(' ', '-').replace(':', ''))}">
    <h3>{html.escape(phase['title'])}</h3>
    <p>{html.escape(phase['subtitle'])}</p>
    <div class="roadmap-stats">
        <div class="stat-chip stat-chip-teal"><strong>{format_compact_eur(phase['total_savings'])}</strong><span>Annual Savings</span></div>
        <div class="stat-chip stat-chip-maroon"><strong>{format_compact_eur(phase['total_cost'])}</strong><span>Migration Costs</span></div>
        <div class="stat-chip stat-chip-blue stat-chip-large"><strong>{roi_value}</strong><span>{roi_unit}<br>Until positive ROI</span></div>
    </div>
    <div class="scenario-count">{len(phase.get('items', []))} scenarios</div>
    <div class="scroll-list compact-list">{items_html}</div>
</article>
""".strip()
                )
        return f"""
<details open class="section-panel" data-testid="section-roadmap">
    <summary>
        <div>
            <h2>Roadmap Proposal</h2>
            <p>Phased approach to portfolio modernization</p>
        </div>
        <span class="chevron">⌃</span>
    </summary>
    <div class="section-panel-body roadmap-grid">
        {'\n'.join(cards)}
    </div>
</details>
""".strip()


def render_portfolio_shell(page_title: str, lead: str, body_html: str, payload: dict) -> str:
        report_data = html.escape(json.dumps(payload, ensure_ascii=False))
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{html.escape(page_title)}</title>
    <style>
        :root {{
            --page-bg: #0b1420;
            --shell-bg: #111d2b;
            --panel-bg: #162233;
            --card-bg: #202c3d;
            --card-bg-soft: #313f54;
            --text-main: #f4f7fb;
            --text-soft: #b7c6d9;
            --border: rgba(47, 196, 215, 0.18);
            --teal: #19cfd1;
            --blue: #1384d6;
            --orange: #ff8a45;
            --red: #ff5f73;
            --maroon: #7b4453;
            --track: #1a2332;
        }}
        * {{ box-sizing: border-box; }}
        body {{ margin: 0; font-family: "Segoe UI", "Helvetica Neue", Arial, sans-serif; color: var(--text-main); background: radial-gradient(circle at top, #132334 0%, var(--page-bg) 55%); }}
        a {{ color: inherit; text-decoration: none; }}
        .page {{ width: min(1760px, calc(100% - 32px)); margin: 14px auto; }}
        .report-shell {{ background: var(--shell-bg); border: 1px solid var(--border); border-radius: 18px; overflow: hidden; box-shadow: 0 28px 70px rgba(0, 0, 0, 0.32); }}
        .header {{ display: flex; justify-content: space-between; align-items: center; gap: 16px; padding: 20px 28px; border-bottom: 1px solid rgba(255,255,255,0.06); }}
        .customer-meta [data-testid="customer-name"] {{ font-size: 1.1rem; font-weight: 700; margin-bottom: 0.25rem; }}
        .customer-meta div:last-child {{ color: var(--text-soft); }}
        .logo {{ height: 42px; width: auto; }}
        .logo svg {{ height: 100%; width: auto; }}
        .logo path {{ fill: #fff; }}
        .content {{ padding: 18px 18px 24px; }}
        .hero {{ padding: 10px 14px 16px; }}
        .hero h1 {{ margin: 0; font-size: 2.2rem; font-weight: 800; }}
        .hero p {{ margin: 10px 0 0; color: var(--text-soft); font-size: 1.05rem; line-height: 1.5; max-width: 1100px; }}
        .section-panel {{ background: var(--panel-bg); border: 1px solid var(--border); border-radius: 16px; margin-bottom: 18px; overflow: hidden; }}
        .section-panel summary {{ display: flex; justify-content: space-between; align-items: flex-start; gap: 16px; cursor: pointer; list-style: none; padding: 22px 28px 14px; }}
        .section-panel summary::-webkit-details-marker {{ display: none; }}
        .section-panel summary h2 {{ margin: 0; font-size: 1.15rem; font-weight: 800; }}
        .section-panel summary p {{ margin: 8px 0 0; color: var(--text-soft); font-size: 0.95rem; }}
        .section-panel .chevron {{ font-size: 1.4rem; line-height: 1; color: #fff; transform: rotate(0deg); transition: transform 140ms ease; }}
        .section-panel[open] .chevron {{ transform: rotate(180deg); }}
        .section-panel-body {{ padding: 0 18px 18px; }}
        .summary-grid {{ display: grid; grid-template-columns: 1.1fr 1.6fr 1fr 1fr 1.4fr; gap: 18px; }}
        .metric-card, .opportunity-card, .roadmap-card {{ background: var(--card-bg); border-radius: 14px; padding: 28px; min-height: 100%; box-shadow: inset 0 0 0 1px rgba(255,255,255,0.02); }}
        .metric-card h3, .opportunity-card h3, .roadmap-card h3 {{ margin: 0 0 18px; font-size: 1rem; font-weight: 800; }}
        .ring-card {{ display: flex; justify-content: center; padding: 16px 0 22px; }}
        .ring {{ width: 262px; aspect-ratio: 1; border-radius: 50%; display: grid; place-items: center; position: relative; }}
        .ring::before {{ content: ""; position: absolute; inset: 22px; border-radius: 50%; background: var(--card-bg); box-shadow: inset 0 0 0 1px rgba(255,255,255,0.04); }}
        .ring span, .ring small {{ position: relative; z-index: 1; display: block; text-align: center; }}
        .ring span {{ font-size: 4rem; font-weight: 800; line-height: 1; }}
        .ring small {{ margin-top: 10px; font-size: 0.95rem; color: var(--text-soft); }}
        .ring-blue {{ background: conic-gradient(var(--blue) 0deg 300deg, rgba(255,255,255,0.15) 300deg 360deg); }}
        .mini-stats {{ display: grid; gap: 16px; }}
        .two-up {{ grid-template-columns: repeat(2, minmax(0, 1fr)); }}
        .mini-stats strong {{ display: block; font-size: 2.1rem; font-weight: 800; line-height: 1.1; margin-bottom: 8px; }}
        .mini-stats span {{ color: var(--text-soft); font-size: 0.95rem; line-height: 1.35; }}
        .dual-ring-block {{ display: grid; gap: 30px; padding-top: 6px; }}
        .ring-row {{ display: grid; grid-template-columns: 180px 1fr; gap: 18px; align-items: center; }}
        .mini-ring {{ width: 170px; height: 170px; border-radius: 50%; position: relative; }}
        .mini-ring::before {{ content: ""; position: absolute; inset: 18px; border-radius: 50%; background: var(--card-bg); box-shadow: inset 0 0 0 1px rgba(255,255,255,0.04); }}
        .ring-teal {{ background: conic-gradient(var(--teal) 0deg 282deg, rgba(255,255,255,0.18) 282deg 360deg); }}
        .ring-orange {{ background: conic-gradient(var(--orange) 0deg 245deg, rgba(255,255,255,0.18) 245deg 360deg); }}
        .ring-copy strong {{ display: block; font-size: 3.6rem; font-weight: 800; line-height: 1; margin-bottom: 10px; }}
        .ring-copy span {{ color: var(--text-soft); font-size: 1rem; line-height: 1.45; }}
        .value-stack {{ display: grid; gap: 20px; }}
        .stat-chip {{ border-radius: 12px; padding: 18px 18px 14px; text-align: center; }}
        .stat-chip strong {{ display: block; font-size: 2.45rem; font-weight: 800; line-height: 1.05; }}
        .stat-chip span {{ display: block; margin-top: 10px; color: rgba(255,255,255,0.9); font-size: 0.95rem; line-height: 1.35; }}
        .stat-chip-large strong {{ font-size: 3rem; }}
        .stat-chip-teal {{ background: #197f83; }}
        .stat-chip-maroon {{ background: #6f3947; }}
        .stat-chip-blue {{ background: #1178c9; }}
        .signal-list {{ display: grid; gap: 26px; padding-top: 8px; }}
        .signal-row strong {{ display: block; font-size: 3rem; font-weight: 800; line-height: 1; margin-bottom: 8px; }}
        .signal-row span {{ display: block; color: var(--text-soft); font-size: 0.98rem; line-height: 1.4; margin-bottom: 12px; }}
        .signal-bar {{ height: 12px; background: var(--track); border-radius: 999px; overflow: hidden; max-width: 240px; }}
        .signal-bar span {{ display: block; height: 100%; width: 62%; margin: 0; }}
        .signal-red span {{ background: var(--red); }}
        .signal-orange span {{ background: var(--orange); }}
        .signal-teal span {{ background: var(--teal); }}
        .signal-blue span {{ background: var(--blue); }}
        .scroll-list {{ display: grid; gap: 12px; max-height: 360px; overflow: auto; padding-right: 4px; }}
        .compact-list {{ max-height: 290px; }}
        .pill-row {{ display: grid; grid-template-columns: minmax(0, 1fr) auto auto; gap: 10px; align-items: center; padding: 12px 14px; border-radius: 10px; background: var(--card-bg-soft); }}
        .pill-title {{ font-size: 0.98rem; font-weight: 700; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }}
        .pill-badge {{ border-radius: 7px; padding: 7px 10px; font-size: 0.82rem; font-weight: 800; white-space: nowrap; }}
        .pill-badge-danger {{ background: var(--red); color: #fff; }}
        .pill-badge-accent {{ background: #1698a9; color: #fff; }}
        .empty-state {{ color: var(--text-soft); padding: 12px 0; }}
        .opportunity-grid {{ display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 18px; }}
        .opportunity-card p, .roadmap-card p {{ color: var(--text-soft); font-size: 0.95rem; line-height: 1.45; margin: 0 0 24px; }}
        .opportunity-number {{ font-size: 3.7rem; font-weight: 800; line-height: 1; margin-bottom: 8px; text-align: center; }}
        .opportunity-label {{ color: var(--text-soft); text-align: center; font-size: 0.95rem; margin-bottom: 16px; }}
        .scenario-count {{ color: var(--text-soft); font-size: 0.92rem; font-weight: 700; letter-spacing: 0.04em; text-transform: uppercase; margin: 18px 0 14px; }}
        .roadmap-grid {{ display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 18px; }}
        .roadmap-stats {{ display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 12px; margin-bottom: 18px; }}
        .footer {{ display: flex; justify-content: space-between; align-items: center; gap: 16px; padding: 20px 28px; border-top: 1px solid rgba(255,255,255,0.06); }}
        .footer p {{ margin: 0.15rem 0; }}
        .meta-primary {{ color: var(--teal); font-weight: 700; font-size: 0.86rem; }}
        .meta-secondary, .meta-muted {{ color: var(--text-soft); font-size: 0.8rem; }}
        @media (max-width: 1500px) {{
            .summary-grid {{ grid-template-columns: repeat(2, minmax(0, 1fr)); }}
            .metric-card:last-child {{ grid-column: 1 / -1; }}
            .opportunity-grid {{ grid-template-columns: repeat(2, minmax(0, 1fr)); }}
            .roadmap-grid {{ grid-template-columns: 1fr; }}
        }}
        @media (max-width: 980px) {{
            .page {{ width: min(100%, calc(100% - 20px)); }}
            .header, .footer {{ flex-direction: column; align-items: flex-start; }}
            .summary-grid, .opportunity-grid {{ grid-template-columns: 1fr; }}
            .ring-row {{ grid-template-columns: 1fr; }}
            .roadmap-stats {{ grid-template-columns: 1fr; }}
            .pill-row {{ grid-template-columns: minmax(0, 1fr) auto; }}
            .pill-row .pill-badge:last-child {{ grid-column: 2; }}
        }}
    </style>
</head>
<body>
    <div class="page">
        <div class="report-shell">
            <div class="header">
                <div class="customer-meta">
                    <div data-testid="customer-name">{html.escape(payload['customer_name'])}</div>
                    <div>{html.escape(payload['subtitle'])}</div>
                </div>
                <div class="logo">{LOGO_SVG}</div>
            </div>
            <div class="content">
                <section class="hero" data-testid="portfolio-report-title">
                    <h1>Portfolio Modernization Report</h1>
                    <p>{html.escape(lead)}</p>
                </section>
                {body_html}
            </div>
            <div class="footer">
                <div>
                    <p class="meta-primary">Generated by GenDiscover</p>
                    <p class="meta-secondary">{html.escape(payload['generated_at'])}</p>
                    <p class="meta-muted">Analysis ID: {html.escape(payload['analysis_id'])}</p>
                </div>
                <div class="logo">{LOGO_SVG}</div>
            </div>
        </div>
    </div>
    <script type="application/json" id="report-data">{report_data}</script>
</body>
</html>
"""


def render_sections(sections: list[dict]) -> str:
    rendered = []
    for section in sections:
        test_id = f"section-{section['slug']}"
        rendered.append(
            f"""
<details open class="section-card" data-testid="{test_id}">
  <summary>
    <div>
      <h2>{html.escape(section['title'])}</h2>
    </div>
    <span class="chevron">▾</span>
  </summary>
  <div class="section-body">
    {section['html']}
  </div>
</details>
""".strip()
        )
    return "\n\n".join(rendered)


def render_app_links(app_links: list[dict]) -> str:
    if not app_links:
        return ""
    items = []
    for index, app in enumerate(app_links, start=1):
        items.append(
            f"""
<a href="application_reports/application_report_{html.escape(app['app_id'])}.html" target="_blank" class="app-link" data-testid="summary-priority-apps-item-{index}">
  <span>{html.escape(app['title'])}</span>
  <span class="arrow">↗</span>
</a>
""".strip()
        )
    return "\n".join(items)


def html_shell(page_title: str, visible_title: str, lead: str, body_html: str, payload: dict) -> str:
    report_data = html.escape(json.dumps(payload, ensure_ascii=False))
    visible_lead = f"<p class=\"lead\">{html.escape(lead)}</p>" if lead else ""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{html.escape(page_title)}</title>
  <style>
    :root {{
      --primary-dark: #081722;
      --report-background: #102737;
      --section-background: #163244;
      --accent: #1ec8d7;
      --accent-rgb: 30, 200, 215;
      --report-text-font-primary: #e9f7ff;
      --report-text-font-secondary-rgb: 184, 216, 232;
      --text-light-blue-rgb: 154, 198, 220;
    }}
    * {{ box-sizing: border-box; }}
    body {{ margin: 0; background: radial-gradient(circle at top, #153044 0%, var(--primary-dark) 55%); color: var(--report-text-font-primary); font-family: "Segoe UI", "Helvetica Neue", sans-serif; }}
    a {{ color: inherit; text-decoration: none; }}
    code {{ background: rgba(255,255,255,0.08); padding: 0.1rem 0.3rem; border-radius: 4px; }}
    pre {{ overflow-x: auto; background: rgba(0,0,0,0.25); padding: 1rem; border-radius: 10px; }}
    table {{ width: 100%; border-collapse: collapse; }}
    th, td {{ padding: 0.75rem; border-bottom: 1px solid rgba(var(--accent-rgb), 0.12); text-align: left; vertical-align: top; }}
    .page {{ max-width: 95%; margin: 0 auto; padding: 2rem 1rem; }}
    .report-shell {{ background: var(--report-background); border: 1px solid rgba(var(--accent-rgb), 0.15); border-radius: 1rem; overflow: hidden; box-shadow: 0 24px 60px rgba(0,0,0,0.35); }}
    .header {{ display: flex; justify-content: space-between; align-items: center; gap: 1rem; padding: 1.5rem 2rem; color: white; background: linear-gradient(180deg, rgba(255,255,255,0.03), rgba(255,255,255,0.01)); }}
    .customer-meta {{ font-size: 0.95rem; font-weight: 300; letter-spacing: 0.02em; }}
    .customer-meta [data-testid="customer-name"] {{ font-weight: 700; font-size: 1.125rem; margin-bottom: 0.25rem; }}
    .logo {{ height: 45px; width: auto; }}
    .logo svg {{ height: 100%; width: auto; }}
    .logo path {{ fill: white; }}
    .content {{ padding: 2rem; }}
    .title-card {{ background: var(--section-background); border: 1px solid rgba(var(--accent-rgb), 0.15); border-radius: 0.75rem; box-shadow: 0 8px 20px rgba(0,0,0,0.18); margin-bottom: 1.5rem; padding: 1.25rem; }}
    .title-card h1 {{ margin: 0; padding-bottom: 1rem; border-bottom: 3px solid var(--accent); color: white; font-size: 2.5rem; text-shadow: 0 0 4px rgba(255,255,255,0.25); }}
    .lead {{ margin: 1rem 0 0; font-size: 1.05rem; line-height: 1.6; color: rgba(var(--report-text-font-secondary-rgb), 0.95); }}
    .section-card {{ background: var(--section-background); border: 1px solid rgba(var(--accent-rgb), 0.15); border-radius: 0.75rem; box-shadow: 0 8px 20px rgba(0,0,0,0.12); margin-bottom: 1.5rem; overflow: hidden; }}
    .section-card summary {{ list-style: none; display: flex; justify-content: space-between; align-items: center; gap: 1rem; cursor: pointer; padding: 1.25rem 1.5rem; }}
    .section-card summary::-webkit-details-marker {{ display: none; }}
    .section-card h2 {{ margin: 0; font-size: 1.5rem; color: white; }}
    .section-card .chevron {{ color: var(--accent); font-size: 1.25rem; }}
    .section-card[open] .chevron {{ transform: rotate(180deg); }}
    .section-body {{ padding: 0 1.5rem 1.5rem; color: rgba(var(--report-text-font-secondary-rgb), 0.95); line-height: 1.65; }}
    .section-body ul {{ margin: 0; padding-left: 1.25rem; }}
    .footer {{ display: flex; justify-content: space-between; align-items: center; gap: 1rem; padding: 1.5rem 2rem; border-top: 1px solid rgba(var(--accent-rgb), 0.2); }}
    .footer p {{ margin: 0.2rem 0; }}
    .footer .meta-primary {{ font-size: 0.875rem; font-weight: 600; color: var(--accent); }}
    .footer .meta-secondary {{ font-size: 0.75rem; color: rgba(var(--text-light-blue-rgb), 0.8); }}
    .footer .meta-muted {{ font-size: 0.75rem; color: rgba(var(--text-light-blue-rgb), 0.6); }}
    .app-link-list {{ display: grid; gap: 0.75rem; }}
    .app-link {{ display: flex; justify-content: space-between; align-items: center; gap: 1rem; padding: 0.75rem 0.9rem; border-radius: 0.5rem; background: rgba(255,255,255,0.08); transition: background-color 160ms ease; }}
    .app-link:hover {{ background: rgba(255,255,255,0.14); }}
    @media (max-width: 768px) {{
      .header, .footer {{ flex-direction: column; text-align: center; }}
      .logo {{ height: 35px; }}
      .content {{ padding: 1.25rem; }}
      .title-card h1 {{ font-size: 2rem; }}
    }}
  </style>
</head>
<body>
  <div class="page">
    <div class="report-shell">
      <div class="header">
        <div class="customer-meta">
          <div class="font-bold text-lg mb-1" data-testid="customer-name">{html.escape(payload['customer_name'])}</div>
          <div>{html.escape(payload['subtitle'])}</div>
        </div>
        <div class="logo">{LOGO_SVG}</div>
      </div>
      <div class="content">
        <div class="title-card" data-testid="app-report-title">
          <h1>{html.escape(visible_title)}</h1>
          {visible_lead}
        </div>
        {body_html}
      </div>
      <div class="footer">
        <div>
          <p class="meta-primary">Generated by GenDiscover</p>
          <p class="meta-secondary">{html.escape(payload['generated_at'])}</p>
          <p class="meta-muted">Analysis ID: {html.escape(payload['analysis_id'])}</p>
        </div>
        <div class="logo">{LOGO_SVG}</div>
      </div>
    </div>
  </div>
  <script type="application/json" id="report-data">{report_data}</script>
</body>
</html>
"""


def render_portfolio_html(markdown_text: str, app_reports: list[dict], output_dir: Path) -> str:
    parsed = parse_markdown(markdown_text)
    dashboard = load_portfolio_dashboard_data(markdown_text, output_dir, app_reports)
    payload = build_payload(
        "portfolio",
        parsed["title"] or "Portfolio Modernization Report",
        parsed["lead"],
        parsed["sections"],
        extra={"app_links": app_reports, "dashboard": dashboard},
    )
    handled_sections = {
        "executive summary",
        "portfolio overview",
        "top modernization opportunities",
        "financial summary",
        "risk applications",
        "per-application reports",
    }
    remaining_sections = [
        section for section in parsed["sections"] if section["title"].strip().lower() not in handled_sections
    ]
    body = [
        render_summary_section(dashboard["summary"]),
        render_opportunities_section(dashboard["opportunities"]),
        render_roadmap_section(dashboard["roadmap"]),
    ]
    if remaining_sections:
        body.append(render_sections(remaining_sections))
    return render_portfolio_shell(
        f"Portfolio Modernization Report - {payload['customer_name']} - GenDiscover",
        parsed["lead"],
        "\n\n".join(part for part in body if part),
        payload,
    )


def render_application_html(app_id: str, markdown_text: str) -> tuple[str, str]:
    parsed = parse_markdown(markdown_text)
    app_name = normalize_application_name(parsed["title"], app_id)
    visible_title = f"Application Report - {app_name}"
    payload = build_payload(
        "application",
        visible_title,
        parsed["lead"],
        parsed["sections"],
        extra={"app_id": app_id, "application_name": app_name},
    )
    body = render_sections(parsed["sections"])
    html_text = html_shell(
        f"Application Report - {app_name} - GenDiscover",
        f"Application Report - {app_name}",
        parsed["lead"],
        body,
        payload,
    )
    return html_text, app_name


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate self-contained GenDiscover legacy HTML reports.")
    parser.add_argument("--portfolio-md", required=True, help="Path to output/reports/portfolio_report.md")
    parser.add_argument("--app-md-dir", required=True, help="Path to output/reports/apps")
    parser.add_argument("--output-dir", required=True, help="Path to output/reports")
    args = parser.parse_args()

    portfolio_md = Path(args.portfolio_md)
    app_md_dir = Path(args.app_md_dir)
    output_dir = Path(args.output_dir)
    app_output_dir = output_dir / "application_reports"
    app_output_dir.mkdir(parents=True, exist_ok=True)

    app_reports = []
    for app_md in sorted(app_md_dir.glob("*.md")):
        app_id = extract_app_id(app_md)
        app_html, app_name = render_application_html(app_id, app_md.read_text(encoding="utf-8"))
        (app_output_dir / f"application_report_{app_id}.html").write_text(app_html, encoding="utf-8")
        app_reports.append({"app_id": app_id, "title": app_name})

    portfolio_html = render_portfolio_html(portfolio_md.read_text(encoding="utf-8"), app_reports, output_dir)
    (output_dir / "portfolio_modernization_report.html").write_text(portfolio_html, encoding="utf-8")


if __name__ == "__main__":
    main()