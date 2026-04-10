# Tables and Lists Examples

## Unordered Lists

- Item 1
- Item 2
  - Nested item A (2 spaces indent)
  - Nested item B
    - Deeper nesting
- Item 3

* Asterisk style
* Also works

+ Plus style
+ Also works

---

## Ordered Lists

1. First item
2. Second item
   1. Nested numbered (3 spaces indent)
   2. Another nested
      1. Even deeper
3. Third item

**Using closing parenthesis** (GFM-compatible):
1) First item
2) Second item
   1) Nested with period
   2) Another nested
3) Third item

> [!note] Tip
> Both `1.` and `1)` syntax work for ordered lists. Use whichever matches your preferred style.

---

## Task Lists (Checkboxes)

- [ ] Incomplete task
- [x] Completed task
- [ ] Parent task
  - [x] Subtask 1 (done)
  - [ ] Subtask 2 (pending)
  - [ ] Subtask 3 (pending)
- [x] Another completed task

Toggle with `Cmd/Ctrl + L` or click in Reading/Live Preview.

---

## Mixed Lists

1. First ordered item
   - Unordered sub-item
   - Another sub-item
2. Second ordered item
   - [ ] Task sub-item
   - [x] Done sub-item
3. Third ordered item

---

## Basic Table

| Header 1 | Header 2 | Header 3 |
|----------|----------|----------|
| Cell 1   | Cell 2   | Cell 3   |
| Cell 4   | Cell 5   | Cell 6   |
| Cell 7   | Cell 8   | Cell 9   |

---

## Column Alignment

| Left Aligned | Center Aligned | Right Aligned |
|:-------------|:--------------:|--------------:|
| Left         |    Center      |         Right |
| Data A       |    Data B      |        Data C |
| 100          |     200        |           300 |

---

## Table with Wikilinks and Embeds

| Name | Link | Image |
|------|------|-------|
| Alice | [[Alice's Note]] | ![[alice.png\|50]] |
| Bob | [[Bob's Note\|Bob]] | ![[bob.png\|50]] |

Note: Use `\|` to escape pipes inside wikilinks within table cells.

---

## Table with Formatting

| Feature | Status | Priority |
|---------|--------|----------|
| **Authentication** | ==Done== | High |
| *Authorization* | ~~Cancelled~~ | Low |
| `API Gateway` | In Progress | Medium |
| OAuth 2.0[^1] | Pending | High |

[^1]: Requires third-party integration.

---

## Wide Comparison Table

| Aspect | Option A | Option B | Option C | Recommendation |
|--------|----------|----------|----------|----------------|
| Cost | $100/mo | $250/mo | $500/mo | Option A |
| Speed | 100ms | 50ms | 20ms | Option C |
| Scale | 1K users | 10K users | 100K users | Option C |
| Setup | 1 hour | 1 day | 1 week | Option A |

---

## 来源

- [Obsidian Basic formatting syntax](https://obsidian.md/help/syntax) — Headings, emphasis, lists
- [CommonMark Specification](https://spec.commonmark.org/) — Standard Markdown syntax
