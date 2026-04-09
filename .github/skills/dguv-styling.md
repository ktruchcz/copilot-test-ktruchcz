# DGUV Design System Styling

Transform plain Bootstrap / standard HTML form elements into their DGUV Angular Material component equivalents.

The DGUV library wraps Angular Material. Use only DGUV library components — no custom CSS styling.

## Rules

- Replace standard HTML form controls with their DGUV component equivalents (see mapping table below).
- **Do not** change `templateUrl` or `styleUrls` in the TypeScript component.
- **Do not** remove any existing imports.
- **Do not** change data types of existing component variables.
- Leave `<div>` elements as-is unless they contain an `<input>` inside them.
- Leave code that is commented out as-is.
- Always ensure closing tags match opening tags (e.g., `<mat-label></mat-label>`).

## Datepicker: TypeScript Side

When transforming a date input (`type="date"`) and there is an existing `FormGroup` or `FormControl`, add this code to `ngOnInit` to reformat the value as an ISO date string:

```typescript
// ngOnInit addition — add rxjs import too:
import { takeUntilDestroyed } from "@angular/core/rxjs-interop";

this.form.get("formcontrolname")?.valueChanges
  .pipe(takeUntilDestroyed())
  .subscribe(dateChange => {
    this.form.get("formcontrolname")?.patchValue(
      dateChange.toISODate(), { emitEvent: false }
    );
  });
```

> If there is **no** FormGroup in the TypeScript file, do **not** add any TypeScript code.

## Table: TypeScript Side

When transforming a `<table>`, declare the displayed columns in the TypeScript file:

```typescript
displayedColumns: string[] = ['firstColumn', 'secondColumn', 'thirdColumn'];
```

## Component Transformation Examples

### Text Input

```html
<!-- Before -->
<label for="id1" class="form-label">Label</label>
<input type="text" class="form-control" id="id1" formControlName="myField" maxlength="60">

<!-- After -->
<dguv-form-field hideOptionalMarker="false">
  <mat-label>Label</mat-label>
  <input matInput formControlName="myField" maxlength="60" />
  <dguv-form-field-status></dguv-form-field-status>
</dguv-form-field>
```

### Date Input

```html
<!-- Before -->
<label for="id1" class="form-label">Date</label>
<input type="date" class="form-control" id="id1" formControlName="myDate">

<!-- After -->
<dguv-form-field>
  <mat-label>Date</mat-label>
  <input matInput type="date" [matDatepicker]="datePicker" formControlName="myDate"/>
  <mat-datepicker-toggle matIconSuffix [for]="datePicker"></mat-datepicker-toggle>
  <mat-datepicker #datePicker></mat-datepicker>
</dguv-form-field>
```

### Radio Group

```html
<!-- Before -->
<label>Status</label>
<div>
  <input type="radio" formControlName="status" value="active">
  <label>Active</label>
  <input type="radio" formControlName="status" value="inactive">
  <label>Inactive</label>
</div>

<!-- After -->
<dguv-form-group alignment="horizontal">
  <dguv-group-label>Status</dguv-group-label>
  <mat-radio-group formControlName="status">
    <mat-radio-button value="active">Active</mat-radio-button>
    <mat-radio-button value="inactive">Inactive</mat-radio-button>
  </mat-radio-group>
</dguv-form-group>
```

### Select / Dropdown

```html
<!-- Before -->
<label for="sel1" class="form-label">Category</label>
<select class="form-control" id="sel1" formControlName="category">
  <option value=""></option>
  <option value="a">Option A</option>
</select>

<!-- After -->
<dguv-form-field>
  <mat-label>Category</mat-label>
  <mat-select [disableRipple]="true" [multiple]="false" [required]="false"
              formControlName="category">
    <mat-option value=""></mat-option>
    <mat-option value="a">Option A</mat-option>
  </mat-select>
</dguv-form-field>
```

### Submit Button

```html
<!-- Before -->
<button type="submit" class="btn btn-primary" (click)="onSubmit()">Search</button>

<!-- After -->
<button mat-flat-button type="submit" (click)="onSubmit()">Search</button>
```

### Secondary Button

```html
<!-- Before -->
<button type="reset" class="btn btn-secondary">Reset</button>

<!-- After -->
<button type="reset" class="me-2" mat-stroked-button>Reset</button>
```

### Table

```html
<!-- Before: <table class="table table-striped"> ... </table> -->

<!-- After -->
<table mat-table [dataSource]="items" dguvTable responsiveMode="responsive">
  <ng-container matColumnDef="columnId">
    <th mat-header-cell *matHeaderCellDef>Column Header</th>
    <td mat-cell *matCellDef="let element"
        dguvHideOnTable [hideOnMobile]="!element.columnId">
      {{ element.columnId }}
    </td>
  </ng-container>
  <!-- repeat ng-container for each column -->
  <tr mat-header-row *matHeaderRowDef="displayedColumns"></tr>
  <tr mat-row *matRowDef="let row; columns: displayedColumns"></tr>
</table>
```

## Review Checklist (Post-Generation)

- [ ] All compiler errors fixed
- [ ] Every referenced DTO, controller, or component has a corresponding import
- [ ] Code referencing a non-existent FormGroup is removed
- [ ] Missing imports added for any referenced data types
- [ ] Data types of existing variables not changed
- [ ] `formControlName` preserved on all transformed elements
- [ ] `templateUrl` and `styleUrls` unchanged in TypeScript
