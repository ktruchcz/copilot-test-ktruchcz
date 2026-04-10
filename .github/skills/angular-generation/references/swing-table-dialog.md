# Swing Table/Dialog Migration to Angular

Migrate Java Swing table-based dialogs to Angular components using TypeScript and the `TOTableModel` table infrastructure. This reference is specific to codebases that use the `@allegro/api` library with `IMyEntityTO` transport objects.

## General Rules

### Type Name Conversion

Java and TypeScript use the same transport object names, but TypeScript drops the `I` prefix:
- Java `IMyEntityTO` → TypeScript `MyEntityTO`
- Java `IAAnzeigeSchriftstueckTO` → TypeScript `AAnzeigeSchriftstueckTO`

Imports for transport objects come from `@allegro/api` with the package hierarchy flattened:
```typescript
// Java: de.example.fallgrunddaten.person.intf.IPersonTO
import { PersonTO } from '@allegro/api';
```

```typescript
import { GVName } from '@allegro/api';
```

- When you encounter identifiers or comments in German, keep them in German.
- Access transport object attributes directly as public members — not via Java-style getters.
- Use `===` for enum comparisons (not `.equals()` as in Java).
- When Java compares with `== null` or `!= null`, use truthy/falsy in TypeScript. Use optional chaining (`?.`) for nested access.

## Loading Data on Initialization (ngOnInit)

The Java model's `prepareModel()` method determines what data loads on dialog open:
1. Inner task classes with `GVName` constructor argument = what backend call to make
2. The task's `processInBackground()` method = actual service method and parameters

**TypeScript pattern:**
```typescript
tableModel: TableModel<MyEntityTO> = new TOTableModel(this.columnConfig);

ngOnInit(): void {
    const callHandler = this.backendCallHandlerService
        .newBackendCallHandler<MyEntityTO[]>(GVName.GV_MY_DATA_LADEN);

    callHandler
        .processResponse(
            this.myService.getMyData(this.bgInfos.aktuelleBedarfsgemeinschaftIDTOOderFehler(), callHandler)
        )
        .subscribe(tos => {
            this.tableModel.setObjects(tos);
        });
}
```

**Service injection:**  
`ServiceBroker.getService(IMyService.class)` in Java → inject `MyService` from `@allegro/api` in TypeScript. The TypeScript service method has the same name but takes one additional `callHandler` parameter.

**BG context:**  
`FallgrunddatenDM.getCurrentBG().asIIDTO()` → `this.bgInfos.aktuelleBedarfsgemeinschaftIDTOOderFehler()`

## Table Column Configuration

The Java `TableModel` implementation defines columns in its constructor via `IMyEntity.PROPERTY_COLUMN_NAME` constants. The column attribute name is the part after `PROPERTY_`.

Each TypeScript column config entry:

```typescript
const columnConfig = [
    {
        columnId: 'lastName',           // from IPersonTO.PROPERTY_LAST_NAME
        label: 'Last Name',             // from Java Properties file
        convertToDisplay: (to: PersonTO) => to.lastName ?? '',
    },
    {
        columnId: 'birthDate',
        label: 'Birth Date',
        convertToDisplay: (to: PersonTO) => TemporalRenderer.plainDateTime(to.birthDate),
    },
];
```

### Deriving `convertToDisplay`

1. **Check `getValueAt` for column logic** → reproduce the logic in TypeScript.
2. **If logic uses a Renderer class** → use the corresponding TypeScript renderer (see mapping below).
3. **If logic uses helper methods** → generate corresponding TypeScript helper methods and call them from `convertToDisplay`.
4. **If the attribute is a transport object** → use `TableColumnClassRendererTool` to find the right renderer.
5. **Check the Java View class** for `setCustomTableCellRenderer(columnIndex, renderer)` → adapt `convertToDisplay` using `getRenderedValue` logic.

### Renderer Mapping

| Java | TypeScript | Import |
|------|-----------|--------|
| `CommonConversionRenderer.renderTextKommasepariert` | `CommonConversionRenderer.renderTextKommasepariert` | `src/app/basislogik/utils/common-conversion-renderer.ts` |
| `ArtVersandConversionRenderer.renderVersandart` | `ArtVersandConversionRenderer.renderVersandart` | `src/app/basislogik/utils/art-versand-conversion-renderer.ts` |
| `DateConversionRenderer.renderDateAndTime` | `TemporalRenderer.plainDateTime` | `src/app/basislogik/utils/temporal-renderer.ts` |
| `DateConversionRenderer.renderIntervalFull` | `TemporalRenderer.zeitraumAusDateTimes` | `src/app/basislogik/utils/temporal-renderer.ts` |
| `AbweichenderConversionRenderer.renderAbweichenderEmpfaenger` | `PersonRenderer.renderAbweichenderEmpfaenger` | `src/app/basislogik/utils/person-renderer.ts` |

### Special Enum Notes

- `AAnzeigeSchriftstueckTO.versandart` → enum `ArtVersand` from `@allegro/api`
- `AAnzeigeSchriftstueckTO.druckstatus` → enum `ArtDruckstatus` from `@allegro/api`
- Java enum access: `Kundentyp.NEUGIERIG` → TypeScript: `Kundentyp.NEUGIERIG` (same)

### Resources/Properties
When Java uses `RESOURCES.getString(key)`, substitute the corresponding string value from the Java Properties file directly in the TypeScript code.

## Date and Time Types

Use the same types as Java (`LocalDate`, `YearMonth`, `DateTime`, `DateMidnight`, `Instant`), which map to the JavaScript Temporal API. Import from `@allegro/api`. Use Temporal API methods for comparisons and manipulations.
