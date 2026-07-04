"""Shared workflow constants and role metadata."""

from __future__ import annotations

from dataclasses import dataclass


EXPECTED_ROLE_DOCS = [
    "00-main-agent.md",
    "01-test-engineer.md",
    "02-developer.md",
    "03-acceptance-engineer.md",
    "04-quality-engineer.md",
    "05-security-engineer.md",
    "06-performance-engineer.md",
    "07-docs-engineer.md",
    "08-integration-engineer.md",
    "09-deploy-engineer.md",
    "10-risk-reviewer.md",
]

EXPECTED_TEMPLATE_DOCS = [
    "spec.md",
    "task-card.md",
    "handoff.md",
    "review.md",
    "verification.md",
    "delivery-report.md",
]

EXPECTED_WORK_DIRS = [
    ".agent-workflow/specs",
    ".agent-workflow/task-cards",
    ".agent-workflow/handoffs",
    ".agent-workflow/reviews",
    ".agent-workflow/verification",
    ".agent-workflow/delivery",
]

EXPECTED_PLUGIN_FILES = [
    (".codex-plugin/plugin.json", "Codex plugin manifest"),
    (".claude-plugin/plugin.json", "Claude plugin manifest"),
    ("skills/agent-workflow/SKILL.md", "agent-workflow skill"),
    ("skills/agent-workflow/agents/openai.yaml", "agent-workflow Codex metadata"),
]

STATE_HEADINGS = [
    "## 当前任务",
    "## 风险等级",
    "## 当前 Hook",
    "## 当前阶段",
    "## 已派发角色",
    "## 打回记录",
    "## 阻塞点",
    "## 用户待确认",
    "## 下一步",
    "## 决策记录",
]

ROLE_SETS = {
    "L1": ["②开发工程师", "③验收工程师"],
    "L2": ["①测试工程师", "②开发工程师", "③验收工程师", "④质量工程师"],
    "L3": [
        "①测试工程师",
        "②开发工程师",
        "③验收工程师",
        "④质量工程师",
        "⑤安全工程师",
        "⑩风险审查官",
        "⑥性能工程师",
        "⑦文档工程师",
        "⑧集成工程师",
        "⑨部署工程师",
    ],
}

DEFAULT_REASON = "由主 Agent 在 intake_hook 中补充。"


@dataclass(frozen=True)
class RoleDefinition:
    slug: str
    hook: str
    doc: str
    skills: list[str]


ROLE_DEFINITIONS = {
    "①测试工程师": RoleDefinition(
        "01-test-engineer",
        "red_hook",
        ".agent-workflow/agents/01-test-engineer.md",
        ["test-driven-development", "testing-anti-patterns"],
    ),
    "②开发工程师": RoleDefinition(
        "02-developer",
        "green_hook",
        ".agent-workflow/agents/02-developer.md",
        ["test-driven-development", "systematic-debugging"],
    ),
    "③验收工程师": RoleDefinition(
        "03-acceptance-engineer",
        "acceptance_hook",
        ".agent-workflow/agents/03-acceptance-engineer.md",
        ["verification-before-completion"],
    ),
    "④质量工程师": RoleDefinition(
        "04-quality-engineer",
        "quality_gate_hook",
        ".agent-workflow/agents/04-quality-engineer.md",
        ["requesting-code-review", "receiving-code-review"],
    ),
    "⑤安全工程师": RoleDefinition(
        "05-security-engineer",
        "security_gate_hook",
        ".agent-workflow/agents/05-security-engineer.md",
        ["codex-security:security-diff-scan"],
    ),
    "⑩风险审查官": RoleDefinition(
        "10-risk-reviewer",
        "risk_gate_hook",
        ".agent-workflow/agents/10-risk-reviewer.md",
        ["codex-security:threat-model"],
    ),
    "⑥性能工程师": RoleDefinition(
        "06-performance-engineer",
        "performance_gate_hook",
        ".agent-workflow/agents/06-performance-engineer.md",
        ["root-cause-tracing"],
    ),
    "⑦文档工程师": RoleDefinition(
        "07-docs-engineer",
        "delivery_hook",
        ".agent-workflow/agents/07-docs-engineer.md",
        ["writing-skills"],
    ),
    "⑧集成工程师": RoleDefinition(
        "08-integration-engineer",
        "integration_hook",
        ".agent-workflow/agents/08-integration-engineer.md",
        ["executing-plans", "verification-before-completion"],
    ),
    "⑨部署工程师": RoleDefinition(
        "09-deploy-engineer",
        "delivery_hook",
        ".agent-workflow/agents/09-deploy-engineer.md",
        ["finishing-a-development-branch"],
    ),
}
