# Embedding Bases Inline

This example shows how to embed base views directly inside a Markdown note
using code blocks, without creating a separate `.base` file.

## Method 1: Embed a .base file

Use standard Obsidian embed syntax:

```markdown
![[MyBase.base]]
```

To embed a specific view from a multi-view base:

```markdown
![[MyBase.base#ViewName]]
```

## Method 2: Inline code block

Use a `base` code block to define the base directly in your note:

````markdown
```base
filters:
  and:
    - file.hasTag("meeting")
    - file.inFolder("Work/Meetings")
formulas:
  date_display: 'file.ctime.format("YYYY-MM-DD")'
views:
  - type: table
    name: "Recent Meetings"
    limit: 10
    order:
      - file.name
      - formula.date_display
    filters:
      and:
        - 'file.ctime > now() - "30d"'
```
````

## Method 3: Inline with multiple views

````markdown
```base
filters:
  and:
    - file.hasTag("recipe")
formulas:
  cook_time_display: 'if(cook_time, cook_time + " min", "")'
  difficulty_stars: 'if(difficulty, "★".repeat(difficulty), "")'
views:
  - type: cards
    name: "Gallery"
    order:
      - file.name
      - formula.cook_time_display
      - formula.difficulty_stars

  - type: table
    name: "Details"
    order:
      - file.name
      - note.cuisine
      - note.cook_time
      - note.difficulty
      - note.servings
    summaries:
      note.cook_time: Average
```
````

## The `this` Object

When a base is embedded in a note, `this` refers to the embedding note.
This is useful for creating contextual views:

````markdown
```base
filters:
  and:
    - file.hasLink(this.file)
views:
  - type: list
    name: "Backlinks"
    order:
      - file.name
      - file.mtime
```
````

This creates a dynamic backlinks panel that shows all notes linking to the current note.

---

> Sources:
> - https://obsidian.md/help/bases/create-base
> - https://obsidian.md/help/bases/syntax
> - https://obsidian.md/help/bases/views
