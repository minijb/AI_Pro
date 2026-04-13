# Links and Embeds Examples

## Wikilinks (Internal Links)

### Basic Links

[[My Note]]
[[My Note|Custom Display Text]]
[[My Note.md]]
[[Folder/Subfolder/Deep Note]]

### Heading Links

[[My Note#Introduction]]
[[My Note#Section Two|Jump to Section 2]]
[[#Heading in This Note]]

### Block Reference Links

[[My Note#^important-paragraph]]
[[My Note#^block-123|See this block]]
[[#^local-block]]

### Search Links

[[##search headings vault-wide]]
[[^^search blocks vault-wide]]

---

## Block References

This paragraph has a block ID that can be referenced from other notes. ^example-paragraph

- Item A
- Item B
- Item C

^example-list

> A memorable quote that deserves
> to be referenced elsewhere.

^example-quote

---

## Markdown-Style Links

[Display Text](Note%20Name.md)
[Link to heading](Note%20Name.md#Introduction)
[External Link](https://example.com)
[Obsidian URI](obsidian://open?vault=MyVault&file=Note.md)

---

## Embed Notes

![[Another Note]]
![[Another Note#Specific Section]]
![[Another Note#^specific-block]]

---

## Embed Images

![[photo.png]]
![[photo.png|640]]
![[photo.png|640x480]]

![External image](https://example.com/image.png)
![Resized external|300](https://example.com/image.png)

Supported formats: `.avif`, `.bmp`, `.gif`, `.jpeg`, `.jpg`, `.png`, `.svg`, `.webp`

---

## Embed Audio

![[podcast.mp3]]
![[recording.ogg]]
![[music.flac]]

Supported formats: `.flac`, `.m4a`, `.mp3`, `.ogg`, `.wav`, `.webm`, `.3gp`

---

## Embed Video

![[tutorial.mp4]]
![[clip.webm]]
![[presentation.ogv]]

Supported formats: `.mp4`, `.webm`, `.ogv`

---

## Embed PDF

![[paper.pdf]]
![[paper.pdf#page=5]]
![[paper.pdf#height=600]]

---

## Embed Search Results

```query
tag:#project status:done
```

---

## Autolinks (GFM)

GFM autolinks are supported — URLs enclosed in `<>` are automatically linked:

<https://example.com>
<mailto:user@example.com>

---

## Obsidian URI Links

Open notes programmatically via Obsidian's URI protocol:

```markdown
[Open vault](obsidian://open?vault=MyVault&file=Note.md)
[Open note](obsidian://open?path=Note.md)
[New note](obsidian://new?vault=MyVault&name=NewNote&path=/Folder/)
```

### File and ID Links

```markdown
file:[[path/to/note.md]]     # Link to a file by path (use %20 for spaces)
id:[[block-id]]              # Link to a specific block by its ID
[[Note#^block-id]]           # Standard block reference syntax
```

---

## 来源

- [Obsidian Internal links](https://obsidian.md/help/links) — Wikilinks, block references, search links
- [Obsidian Embed files](https://obsidian.md/help/embeds) — Note, image, audio, video, PDF embeds
- [Obsidian Basic syntax](https://obsidian.md/help/syntax) — Markdown links, images
- [GitHub Flavored Markdown](https://docs.github.com/en/get-started/writing-on-github) — Autolinks
