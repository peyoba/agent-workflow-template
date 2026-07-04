"""Task card, handoff, and state markdown renderers."""

from __future__ import annotations

from workflow_lib.metadata import ROLE_DEFINITIONS, ROLE_SETS


def skill_source(skill: str) -> str:
    if skill.startswith("codex-security:"):
        return skill
    return f"superpowers:{skill} 或同名本地 skill"


def render_task_card(title: str, level: str, role: str, spec_path: str) -> str:
    definition = ROLE_DEFINITIONS[role]
    skill_lines = "\n".join(f"- `{skill}`" for skill in definition.skills)
    skill_table = "\n".join(
        f"| `{skill}` | AVAILABLE_NOT_READ | {skill_source(skill)} | 启动 {role} 前必须确认并读取 |"
        for skill in definition.skills
    )

    return f"""# {title} {role} 任务卡

## 角色
{role}

## 任务等级
{level}

## 当前 Hook
{definition.hook}

## 必加载 Skill
{skill_lines}

## Skill 加载说明
| Skill | 状态 | 来源 | 说明 |
|-------|------|------|------|
{skill_table}

## 角色说明文档
`{definition.doc}`

## 输入
- SPEC：`{spec_path}`
- 相关文件：由主 Agent 在 intake_hook 中补充。
- 前置产出：由主 Agent 按 hook 顺序补充。

## 允许触碰文件
- 由主 Agent 在实施计划中补充。

## 禁止事项
- 未确认 SPEC 前不得进入实现。
- 未更新 `.agent-workflow/state.md` 前不得进入下一个 hook。
- 不得跳过当前等级要求的质量门。

## 预期产出
- SPEC 确认记录。
- 对应角色交接记录。
- 验证记录。
- 交付报告。

## 验证命令
```bash
读取 PROJECT_PROFILE.md 后补充
```

## 完成标准
- 本角色按 `{definition.doc}` 完成职责。
- 输出 handoff，结论只能是 `PASS / FAIL / BLOCKED`。
"""


def render_handoff(title: str, level: str, spec_path: str, task_card_paths: list[str]) -> str:
    task_card_lines = "\n".join(f"- `{path}`" for path in task_card_paths)

    return f"""# {title} 初始交接

## 本轮角色
主 Agent

## 当前 Hook
intake_hook

## 结论
RUNNING

## 完成内容
- 创建初始 SPEC：`{spec_path}`
- 创建角色任务卡：
{task_card_lines}
- 更新工作流状态。

## 修改文件
- `{spec_path}`
{task_card_lines}
- `.agent-workflow/state.md`

## 验证结果
- 命令：待补充
- 结果：待补充

## 风险或遗留问题
- 当前任务等级为 {level}，需要先完成 SPEC 澄清。

## 建议下一步
主 Agent 读取 PROJECT_PROFILE.md，补全 SPEC 并请求用户确认。
"""


def render_state(title: str, level: str, reason: str, task_cards: dict[str, str]) -> str:
    rows = ["| 主 Agent | RUNNING | 无 | intake_hook |"]
    rows.extend(f"| {role} | READY | {task_cards[role]} | 待派发 |" for role in ROLE_SETS[level])
    role_table = "\n".join(rows)

    return f"""# Agent Workflow State

## 当前任务
{title}

## 风险等级
{level}

## 当前 Hook
intake_hook

## 当前阶段
spec

## 已派发角色
| 角色 | 状态 | 任务卡 | 产出 |
|------|------|--------|------|
{role_table}

状态只能使用：`READY / RUNNING / PASS / FAIL / BLOCKED / SKIPPED`

## 打回记录
| 时间 | 来源角色 | 打回对象 | 次数 | 原因 |
|------|----------|----------|------|------|

## 阻塞点
无

## 用户待确认
SPEC、任务范围、验收标准

## 下一步
主 Agent 补全 SPEC，说明风险等级触发原因：{reason}

## 决策记录
| 时间 | 决策 | 理由 |
|------|------|------|
"""
