# Swing Validator Migration to Angular

Migrate Java Swing validation logic to Angular TypeScript validators. This reference is specific to codebases that use the `@allegro/api` library and the `IValidator` interface.

## Output Contract

A TypeScript validator must implement the `IValidator` interface located at:
`src/app/basislogik/plausis/validator.ts`

Add messages using the `IValidationGlobalContext` methods. The interface is at:
`src/app/basislogik/plausis/validation-global-context.ts`

## General Rules

### Type Name Conversion

Transport object imports come from `@allegro/api` with package hierarchy flattened and `I` prefix removed:
```typescript
// Java: de.example.fallgrunddaten.person.intf.IBetriebTO
import { BetriebTO } from '@allegro/api';
import { GVName } from '@allegro/api';
```

### Attribute Access

- Java getters → TypeScript public member access:
  - Java: `entityTO.getAttribute()` → TypeScript: `entityTO.attribute`
- Java `== null` / `!= null` → TypeScript falsy/truthy: `if (!value)` / `if (value)`
- Use optional chaining (`?.`) for nested property access.

### Property Path

Java: `context.setPropertyPath(EntityTO.PROPERTY_MY_ATTRIBUTE)` →
TypeScript: `localContext.propertyPath = ['myAttribute']`

(Use the property name as a string directly — don't reference the Java static constant.)

### Null / Undefined

Attributes may be `undefined` in TypeScript. Guard with optional chaining and falsy checks rather than explicit null comparisons.

### Predicates

Java `Predicate` code → TypeScript lambda + `PredicateHelper` utilities:
```typescript
import { PredicateHelper } from 'src/app/basislogik/utils/predicate-helper.ts';
// and/or/negate via PredicateHelper methods
```

### Validation Message Keys

Java `ValidationMessageKeys` → TypeScript enum `ValidationMessageKeys`:
`src/app/basislogik/plausis/validation-message-keys.ts`

### Date and Time

Use the same types as Java (`LocalDate`, `YearMonth`, `DateTime`, `DateMidnight`, `Instant`) mapped to the JavaScript Temporal API. Import from `@allegro/api`. Use Temporal API methods for date comparisons and arithmetic.

## Utility Method Mapping

| Java | TypeScript | Import |
|------|-----------|--------|
| `AbstractCommonCondition.validateDatumVonGueltig` | `CommonValidationUtils.validateDatumVonGueltig` | `src/app/basislogik/utils/common-validation-utils.ts` |
| `ValidationMessageUtil.buildValidationMessageId` | `ValidationMessageUtil.buildValidationMessageId` | `src/app/basislogik/utils/validation-message-util.ts` |
| `ValidationUtils.isValid` | `ValidationUtils.isValid` | `src/app/basislogik/utils/validation-utils.ts` |
| `AbstractCommonCondition.getGVName` | `CommonValidationUtils.getGVName` | `src/app/basislogik/utils/common-validation-utils.ts` |
| `ValidationAuEUtil.isAufhebungAnhoerungErstattung` | `ValidationAuEUtil.isAufhebungAnhoerungErstattung` | `src/app/basislogik/utils/validation-aue-util.ts` |
| `LocalDateUtil.geburtstagInJahr` | `LocalDateUtil.geburtstagInJahr` | `src/app/basislogik/utils/local-date-util.ts` |

## Language and Comments

- Keep all German identifiers and comments in German — do not translate to English.
- Transfer class-level and method-level comments from the Java source.
