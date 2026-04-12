# Advanced Features Examples

## Footnotes

### Reference-Style Footnotes

This is a statement that needs a citation[^1].
Another claim with a named footnote[^source].
Multiple references in one sentence[^2][^3].

[^1]: First footnote content. Can include **formatting** and [[wikilinks]].
[^source]: Named footnotes still render as sequential numbers in the output.
[^2]: Second footnote.
[^3]: Third footnote with a longer explanation that provides additional context about the claim made in the main text.

### Inline Footnotes

This has an inline footnote.^[This content appears at the bottom of the note. Only renders in Reading view, NOT in Live Preview.]

Inline footnotes are convenient^[No need to define them separately] but have limited rendering support.

---

## Comments (Obsidian-specific)

### Inline Comment

This text is visible %%but this part is hidden in Reading view%% and this is visible again.

Use comments to leave %%TODO: rewrite this section%% notes to yourself.

### Block Comment

%%
This entire block is hidden in Reading view.
It's only visible in Editing/Source view.

Use for:
- Personal reminders
- Draft content
- Internal notes
%%

### HTML Comments (Portable)

<!-- This comment works in any Markdown renderer -->
<!-- 
  Multi-line HTML comments
  also work in Obsidian
-->

---

## HTML in Obsidian

### Collapsible Section

<details>
<summary>Click to expand this section</summary>

This content is hidden by default. It supports:
- Markdown formatting
- **Bold** and *italic*
- Lists and other elements

</details>

### Keyboard Shortcuts

Press <kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>P</kbd> to open the command palette.

Use <kbd>Cmd</kbd> + <kbd>E</kbd> to toggle between Edit and Reading view.

### Styled Text

<span style="color: red;">Red text</span>
<span style="color: #00aa00;">Green text</span>
<mark>Highlighted with HTML mark tag</mark>

### Custom Container

<div style="border: 1px solid #ccc; padding: 1rem; border-radius: 8px;">

**Note:** This is a custom container using HTML div with inline styles.

- Works in Obsidian
- May not render in all Markdown viewers

</div>

### Line Break

First line<br>Second line (using HTML br tag)

### Subscript and Superscript

H<sub>2</sub>O is water.
E = mc<sup>2</sup> is Einstein's equation.

---

## Collapsible / Expandable Sections

Use HTML `<details>` and `<summary>` for collapsible content (works in Obsidian and GitHub):

```html
<details>
<summary>Click to expand</summary>

Hidden content here.
Supports **Markdown** inside.

</details>
```

Rendered example:

<details>
<summary>Click to expand</summary>

Hidden content — supports Markdown like **bold**, *italic*, and `code`.

</details>

---

## Source-Destination Comparison Table

| Feature | Obsidian | GitHub | Standard MD |
|---------|----------|--------|-------------|
| `[[wikilinks]]` | Yes | No | No |
| `![[embeds]]` | Yes | No | No |
| `#^block-ref` | Yes | No | No |
| `==highlight==` | Yes | No | No |
| `%%comment%%` | Yes | No | No |
| `![[img\|300]]` sizing | Yes | No | No |
| Callout folding `+`/`-` | Yes | No | No |
| `$math$` | Yes | Yes | No |
| Mermaid | Yes | Yes | No |
| `[^footnote]` | Yes | Yes | No |
| 5 callout types | Yes | Yes | No |
| Tables | Yes | Yes | No |
| Task lists | Yes | Yes | No |
| `~~strikethrough~~` | Yes | Yes | No |
| `<!-- HTML comment -->` | Yes | Yes | Yes |
| `<details>` | Yes | Yes | Partial |

---

## 来源

- [Obsidian Advanced formatting syntax](https://obsidian.md/help/advanced-syntax) — Footnotes, comments, math, diagrams
- [Obsidian Flavored Markdown](https://obsidian.md/help/obsidian-flavored-markdown) — HTML interaction rules
- [CommonMark Specification](https://spec.commonmark.org/) — Standard Markdown HTML blocks
