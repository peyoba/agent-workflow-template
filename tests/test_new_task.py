from pathlib import Path

from tests.workflow_test_helpers import copy_template, run_workflow


def test_new_task_creates_standard_artifacts_and_updates_state(tmp_path: Path) -> None:
    project = copy_template(tmp_path)

    result = run_workflow(
        project,
        "new-task",
        "Add CLI report",
        "--level",
        "L2",
        "--reason",
        "Adds a user-visible local CLI report.",
        "--date",
        "2026-06-28",
    )

    assert result.returncode == 0, result.stderr

    spec = project / ".agent-workflow" / "specs" / "2026-06-28-add-cli-report.md"
    test_card = project / ".agent-workflow" / "task-cards" / "2026-06-28-add-cli-report-01-test-engineer.md"
    dev_card = project / ".agent-workflow" / "task-cards" / "2026-06-28-add-cli-report-02-developer.md"
    acceptance_card = project / ".agent-workflow" / "task-cards" / "2026-06-28-add-cli-report-03-acceptance-engineer.md"
    quality_card = project / ".agent-workflow" / "task-cards" / "2026-06-28-add-cli-report-04-quality-engineer.md"
    handoff = project / ".agent-workflow" / "handoffs" / "2026-06-28-add-cli-report.md"
    state = project / ".agent-workflow" / "state.md"

    assert spec.exists()
    assert test_card.exists()
    assert dev_card.exists()
    assert acceptance_card.exists()
    assert quality_card.exists()
    assert handoff.exists()

    spec_text = spec.read_text(encoding="utf-8")
    assert "# Add CLI report SPEC" in spec_text
    assert "## 风险等级\nL2" in spec_text
    assert "Adds a user-visible local CLI report." in spec_text
    assert "## 文件边界" in spec_text
    assert "## 验收证据" in spec_text

    test_card_text = test_card.read_text(encoding="utf-8")
    assert "## 角色\n①测试工程师" in test_card_text
    assert "## 当前 Hook\nred_hook" in test_card_text
    assert "`.agent-workflow/agents/01-test-engineer.md`" in test_card_text

    dev_card_text = dev_card.read_text(encoding="utf-8")
    assert "## 角色\n②开发工程师" in dev_card_text
    assert "## 当前 Hook\ngreen_hook" in dev_card_text
    assert "systematic-debugging" in dev_card_text

    state_text = state.read_text(encoding="utf-8")
    assert "## 当前任务\nAdd CLI report" in state_text
    assert "## 风险等级\nL2" in state_text
    assert "| 角色 | 状态 | 任务卡 | 产出 |" in state_text
    assert "| ①测试工程师 | READY | .agent-workflow/task-cards/2026-06-28-add-cli-report-01-test-engineer.md | 待派发 |" in state_text
    assert "| ④质量工程师 | READY | .agent-workflow/task-cards/2026-06-28-add-cli-report-04-quality-engineer.md | 待派发 |" in state_text
    assert "## 打回记录" in state_text


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


def test_new_task_refuses_to_downgrade_l3_triggers(tmp_path: Path) -> None:
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

    assert result.returncode == 1
    assert "requires L3" in result.stdout
    assert "--allow-downgrade" in result.stdout


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
    security_card = project / ".agent-workflow" / "task-cards" / "2026-06-28-add-payment-checkout-05-security-engineer.md"
    risk_card = project / ".agent-workflow" / "task-cards" / "2026-06-28-add-payment-checkout-10-risk-reviewer.md"

    spec_text = spec.read_text(encoding="utf-8")
    security_card_text = security_card.read_text(encoding="utf-8")
    risk_card_text = risk_card.read_text(encoding="utf-8")

    assert "## 风险等级\nL3" in spec_text
    assert "自动风险评分" in spec_text
    assert "## 角色\n⑤安全工程师" in security_card_text
    assert "codex-security:security-diff-scan" in security_card_text
    assert "## 角色\n⑩风险审查官" in risk_card_text
    assert "codex-security:threat-model" in risk_card_text


def test_chinese_task_titles_get_unique_ascii_stems(tmp_path: Path) -> None:
    project = copy_template(tmp_path)

    first = run_workflow(
        project,
        "new-task",
        "新增支付结账",
        "--level",
        "auto",
        "--summary",
        "新增支付结账",
        "--date",
        "2026-06-28",
    )
    second = run_workflow(
        project,
        "new-task",
        "修改登录权限",
        "--level",
        "auto",
        "--summary",
        "修改登录权限",
        "--date",
        "2026-06-28",
    )

    assert first.returncode == 0
    assert second.returncode == 0

    generated = sorted(path.name for path in (project / ".agent-workflow" / "specs").glob("2026-06-28-*.md"))
    assert len(generated) == 2
    assert generated[0] != generated[1]
    assert all(name.startswith("2026-06-28-task-") for name in generated)
