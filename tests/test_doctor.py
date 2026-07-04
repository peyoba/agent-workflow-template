from __future__ import annotations

import shutil
from pathlib import Path

from tests.workflow_test_helpers import copy_template, run_workflow


def test_doctor_passes_for_complete_template(tmp_path: Path) -> None:
    project = copy_template(tmp_path)

    result = run_workflow(project, "doctor")

    assert result.returncode == 0
    assert "PASS required files present" in result.stdout
    assert "PASS role documents present" in result.stdout
    assert "PASS PROJECT_PROFILE.md appears filled" in result.stdout
    assert "WARN PROJECT_PROFILE.md still has placeholders" not in result.stdout


def test_template_package_includes_project_profile_template(tmp_path: Path) -> None:
    project = copy_template(tmp_path)

    result = run_workflow(project, "doctor", "--mode", "template")

    assert result.returncode == 0
    assert "PASS PROJECT_PROFILE.template.md present" in result.stdout

    template = project / "PROJECT_PROFILE.template.md"
    template_text = template.read_text(encoding="utf-8")
    assert "[填写项目名称]" in template_text
    assert "[命令]" in template_text


def test_doctor_installed_mode_does_not_require_plugin_package(tmp_path: Path) -> None:
    source = copy_template(tmp_path)
    project = tmp_path / "installed-project"
    project.mkdir()
    for item in ["AGENTS.md", "Agent.md", ".agent-workflow", "scripts"]:
        source_path = source / item
        target_path = project / item
        if source_path.is_dir():
            shutil.copytree(source_path, target_path)
        else:
            shutil.copy2(source_path, target_path)
    shutil.copy2(source / "PROJECT_PROFILE.template.md", project / "PROJECT_PROFILE.md")

    result = run_workflow(project, "doctor", "--mode", "installed")

    assert result.returncode == 0
    assert "PASS required files present" in result.stdout
    assert "PASS installed workflow files present" in result.stdout
    assert "Codex plugin manifest" not in result.stdout
    assert "Claude plugin manifest" not in result.stdout


def test_doctor_checks_real_superpowers_skill_files(tmp_path: Path) -> None:
    project = copy_template(tmp_path)
    fake_home = tmp_path / "home"
    (fake_home / ".agents" / "skills").mkdir(parents=True)

    result = run_workflow(project, "doctor", extra_env={"HOME": str(fake_home)})

    assert result.returncode == 0
    assert "WARN Superpowers skills not found in common local paths" in result.stdout


def test_doctor_fails_when_required_file_is_missing(tmp_path: Path) -> None:
    project = copy_template(tmp_path)
    (project / ".agent-workflow" / "WORKFLOW.md").unlink()

    result = run_workflow(project, "doctor")

    assert result.returncode == 1
    assert "FAIL missing .agent-workflow/WORKFLOW.md" in result.stdout
