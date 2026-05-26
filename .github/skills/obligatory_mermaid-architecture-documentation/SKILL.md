---
name: obligatory_mermaid-architecture-documentation
description: >
  Enforces the rule that all application architecture documentation must include Mermaid diagrams.
  Apply this skill whenever creating or updating architecture documents, README files that describe
  system structure, arc42 documents, ADRs, or any documentation that describes how components,
  services, or modules interact. Always add the required Mermaid diagrams even if the user does not
  explicitly ask for them — they are mandatory for architecture documentation.
---

# Skill: Mermaid Architecture Documentation

**Enforcement level:** Obligatory — every architecture document must contain the required Mermaid diagrams.

## Rule

When creating or updating application architecture documentation, always include Mermaid diagrams.
Three diagram types are the minimum requirement; additional diagrams are encouraged.

## Required Diagrams (minimum set)

Every architecture document MUST contain all three of the following:

### 1. High-Level System Context Diagram
Shows the system as a whole and its relationships with external actors and systems.

**Recommended syntax:** `flowchart TD` or `graph TD`

```mermaid
flowchart TD
    User([User]) --> App[Your Application]
    App --> DB[(Database)]
    App --> ExtAPI[External API]
```

### 2. Component / Module Interaction Diagram
Shows the internal components or modules and how they interact with each other.

**Recommended syntax:** `flowchart LR`, `graph LR`, or `classDiagram`

```mermaid
flowchart LR
    UI[UI Layer] --> SVC[Service Layer]
    SVC --> REPO[Repository Layer]
    REPO --> DB[(Database)]
```

### 3. Runtime Flow Diagram
Shows the step-by-step flow of a key user journey or service interaction at runtime.

**Recommended syntax:** `sequenceDiagram`

```mermaid
sequenceDiagram
    actor User
    User->>Controller: HTTP Request
    Controller->>Service: processRequest()
    Service->>Repository: findById(id)
    Repository-->>Service: entity
    Service-->>Controller: ResponseDTO
    Controller-->>User: HTTP Response
```

## Diagram Standards

- **Node naming**: diagram nodes MUST match real package/module/service/class names from the codebase.
- **No fictional components**: do not invent components that do not exist in the code.
- **Keep updated**: whenever architecture-relevant code changes, update the corresponding Mermaid diagrams.

## Recommended Mermaid Diagram Types Reference

| Diagram type      | Mermaid keyword     | Best for                                      |
|-------------------|---------------------|-----------------------------------------------|
| Process flow      | `flowchart`         | Request flows, data flows, process steps      |
| Component graph   | `graph TD / LR`     | Component dependency overviews                |
| Sequence          | `sequenceDiagram`   | Service interactions over time                |
| Class/domain model| `classDiagram`      | Domain model structure, entity relationships  |
| State machine     | `stateDiagram-v2`   | Lifecycle states of an entity or process      |
| Entity-relationship| `erDiagram`        | Database schema relationships                 |

## Example: Complete Architecture Document Section

```markdown
## System Architecture

### System Context

```mermaid
flowchart TD
    User([Browser Client]) --> Gateway[API Gateway]
    Gateway --> OrderSvc[Order Service]
    Gateway --> UserSvc[User Service]
    OrderSvc --> OrderDB[(Orders DB)]
    UserSvc --> UserDB[(Users DB)]
    OrderSvc --> PaymentAPI[Payment API]
```

### Component Interactions

```mermaid
flowchart LR
    OrderController --> OrderService
    OrderService --> OrderRepository
    OrderService --> PaymentClient
    OrderRepository --> OrderDB[(PostgreSQL)]
```

### Key Runtime Flow: Place Order

```mermaid
sequenceDiagram
    actor Client
    Client->>OrderController: POST /orders
    OrderController->>OrderService: createOrder(dto)
    OrderService->>PaymentClient: charge(amount)
    PaymentClient-->>OrderService: paymentConfirmation
    OrderService->>OrderRepository: save(order)
    OrderRepository-->>OrderService: savedOrder
    OrderService-->>OrderController: OrderResponseDTO
    OrderController-->>Client: 201 Created
```
```

## Checklist Before Finalising Any Architecture Document

- [ ] High-level system context diagram is present (using `flowchart` or `graph`).
- [ ] Component/module interaction diagram is present.
- [ ] Runtime flow diagram is present (using `sequenceDiagram`).
- [ ] All diagram nodes correspond to real names in the codebase.
- [ ] Diagrams are enclosed in fenced code blocks with the `mermaid` language tag.
- [ ] Diagrams have been updated if any architecture-relevant code changed.
