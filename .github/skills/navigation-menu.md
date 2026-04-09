# Angular Navigation Menu Generation (DGUV Sidenav)

Generate a navigation sidebar using the DGUV `dguv-sidenav` component.

## Rules

- Use only DGUV sidenav components — no custom styling.
- Preserve all menu items and their hierarchy from the source file exactly.
- Do not create menu items that are not present in the source (e.g., do not add a default "Home" item).
- Remove any source-framework action listeners; replace with Angular `routerLink` navigation.
- Derive `routerLink` values from the provided Angular routes module. Match the path exactly.
- Use `<dguv-sidenav-collapsible>` for menu groups that have child items.
- Use `<dguv-sidenav-item>` for leaf menu items (no children).

## Routing Reference Pattern

Given routes like:

```typescript
const routes: Routes = [
  { path: 'customers/list', component: CustomerListComponent },
  { path: 'orders/detail', component: OrderDetailComponent },
];
```

Use the `path` values as `routerLink` targets.

## Output Template

```html
<dguv-sidenav>

  <!-- Group with nested items -->
  <dguv-sidenav-collapsible
    title="Group Title"
    svgIcon="users-four"
  >
    <dguv-sidenav-item>
      <a routerLink="customers/list"
         routerLinkActive="active"
         dguvSidenavLink>
        Customer List
      </a>
    </dguv-sidenav-item>

    <dguv-sidenav-item>
      <a routerLink="orders/detail"
         routerLinkActive="active"
         dguvSidenavLink>
        Order Detail
      </a>
    </dguv-sidenav-item>
  </dguv-sidenav-collapsible>

  <!-- Standalone item (no children) -->
  <dguv-sidenav-item svgIcon="chart-bar">
    <a routerLink="dashboard"
       routerLinkActive="active"
       dguvSidenavLink>
      Dashboard
    </a>
  </dguv-sidenav-item>

</dguv-sidenav>
```

## ADF Source Notes (skip if not migrating from ADF)

When the source is an ADF menu XML or `navigationBar` component:

- Map each `af:commandNavigationItem` to a `<dguv-sidenav-item>` with `routerLink`.
- Map `af:navigationPane` to `<dguv-sidenav-collapsible>`.
- Ignore `actionListener` attributes — replace with `routerLink`.
- Derive menu item labels from the `text` attribute of ADF navigation items.
