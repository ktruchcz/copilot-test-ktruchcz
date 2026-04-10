# Static HTML Mockup Generation (Bootstrap 5)

Generate a **static Bootstrap 5 HTML mockup** from a source view definition (e.g., ADF/JSF JSPX or any other UI framework). No dynamic bindings — pure static HTML.

## Rules

- Output **pure HTML5 with Bootstrap 5 styling**. No `{{ }}` bindings, no Angular directives, no JavaScript framework constructs.
- Do not wrap the output in `<html>` or `<body>` tags — the fragment will be embedded in another file.
- All ADF / JSF / source-framework-specific attributes must be translated to standard HTML5 attributes.
- Preserve the hierarchical structure of the source UI exactly.
- Replace example/placeholder data with static representative values.

## Layout Component Mapping

| Source Component | HTML5 / Bootstrap Target |
|-----------------|--------------------------|
| `af:panelFormLayout` | `<form>` |
| `af:panelGroupLayout` / `af:panelGridLayout` | `<div>` / `<table>` with Bootstrap grid |
| `af:panelTabbed` | Bootstrap nav + nav-tabs container; each child tab is one `<div class="tab-pane">` |
| `af:panelSplitter` | Bootstrap grid row; each child element is a column in a single row |
| `af:table` | Bootstrap responsive `<table class="table table-striped">` |
| `af:column` | `<thead>` + `<tbody>` cells |
| `af:outputText` | `<span>` or `<p>` with static text value |
| `af:link` | `<a href="#">` with appropriate label |
| `af:button` / `af:commandButton` | `<button class="btn btn-primary">` or `<button class="btn btn-secondary">` |
| `af:inputText` | `<input type="text" class="form-control">` |
| `af:selectOneChoice` | `<select class="form-select">` with `<option>` children |
| `af:inputDate` | `<input type="date" class="form-control">` |

## Attribute Handling

- Map `label` attributes to `<label>` elements.
- Translate `rendered` conditions to HTML `style="display: none"` or simply include/exclude the element based on the most likely rendering.
- Preserve the `id` attribute values where meaningful.
- For ADF `binding` attributes — remove them (they're server-side).

## Example: Panel Tabbed

```html
<!-- Source: af:panelTabbed -->
<ul class="nav nav-tabs" id="myTab">
  <li class="nav-item">
    <button class="nav-link active" data-bs-toggle="tab" data-bs-target="#tab1">Tab One</button>
  </li>
  <li class="nav-item">
    <button class="nav-link" data-bs-toggle="tab" data-bs-target="#tab2">Tab Two</button>
  </li>
</ul>
<div class="tab-content">
  <div class="tab-pane fade show active" id="tab1">
    <!-- Tab 1 content here -->
  </div>
  <div class="tab-pane fade" id="tab2">
    <!-- Tab 2 content here -->
  </div>
</div>
```

## Example: Panel Splitter → Two Columns

```html
<!-- Source: af:panelSplitter with two children -->
<div class="row">
  <div class="col-6">
    <!-- first child content -->
  </div>
  <div class="col-6">
    <!-- second child content -->
  </div>
</div>
```
