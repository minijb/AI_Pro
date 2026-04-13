# Callout Examples

## All 12 Built-in Callout Types

> [!note]
> This is a **note** callout. Default style for any unrecognized type.

> [!abstract] Abstract / Summary / TLDR
> Use for executive summaries or TLDR sections.

> [!info] Information
> Alias: `todo`. General informational content.

> [!tip] Tip / Hint / Important
> Helpful advice and best practices.

> [!success] Success / Check / Done
> Indicates successful completion or positive outcomes.

> [!question] Question / Help / FAQ
> For questions, FAQs, or help sections.

> [!warning] Warning / Caution / Attention
> Important warnings the reader should be aware of.

> [!failure] Failure / Fail / Missing
> Indicates something that failed or is missing.

> [!danger] Danger / Error
> Critical errors or dangerous situations.

> [!bug] Bug
> Known bugs or issues to track.

> [!example] Example
> Code examples, use cases, or demonstrations.

> [!quote] Quote / Cite
> Notable quotations or citations.

---

## Foldable Callouts

> [!tip]+ Expanded by Default (click to collapse)
> This content is visible when the note loads.
> The `+` after the type makes it expanded by default.

> [!warning]- Collapsed by Default (click to expand)
> This content is hidden when the note loads.
> The `-` after the type makes it collapsed by default.

> [!note] Not Foldable
> This callout cannot be folded. No `+` or `-` after type.

---

## Custom Titles

> [!tip] My Custom Title Here
> The text after the type identifier becomes the title.

> [!danger] DO NOT DELETE
> Custom titles can be used for emphasis.

> [!info]
> Without a custom title, the type name is used as the title.

---

## Nested Callouts

> [!question] Can callouts be nested?
> Yes! Use additional `>` characters.
> > [!success] Answer
> > Callouts can nest to any depth.
> > > [!example] Like this
> > > Three levels deep.

> [!tip] Understanding Attention
> Think of attention as a weighted retrieval process.
> > [!example] Translation Example
> > When translating "The cat sat", the Query for "猫"
> > gives highest weight to "cat".

---

## Rich Content in Callouts

> [!info] Callouts Support Full Markdown
> - **Bold**, *italic*, ==highlighted==, ~~strikethrough~~
> - [[Wikilinks]] and [external links](https://example.com)
> - `inline code` and code blocks
> - ![[embedded-image.png|200]]
> - Task lists:
>   - [x] Completed
>   - [ ] Pending
>
> | Column A | Column B |
> |----------|----------|
> | Data 1   | Data 2   |
>
> Even math: $E = mc^2$

---

## Custom Callout Type (CSS Snippet)

To create a custom callout type, save this CSS in `.obsidian/snippets/custom-callouts.css`:

```css
.callout[data-callout="custom-type"] {
    --callout-color: 255, 100, 50;
    --callout-icon: lucide-sparkles;
}

.callout[data-callout="goal"] {
    --callout-color: 50, 200, 100;
    --callout-icon: lucide-target;
}

.callout[data-callout="brain"] {
    --callout-color: 200, 150, 255;
    --callout-icon: lucide-brain;
}
```

Then use in notes:

> [!goal] Q2 Goals
> - Increase user retention by 15%
> - Launch mobile app beta

---

## GitHub-Compatible Callouts (5 types only)

> [!NOTE]
> Works on both Obsidian and GitHub.

> [!TIP]
> Works on both Obsidian and GitHub.

> [!IMPORTANT]
> Works on both Obsidian and GitHub.

> [!WARNING]
> Works on both Obsidian and GitHub.

> [!CAUTION]
> Works on both Obsidian and GitHub.

---

## Case Sensitivity

All callout type identifiers are **case-insensitive**. These all work identically:

> [!NOTE]
> Uppercase works.

> [!note]
> Lowercase works.

> [!Note]
> Mixed case works.

> [!NoTe]
> Any casing works — Obsidian normalizes to lowercase internally.

---

## 来源

- [Obsidian Callouts](https://obsidian.md/help/callouts) — All callout types, folding, nesting, custom CSS
- [Obsidian Flavored Markdown](https://obsidian.md/help/obsidian-flavored-markdown) — Overview of OFM extensions
