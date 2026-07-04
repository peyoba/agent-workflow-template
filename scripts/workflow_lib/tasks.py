"""Task artifact generation for workflow projects."""

from __future__ import annotations

import argparse
import hashlib
import re
from pathlib import Path

from workflow_lib.metadata import DEFAULT_REASON, EXPECTED_WORK_DIRS, ROLE_DEFINITIONS, ROLE_SETS
from workflow_lib.paths import relative
from workflow_lib.render import render_handoff, render_spec, render_state, render_task_card
from workflow_lib.risk import assess_risk, format_assessment_reason


def slugify(title: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", title.strip().lower()).strip("-")
    if slug:
        return slug
    digest = hashlib.sha1(title.encode("utf-8")).hexdigest()[:8]
    return f"task-{digest}"


def ensure_workflow_dirs(root: Path) -> None:
    for item in EXPECTED_WORK_DIRS:
        (root / item).mkdir(parents=True, exist_ok=True)


def run_new_task(args: argparse.Namespace) -> int:
    root = Path(args.project_root).resolve()
    workflow_root = root / ".agent-workflow"
    if not workflow_root.exists():
        print("FAIL missing .agent-workflow directory")
        return 1

    ensure_workflow_dirs(root)
    level = args.level
    reason = args.reason
    assessment = assess_risk(f"{args.title}\n{args.summary}\n{args.reason}")
    if level == "auto":
        level = assessment.level
        if reason == DEFAULT_REASON:
            reason = format_assessment_reason(assessment)
    elif assessment.level == "L3" and level != "L3" and not args.allow_downgrade:
        print(f"FAIL task requires L3 because: {', '.join(assessment.reasons)}")
        print("Use --level L3, or pass --allow-downgrade only after recording the user decision.")
        return 1

    stem = f"{args.date}-{slugify(args.title)}"
    spec_path = root / ".agent-workflow" / "specs" / f"{stem}.md"
    handoff_path = root / ".agent-workflow" / "handoffs" / f"{stem}.md"
    state_path = root / ".agent-workflow" / "state.md"
    task_card_paths = {
        role: root / ".agent-workflow" / "task-cards" / f"{stem}-{ROLE_DEFINITIONS[role].slug}.md"
        for role in ROLE_SETS[level]
    }

    generated = [spec_path, *task_card_paths.values(), handoff_path]
    existing = [path for path in generated if path.exists()]
    if existing and not args.force:
        for path in existing:
            print(f"FAIL {relative(path, root)} already exists")
        return 1

    spec_rel = relative(spec_path, root)
    task_card_rels = {role: relative(path, root) for role, path in task_card_paths.items()}
    handoff_rel = relative(handoff_path, root)

    spec_path.write_text(render_spec(args.title, level, reason, args.summary), encoding="utf-8")
    for role, task_card_path in task_card_paths.items():
        task_card_path.write_text(
            render_task_card(args.title, level, role, spec_rel),
            encoding="utf-8",
        )
    handoff_path.write_text(
        render_handoff(args.title, level, spec_rel, list(task_card_rels.values())),
        encoding="utf-8",
    )
    state_path.write_text(render_state(args.title, level, reason, task_card_rels), encoding="utf-8")

    print(f"CREATED {spec_rel}")
    for task_card_rel in task_card_rels.values():
        print(f"CREATED {task_card_rel}")
    print(f"CREATED {handoff_rel}")
    print("UPDATED .agent-workflow/state.md")
    return 0
