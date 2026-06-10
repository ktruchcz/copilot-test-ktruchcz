#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUTPUT_ROOT = ROOT / "output"
REPORTS_DIR = OUTPUT_ROOT / "reports"
APP_REPORTS_DIR = REPORTS_DIR / "apps"
APPLICATION_HTML_DIR = REPORTS_DIR / "application_reports"
TECH_DIR = OUTPUT_ROOT / "technology_assessment"
COMPLEXITY_DIR = OUTPUT_ROOT / "complexity_results"
SCENARIO_DIR = OUTPUT_ROOT / "scenario_applicability_results"
BUSINESS_CASE_PATH = OUTPUT_ROOT / "business_case_results" / "business_case.json"
OUT_OF_SCOPE_DIR = OUTPUT_ROOT / "out_of_scope_results"
LOGO_SVG = (ROOT / ".github" / "skills" / "logo.svg").read_text(encoding="utf-8").strip()
CUSTOMER_NAME = "GenDiscover"
SUBTITLE = "Application modernization with Agentic AI powered by Capgemini GenSuite"


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def safe(value) -> str:
    return "" if value is None else str(value)


def escape_html(value) -> str:
    return (
        safe(value).replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&#39;")
    )


def currency(value) -> str:
    if value is None:
        return "n/a"
    return f"EUR {float(value):,.2f}"


def percent(value) -> str:
    if value is None:
        return "n/a"
    return f"{float(value):.2f}%"


def json_script(payload: dict) -> str:
    return json.dumps(payload, ensure_ascii=False).replace("</", "<\\/")


def analysis_id(*parts: str) -> str:
    digest = hashlib.md5()
    for part in parts:
        digest.update(part.encode("utf-8"))
    return digest.hexdigest()


def page_shell(title: str, body: str, payload: dict) -> str:
    return f"""<!DOCTYPE html>
<html lang=\"en\">
<head>
  <meta charset=\"UTF-8\">
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">
  <title>{escape_html(title)}</title>
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
      --danger: #ff6b81;
      --warning: #ffb347;
      --success: #58d68d;
    }}
    * {{ box-sizing: border-box; }}
    body {{ margin: 0; background: radial-gradient(circle at top, #153044 0%, var(--primary-dark) 58%); color: var(--report-text-font-primary); font-family: Arial, Helvetica, sans-serif; }}
    a {{ color: var(--accent); }}
    .page {{ max-width: 1400px; margin: 0 auto; padding: 24px 16px; }}
    .shell {{ background: var(--report-background); border: 1px solid rgba(var(--accent-rgb), 0.18); border-radius: 18px; box-shadow: 0 30px 70px rgba(0, 0, 0, 0.35); overflow: hidden; }}
    .header, .footer {{ display: flex; justify-content: space-between; align-items: center; gap: 16px; padding: 20px 24px; border-bottom: 1px solid rgba(255,255,255,0.06); }}
    .footer {{ border-top: 1px solid rgba(255,255,255,0.06); border-bottom: 0; }}
    .customer-meta [data-testid=\"customer-name\"] {{ font-size: 1.1rem; font-weight: 700; margin-bottom: 4px; }}
    .customer-meta div:last-child {{ color: rgba(var(--report-text-font-secondary-rgb), 0.92); font-size: 0.95rem; }}
    .logo svg {{ height: 44px; width: auto; }}
    .logo path {{ fill: white; }}
    .content {{ padding: 24px; }}
    .card, details {{ background: var(--section-background); border: 1px solid rgba(var(--accent-rgb), 0.16); border-radius: 14px; margin-bottom: 18px; box-shadow: 0 12px 30px rgba(0,0,0,0.18); }}
    .title-card {{ padding: 20px; }}
    .title-card h1 {{ margin: 0; font-size: 2.3rem; text-shadow: 0 0 18px rgba(var(--accent-rgb), 0.35); }}
    .lead {{ margin: 12px 0 0; color: rgba(var(--report-text-font-secondary-rgb), 0.95); line-height: 1.55; }}
    details summary {{ list-style: none; cursor: pointer; padding: 18px 20px; display: flex; justify-content: space-between; align-items: center; gap: 12px; }}
    details summary::-webkit-details-marker {{ display: none; }}
    details summary h2 {{ margin: 0; font-size: 1.35rem; }}
    .body {{ padding: 0 20px 20px; color: rgba(var(--report-text-font-secondary-rgb), 0.96); line-height: 1.6; }}
    table {{ width: 100%; border-collapse: collapse; margin-top: 12px; }}
    th, td {{ text-align: left; vertical-align: top; padding: 10px 12px; border-bottom: 1px solid rgba(var(--accent-rgb), 0.12); }}
    th {{ color: var(--report-text-font-primary); }}
    .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 16px; }}
    .metric {{ background: rgba(255,255,255,0.04); border: 1px solid rgba(var(--accent-rgb), 0.12); border-radius: 12px; padding: 16px; }}
    .metric .value {{ font-size: 2.2rem; font-weight: 800; color: var(--accent); text-shadow: 0 0 16px rgba(var(--accent-rgb), 0.45); }}
    .metric .label {{ margin-top: 6px; color: rgba(var(--report-text-font-secondary-rgb), 0.9); }}
    .badge {{ display: inline-block; padding: 4px 8px; border-radius: 999px; font-size: 0.78rem; font-weight: 700; }}
    .badge-critical, .badge-eol, .badge-blocked {{ background: rgba(255, 107, 129, 0.18); color: #ffd3da; }}
    .badge-high, .badge-outdated, .badge-partially_fulfilled {{ background: rgba(255, 179, 71, 0.18); color: #ffe0ab; }}
    .badge-current_version, .badge-fulfilled, .badge-low {{ background: rgba(88, 214, 141, 0.18); color: #d7ffe5; }}
    .badge-applicable, .badge-medium {{ background: rgba(var(--accent-rgb), 0.18); color: #d7fbff; }}
    .badge-no_knowledge, .badge-lack_of_data, .badge-not_applicable {{ background: rgba(255,255,255,0.1); color: #ecf7ff; }}
    .link-list {{ display: grid; gap: 10px; }}
    .link-card {{ display: flex; justify-content: space-between; align-items: center; gap: 12px; padding: 12px 14px; border-radius: 10px; background: rgba(255,255,255,0.05); border: 1px solid rgba(var(--accent-rgb), 0.12); }}
    .footer-meta p {{ margin: 2px 0; }}
    .footer-meta .primary {{ color: var(--accent); font-weight: 700; }}
    ul {{ margin: 0; padding-left: 20px; }}
    @media (max-width: 800px) {{ .header, .footer {{ flex-direction: column; align-items: flex-start; }} .content {{ padding: 16px; }} }}
  </style>
</head>
<body>
  <div class=\"page\">
    <div class=\"shell\">
      <div class=\"header\">
        <div class=\"customer-meta\">
          <div data-testid=\"customer-name\">{escape_html(CUSTOMER_NAME)}</div>
          <div>{escape_html(SUBTITLE)}</div>
        </div>
        <div class=\"logo\">{LOGO_SVG}</div>
      </div>
      <div class=\"content\">{body}</div>
      <div class=\"footer\">
        <div class=\"footer-meta\">
          <p class=\"primary\">Generated by GenDiscover</p>
          <p>{escape_html(payload['generated_timestamp'])}</p>
          <p>Analysis ID: {escape_html(payload['analysis_id'])}</p>
        </div>
        <div class=\"logo\">{LOGO_SVG}</div>
      </div>
    </div>
  </div>
  <script type=\"application/json\" id=\"report-data\">{json_script(payload)}</script>
</body>
</html>
"""


def status_badge(value: str) -> str:
    slug = safe(value).lower().replace(" ", "_")
    return f'<span class="badge badge-{escape_html(slug)}">{escape_html(value)}</span>'


def render_table(headers: list[str], rows: list[list[str]]) -> str:
    head = "".join(f"<th>{escape_html(header)}</th>" for header in headers)
    body = "".join("<tr>" + "".join(f"<td>{cell}</td>" for cell in row) + "</tr>" for row in rows)
    return f"<table><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table>"


def detail_section(test_id: str, title: str, inner: str) -> str:
    return f"<details open data-testid=\"{escape_html(test_id)}\"><summary><h2>{escape_html(title)}</h2><span>▾</span></summary><div class=\"body\">{inner}</div></details>"


def load_app_inputs(app_id: str) -> tuple[dict, dict, dict]:
    tech = read_json(TECH_DIR / f"technology_assessment_{app_id}.json")
    complexity = read_json(COMPLEXITY_DIR / f"complexity_{app_id}.json")
    scenario = read_json(SCENARIO_DIR / f"scenario_assessment_{app_id}.json")
    return tech, complexity, scenario


def build_application_html(app_entry: dict) -> str:
    app_id = app_entry["app_id"]
    tech, complexity, scenario = load_app_inputs(app_id)
    component_rows = [
        [
            escape_html(component["component_type"]),
            escape_html(component["name"]),
            escape_html(component["version"]),
            status_badge(component["status"]),
            escape_html(component["notes"]),
        ]
        for component in tech.get("components", [])
    ]
    scenario_rows = [
        [
            escape_html(item["scenario_name"]),
            status_badge(item["status"]),
            escape_html(item["rationale"]),
        ]
        for item in scenario.get("scenarios", [])
    ]
    business_rows = [
        [
            escape_html(item["scenario_name"]),
            escape_html(currency(item.get("adjusted_cost"))),
            escape_html(currency(item.get("annual_savings"))),
            escape_html(percent(item.get("roi_3year"))),
        ]
        for item in app_entry.get("scenarios", [])
    ] or [["No quantified scenario", "EUR 0.00", "EUR 0.00", "n/a"]]
    summary_body = f"""
      <section class=\"card title-card\" data-testid=\"app-report-title\">
        <h1>Application Report - {escape_html(app_entry['app_name'])}</h1>
        <p class=\"lead\">Technology, complexity, scenario, and business-case assessment for application {escape_html(app_id)}.</p>
      </section>
    """
    tech_body = render_table(["Component", "Name", "Version", "Status", "Notes"], component_rows)
    tech_body += f"<p><strong>Overall technology risk:</strong> {status_badge(tech.get('overall_technology_risk'))}</p>"
    complexity_body = f"""
      <div class=\"grid\">
        <div class=\"metric\"><div class=\"value\">{escape_html(complexity['complexity_score'])}</div><div class=\"label\">Complexity Score</div></div>
        <div class=\"metric\"><div class=\"value\">{escape_html(complexity['complexity_label'])}</div><div class=\"label\">Complexity Label</div></div>
        <div class=\"metric\"><div class=\"value\">{escape_html(complexity['estimated_effort'])}</div><div class=\"label\">Estimated Effort</div></div>
      </div>
      <p>{escape_html(complexity['reasoning'])}</p>
      {render_table(["Factor", "Value"], [[escape_html(key.replace('_', ' ').title()), escape_html(value)] for key, value in complexity.get('factors', {}).items()])}
    """
    scenario_body = render_table(["Scenario", "Status", "Rationale"], scenario_rows)
    business_body = f"""
      <div class=\"grid\">
        <div class=\"metric\"><div class=\"value\">{escape_html(currency(app_entry.get('total_investment')))}</div><div class=\"label\">Total Investment</div></div>
        <div class=\"metric\"><div class=\"value\">{escape_html(currency(app_entry.get('total_annual_savings')))}</div><div class=\"label\">Annual Savings</div></div>
      </div>
      {render_table(["Scenario", "Adjusted Cost", "Annual Savings", "3-Year ROI"], business_rows)}
    """
    payload = {
        "app_id": app_id,
        "report_title": f"Application Report - {app_entry['app_name']}",
        "lead_text": f"Technology, complexity, scenario, and business-case assessment for {app_entry['app_name']}.",
        "generated_timestamp": datetime.now(timezone.utc).isoformat(),
        "analysis_id": analysis_id(app_id, app_entry["app_name"]),
        "customer_name": CUSTOMER_NAME,
        "sections": [
            {"id": "technology-assessment", "title": "Technology Assessment"},
            {"id": "complexity-assessment", "title": "Complexity Assessment"},
            {"id": "scenario-analysis", "title": "Scenario Analysis"},
            {"id": "business-case", "title": "Business Case"},
        ],
        "application": app_entry,
        "technology": tech,
        "complexity": complexity,
        "scenario_analysis": scenario,
    }
    body = "".join([
        summary_body,
        detail_section("technology-assessment", "Technology Assessment", tech_body),
        detail_section("complexity-assessment", "Complexity Assessment", complexity_body),
        detail_section("scenario-analysis", "Scenario Analysis", scenario_body),
        detail_section("business-case", "Business Case", business_body),
    ])
    return page_shell(f"Application Report - {app_entry['app_name']} - GenDiscover", body, payload)


def build_portfolio_html(business_case: dict) -> str:
    app_links = []
    out_of_scope = 0
    for path in OUT_OF_SCOPE_DIR.glob("out_of_scope_*.json"):
        if read_json(path).get("out_of_scope"):
            out_of_scope += 1
    technology_by_app = {}
    complexity_by_app = {}
    scenario_counts = {}
    phase_1 = []
    phase_2 = []
    phase_3 = []
    for app_entry in business_case.get("applications", []):
        app_id = app_entry["app_id"]
        tech = read_json(TECH_DIR / f"technology_assessment_{app_id}.json")
        complexity = read_json(COMPLEXITY_DIR / f"complexity_{app_id}.json")
        scenarios = read_json(SCENARIO_DIR / f"scenario_assessment_{app_id}.json")
        technology_by_app[app_id] = tech
        complexity_by_app[app_id] = complexity
        app_links.append({"app_id": app_id, "app_name": app_entry["app_name"]})
        for item in scenarios.get("scenarios", []):
            if item.get("status") in {"APPLICABLE", "PARTIALLY_FULFILLED"}:
                scenario_counts[item["scenario_name"]] = scenario_counts.get(item["scenario_name"], 0) + 1
        risk = tech.get("overall_technology_risk")
        label = complexity.get("complexity_label")
        line = f"{app_entry['app_name']} ({risk}, {label})"
        if risk == "CRITICAL":
            phase_1.append(line)
        elif risk == "HIGH":
            phase_2.append(line)
        else:
            phase_3.append(line)
    scenario_rows = [[escape_html(name), escape_html(count)] for name, count in sorted(scenario_counts.items(), key=lambda item: (-item[1], item[0]))]
    app_link_cards = "".join(
        f'<a class="link-card" href="application_reports/application_report_{escape_html(item["app_id"])}.html"><span>{escape_html(item["app_name"])} ({escape_html(item["app_id"])})</span><span>Open report ↗</span></a>'
        for item in app_links
    )
    summary_section = f"""
      <div class=\"grid\">
        <div class=\"metric\"><div class=\"value\">{business_case['portfolio_summary']['total_apps']}</div><div class=\"label\">Total Apps</div></div>
        <div class=\"metric\"><div class=\"value\">{business_case['portfolio_summary']['in_scope_apps']}</div><div class=\"label\">In Scope</div></div>
        <div class=\"metric\"><div class=\"value\">{out_of_scope}</div><div class=\"label\">Out of Scope</div></div>
        <div class=\"metric\"><div class=\"value\">{escape_html(currency(business_case['portfolio_summary']['total_investment']))}</div><div class=\"label\">Total Investment</div></div>
        <div class=\"metric\"><div class=\"value\">{escape_html(currency(business_case['portfolio_summary']['total_annual_savings']))}</div><div class=\"label\">Annual Savings</div></div>
        <div class=\"metric\"><div class=\"value\">{escape_html(percent(business_case['portfolio_summary']['portfolio_roi_3year']))}</div><div class=\"label\">Portfolio 3-Year ROI</div></div>
      </div>
    """
    opportunities = sorted(scenario_counts.items(), key=lambda item: (-item[1], item[0]))[:5]
    opportunity_body = "<ul>" + "".join(f"<li><strong>{escape_html(name)}</strong> applies to {count} application(s).</li>" for name, count in opportunities) + "</ul>"
    roadmap_body = f"""
      <div class=\"grid\">
        <div class=\"metric\"><div class=\"value\">Phase 1</div><div class=\"label\">Critical-risk apps first</div><ul>{''.join(f'<li>{escape_html(item)}</li>' for item in phase_1) or '<li>No apps</li>'}</ul></div>
        <div class=\"metric\"><div class=\"value\">Phase 2</div><div class=\"label\">High-risk remediation</div><ul>{''.join(f'<li>{escape_html(item)}</li>' for item in phase_2) or '<li>No apps</li>'}</ul></div>
        <div class=\"metric\"><div class=\"value\">Phase 3</div><div class=\"label\">Optimization and strategic moves</div><ul>{''.join(f'<li>{escape_html(item)}</li>' for item in phase_3) or '<li>No apps</li>'}</ul></div>
      </div>
    """
    scenario_overview = render_table(["Scenario", "Applicable Apps"], scenario_rows or [["No applicable scenarios", "0"]])
    scenario_overview += f'<div class="link-list" style="margin-top:16px;">{app_link_cards}</div>'
    payload = {
        "report_title": "Portfolio Modernization Report",
        "lead_text": "Portfolio-wide summary of technology risk, complexity, modernization scenarios, and indicative business case.",
        "generated_timestamp": datetime.now(timezone.utc).isoformat(),
        "analysis_id": analysis_id("portfolio", str(business_case['portfolio_summary']['total_apps'])),
        "customer_name": CUSTOMER_NAME,
        "sections": [
            {"id": "section-summary", "title": "Summary"},
            {"id": "section-modernization-opportunities", "title": "Modernization Opportunities"},
            {"id": "section-roadmap-proposal", "title": "Roadmap Proposal"},
            {"id": "section-scenario-overview", "title": "Scenario Overview"},
        ],
        "app_links": app_links,
        "portfolio": business_case,
        "scenario_counts": scenario_counts,
    }
    body = "".join([
        '<section class="card title-card" data-testid="app-report-title"><h1>Portfolio Modernization Report</h1><p class="lead">Portfolio-wide summary of technology risk, complexity, modernization scenarios, and indicative business case.</p></section>',
        detail_section("section-summary", "Summary", summary_section),
        detail_section("section-modernization-opportunities", "Modernization Opportunities", opportunity_body),
        detail_section("section-roadmap-proposal", "Roadmap Proposal", roadmap_body),
        detail_section("section-scenario-overview", "Scenario Overview", scenario_overview),
    ])
    return page_shell("Portfolio Modernization Report - GenDiscover", body, payload)


def main() -> None:
    APPLICATION_HTML_DIR.mkdir(parents=True, exist_ok=True)
    business_case = read_json(BUSINESS_CASE_PATH)
    for app_entry in business_case.get("applications", []):
        html = build_application_html(app_entry)
        (APPLICATION_HTML_DIR / f"application_report_{app_entry['app_id']}.html").write_text(html, encoding="utf-8")
    portfolio_html = build_portfolio_html(business_case)
    (REPORTS_DIR / "portfolio_modernization_report.html").write_text(portfolio_html, encoding="utf-8")


if __name__ == "__main__":
    main()
