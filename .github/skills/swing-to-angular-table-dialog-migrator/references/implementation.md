# Implementation Guide

## Goal

Migrate a Swing table dialog into Angular using the target application's backend API patterns and table library conventions.

## Transport object and import rules

- Follow the target project's naming conventions for data transfer objects (DTOs).
- Import DTOs from the project's standard API/service package.
- Preserve source code identifiers and comments in their original form.

## Initialization rules

- Read the initialization method (e.g., `prepareModel()`, `init()`, or the dialog constructor) to learn what loads on dialog open.
- Track inner task/loader classes and the data types they work with.
- Map legacy service lookup patterns to the target project's dependency injection pattern (e.g., Angular `@Injectable`, constructor parameters).
- Check if the target project uses a call handler or response wrapper pattern; if so, apply it consistently.
- Store loaded results in the component's data source using the target table library's expected pattern.

## Table-display rules

- Derive columns from the Java TableModel constructor or column definition constants (e.g., `PROPERTY_...` constants).
- Build column configuration objects: `id/key`, `label/header`, and `formatter/renderer` function for each column.
- Recreate `getValueAt()` logic in TypeScript using Angular pipes or custom formatters.
- For custom Java renderers, look for equivalent formatters in the target project.
- If the source uses a nested object renderer, apply the target project's nested object display pattern.
- Resolve labels from resource bundles or property files in the source; apply the target project's i18n or label lookup method.

## Special cases

- Preserve enum semantics from the source. Map Java enums to TypeScript union types or enums as appropriate.
- For date/time columns, use Angular's built-in pipes (e.g., `date`, `datetime`) or the target project's temporal formatting helpers.
- For nested or complex objects, use the target project's existing renderer libraries rather than custom code.

## Output checklist

- Backend loading flow uses the target project's service injection and API call patterns correctly.
- Column configuration matches the target table library's expected format.
- Renderer/formatter logic is mapped to existing TypeScript helpers or Angular pipes rather than custom implementations.
- All DTOs and service names follow the target project's conventions.
