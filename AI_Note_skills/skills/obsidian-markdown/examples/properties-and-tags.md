# Properties and Tags Examples

## Basic Frontmatter

---
title: My Note Title
date: 2024-01-15
tags:
  - project
  - important
---

---

## Full Frontmatter (All Property Types)

---
title: Complete Example Note
date: 2024-08-21
due: 2024-09-15T14:30:00
tags:
  - project/active
  - research
  - AI
aliases:
  - Example Note
  - Complete Demo
cssclasses:
  - academic-note
  - wide-page
status: in-progress
priority: high
rating: 4.5
completed: false
author: John Doe
related: "[[Other Note]]"
sources:
  - "[[Reference A]]"
  - "[[Reference B]]"
  - "[[Reference C]]"
---

### Property Type Reference

| Type | Example | Notes |
|------|---------|-------|
| Text | `title: "My Title"` | Quotes optional unless special chars |
| Number | `rating: 4.5` | Integer or decimal |
| Boolean | `completed: true` | `true` / `false` |
| Date | `date: 2024-01-15` | ISO 8601 |
| Date+Time | `due: 2024-01-15T14:30:00` | ISO 8601 |
| List | `tags: [a, b, c]` | Inline or YAML list |
| Link | `related: "[[Note]]"` | Must be quoted |

---

## Default Properties

### tags (Searchable labels)

---
tags:
  - daily
  - meeting/standup
---

### aliases (Alternative note names)

---
aliases:
  - ML
  - Machine Learning
  - 机器学习
---

Typing `[[ML` in another note will find this note and generate: `[[Full Note Name|ML]]`

### cssclasses (Custom CSS styling)

---
cssclasses:
  - kanban
  - no-inline-title
---

---

## Deprecated Property Forms

As of Obsidian 1.9, use plural forms:

| Deprecated | Use Instead |
|------------|-------------|
| `tag: value` | `tags: [value]` |
| `alias: value` | `aliases: [value]` |
| `cssclass: value` | `cssclasses: [value]` |

---

## Links in Properties

Internal links in YAML must be quoted:

---
related: "[[Project Alpha]]"
references:
  - "[[Meeting Notes 2024-01-10]]"
  - "[[Design Document]]"
  - "[[API Specification]]"
---

---

# Tags

## Inline Tags

#tag
#nested/tag
#tag-with-dashes
#tag_with_underscores
#CamelCaseTag
#日本語タグ

## Nested Tags (Hierarchical)

#project/active
#project/archived
#status/in-progress
#status/done
#reading/fiction
#reading/non-fiction/science

In the Tags view, these display as collapsible trees.
Searching `#project` matches both `#project` and `#project/active`.

## Tag Rules

Valid tags:
- #valid-tag
- #tag123
- #y2024
- #café
- #日记

Invalid tags (will NOT be recognized):
- #1984 (purely numeric)
- #tag.name (period not allowed)
- #tag@work (@ not allowed)
- #tag$value ($ not allowed)
- #tag name (spaces not allowed)

## Tags in Frontmatter vs Inline

Both methods are equivalent. Frontmatter tags don't need `#`:

---
tags:
  - project
  - active
---

This note also has an #inline-tag in the body text.

---

## 来源

- [Obsidian Properties](https://obsidian.md/help/properties) — Frontmatter YAML, all property types, defaults
- [Obsidian Tags](https://obsidian.md/help/tags) — Inline tags, nested tags, tag rules
