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

## 常见陷阱（Common Pitfalls）

以下是需要特别注意的语法问题，这些错误在 Obsidian 中会导致 Mermaid 图表无法渲染。

### 1. 避免在节点标签中使用 `]`

Mermaid 使用 `]` 来关闭节点定义。在节点标签文本中出现的 `]` 会导致节点被提前终止：

```mermaid
%% ❌ 错误 — 标签中的 ] 会提前关闭节点
A{"答案有价值？<br/><sub>是否有价值？</sub>"]
B["处理完成"]

%% ✅ 正确 — 菱形节点用 } 关闭
A{"答案有价值？<br/><sub>是否有价值？</sub>"}
B["处理完成"]
```

**常见错误场景**：在 decision diamond 节点 `{...}` 中使用 `</sub>` 等 HTML 标签时，闭合的 `</sub>` 包含 `/sub` 后的 `>`，但如果写成了 `]</sub>` 形式，`]` 会破坏语法。

### 2. 菱形决策节点必须使用 `{...}` 而非 `[...]`

```mermaid
%% ❌ 错误
A[这是一个判断？]

%% ✅ 正确 — 菱形用 {}
A{这是一个判断？}
```

### 3. `flowchart` vs `graph` — 优先使用 `flowchart`

```mermaid
%% 推荐 — 支持更丰富的样式和更好的渲染
flowchart TD
    A[Start] --> B{Decision}
    B -->|"Yes"| C[Action]

%% 旧语法，仍可用但不推荐
graph TD
    A[Start] --> B{Decision}
```

### 4. 子图（Subgraph）语法

```mermaid
flowchart TD
    subgraph Phase1["阶段一：输入"]
        A[用户输入] --> B[数据验证]
    end

    subgraph Phase2["阶段二：处理"]
        B --> C[核心处理]
    end

    Phase1 --> Phase2
```

> 子图的 `["标题"]` 需要加引号才能包含中文。

### 5. 样式应用（Style）

```mermaid
flowchart TD
    A[开始] --> B{判断}
    B -->|"是"| C[成功]
    B -->|"否"| D[失败]
    C --> E[结束]
    D --> E

    %% 按节点 ID 应用样式
    style A fill:#E6FFFA,stroke:#38B2AC,color:#1A535C
    style C fill:#FFFFF0,stroke:#9AE6B4,color:#22543D
    style D fill:#FFF5F5,stroke:#FC8181,color:#742A2A
```

---

## 来源

- [Obsidian Advanced formatting syntax](https://obsidian.md/help/advanced-syntax) — Mermaid diagrams, internal links from diagrams
- [Mermaid.js Documentation](https://mermaid.js.org/) — All supported diagram types and syntax
