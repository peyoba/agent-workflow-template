# Agent Workflow Template

一个可复制到任意开发项目的多子 Agent 工程工作流模板。

它把 AI 代码协作拆成主 Agent、测试工程师、开发工程师、验收工程师、质量工程师、安全工程师、性能工程师、文档工程师、集成工程师、部署工程师和风险审查官等角色，并通过 L1 / L2 / L3 分级控制实际启用范围。

## 定位

本项目刻意保持轻量：

- 比单个 `AGENTS.md` 更完整：包含角色、hook、状态、任务卡、验证和交付模板。
- 比重型多 Agent 平台更轻：没有后台服务、dashboard、MCP 编排器或知识图谱。
- 适合真实项目：强调 SPEC 边界、风险分级、TDD、证据门和交付记录。

## 快速使用

复制以下内容到目标项目根目录：

```text
AGENTS.md
Agent.md
.agent-workflow/
scripts/
tests/
PROJECT_PROFILE.md
QUICKSTART.md
INSTALL_SUPERPOWERS.md
```

检查接入状态：

```bash
python3 scripts/workflow.py doctor
```

评估任务风险等级：

```bash
python3 scripts/workflow.py assess-risk "Add payment checkout with API keys"
```

初始化一个新任务：

```bash
python3 scripts/workflow.py new-task "Add user login" \
  --level L2 \
  --reason "Touches authentication and user sessions."
```

也可以让 CLI 自动建议等级：

```bash
python3 scripts/workflow.py new-task "Add payment checkout" \
  --level auto \
  --summary "Add payment checkout with API keys and production deployment."
```

然后让主 Agent 读取 `AGENTS.md`、`PROJECT_PROFILE.md` 和 `.agent-workflow/state.md`，从 `intake_hook` 开始推进。

## 核心文件

- `Agent.md` / `AGENTS.md`：项目级 Agent 入口规则。
- `.agent-workflow/WORKFLOW.md`：完整工作流。
- `.agent-workflow/SKILLS.md`：Skill 加载约定。
- `.agent-workflow/STATE_RULES.md`：状态推进规则。
- `.agent-workflow/agents/`：各子 Agent 职责文档。
- `.agent-workflow/templates/`：SPEC、任务卡、交接、审查、验证和交付模板。
- `scripts/workflow.py`：本地 CLI，包含 `doctor` 和 `new-task`。
- `PROJECT_PROFILE.md`：目标项目技术栈、命令、环境变量和约束。

## 给 Agent 的安装提示

在目标项目根目录打开 coding agent，直接粘贴：

```text
请把 https://github.com/peyoba/agent-workflow-template 安装到当前项目。

要求：
1. 复制 AGENTS.md、Agent.md、PROJECT_PROFILE.md、QUICKSTART.md、INSTALL_SUPERPOWERS.md、.agent-workflow/、scripts/ 和 tests/。
2. 如果目标项目已经有 AGENTS.md、Agent.md 或 .agent-workflow/，不要覆盖，先展示差异并等待确认。
3. 安装后运行 python3 scripts/workflow.py doctor。
4. 如果 PROJECT_PROFILE.md 仍有占位符，先根据项目文件补全；无法确认的再问我。
```

## 任务等级

- `L1`：小改动，启用开发工程师和验收工程师。
- `L2`：常规功能，启用测试、开发、验收和质量工程师。
- `L3`：高风险任务，在 L2 基础上加入安全、风险、性能、文档、集成和部署角色。

风险分级是质量门选择，不是团队人数。大多数任务应落在 L1 或 L2；只有涉及安全、支付、密钥、数据库、外部 API、部署或生产风险时才进入 L3。

## 验证

```bash
python3 -m pytest tests/test_workflow_cli.py -v
python3 scripts/workflow.py doctor
```
