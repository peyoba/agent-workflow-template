import json
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


def test_doctor_checks_cross_agent_plugin_package(tmp_path: Path) -> None:
    project = copy_template(tmp_path)

    result = run_workflow(project, "doctor")

    assert result.returncode == 0
    assert "PASS Codex plugin manifest present" in result.stdout
    assert "PASS Claude plugin manifest present" in result.stdout
    assert "PASS agent-workflow skill present" in result.stdout


def test_codex_plugin_manifest_points_to_shared_skills() -> None:
    manifest_path = REPO_ROOT / ".codex-plugin" / "plugin.json"

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

    assert manifest["name"] == "agent-workflow"
    assert manifest["skills"] == "./skills/"
    assert manifest["interface"]["displayName"] == "Agent Workflow"
    assert "Developer Tools" == manifest["interface"]["category"]


def test_claude_plugin_manifest_uses_same_plugin_identity() -> None:
    manifest_path = REPO_ROOT / ".claude-plugin" / "plugin.json"

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

    assert manifest["name"] == "agent-workflow"
    assert manifest["repository"] == "https://github.com/peyoba/agent-workflow-template"
    assert "skills" in manifest["keywords"]


def test_agent_workflow_skill_has_valid_trigger_and_resources() -> None:
    skill_path = REPO_ROOT / "skills" / "agent-workflow" / "SKILL.md"
    metadata_path = REPO_ROOT / "skills" / "agent-workflow" / "agents" / "openai.yaml"

    skill_text = skill_path.read_text(encoding="utf-8")
    metadata_text = metadata_path.read_text(encoding="utf-8")

    assert skill_text.startswith("---\n")
    assert "name: agent-workflow" in skill_text
    assert "description:" in skill_text
    assert "AGENTS.md" in skill_text
    assert ".agent-workflow/WORKFLOW.md" in skill_text
    assert "scripts/workflow.py doctor" in skill_text
    assert '  display_name: "Agent Workflow"' in metadata_text
    assert "Use $agent-workflow" in metadata_text


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
    assert "## 文件边界" in spec_text
    assert "## 验收证据" in spec_text

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


def test_assess_risk_recommends_level_with_reasons(tmp_path: Path) -> None:
    project = copy_template(tmp_path)

    result = run_workflow(
        project,
        "assess-risk",
        "Add payment checkout with API keys, database writes, and production deployment",
    )

    assert result.returncode == 0
    assert "Recommended level: L3" in result.stdout
    assert "payment" in result.stdout
    assert "api key" in result.stdout
    assert "database" in result.stdout
    assert "deployment" in result.stdout


def test_assess_risk_supports_chinese_task_text(tmp_path: Path) -> None:
    project = copy_template(tmp_path)

    result = run_workflow(
        project,
        "assess-risk",
        "新增支付结账，保存数据库，并部署到生产环境",
    )

    assert result.returncode == 0
    assert "Recommended level: L3" in result.stdout
    assert "payment" in result.stdout
    assert "database" in result.stdout
    assert "deployment" in result.stdout


def test_new_task_auto_level_uses_risk_assessment(tmp_path: Path) -> None:
    project = copy_template(tmp_path)

    result = run_workflow(
        project,
        "new-task",
        "Add payment checkout",
        "--level",
        "auto",
        "--summary",
        "Add payment checkout with API keys and production deployment.",
        "--date",
        "2026-06-28",
    )

    assert result.returncode == 0, result.stderr

    spec = project / ".agent-workflow" / "specs" / "2026-06-28-add-payment-checkout.md"
    task_card = project / ".agent-workflow" / "task-cards" / "2026-06-28-add-payment-checkout.md"

    spec_text = spec.read_text(encoding="utf-8")
    task_card_text = task_card.read_text(encoding="utf-8")

    assert "## 风险等级\nL3" in spec_text
    assert "自动风险评分" in spec_text
    assert "⑤安全工程师" in task_card_text
    assert "⑩风险审查官" in task_card_text
