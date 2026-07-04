import json
from pathlib import Path

from tests.workflow_test_helpers import REPO_ROOT, copy_template, run_workflow


def test_doctor_checks_cross_agent_plugin_package(tmp_path: Path) -> None:
    project = copy_template(tmp_path)

    result = run_workflow(project, "doctor", "--mode", "template")

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
