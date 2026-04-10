---
name: obsidian-bases
description: >
  Create and configure Obsidian Base files (.base) — database-like views with tables, cards, lists, and maps.
  Trigger on: "bases", "base file", "obsidian database", "note database", "table/card/list/map view",
  organizing/querying notes with properties. Use whenever creating .base files, building database views,
  setting up filtered/sorted/grouped views, writing Bases formulas, or embedding a base view into a note.
paths: "**/*.base"
---

# Obsidian Bases

Bases is a core Obsidian plugin that creates database-like views of notes. It lets users view, edit, sort, filter, and group files by their properties. All data lives in standard Markdown files and their frontmatter properties — Bases just provides the view layer.

## File Format

A Base is saved as a `.base` file containing YAML. It can also be embedded inline via a `base` code block.

## Root-Level YAML Structure

```yaml
filters:       # Global conditions narrowing the dataset (apply to all views)
formulas:      # Custom computed properties
properties:    # Display configuration for properties
summaries:     # Custom aggregation formulas
views:         # List of view configurations
```

---

## Filters

Filters narrow down which files appear. They can be defined globally (root level) or per-view. Global and view-level filters are combined with AND.

### Filter Conjunctions

- `and:` — all conditions must be true
- `or:` — at least one condition must be true  
- `not:` — none of the conditions can be true

### Filter Syntax

```yaml
filters:
  and:
    - file.hasTag("project")
    - 'status != "done"'
  or:
    - file.inFolder("Work")
    - file.inFolder("Personal")
  not:
    - file.hasTag("archived")
```

Filters can be nested:

```yaml
filters:
  or:
    - file.hasTag("tag")
    - and:
        - file.hasTag("book")
        - file.hasLink("Textbook")
    - not:
        - file.hasTag("archive")
```

### Common Filter Expressions

| Expression | Description |
|---|---|
| `file.hasTag("tagname")` | File has the specified tag (includes nested) |
| `file.inFolder("folder")` | File is in folder or subfolder |
| `file.hasLink("filename")` | File links to the specified file |
| `file.hasProperty("prop")` | File has the specified property |
| `'property == "value"'` | Property equals value |
| `'property != "value"'` | Property does not equal value |
| `'property > 5'` | Numeric comparison |
| `'file.mtime > now() - "1 week"'` | Modified within last week |

---

## Formulas

Formulas create calculated properties from existing data. Use the `if()` function for conditional logic — ternary operators (`? :`) are **not supported**.

```yaml
formulas:
  formatted_price: 'if(price, "$" + price.toFixed(2), "")'
  priority_score: "(impact * urgency) / effort"
  full_name: 'first_name + " " + last_name'
  overdue: 'if(due_date < now() && status != "Done", "Overdue", "")'
  deadline: 'start_date + "2w"'
  # Nested if() for multiple conditions:
  level: 'if(score >= 90, "A", if(score >= 70, "B", "C"))'
```

### Property References

| Reference | Example |
|---|---|
| Note property (shorthand) | `price`, `status` |
| Note property (explicit) | `note.price`, `note["my prop"]` |
| File property | `file.name`, `file.size`, `file.mtime` |
| Formula property | `formula.formatted_price` |

Formulas cannot reference themselves (no circular references).

---

## Properties Configuration

Control display names for properties:

```yaml
properties:
  status:
    displayName: Status
  formula.formatted_price:
    displayName: "Price (USD)"
  file.ext:
    displayName: Extension
```

---

## Summaries

Aggregate values across all notes in the result set.

### Built-in Summaries

| Summary | Input Type | Description |
|---|---|---|
| Average | Number | Mathematical mean |
| Sum | Number | Sum of all values |
| Min / Max | Number | Smallest / Largest |
| Median | Number | Mathematical median |
| Range | Number | Max minus Min |
| Stddev | Number | Standard deviation |
| Earliest / Latest | Date | Earliest / Latest date |
| Range | Date | Latest minus Earliest |
| Checked / Unchecked | Boolean | Count of true / false |
| Empty / Filled | Any | Count of empty / non-empty |
| Unique | Any | Count of unique values |

### Custom Summaries

```yaml
summaries:
  customAverage: 'values.mean().round(3)'
```

In summary formulas, `values` is a list of all values for that property across every note.

---

## Views

Each view defines a layout type and its configuration.

```yaml
views:
  - type: table          # table | cards | list | map
    name: "My View"
    limit: 10            # Max rows to display
    groupBy:
      property: note.status
      direction: DESC    # ASC or DESC
    filters:             # View-specific filters (combined with global via AND)
      and:
        - 'status != "done"'
    order:               # Column/property display order
      - file.name
      - note.status
      - formula.priority_score
    summaries:
      note.price: Sum
      formula.priority_score: Average
```

> **Note:** YAML syntax does not have a `sortBy` field. Sorting can only be done via `groupBy` (which groups AND sorts) or through the Bases UI. If you only need sorting without grouping, configure it in the UI instead of YAML.

### View Types

#### Table View
Displays files as rows with property columns. See `examples/table-task-tracker.base` for a full example.

Settings: Row height (Short / Medium / Tall / Extra tall).

#### Cards View
Gallery-like grid layout with optional cover images. See `examples/cards-reading-list.base`.

Settings:
- **Card size** — width of each card
- **Image property** — property containing the cover image (wiki link, URL, or hex color)
- **Image fit** — `cover` (fill + crop) or `contain` (fit without cropping)
- **Image aspect ratio** — defaults to 1:1

#### List View
Bulleted or numbered list. See `examples/list-simple-notes.base`.

Settings:
- **Markers** — bullets, numbers, or none
- **Indent properties** — show properties as indented sub-items
- **Separators** — character separating properties when indent is off (default: comma)

#### Map View
Interactive map with markers. Requires the Maps plugin. See `examples/map-places.base`.

Settings:
- Embedded height, center coordinates, zoom constraints
- Marker coordinates, color, icon
- Background map tiles

---

## File Properties (Available for All Files)

| Property | Type | Description |
|---|---|---|
| `file.name` | String | File name |
| `file.path` | String | Full file path |
| `file.folder` | String | Folder path |
| `file.ext` | String | File extension |
| `file.size` | Number | File size |
| `file.ctime` | Date | Created time |
| `file.mtime` | Date | Modified time |
| `file.tags` | List | All tags |
| `file.links` | List | All internal links |
| `file.backlinks` | List | Backlinks (performance heavy) |
| `file.embeds` | List | All embeds |
| `file.properties` | Object | All frontmatter properties |

---

## Operators

### Arithmetic: `+`, `-`, `*`, `/`, `%`, `()`  
### Comparison: `==`, `!=`, `>`, `<`, `>=`, `<=`  
### Boolean: `!`, `&&`, `||`

---

## Date Arithmetic

Duration units: `y`/`year`, `M`/`month`, `d`/`day`, `w`/`week`, `h`/`hour`, `m`/`minute`, `s`/`second`

```yaml
# Examples
date + "1M"              # Add 1 month
now() - "1 week"         # 1 week ago
file.mtime > now() - "7d"  # Modified in last 7 days
```

---

## Types

- **String**: `"hello"` or `'world'`
- **Number**: `42`, `3.14`
- **Boolean**: `true`, `false`
- **Date**: `date("2025-01-01")`, `now()`, `today()`
- **List**: `[1, 2, 3]`, access with `property[0]`
- **Link**: `link("filename")`, `link("filename", "display text")`

---

## Key Global Functions

| Function | Signature | Description |
|---|---|---|
| `if()` | `if(condition, trueVal, falseVal?)` | Conditional |
| `now()` | `now()` | Current datetime |
| `today()` | `today()` | Current date (time = 0) |
| `date()` | `date("YYYY-MM-DD HH:mm:ss")` | Parse date string |
| `link()` | `link(path, display?)` | Create link |
| `image()` | `image(path)` | Render image |
| `icon()` | `icon("lucide-name")` | Render Lucide icon |
| `max()` / `min()` | `max(a, b, ...)` | Max/min of numbers |
| `number()` | `number(input)` | Convert to number |
| `list()` | `list(element)` | Wrap in list |
| `html()` | `html(string)` | Render as HTML |
| `escapeHTML()` | `escapeHTML(string)` | Escape HTML chars |
| `duration()` | `duration("5h")` | Parse duration |
| `file()` | `file(path)` | Get file object |
| `random()` | `random()` | Random 0-1 |

## Key Method Functions

**String**: `.contains()`, `.containsAll()`, `.containsAny()`, `.lower()`, `.title()`, `.replace()`, `.split()`, `.slice()`, `.trim()`, `.startsWith()`, `.endsWith()`, `.repeat()`, `.reverse()`, `.length`

**Number**: `.abs()`, `.ceil()`, `.floor()`, `.round(digits)`, `.toFixed(precision)`

**Date**: `.format("YYYY-MM-DD")`, `.relative()`, `.date()`, `.time()`, `.year`, `.month`, `.day`, `.hour`

**List**: `.contains()`, `.filter(expr)`, `.map(expr)`, `.reduce(expr, acc)`, `.sort()`, `.join(sep)`, `.unique()`, `.flat()`, `.slice()`, `.reverse()`, `.length`

**File**: `.hasTag()`, `.hasLink()`, `.hasProperty()`, `.inFolder()`, `.asLink()`

**Link**: `.asFile()`, `.linksTo(file)`

For the complete function reference, see the official documentation at https://obsidian.md/help/bases/functions

---

## The `this` Object

`this` refers to different things depending on context:
- **In a .base file**: points to the base file's own properties
- **Embedded in a note**: points to the embedding note's properties
- **In the sidebar**: points to the active file in the main content area

Useful pattern: `file.hasLink(this.file)` — replicates a backlinks pane.

---

## Creating a Base

### As a standalone file
- Command palette → "Bases: Create new base"
- Right-click folder in file explorer → "New base"
- Ribbon → "Create new base"

### Embedded in a note

**Embed a .base file:**
```markdown
![[MyBase.base]]
![[MyBase.base#ViewName]]
```

**Inline code block:**
````markdown
```base
filters:
  and:
    - file.hasTag("project")
views:
  - type: table
    name: Projects
```
````

---

## Examples

Refer to the `examples/` folder for ready-to-use templates:

- [table-task-tracker.base](examples/table-task-tracker.base) — Task management with status, priority, due dates, and overdue detection
- [cards-reading-list.base](examples/cards-reading-list.base) — Reading list with cover images in card layout
- [list-simple-notes.base](examples/list-simple-notes.base) — Simple filtered note list
- [map-places.base](examples/map-places.base) — Places displayed on an interactive map
- [table-project-dashboard.base](examples/table-project-dashboard.base) — Project dashboard with formulas and summaries
- [embedded-inline.md](examples/embedded-inline.md) — How to embed bases inline in a note

---

> Sources:
> - https://obsidian.md/help/bases
> - https://obsidian.md/help/bases/create-base
> - https://obsidian.md/help/bases/views
> - https://obsidian.md/help/bases/syntax
> - https://obsidian.md/help/bases/functions
> - https://obsidian.md/help/formulas
> - https://obsidian.md/help/bases/views/cards
> - https://obsidian.md/help/bases/views/list
> - https://obsidian.md/help/bases/views/map
> - https://obsidian.md/help/bases/views/table
