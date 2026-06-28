import os
import shutil
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = REPO_ROOT / "scripts" / "workflow.py"


def copy_template(tmp_path: Path) -> Path:
    project = tmp_path / "project"
    ignore = shutil.ignore_patterns(".git", "__pycache__", ".pytest_cache")
    shutil.copytree(REPO_ROOT, project, ignore=ignore)
    return project


def run_workflow(project: Path, *args: str) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["PYTHONPATH"] = str(REPO_ROOT)
    return subprocess.run(
        [sys.executable, str(WORKFLOW), *args, "--project-root", str(project)],
        text=True,
        capture_output=True,
        env=env,
        check=False,
    )


def test_doctor_passes_for_complete_template(tmp_path: Path) -> None:
    project = copy_template(tmp_path)

    result = run_workflow(project, "doctor")

    assert result.returncode == 0
    assert "PASS required files present" in result.stdout
    assert "PASS role documents present" in result.stdout
    assert "WARN PROJECT_PROFILE.md still has placeholders" in result.stdout


def test_doctor_fails_when_required_file_is_missing(tmp_path: Path) -> None:
    project = copy_template(tmp_path)
    (project / ".agent-workflow" / "WORKFLOW.md").unlink()

    result = run_workflow(project, "doctor")

    assert result.returncode == 1
    assert "FAIL missing .agent-workflow/WORKFLOW.md" in result.stdout


def test_new_task_creates_standard_artifacts_and_updates_state(tmp_path: Path) -> None:
    project = copy_template(tmp_path)

    result = run_workflow(
        project,
        "new-task",
        "Add user login",
        "--level",
        "L2",
        "--reason",
        "Touches authentication and user sessions.",
        "--date",
        "2026-06-28",
    )

    assert result.returncode == 0, result.stderr

    spec = project / ".agent-workflow" / "specs" / "2026-06-28-add-user-login.md"
    task_card = project / ".agent-workflow" / "task-cards" / "2026-06-28-add-user-login.md"
    handoff = project / ".agent-workflow" / "handoffs" / "2026-06-28-add-user-login.md"
    state = project / ".agent-workflow" / "state.md"

    assert spec.exists()
    assert task_card.exists()
    assert handoff.exists()

    spec_text = spec.read_text(encoding="utf-8")
    assert "# Add user login SPEC" in spec_text
    assert "## 风险等级\nL2" in spec_text
    assert "Touches authentication and user sessions." in spec_text

    task_card_text = task_card.read_text(encoding="utf-8")
    assert "## 任务等级\nL2" in task_card_text
    assert "①测试工程师" in task_card_text
    assert "④质量工程师" in task_card_text
    assert "⑤安全工程师" not in task_card_text

    state_text = state.read_text(encoding="utf-8")
    assert "## 当前任务\nAdd user login" in state_text
    assert "## 风险等级\nL2" in state_text
    assert "| ①测试工程师 | READY |" in state_text
    assert "| ④质量工程师 | READY |" in state_text


def test_new_task_refuses_to_overwrite_existing_artifacts(tmp_path: Path) -> None:
    project = copy_template(tmp_path)
    args = (
        "new-task",
        "Add billing audit",
        "--level",
        "L3",
        "--reason",
        "Touches payments.",
        "--date",
        "2026-06-28",
    )

    first = run_workflow(project, *args)
    second = run_workflow(project, *args)

    assert first.returncode == 0
    assert second.returncode == 1
    assert "already exists" in second.stdout
