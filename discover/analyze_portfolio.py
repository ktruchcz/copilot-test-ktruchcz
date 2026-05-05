#!/usr/bin/env python3
"""Portfolio Discovery Analysis Script.

Reads application portfolio data from an Excel file located in discover/input/
and generates a portfolio modernization discovery report in discover/output/.
"""

import os
import sys
from collections import Counter
from datetime import datetime

try:
    import openpyxl
except ImportError:
    print("Installing openpyxl...", file=sys.stderr)
    os.system(f"{sys.executable} -m pip install openpyxl -q")
    import openpyxl

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, "input", "apps_db_complete.xlsx")
OUTPUT_FILE = os.path.join(SCRIPT_DIR, "output", "portfolio-discovery.md")

# Technology maturity classification
LEGACY_TECH = [
    "COBOL", "FORTRAN", "VB.NET", "Perl", "Java 8", "Java 11",
    "Python 3.7", "Python 3.8", "Ruby 2.7", "Node.js 14",
    "PHP 7", "Angular.js",
]

MODERN_TECH = [
    "Java 17", "Java 21", "Python 3.11", "Python 3.12",
    "Node.js 18", "Node.js 20", "Go 1.19", "Go 1.21",
    "Rust", ".NET 8", ".NET 9", "ASP.NET Core",
]

# Modernization strategy mapping (7-R model)
MODERNIZATION_STRATEGIES = {
    "Retire": "Application is no longer needed; decommission it.",
    "Retain": "Keep as-is; revisit later (too risky or costly to change now).",
    "Rehost": "Lift-and-shift to cloud with minimal changes.",
    "Replatform": "Lift-and-reshape: minor optimisations to cloud-native services.",
    "Repurchase": "Move to a SaaS or 3rd-party commercial product.",
    "Refactor/Re-architect": "Redesign to be cloud-native (microservices, containers).",
    "Rebuild": "Rewrite the application from scratch using a modern cloud-native approach.",
}


def load_portfolio(filepath: str) -> list[dict]:
    """Load portfolio data from an Excel workbook."""
    wb = openpyxl.load_workbook(filepath)
    ws = wb.active
    rows = list(ws.iter_rows(values_only=True))
    headers = rows[0]
    return [dict(zip(headers, row)) for row in rows[1:] if any(row)]


def classify_tech_maturity(lang: str) -> str:
    """Classify a programming language as legacy, modern, or current."""
    lang = str(lang or "")
    for tech in LEGACY_TECH:
        if tech.lower() in lang.lower():
            return "Legacy"
    for tech in MODERN_TECH:
        if tech.lower() in lang.lower():
            return "Modern"
    return "Current"


def suggest_strategy(app: dict) -> str:
    """Suggest a 7-R modernization strategy for an application."""
    status = str(app.get("Application status", "")).lower()
    sol_type = str(app.get("Solution type", "")).lower()
    deploy = str(app.get("Deployment type", "")).lower()
    lang = str(app.get("programming language", ""))
    arch = str(app.get("Application Architecture", "")).lower()
    containerized = str(app.get("Application is containerized", "")).lower()
    criticality = str(app.get("criticality", "")).lower()
    decomm = str(app.get("Decomission date", "") or app.get("Decommission date", ""))

    if status == "retired" or (decomm.isdigit() and int(decomm) <= datetime.now().year + 1):
        return "Retire"

    if "3rd party" in sol_type or "open source" in sol_type:
        return "Repurchase"

    tech_maturity = classify_tech_maturity(lang)

    if "on-premise" in deploy and containerized == "no":
        if tech_maturity == "Legacy" and criticality in ("high", "critical"):
            return "Refactor/Re-architect"
        if tech_maturity == "Legacy":
            return "Replatform"
        return "Rehost"

    if tech_maturity == "Legacy" and "1-tier" in arch:
        return "Rebuild"

    if tech_maturity == "Legacy":
        return "Refactor/Re-architect"

    if "on-premise" in deploy:
        return "Rehost"

    return "Retain"


def generate_report(apps: list[dict]) -> str:
    """Generate the portfolio discovery Markdown report."""
    total = len(apps)
    active = [a for a in apps if str(a.get("Application status", "")).lower() == "production"]
    retired = [a for a in apps if str(a.get("Application status", "")).lower() == "retired"]

    criticality_dist = Counter(a.get("criticality") for a in apps)
    solution_dist = Counter(a.get("Solution type") for a in apps)
    deploy_dist = Counter(a.get("Deployment type") for a in apps)
    arch_dist = Counter(a.get("Application Architecture") for a in apps)
    lang_dist = Counter(a.get("programming language") for a in apps)
    containerized_dist = Counter(a.get("Application is containerized") for a in apps)
    cicd_dist = Counter(a.get("CI_CD present") for a in apps)
    os_dist = Counter(a.get("Operating system") for a in apps)

    # Technology maturity
    legacy_apps = [a for a in apps if classify_tech_maturity(str(a.get("programming language", ""))) == "Legacy"]
    modern_apps = [a for a in apps if classify_tech_maturity(str(a.get("programming language", ""))) == "Modern"]
    current_apps = [a for a in apps if classify_tech_maturity(str(a.get("programming language", ""))) == "Current"]

    # On-premise apps
    onprem_apps = [a for a in apps if "on-premise" in str(a.get("Deployment type", "")).lower()]
    cloud_apps = [a for a in apps if str(a.get("Deployment type", "")).lower() == "aws"]

    # No CI/CD
    no_cicd = [a for a in apps if str(a.get("CI_CD present", "")).lower() == "no"]

    # Not containerized (active only)
    not_containerized = [a for a in active if str(a.get("Application is containerized", "")).lower() == "no"]

    # DB licensing costs
    licensed_db = [a for a in apps if str(a.get("DB License required", "")).lower() == "yes"]

    # Strategy assignments
    for app in apps:
        app["_strategy"] = suggest_strategy(app)

    strategy_dist = Counter(a["_strategy"] for a in apps)

    lines = []
    lines.append("# Portfolio Discovery Report")
    lines.append(f"\n**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}")
    lines.append(f"**Source**: `discover/input/apps_db_complete.xlsx`")

    lines.append("\n---\n")
    lines.append("## 1. Executive Summary\n")
    lines.append(
        f"The portfolio comprises **{total} applications** across multiple business units. "
        f"Of these, **{len(active)}** are currently in production and **{len(retired)}** are retired. "
        f"**{len(legacy_apps)}** applications ({len(legacy_apps)*100//total}%) rely on legacy or "
        f"end-of-life technologies and represent the highest modernization risk. "
        f"**{len(onprem_apps)}** applications ({len(onprem_apps)*100//total}%) are fully or partially "
        f"on-premise and are candidates for cloud migration. "
        f"**{len(no_cicd)}** applications lack CI/CD pipelines, indicating significant DevOps maturity gaps."
    )

    lines.append("\n---\n")
    lines.append("## 2. Portfolio Overview\n")
    lines.append(f"| Metric | Value |")
    lines.append(f"|--------|-------|")
    lines.append(f"| Total Applications | {total} |")
    lines.append(f"| Production | {len(active)} |")
    lines.append(f"| Retired | {len(retired)} |")
    lines.append(f"| Custom-Made | {solution_dist.get('Custom made', 0)} |")
    lines.append(f"| 3rd Party / SaaS | {solution_dist.get('3rd party software', 0)} |")
    lines.append(f"| Open Source | {solution_dist.get('Open Source', 0)} |")

    lines.append("\n### 2.1 Criticality Distribution\n")
    lines.append("| Criticality | Count | % |")
    lines.append("|-------------|-------|---|")
    for level in ["Critical", "High", "Medium", "Low"]:
        cnt = criticality_dist.get(level, 0)
        lines.append(f"| {level} | {cnt} | {cnt*100//total}% |")

    lines.append("\n### 2.2 Deployment Distribution\n")
    lines.append("| Deployment Type | Count | % |")
    lines.append("|-----------------|-------|---|")
    for dtype, cnt in sorted(deploy_dist.items(), key=lambda x: -x[1]):
        lines.append(f"| {dtype} | {cnt} | {cnt*100//total}% |")

    lines.append("\n### 2.3 Architecture Distribution\n")
    lines.append("| Architecture | Count |")
    lines.append("|--------------|-------|")
    for arch, cnt in sorted(arch_dist.items(), key=lambda x: -x[1]):
        lines.append(f"| {arch} | {cnt} |")

    lines.append("\n---\n")
    lines.append("## 3. Technology Assessment\n")

    lines.append("### 3.1 Programming Languages\n")
    lines.append("| Language | Count | Maturity |")
    lines.append("|----------|-------|----------|")
    for lang, cnt in sorted(lang_dist.items(), key=lambda x: -x[1]):
        maturity = classify_tech_maturity(str(lang))
        lines.append(f"| {lang} | {cnt} | {maturity} |")

    lines.append("\n### 3.2 Technology Maturity Summary\n")
    lines.append("| Maturity | Count | % |")
    lines.append("|----------|-------|---|")
    lines.append(f"| Legacy | {len(legacy_apps)} | {len(legacy_apps)*100//total}% |")
    lines.append(f"| Current | {len(current_apps)} | {len(current_apps)*100//total}% |")
    lines.append(f"| Modern | {len(modern_apps)} | {len(modern_apps)*100//total}% |")

    lines.append("\n### 3.3 Legacy Applications (High Priority)\n")
    lines.append("| App ID | Name | Language | Criticality | Deployment | Strategy |")
    lines.append("|--------|------|----------|-------------|------------|----------|")
    for a in sorted(legacy_apps, key=lambda x: {"Critical": 0, "High": 1, "Medium": 2, "Low": 3}.get(str(x.get("criticality")), 4)):
        lines.append(
            f"| {a['app_id']} | {a['name']} | {a['programming language']} "
            f"| {a['criticality']} | {a['Deployment type']} | {a['_strategy']} |"
        )

    lines.append("\n### 3.4 Operating Systems\n")
    lines.append("| OS | Count |")
    lines.append("|----|-------|")
    for os_name, cnt in sorted(os_dist.items(), key=lambda x: -x[1]):
        lines.append(f"| {os_name} | {cnt} |")

    lines.append("\n---\n")
    lines.append("## 4. Cloud Migration Analysis\n")

    lines.append(f"### 4.1 On-Premise Applications ({len(onprem_apps)} total)\n")
    lines.append("| App ID | Name | Criticality | Architecture | Containerized | CI/CD | Strategy |")
    lines.append("|--------|------|-------------|--------------|---------------|-------|----------|")
    for a in sorted(onprem_apps, key=lambda x: {"Critical": 0, "High": 1, "Medium": 2, "Low": 3}.get(str(x.get("criticality")), 4)):
        lines.append(
            f"| {a['app_id']} | {a['name']} | {a['criticality']} "
            f"| {a['Application Architecture']} | {a['Application is containerized']} "
            f"| {a['CI_CD present']} | {a['_strategy']} |"
        )

    lines.append("\n### 4.2 Database Analysis\n")
    db_dist = Counter(a.get("db_engine") for a in apps)
    lines.append("| Database | Count |")
    lines.append("|----------|-------|")
    for db, cnt in sorted(db_dist.items(), key=lambda x: -x[1]):
        lines.append(f"| {db} | {cnt} |")

    lines.append(f"\n**Applications with licensed databases**: {len(licensed_db)} "
                 f"({len(licensed_db)*100//total}%) — consider open-source alternatives or managed cloud services.")

    total_db_storage = sum(int(a.get("DB storage in GB", 0) or 0) for a in apps)
    lines.append(f"\n**Total DB Storage**: {total_db_storage:,} GB across all applications.")

    lines.append("\n---\n")
    lines.append("## 5. DevOps & Operational Readiness\n")

    lines.append("| Indicator | Yes | No | % Ready |")
    lines.append("|-----------|-----|-----|---------|")
    yes_cicd = cicd_dist.get("Yes", 0)
    no_cicd_cnt = cicd_dist.get("No", 0)
    lines.append(f"| CI/CD Pipeline | {yes_cicd} | {no_cicd_cnt} | {yes_cicd*100//total}% |")
    yes_cont = containerized_dist.get("Yes", 0)
    no_cont = containerized_dist.get("No", 0)
    lines.append(f"| Containerized | {yes_cont} | {no_cont} | {yes_cont*100//total}% |")

    logging_dist = Counter(a.get("logging_solution") for a in apps)
    no_logging = logging_dist.get("None", 0)
    monitoring_dist = Counter(a.get("monitoring_tool") for a in apps)
    no_monitoring = monitoring_dist.get("None", 0)
    lines.append(f"| Logging Solution | {total - no_logging} | {no_logging} | {(total - no_logging)*100//total}% |")
    lines.append(f"| Monitoring Tool | {total - no_monitoring} | {no_monitoring} | {(total - no_monitoring)*100//total}% |")

    lines.append("\n### 5.1 Applications Without CI/CD\n")
    lines.append("| App ID | Name | Criticality | Language | Deployment |")
    lines.append("|--------|------|-------------|----------|------------|")
    for a in no_cicd:
        lines.append(
            f"| {a['app_id']} | {a['name']} | {a['criticality']} "
            f"| {a['programming language']} | {a['Deployment type']} |"
        )

    lines.append("\n---\n")
    lines.append("## 6. Modernization Strategy (7-R Model)\n")
    lines.append("| Strategy | Count | % |")
    lines.append("|----------|-------|---|")
    for strategy, cnt in sorted(strategy_dist.items(), key=lambda x: -x[1]):
        lines.append(f"| {strategy} | {cnt} | {cnt*100//total}% |")

    lines.append("\n### 6.1 Strategy Descriptions\n")
    for strategy, desc in MODERNIZATION_STRATEGIES.items():
        if strategy in strategy_dist:
            lines.append(f"- **{strategy}**: {desc}")

    lines.append("\n### 6.2 Full Application Strategy Map\n")
    lines.append("| App ID | Name | Business Unit | Criticality | Language | Current Deploy | Strategy |")
    lines.append("|--------|------|---------------|-------------|----------|----------------|----------|")
    for a in sorted(apps, key=lambda x: (x["_strategy"], str(x.get("criticality")))):
        lines.append(
            f"| {a['app_id']} | {a['name']} | {a.get('business unit')} | {a['criticality']} "
            f"| {a['programming language']} | {a['Deployment type']} | {a['_strategy']} |"
        )

    lines.append("\n---\n")
    lines.append("## 7. Risk Assessment\n")
    lines.append("| Risk | Applications Affected | Severity |")
    lines.append("|------|-----------------------|----------|")
    lines.append(f"| Legacy/EOL technology | {len(legacy_apps)} | High |")
    lines.append(f"| No CI/CD pipeline | {len(no_cicd)} | High |")
    lines.append(f"| On-Premise infrastructure | {len(onprem_apps)} | Medium |")
    lines.append(f"| Not containerized (production) | {len(not_containerized)} | Medium |")
    lines.append(f"| Proprietary DB licensing | {len(licensed_db)} | Medium |")
    lines.append(f"| Unknown architecture | {arch_dist.get('unknown', 0)} | Low |")
    lines.append(f"| No monitoring | {no_monitoring} | Low |")

    lines.append("\n---\n")
    lines.append("## 8. Recommendations\n")
    lines.append("### Priority 1 — Immediate Actions\n")
    lines.append(
        f"1. **Address Legacy Critical Apps**: {len([a for a in legacy_apps if a.get('criticality') in ('Critical','High')])} "
        "applications with legacy technology are critical/high-criticality. Initiate refactoring or rebuild plans immediately."
    )
    lines.append(
        f"2. **Implement CI/CD**: {len(no_cicd)} applications lack automated pipelines. "
        "Implement CI/CD for all production applications to reduce deployment risk."
    )

    lines.append("\n### Priority 2 — Short-Term (3-6 months)\n")
    lines.append(
        f"3. **Cloud Migration**: {len(onprem_apps)} on-premise applications should be assessed "
        "for cloud migration (Rehost or Replatform). Begin with low-criticality, non-legacy apps."
    )
    lines.append(
        f"4. **Containerization**: {len(not_containerized)} production applications are not containerized. "
        "Containerize applications before cloud migration to simplify operations."
    )

    lines.append("\n### Priority 3 — Medium-Term (6-12 months)\n")
    lines.append(
        f"5. **DB Licensing**: {len(licensed_db)} applications use licensed databases. "
        "Evaluate migration to open-source (PostgreSQL, MySQL) or managed cloud database services to reduce costs."
    )
    lines.append(
        "6. **Observability**: Standardize on a single logging and monitoring stack across all applications."
    )
    lines.append(
        "7. **Architecture Modernization**: 6 applications have unknown architecture. "
        "Document and assess these for potential 3-tier or microservices refactoring."
    )

    lines.append("\n---\n")
    lines.append("*Report generated by `discover/analyze_portfolio.py` from `discover/input/apps_db_complete.xlsx`.*\n")

    return "\n".join(lines)


def main():
    """Main entry point."""
    if not os.path.exists(INPUT_FILE):
        print(f"ERROR: Input file not found: {INPUT_FILE}", file=sys.stderr)
        sys.exit(1)

    print(f"Loading portfolio from: {INPUT_FILE}")
    apps = load_portfolio(INPUT_FILE)
    print(f"Loaded {len(apps)} applications.")

    report = generate_report(apps)

    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(report)

    print(f"Portfolio discovery report written to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
