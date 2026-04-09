---
name: angular-generation
description: "Generate Angular TypeScript components, HTML templates, validators, and navigation. Use when the TARGET is Angular—regardless of source technology (ADF/JSF, Java Swing, React, .NET, etc.). Invoke whenever generating .component.ts files, Angular reactive forms, @Input/@Output patterns, table/list components, navigation menus, or Angular validators. Also use when the user mentions migrating a UI to Angular, setting up component routing, applying a DGUV design system, or converting Swing tables/dialogs."
---

# Angular Generation Skill

This skill guides the generation of idiomatic Angular / TypeScript UI code. All core rules apply regardless of what source technology is being migrated. Source-specific input-parsing notes are in separate reference sections.

## Core Angular Conventions (apply everywhere)

- Use **TypeScript strict mode** patterns: initialize all properties, use definite assignment (`!`) or initializer expressions — no uninitialized properties left hanging.
- Use `@Input()` with DTO model types as inputs — not individual fields.
  ```typescript
  @Input() customerDto: CustomerDto;
  ```
- Use `@Output()` and `EventEmitter` for outbound events.
- Pass data to other components via **Route Parameters** (not component properties across router boundary).
- Initialize global attributes in the **constructor** or with field initializers to ensure definite assignment.
- Use **Angular Reactive Forms** (`ReactiveFormsModule`) for form handling.
- Fetch data via injected services. Never hardcode dummy data in production component code.
- Use `.scss` file extension for component stylesheets:
  ```typescript
  styleUrls: ['./<component>.component.scss']
  ```
- Import models from the `model` package:
  ```typescript
  import { MyModel } from 'src/app/model/models';
  ```
- Subscribe to input parameters in `ngOnInit`.

## TypeScript Strictness Patterns

Handle these common TypeScript strict-mode errors with the **default value approach**:

- `TS2322: Type 'string | undefined' is not assignable to type 'string'` → use `?? ''`
- `TS2322: Type 'number | undefined' is not assignable to type 'number'` → use `?? 0`
- `TS2564: Property has no initializer` → use field initializer or `= {} as MyType`
- Use the optional chaining operator (`?.`) when accessing nested properties that may be `undefined`.
- Prefer `if (value)` / `if (!value)` over `value != null` / `value == null` comparisons.

## Reference Files

| Task | Reference |
|------|-----------|
| Generate a full Angular component (TypeScript + HTML) | [references/component-generation.md](references/component-generation.md) |
| Generate a static HTML mockup from ADF/JSF | [references/html-mockup-generation.md](references/html-mockup-generation.md) |
| Apply DGUV design system components to HTML | [references/dguv-styling.md](references/dguv-styling.md) |
| Generate a DGUV navigation sidebar | [references/navigation-menu.md](references/navigation-menu.md) |
| Migrate a Java Swing table/dialog to Angular | [references/swing-table-dialog.md](references/swing-table-dialog.md) |
| Migrate a Java Swing validator to Angular | [references/swing-validation.md](references/swing-validation.md) |

Read the relevant reference file before generating code for that scenario.
