"""Shared utilities for agent-creator scripts."""

import re
from pathlib import Path


def parse_agent_md(agent_path: Path) -> dict:
    """Parse an agent .md file, returning structured data.

    Returns dict with keys: name, description, tools, model, hooks,
    memory, full_content, frontmatter_raw, system_prompt.
    """
    content = agent_path.read_text(encoding="utf-8")
    lines = content.split("\n")

    if not lines or lines[0].strip() != "---":
        raise ValueError(f"{agent_path}: missing frontmatter (no opening ---)")

    end_idx = None
    for i, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            end_idx = i
            break

    if end_idx is None:
        raise ValueError(f"{agent_path}: missing frontmatter (no closing ---)")

    frontmatter_raw = "\n".join(lines[1:end_idx])
    system_prompt = "\n".join(lines[end_idx + 1 :]).strip()

    # Parse key fields from frontmatter
    result = {
        "name": "",
        "description": "",
        "tools": "",
        "model": "",
        "hooks": None,
        "memory": "",
        "full_content": content,
        "frontmatter_raw": frontmatter_raw,
        "system_prompt": system_prompt,
    }

    frontmatter_lines = lines[1:end_idx]
    i = 0
    while i < len(frontmatter_lines):
        line = frontmatter_lines[i]

        for field in ("name", "description", "tools", "model", "memory"):
            if line.startswith(f"{field}:"):
                value = line[len(field) + 1 :].strip()
                # Handle YAML multiline indicators
                if value in (">", "|", ">-", "|-"):
                    continuation: list[str] = []
                    i += 1
                    while i < len(frontmatter_lines) and (
                        frontmatter_lines[i].startswith("  ")
                        or frontmatter_lines[i].startswith("\t")
                    ):
                        continuation.append(frontmatter_lines[i].strip())
                        i += 1
                    result[field] = " ".join(continuation)
                    break
                else:
                    result[field] = value.strip("\"'")
                break

        if line.startswith("hooks:"):
            result["hooks"] = "present"

        i += 1

    return result


def validate_agent_name(name: str) -> tuple[bool, str]:
    """Validate agent name format."""
    if not name:
        return False, "name is empty"
    if not re.match(r"^[a-z0-9-]+$", name):
        return False, f"name '{name}' must be kebab-case (lowercase, digits, hyphens)"
    if name.startswith("-") or name.endswith("-") or "--" in name:
        return False, f"name '{name}' cannot start/end with hyphen or have consecutive hyphens"
    if len(name) > 64:
        return False, f"name is {len(name)} chars, max is 64"
    return True, "valid"


VALID_TOOLS = {
    "Read", "Write", "Edit", "Bash", "Glob", "Grep",
    "Agent", "NotebookEdit", "WebFetch", "WebSearch",
}

VALID_MODELS = {"haiku", "sonnet", "opus", "inherit"}

VALID_MEMORY_SCOPES = {"user", "project", "local"}
