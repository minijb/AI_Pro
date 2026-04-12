# Mermaid Diagram Examples

Mermaid diagrams are rendered natively in Obsidian -- no plugins needed.

---

## Flowchart (Top-Down)

```mermaid
graph TD
    A[Start] --> B{Is it raining?}
    B -->|Yes| C[Take umbrella]
    B -->|No| D[Enjoy the sun]
    C --> E[Go outside]
    D --> E
    E --> F[End]
```

## Flowchart (Left-Right)

```mermaid
graph LR
    A[Input] --> B[Process]
    B --> C[Output]
    B --> D[(Database)]
    D --> B
```

## Flowchart with Subgraphs

```mermaid
graph TD
    subgraph Frontend
        A[React App] --> B[API Client]
    end

    subgraph Backend
        C[API Server] --> D[Business Logic]
        D --> E[(PostgreSQL)]
    end

    B --> C
```

---

## Sequence Diagram

```mermaid
sequenceDiagram
    participant U as User
    participant C as Client
    participant S as Server
    participant DB as Database

    U->>C: Click Login
    C->>S: POST /auth/login
    S->>DB: Query user
    DB-->>S: User record
    S-->>C: JWT Token
    C-->>U: Show Dashboard

    Note over C,S: All traffic is HTTPS
```

---

## Gantt Chart

```mermaid
gantt
    title Project Timeline
    dateFormat YYYY-MM-DD

    section Planning
    Requirements    :a1, 2024-01-01, 14d
    Design          :a2, after a1, 10d

    section Development
    Backend         :b1, after a2, 30d
    Frontend        :b2, after a2, 25d
    Integration     :b3, after b1, 10d

    section Testing
    QA Testing      :c1, after b3, 14d
    UAT             :c2, after c1, 7d

    section Launch
    Deployment      :milestone, after c2, 0d
```

---

## Pie Chart

```mermaid
pie title Time Distribution
    "Deep Work" : 40
    "Meetings" : 25
    "Shallow Work" : 20
    "Breaks" : 15
```

---

## Class Diagram

```mermaid
classDiagram
    class Animal {
        +String name
        +int age
        +makeSound() void
        +move() void
    }

    class Dog {
        +String breed
        +fetch() void
    }

    class Cat {
        +bool isIndoor
        +purr() void
    }

    class Owner {
        +String name
        +List~Animal~ pets
        +adopt(Animal a) void
    }

    Animal <|-- Dog
    Animal <|-- Cat
    Owner "1" --> "*" Animal : owns
```

---

## State Diagram

```mermaid
stateDiagram-v2
    [*] --> Draft
    Draft --> Review : Submit
    Review --> Approved : Accept
    Review --> Draft : Request Changes
    Approved --> Published : Publish
    Published --> Archived : Archive
    Archived --> [*]
```

---

## Entity Relationship Diagram

```mermaid
erDiagram
    USER ||--o{ ORDER : places
    USER {
        int id PK
        string name
        string email
    }
    ORDER ||--|{ LINE_ITEM : contains
    ORDER {
        int id PK
        date created_at
        string status
    }
    PRODUCT ||--o{ LINE_ITEM : "ordered in"
    PRODUCT {
        int id PK
        string name
        float price
    }
    LINE_ITEM {
        int quantity
        float subtotal
    }
```

---

## Linking Nodes to Notes

Nodes with the `internal-link` class become clickable links to Obsidian notes (do NOT appear in Graph view):

```mermaid
graph LR
    A[Machine Learning]
    B[Deep Learning]
    C[Transformers]
    A --> B --> C
    class A,B,C internal-link;
```

---

## Requirement Diagram

```mermaid
requirementDiagram
    requirement TestReq {
        id: 1
        text: "System shall do X"
    }
    functionalRequirement TestReq2 {
        id: 1.1
        text: "System shall do Y"
    }
    TestReq -ren-> TestReq2
```

---

## Git Graph

```mermaid
gitGraph
    commit id: "v1.0"
    commit id: "Feature A"
    branch feature
    checkout feature
    commit id: "WIP"
    checkout main
    commit id: "Hotfix"
    merge feature id: "Merge feature"
    commit id: "v1.1"
```

---

## Journey Diagram

```mermaid
journey
    title User Shopping Journey
    section Browse
      Search product: 5: User
      View details: 3: User
    section Purchase
      Add to cart: 5: User
      Checkout: 1: User
    section Post-purchase
      Receive confirmation: 5: User
      Rate product: 3: User
```

---

## C4 Context Diagram

```mermaid
C4Context
    Person(customer, "Customer", "Buys products online")
    System(shop, "Online Shop", "Sells products")
    System(payment, "Payment System", "Processes payments")
    Rel(customer, shop, "Uses")
    Rel(shop, payment, "Calls")
```

> [!note] Tip
> C4 diagrams require the `c4d3` or similar Mermaid plugin in some renderers. They work natively in Obsidian with the built-in Mermaid renderer.

---

## 来源

- [Obsidian Advanced formatting syntax](https://obsidian.md/help/advanced-syntax) — Mermaid diagrams, internal links from diagrams
- [Mermaid.js Documentation](https://mermaid.js.org/) — All supported diagram types and syntax
