from pathlib import Path

from tests.workflow_test_helpers import copy_template, run_workflow


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


def test_assess_risk_covers_l3_workflow_triggers(tmp_path: Path) -> None:
    project = copy_template(tmp_path)
    l3_tasks = [
        "调用外部服务同步客户资料",
        "新增环境变量配置",
        "修改订单状态",
        "调用搜索 API 获取结果",
        "修改 prompt 输出解析",
    ]

    for text in l3_tasks:
        result = run_workflow(project, "assess-risk", text)

        assert result.returncode == 0
        assert "Recommended level: L3" in result.stdout
