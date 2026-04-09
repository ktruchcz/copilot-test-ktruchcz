# Angular Component Code Generation

Generate a complete Angular component (TypeScript + HTML template).

## Rules

### Scope

- Generate only `{component}.component.ts` and `{component}.component.html`. Do not generate or modify module files, API files, or model files.
- Do not rename files or change module structure.

### TypeScript Component

- Keep naming conventions for components, operations, and models exactly as provided.
- Use `.scss` for stylesheets: `styleUrls: ['./<component>.component.scss']`
- Import services from the `api` package:
  ```typescript
  import { MyService } from 'src/app/api/my.service';
  ```
- Import models from the `model` package:
  ```typescript
  import { Model1, Model2 } from 'src/app/model/models';
  ```
- Use `@Input()` with full DTO model types — not individual fields:
  ```typescript
  @Input() customerDto: CustomerDto;
  ```
- Use `@Output()` and `EventEmitter` for events.
- Pass DTO models to other components via Route Parameters:
  ```typescript
  navigate() {
    this.router.navigate(['/target-route', model]);
  }
  ```
- Handle the case where the input model is not passed (null/undefined guard in `ngOnInit`).
- Initialize models and subscribe to input parameters in `ngOnInit`.
- Initialize all global attributes in the constructor or with field initializers to ensure definite assignment.
- Fetch data via injected services. Replace any example/placeholder data with real service calls.
- Make all code type-safe — no `any` types unless absolutely unavoidable.
- Implement all HTML elements fully. Do not leave any placeholders.
- Use Angular `DatePipe` with the `'shortDate'` format for dates.
- Use Angular's reactive forms (`FormGroup`, `FormControl`) for form inputs.
- Import `ReactiveFormsModule` where reactive forms are used.

### HTML Template

- Do not modify the layout or styling of existing HTML.
- Bind all component properties to the template.
- Apply integrated form validation using Angular's reactive form approach.
- Use the `short` locale for `DatePipe` when displaying dates.

### Handling TypeScript Strict Errors

Use the default value (initializer) approach:

```typescript
// TS2564: Property has no initializer
myProp: string = '';
myModel: MyDto = {} as MyDto;

// TS2322: Type 'string | undefined' is not assignable
displayName: string = this.dto?.name ?? '';
```

## Variant: Component Without API Calls

When the component has no API/service calls:

- Follow all rules above but do not inject or use any services.
- All data comes via `@Input()` — no API calls in the component.
- There is no `api` package import needed.

## Validation Checklist

- [ ] Only `{component}.component.ts` and `.html` generated — no other files changed
- [ ] All properties initialized (no TS2564 errors)
- [ ] Type-safe — no `string | undefined` assignments where `string` is expected
- [ ] Models fetched from services (not hardcoded)
- [ ] `@Input()` uses DTO models, not individual fields
- [ ] `ReactiveFormsModule` imported if reactive forms are used
- [ ] `ngOnInit` subscribes to route parameters and loads data

---

## ADF Source Notes (skip if not migrating from ADF)

When the source is an ADF `.jspx` / `.jsff` view:

- Map `af:` JSF component attributes to Angular bindings.
- ADF operations translate to Angular service calls.
- ADF `inputText` → `formControlName` bound input
- ADF `selectOneChoice` → reactive form select or `mat-select`
