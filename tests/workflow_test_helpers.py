from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = REPO_ROOT / "scripts" / "workflow.py"


def ignore_template_noise(directory: str, names: list[str]) -> set[str]:
    ignored = {".git", "__pycache__", ".pytest_cache"}
    if Path(directory).resolve() == REPO_ROOT / ".agent-workflow":
        ignored.add("examples")
    return ignored.intersection(names)


def copy_template(tmp_path: Path) -> Path:
    project = tmp_path / "project"
    shutil.copytree(REPO_ROOT, project, ignore=ignore_template_noise)
    return project


def run_workflow(
    project: Path,
    *args: str,
    extra_env: dict[str, str] | None = None,
) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["PYTHONPATH"] = str(REPO_ROOT)
    if extra_env:
        env.update(extra_env)
    return subprocess.run(
        [sys.executable, str(WORKFLOW), *args, "--project-root", str(project)],
        text=True,
        capture_output=True,
        env=env,
        check=False,
    )
