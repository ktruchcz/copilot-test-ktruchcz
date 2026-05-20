---
name: swing-to-angular-table-dialog-migrator
description: Migrate Java Swing table dialogs into Angular data-table components using TypeScript. Converts table models, initialization logic, column definitions, and renderer logic from Swing to Angular, compatible with any table library (Angular Material, PrimeNG, ng-zorro, etc.) and backend API pattern. Use this when converting Swing table dialogs where the source contains TableModel classes, column definitions, initialization methods, or custom renderer logic.
---

# Swing to Angular Table Dialog Migrator

Generate Angular code that respects the target application's existing table infrastructure, TypeScript conventions, and backend API patterns.

## Required inputs

- Java Swing dialog or model classes
- Java TableModel and any renderer/helper classes  
- Column definitions, labels, and properties used in the source
- Target TypeScript table library and service/API patterns
- Any table initialization or backend call patterns used in the target application

## Workflow

1. Read [references/implementation.md](references/implementation.md).
2. Identify initialization logic and related task/loader classes in the Swing source.
3. Map backend service calls and initialization patterns into Angular `ngOnInit` and `OnInit` hooks.
4. Extract Java table columns and convert them into the target table library's column configuration format.
5. Recreate renderer/formatter logic using the target application's existing TypeScript renderer helpers or standard Angular pipes.

## Output contract

- Output an Angular component using the target application's table library and conventions.
- Preserve source code identifiers and comments (maintain original language if applicable).
- Use the target application's API/transport object naming conventions.
- Match the target project's service injection and backend-call patterns.

## Reference files

- [references/implementation.md](references/implementation.md): migration rules for initialization, table columns, and renderer mapping.
