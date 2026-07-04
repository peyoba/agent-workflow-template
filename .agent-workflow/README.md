# .agent-workflow

本目录保存 Agent Workflow 的项目内执行协议、角色说明、状态文件和产物模板。

普通业务项目安装时，需要复制本目录中的运行文件和空产物目录：

```text
.agent-workflow/
  WORKFLOW.md
  SKILLS.md
  STATE_RULES.md
  state.md
  agents/
  specs/
  task-cards/
  handoffs/
  reviews/
  verification/
  delivery/
  templates/
```

启动开发时，主 Agent 必须读取：

- 根目录 `AGENTS.md` 或 `Agent.md`
- 根目录 `PROJECT_PROFILE.md`
- `.agent-workflow/WORKFLOW.md`
- `.agent-workflow/SKILLS.md`
- `.agent-workflow/STATE_RULES.md`
- `.agent-workflow/state.md`
- `.agent-workflow/agents/00-main-agent.md`

运行过程中，SPEC、任务卡、交接报告、审查报告、验证记录和交付报告应写入对应目录。

模板仓库中的示例目录只用于维护和测试本模板，普通业务项目安装时不需要复制。
