"""SPEC markdown renderer."""

from __future__ import annotations


def render_spec(title: str, level: str, reason: str, summary: str) -> str:
    return f"""# {title} SPEC

## 背景
{summary}

## 目标
由主 Agent 在 intake_hook 中补充可验证目标。

## 非目标
由主 Agent 在 intake_hook 中补充明确不做的内容。

## 用户路径 / 调用路径
由主 Agent 在 intake_hook 中补充用户操作路径或系统调用路径。

## 功能要求
- 由主 Agent 在 intake_hook 中拆解需求。

## 边界情况
- 空输入：由主 Agent 补充。
- 非法输入：由主 Agent 补充。
- 重复输入：由主 Agent 补充。
- 外部服务失败：由主 Agent 补充。

## 技术选择
- 语言/框架：读取 PROJECT_PROFILE.md 后确认。
- 测试：读取 PROJECT_PROFILE.md 后确认。
- 包管理：读取 PROJECT_PROFILE.md 后确认。
- 数据库：读取 PROJECT_PROFILE.md 后确认。
- 部署：读取 PROJECT_PROFILE.md 后确认。

## 文件边界
- 允许修改：由主 Agent 在实施计划中列出具体路径。
- 禁止修改：由主 Agent 在实施计划中列出配置、密钥、迁移或用户文件边界。
- 需要先读取：PROJECT_PROFILE.md、相关源码、相关测试、当前状态文件。

## 依赖关系
- 前置任务：无，或由主 Agent 补充。
- 依赖模块：由主 Agent 根据代码结构补充。
- 可并行任务：由主 Agent 判断，只有互不共享文件的任务才可并行。

## 任务拆分判断
- 是否需要拆分：由主 Agent 判断。
- 拆分理由：如果跨多个子系统、跨前后端、跨数据模型和部署，应拆成多个 SPEC。

## 风险等级
{level}

## 触发原因
{reason}

## 验收标准
- SPEC 经用户确认。
- 任务卡已派发给 {level} 对应角色。
- 完成前写入真实验证记录和交付报告。

## 验收证据
- 必须记录实际运行的测试、构建、lint 或人工验证命令。
- 必须记录命令结果摘要。
- 未验证项必须明确列出，不得用“应该可以”代替证据。
"""
