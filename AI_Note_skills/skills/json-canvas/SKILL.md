---
name: json-canvas
description: >
  Create and edit JSON Canvas (.canvas) files — the open format for infinite canvas / whiteboard data,
  originally created for Obsidian. Covers the full JSON Canvas 1.0 spec (nodes, edges, colors, groups)
  and Obsidian Canvas plugin integration (embedding vault notes, media, web pages, connections, groups).
  Trigger on: ".canvas files", "canvas", "whiteboard", "json canvas", "visual note", "mind map on canvas",
  "flowchart canvas", "node graph", "spatial layout", "infinite canvas", "Obsidian whiteboard",
  "canvas diagram", or any request to create/edit/generate .canvas files.
  Also trigger when users want to visually organize notes, create spatial layouts, or build
  node-and-edge diagrams in Obsidian — even if they don't explicitly mention "canvas".
paths: "**/*.canvas"
---

# JSON Canvas Skill

Create `.canvas` files conforming to the [JSON Canvas 1.0 spec](https://jsoncanvas.org/spec/1.0/), with full support for Obsidian Canvas plugin features.

## Quick Reference — Examples

Read from `examples/` when you need concrete patterns:

| File | Demonstrates |
|---|---|
| `basic-text-nodes.canvas` | Text nodes, Markdown content, edges with labels |
| `vault-embedding.canvas` | File nodes (notes, images, PDFs), subpath linking |
| `mind-map.canvas` | Radial layout, color coding, hierarchical edges |
| `project-board.canvas` | Groups as swim lanes, link nodes, complex edge routing |

## Top-Level Structure

A `.canvas` file is JSON with two optional top-level arrays:

```json
{
  "nodes": [],
  "edges": []
}
```

- **nodes** — visual objects on the canvas (text, file, link, group)
- **edges** — lines connecting nodes

Z-order: nodes earlier in the array render below later ones.

---

## Nodes

Every node shares these base properties:

| Property | Required | Type | Description |
|---|---|---|---|
| `id` | Yes | string | Unique identifier (use 16-char hex, e.g. `"a1b2c3d4e5f67890"`) |
| `type` | Yes | string | `"text"` / `"file"` / `"link"` / `"group"` |
| `x` | Yes | integer | X position in pixels (0,0 = canvas center) |
| `y` | Yes | integer | Y position in pixels (negative = up) |
| `width` | Yes | integer | Width in pixels (typical card: 250–400) |
| `height` | Yes | integer | Height in pixels (typical card: 100–400) |
| `color` | No | canvasColor | Node color — see Color section |

### Text Node

Stores Markdown-formatted text directly in the canvas.

```json
{
  "id": "abc123", "type": "text",
  "x": 0, "y": 0, "width": 300, "height": 200,
  "text": "# Title\n\nThis is **bold** and a [[wikilink]]."
}
```

| Property | Required | Type |
|---|---|---|
| `text` | Yes | string — plain text with Markdown syntax |

In Obsidian, text nodes support full Markdown: headings, bold/italic, lists, code blocks, wikilinks (`[[note]]`), and embeds (`![[image.png]]`). Text nodes do NOT appear in Backlinks until converted to files via right-click > "Convert to file...".

### File Node

Embeds a file from the vault (notes, images, PDFs, videos).

```json
{
  "id": "def456", "type": "file",
  "x": 400, "y": 0, "width": 400, "height": 300,
  "file": "Projects/My Project.md",
  "subpath": "#Overview"
}
```

| Property | Required | Type | Description |
|---|---|---|---|
| `file` | Yes | string | Path to file, relative to vault root |
| `subpath` | No | string | Link to heading (`#Heading`) or block (`#^block-id`) |

Tips:
- Images/PDFs render inline as previews
- Use `subpath` to show a specific section of a long note
- Drag files from the Obsidian file explorer onto the canvas to create file nodes

### Link Node

Embeds an external web page as an iframe.

```json
{
  "id": "ghi789", "type": "link",
  "x": 0, "y": 300, "width": 400, "height": 300,
  "url": "https://example.com"
}
```

| Property | Required | Type |
|---|---|---|
| `url` | Yes | string — fully qualified URL |

In Obsidian, Ctrl/Cmd+click opens the link in a browser. Not all websites allow iframe embedding.

### Group Node

A visual container that groups other nodes. Nodes inside the group's bounding box belong to it.

```json
{
  "id": "jkl012", "type": "group",
  "x": -50, "y": -50, "width": 800, "height": 500,
  "label": "Phase 1",
  "background": "Assets/bg-pattern.png",
  "backgroundStyle": "repeat"
}
```

| Property | Required | Type | Description |
|---|---|---|---|
| `label` | No | string | Text label displayed on the group |
| `background` | No | string | Path to background image |
| `backgroundStyle` | No | string | `"cover"` / `"ratio"` / `"repeat"` |

Background styles:
- `"cover"` — fills entire group area, may crop
- `"ratio"` — maintains aspect ratio, may leave gaps
- `"repeat"` — tiles the image as a pattern

Groups should appear **before** their contained nodes in the `nodes` array (lower z-index = rendered behind).

---

## Edges

Lines connecting two nodes:

```json
{
  "id": "edge01",
  "fromNode": "abc123", "fromSide": "right",
  "toNode": "def456", "toSide": "left",
  "toEnd": "arrow",
  "color": "4",
  "label": "references"
}
```

| Property | Required | Type | Default | Description |
|---|---|---|---|---|
| `id` | Yes | string | — | Unique identifier |
| `fromNode` | Yes | string | — | Source node `id` |
| `fromSide` | No | string | — | `"top"` / `"right"` / `"bottom"` / `"left"` |
| `fromEnd` | No | string | `"none"` | `"none"` / `"arrow"` |
| `toNode` | Yes | string | — | Target node `id` |
| `toSide` | No | string | — | `"top"` / `"right"` / `"bottom"` / `"left"` |
| `toEnd` | No | string | `"arrow"` | `"none"` / `"arrow"` |
| `color` | No | canvasColor | — | Line color |
| `label` | No | string | — | Text label on the edge |

When `fromSide`/`toSide` are omitted, Obsidian auto-routes the connection to the nearest side.

---

## Color

The `canvasColor` type supports two formats:

**Preset colors** (single digit string):

| Value | Color |
|---|---|
| `"1"` | Red |
| `"2"` | Orange |
| `"3"` | Yellow |
| `"4"` | Green |
| `"5"` | Cyan |
| `"6"` | Purple |

**Hex color**: any `"#RRGGBB"` string, e.g. `"#FF5722"`.

Preset values are preferred — they adapt to the user's theme (light/dark mode).

---

## Obsidian Canvas Integration

### Creating a Canvas in Obsidian

- Command palette: "Canvas: Create new canvas"
- Right-click in file explorer > "New canvas"
- Ribbon icon (dashboard icon)

Canvas files are saved as `.canvas` in the vault with standard JSON.

### Card Operations in Obsidian

| Action | Method |
|---|---|
| Add text card | Double-click canvas or click blank-file icon at bottom |
| Add note from vault | Click document icon or drag from file explorer |
| Add media | Click image icon or drag file |
| Add web page | Right-click > "Add web page" or drag URL from browser |
| Add folder of files | Drag folder from file explorer |
| Edit card | Double-click; Escape to finish |
| Delete | Right-click > Delete, or Backspace/Delete key |
| Duplicate | Alt/Option + drag |
| Convert text to file | Right-click text card > "Convert to file..." |

### Selection & Movement

- **Select multiple**: drag-select area, or Shift+click to toggle
- **Select all**: Ctrl/Cmd+A
- **Move**: drag selected cards; Shift+drag constrains to one axis
- **Disable snapping**: hold Space while dragging/resizing
- **Maintain aspect ratio**: hold Shift while resizing

### Connections in Obsidian

- Hover card edge until filled circle appears, then drag to target
- Double-click a connection line to add/edit its label
- Right-click line > "Go to target" / "Go to source" to navigate
- Select items > palette icon to change color

### Groups in Obsidian

- Right-click canvas > "Create group" (empty)
- Select cards > right-click > "Create group" (wraps selection)
- Double-click group name to rename

### Navigation

| Action | Shortcut |
|---|---|
| Pan | Space+drag / middle-mouse drag / scroll |
| Horizontal pan | Shift+scroll |
| Zoom | Ctrl/Cmd+scroll or Space+scroll |
| Zoom to fit all | Shift+1 |
| Zoom to selection | Shift+2 |

---

## Layout Guidelines

When generating `.canvas` files programmatically, follow these conventions for readable layouts:

### Sizing
- **Text cards**: 250–400px wide, 100–250px tall (scale with content)
- **File embeds**: 300–500px wide, 200–500px tall
- **Link embeds**: 400–600px wide, 300–400px tall
- **Groups**: add 40–60px padding around contained nodes

### Spacing
- Leave 40–80px gaps between nodes horizontally and vertically
- Align nodes to a grid (multiples of 20px) for visual consistency

### Common Layouts

**Left-to-right flow** (process, timeline):
```
x increases →
Node1(x:0) --→ Node2(x:400) --→ Node3(x:800)
```

**Top-to-bottom hierarchy** (org chart, decomposition):
```
y increases ↓
        Parent(y:0)
       /          \
Child1(y:300)  Child2(y:300)
```

**Radial / mind map** (center topic, branches radiate):
```
Place center node at (0,0), branches at equal angles, 400–600px from center.
```

**Grid / kanban** (board, matrix):
```
Use groups as columns, nodes stacked vertically inside each group.
```

### ID Generation

Use 16-character lowercase hex strings for `id` values to match Obsidian's convention:

```
"a1b2c3d4e5f67890"
```

Each `id` must be unique within the file. Generate deterministically or randomly — both work.
