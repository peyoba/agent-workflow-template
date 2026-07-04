"""Doctor checks for template and installed workflow projects."""

from __future__ import annotations

from pathlib import Path

from workflow_lib.metadata import (
    EXPECTED_PLUGIN_FILES,
    EXPECTED_ROLE_DOCS,
    EXPECTED_TEMPLATE_DOCS,
    EXPECTED_WORK_DIRS,
    STATE_HEADINGS,
)
from workflow_lib.paths import relative


def has_agent_entrypoint(root: Path) -> bool:
    return (root / "Agent.md").exists() or (root / "AGENTS.md").exists()


def has_superpowers() -> bool:
    home = Path.home()
    candidates = [
        home / ".codex" / "superpowers" / "skills",
        home / ".agents" / "skills",
        home / ".codex" / "plugins" / "cache" / "openai-api-curated" / "superpowers" / "skills",
    ]
    expected_names = {
        "using-superpowers",
        "test-driven-development",
        "verification-before-completion",
        "writing-plans",
    }
    expected_dirs = expected_names | {f"skill-{name}" for name in expected_names}

    for root in candidates:
        if not root.exists():
            continue
        for skill_file in root.rglob("SKILL.md"):
            if skill_file.parent.name in expected_dirs:
                return True
            try:
                first_chunk = skill_file.read_text(encoding="utf-8")[:240]
            except OSError:
                continue
            if any(f"name: {name}" in first_chunk for name in expected_names):
                return True
    return False


def markdown_fences_are_balanced(root: Path) -> tuple[bool, list[str]]:
    broken: list[str] = []
    for path in root.rglob("*.md"):
        if ".git" in path.parts:
            continue
        relative_parts = path.relative_to(root).parts
        if relative_parts[:2] == (".agent-workflow", "examples"):
            continue
        text = path.read_text(encoding="utf-8")
        if text.count("```") % 2 != 0:
            broken.append(relative(path, root))
    return not broken, broken


def doctor_mode(root: Path, requested: str) -> str:
    if requested != "auto":
        return requested
    plugin_paths = [root / ".codex-plugin", root / ".claude-plugin", root / "skills" / "agent-workflow"]
    if any(path.exists() for path in plugin_paths):
        return "template"
    return "installed"


def run_doctor(root: Path, mode: str = "auto") -> int:
    failed = False
    resolved_mode = doctor_mode(root, mode)

    if has_agent_entrypoint(root):
        entry_missing = False
    else:
        entry_missing = True
        failed = True
        print("FAIL missing Agent.md or AGENTS.md")

    required_files = [
        ".agent-workflow/WORKFLOW.md",
        ".agent-workflow/SKILLS.md",
        ".agent-workflow/STATE_RULES.md",
        ".agent-workflow/state.md",
        "PROJECT_PROFILE.md",
    ]
    for item in required_files:
        if not (root / item).exists():
            failed = True
            print(f"FAIL missing {item}")

    if all((root / item).exists() for item in required_files) and not entry_missing:
        print("PASS required files present")

    missing_roles = [
        name for name in EXPECTED_ROLE_DOCS if not (root / ".agent-workflow" / "agents" / name).exists()
    ]
    if missing_roles:
        failed = True
        for name in missing_roles:
            print(f"FAIL missing .agent-workflow/agents/{name}")
    else:
        print("PASS role documents present")

    for name in EXPECTED_TEMPLATE_DOCS:
        path = root / ".agent-workflow" / "templates" / name
        if not path.exists():
            failed = True
            print(f"FAIL missing .agent-workflow/templates/{name}")

    for name in EXPECTED_WORK_DIRS:
        if not (root / name).is_dir():
            failed = True
            print(f"FAIL missing directory {name}")

    if resolved_mode == "template":
        if (root / "PROJECT_PROFILE.template.md").exists():
            print("PASS PROJECT_PROFILE.template.md present")
        else:
            failed = True
            print("FAIL missing PROJECT_PROFILE.template.md")
        for path_name, label in EXPECTED_PLUGIN_FILES:
            if (root / path_name).exists():
                print(f"PASS {label} present")
            else:
                failed = True
                print(f"FAIL missing {path_name}")
    else:
        print("PASS installed workflow files present")

    state_path = root / ".agent-workflow" / "state.md"
    if state_path.exists():
        state_text = state_path.read_text(encoding="utf-8")
        for heading in STATE_HEADINGS:
            if heading not in state_text:
                failed = True
                print(f"FAIL state.md missing heading {heading}")

    profile_path = root / "PROJECT_PROFILE.md"
    if profile_path.exists():
        profile_text = profile_path.read_text(encoding="utf-8")
        if "[填写" in profile_text or "[命令" in profile_text or "[说明" in profile_text:
            print("WARN PROJECT_PROFILE.md still has placeholders")
        else:
            print("PASS PROJECT_PROFILE.md appears filled")

    if has_superpowers():
        print("PASS Superpowers skills found")
    else:
        print("WARN Superpowers skills not found in common local paths")

    balanced, broken = markdown_fences_are_balanced(root)
    if balanced:
        print("PASS markdown code fences balanced")
    else:
        failed = True
        for path in broken:
            print(f"FAIL unbalanced markdown code fence in {path}")

    return 1 if failed else 0
