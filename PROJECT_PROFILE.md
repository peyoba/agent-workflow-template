# Project Profile

本文件记录当前仓库自身的技术栈、命令、环境变量和运行约定。安装到用户项目时，应把 `PROJECT_PROFILE.template.md` 复制为目标项目的 `PROJECT_PROFILE.md`，再按目标项目实际情况补全。

## 1. 项目基本信息

| 项目 | 内容 |
|------|------|
| 项目名称 | Agent Workflow Template |
| 项目类型 | CLI / Template / Plugin package |
| 主要语言 | Python |
| 主要框架 | Python standard library CLI with pytest tests |
| 运行环境 | Python 3.9+ on local filesystem |

## 2. 包管理器

| 项目 | 内容 |
|------|------|
| 包管理器 | none |
| 安装命令 | `无` |
| 锁文件 | `无` |

## 3. 常用命令

| 用途 | 命令 | 备注 |
|------|------|------|
| 安装依赖 | `无` | 使用系统 Python 和已安装 pytest |
| 启动开发服务 | `无` | 本项目没有常驻服务 |
| 运行测试 | `python3 -m pytest tests -v` | 全量测试 |
| 运行单个测试 | `python3 -m pytest tests/test_doctor.py -v` | 按需替换测试文件 |
| Lint | `无` | 当前未配置独立 lint |
| Typecheck | `无` | 当前未配置类型检查 |
| Build | `无` | 本项目无需构建 |
| Format | `无` | 当前未配置格式化命令 |

## 4. 目录结构

| 路径 | 说明 |
|------|------|
| `.agent-workflow/` | 工作流规则、角色、模板、示例和状态文件 |
| `scripts/` | 本地 CLI 入口和 workflow 库 |
| `scripts/workflow_lib/` | doctor、风险评估、任务生成和渲染逻辑 |
| `tests/` | pytest 测试 |
| `skills/` | agent-workflow Skill 包 |
| `.codex-plugin/` | Codex 插件 manifest |
| `.claude-plugin/` | Claude Code 插件 manifest |

## 5. 环境变量

当前仓库不要求环境变量。测试和 doctor 不需要 API key、token 或外部服务凭证。

## 6. 本地环境文件

当前仓库不要求 `.env`。不要把用户项目的密钥、token 或本地私有配置写入本仓库。

## 7. 测试策略

- 单元测试命令：`python3 -m pytest tests -v`
- 集成测试命令：`python3 scripts/workflow.py doctor --mode template`
- E2E 测试命令：`无`
- 真实验证命令：`python3 scripts/workflow.py doctor --mode installed`
- 允许 mock 的范围：文件系统临时目录、HOME 路径和复制出的模板项目。
- 必须真实验证的路径：CLI 参数解析、模板完整性、installed/template doctor 模式、任务产物生成、风险分级。

## 8. 部署信息

| 项目 | 内容 |
|------|------|
| 部署方式 | Repository or plugin installation |
| CI/CD | Not configured in this repository |
| 生产环境入口 | None; this is a local workflow template and CLI |
| 回滚方式 | Git revert or restore the installed template files from source |

## 9. 项目约束

- 禁止事项：不要引入运行时服务、后台调度器、数据库或网络依赖来完成当前轻量模板目标。
- 代码风格：优先小模块、清晰命名、标准库实现；Python 代码文件默认不超过 200 行。
- 依赖引入规则：新增依赖必须先说明必要性并获得确认。
- 安全要求：不得写入真实 API key、token、用户私有数据或伪造验证结果。
- 性能要求：CLI 应保持本地快速执行，doctor 不应访问网络。

## 10. 主 Agent 启动要求

主 Agent 在执行本仓库开发前必须：

1. 读取本文件、`DECISIONS.md`、`AGENTS.md` 和 `.agent-workflow/state.md`。
2. 使用适用的 Superpowers skill，涉及实现时先写测试。
3. 改动前说明将编辑哪些文件、原因、依赖影响和验证方式。
4. 完成前运行相关 pytest、compileall、doctor 和 diff 检查。
