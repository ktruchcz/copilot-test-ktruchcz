# Portfolio HTML Contract

## Title

- `<title>` must be `Portfolio Modernization Report - <customer_name> - GenDiscover`
- The visible H1 inside the title card must be `Portfolio Modernization Report`

## Required top block

- The first body card must use `data-testid="app-report-title"`
- It must contain the H1 and an optional lead paragraph.

## Required section conventions

- Summary section wrapper test id: `section-summary`
- Modernization opportunities section wrapper test id: `section-modernization-opportunities`
- Roadmap section wrapper test id: `section-roadmap-proposal`
- Scenario overview section wrapper test id: `section-scenario-overview`

## Portfolio navigation

- If application HTML pages are generated, include relative links:
  - `application_reports/application_report_<app_id>.html`
- These links should appear in at least one visible portfolio section.

## Metrics style

- Highlight major numeric values in large, glowing text.
- Use accent-colored numbers for key modernization metrics.

## Embedded data

- The embedded JSON payload should include:
  - report title
  - lead text
  - section list
  - optional app link list
  - generated timestamp
  - analysis ID