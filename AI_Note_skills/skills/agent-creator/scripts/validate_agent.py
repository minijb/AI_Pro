#!/usr/bin/env python3
"""
Validate an agent .md file's structure, frontmatter, and system prompt.

Usage:
    python validate_agent.py <agent_file.md>
    python -m scripts.validate_agent <agent_file.md>

Exit codes:
    0 - valid
    1 - invalid (issues found)
"""

import re
import sys
from pathlib import Path

try:
    import yaml

    HAS_YAML = True
except ImportError:
    HAS_YAML = False

from .utils import VALID_MODELS, VALID_MEMORY_SCOPES, VALID_TOOLS, validate_agent_name


def validate_agent(agent_path: Path) -> tuple[bool, list[str], list[str]]:
    """Validate an agent file.

    Returns (is_valid, errors, warnings).
    """
    errors: list[str] = []
    warnings: list[str] = []

    agent_path = Path(agent_path)
    if not agent_path.exists():
        return False, [f"File not found: {agent_path}"], []

    content = agent_path.read_text(encoding="utf-8")

    # --- Frontmatter extraction ---
    if not content.startswith("---"):
        return False, ["Missing YAML frontmatter (no opening ---)"], []

    match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return False, ["Invalid frontmatter format (no closing ---)"], []

    frontmatter_text = match.group(1)
    body = content[match.end() :].strip()

    # --- Parse YAML ---
    if HAS_YAML:
        try:
            fm = yaml.safe_load(frontmatter_text)
            if not isinstance(fm, dict):
                return False, ["Frontmatter must be a YAML mapping"], []
        except yaml.YAMLError as e:
            return False, [f"Invalid YAML: {e}"], []
    else:
        # Fallback: simple key extraction
        fm = {}
        for line in frontmatter_text.split("\n"):
            if ":" in line and not line.startswith(" ") and not line.startswith("\t"):
                key = line.split(":")[0].strip()
                value = line.split(":", 1)[1].strip()
                fm[key] = value

    # --- Allowed fields ---
    ALLOWED_FIELDS = {
        "name", "description", "tools", "disallowedTools", "model", "effort",
        "maxTurns", "permissionMode", "hooks", "memory", "mcpServers",
        "skills", "background", "isolation", "color", "initialPrompt",
    }
    unexpected = set(fm.keys()) - ALLOWED_FIELDS
    if unexpected:
        errors.append(
            f"Unexpected frontmatter fields: {', '.join(sorted(unexpected))}. "
            f"Allowed: {', '.join(sorted(ALLOWED_FIELDS))}"
        )

    # --- Required: name ---
    name = fm.get("name", "")
    if not name:
        errors.append("Missing required field: name")
    else:
        if isinstance(name, str):
            valid, msg = validate_agent_name(name)
            if not valid:
                errors.append(f"Invalid name: {msg}")

    # --- Required: description ---
    desc = fm.get("description", "")
    if not desc:
        errors.append("Missing required field: description")
    elif isinstance(desc, str):
        if len(desc) > 1024:
            warnings.append(f"Description is {len(desc)} chars (recommended max 1024)")
        # Check for trigger language
        has_trigger = any(
            kw in desc.lower()
            for kw in ["use when", "use proactively", "trigger when", "用于", "当"]
        )
        if not has_trigger:
            warnings.append("Description lacks trigger language (Use when.../Use proactively...)")

    # --- model ---
    model = fm.get("model")
    if model and isinstance(model, str):
        if model not in VALID_MODELS and not model.startswith("claude-"):
            warnings.append(f"Unusual model value: '{model}'. Expected: {', '.join(sorted(VALID_MODELS))}")

    # --- tools ---
    tools_raw = fm.get("tools", "")
    if tools_raw and isinstance(tools_raw, str):
        tool_list = [t.strip() for t in tools_raw.split(",")]
        for tool in tool_list:
            # Handle Agent(type) syntax
            base_tool = re.match(r"^(\w+)", tool)
            if base_tool and base_tool.group(1) not in VALID_TOOLS:
                warnings.append(f"Unknown tool: '{tool}'")

    # --- memory ---
    memory = fm.get("memory")
    if memory and isinstance(memory, str) and memory not in VALID_MEMORY_SCOPES:
        errors.append(f"Invalid memory scope: '{memory}'. Must be: {', '.join(sorted(VALID_MEMORY_SCOPES))}")

    # --- effort ---
    effort = fm.get("effort")
    if effort and effort not in ("low", "medium", "high", "max"):
        errors.append(f"Invalid effort: '{effort}'. Must be: low, medium, high, max")

    # --- permissionMode ---
    perm = fm.get("permissionMode")
    valid_perms = {"default", "acceptEdits", "auto", "dontAsk", "bypassPermissions", "plan"}
    if perm and perm not in valid_perms:
        errors.append(f"Invalid permissionMode: '{perm}'. Must be: {', '.join(sorted(valid_perms))}")

    # --- background ---
    bg = fm.get("background")
    if bg is not None and not isinstance(bg, bool):
        errors.append(f"'background' must be boolean, got {type(bg).__name__}")

    # --- isolation ---
    iso = fm.get("isolation")
    if iso and iso != "worktree":
        errors.append(f"'isolation' must be 'worktree' if set, got '{iso}'")

    # --- System prompt checks ---
    if not body:
        warnings.append("System prompt (markdown body) is empty")
    else:
        # Check for workflow steps
        has_steps = bool(re.search(r"^\d+\.", body, re.MULTILINE))
        if not has_steps:
            warnings.append("System prompt has no numbered workflow steps (1. 2. 3. ...)")

        # Check for role definition
        lines = body.split("\n")
        first_para = ""
        for line in lines:
            if line.strip():
                first_para = line.strip()
                break
        if first_para and not any(
            kw in first_para for kw in ["你是", "You are", "专家", "expert", "负责", "responsible"]
        ):
            warnings.append("System prompt may lack a role definition in the opening line")

    is_valid = len(errors) == 0
    return is_valid, errors, warnings


def main():
    if len(sys.argv) < 2:
        print("Usage: python validate_agent.py <agent_file.md> [agent_file2.md ...]")
        sys.exit(1)

    all_valid = True
    for path_str in sys.argv[1:]:
        path = Path(path_str)
        valid, errors, warnings = validate_agent(path)

        print(f"\n{'=' * 60}")
        print(f"  {path.name}")
        print(f"{'=' * 60}")

        if valid:
            print(f"  [PASS] VALID")
        else:
            print(f"  [FAIL] INVALID")
            all_valid = False

        for err in errors:
            print(f"  ERROR: {err}")
        for warn in warnings:
            print(f"  WARN:  {warn}")

    sys.exit(0 if all_valid else 1)


if __name__ == "__main__":
    main()
