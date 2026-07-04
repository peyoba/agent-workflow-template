# Project Profile

本文件记录当前项目的技术栈、命令、环境变量和运行约定。主 Agent 启动工作流时必须读取本文件，避免每次重新猜测项目配置。

## 1. 项目基本信息

| 项目 | 内容 |
|------|------|
| 项目名称 | [填写项目名称] |
| 项目类型 | [Web / API / CLI / Mobile / Desktop / Library / Other] |
| 主要语言 | [例如 TypeScript / Python / Swift / Go] |
| 主要框架 | [例如 Next.js / FastAPI / React / Django] |
| 运行环境 | [Node / Python / Docker / Browser / macOS / Cloud] |

## 2. 包管理器

| 项目 | 内容 |
|------|------|
| 包管理器 | [pnpm / npm / yarn / uv / pip / poetry / cargo / go / other] |
| 安装命令 | `[填写命令]` |
| 锁文件 | [pnpm-lock.yaml / package-lock.json / uv.lock / poetry.lock / other] |

## 3. 常用命令

| 用途 | 命令 | 备注 |
|------|------|------|
| 安装依赖 | `[命令]` | |
| 启动开发服务 | `[命令]` | |
| 运行测试 | `[命令]` | |
| 运行单个测试 | `[命令模板]` | |
| Lint | `[命令]` | 没有则写“无” |
| Typecheck | `[命令]` | 没有则写“无” |
| Build | `[命令]` | |
| Format | `[命令]` | 没有则写“无” |

## 4. 目录结构

| 路径 | 说明 |
|------|------|
| `src/` | [说明] |
| `tests/` | [说明] |
| `docs/` | [说明] |
| `scripts/` | [说明] |

## 5. 环境变量

| 变量名 | 用途 | 是否敏感 | 来源 |
|--------|------|----------|------|
| `[VAR_NAME]` | [用途] | 是/否 | `.env` / CI / Secret Manager |

## 6. 本地环境文件

| 文件 | 用途 | 是否可提交 |
|------|------|------------|
| `.env` | 本地密钥 | 否 |
| `.env.example` | 示例配置 | 是 |

## 7. 测试策略

- 单元测试命令：
- 集成测试命令：
- E2E 测试命令：
- 真实验证命令：
- 哪些测试允许 mock：
- 哪些路径必须真实验证：

## 8. 部署信息

| 项目 | 内容 |
|------|------|
| 部署方式 | [Vercel / Docker / Kubernetes / VPS / Manual / Other] |
| CI/CD | [GitHub Actions / CircleCI / None / Other] |
| 生产环境入口 | [URL 或说明] |
| 回滚方式 | [说明] |

## 9. 项目约束

- 禁止事项：
- 代码风格：
- 依赖引入规则：
- 安全要求：
- 性能要求：

## 10. 主 Agent 启动要求

主 Agent 在执行 `intake_hook` 前必须：

1. 读取本文件。
2. 如果本文件存在 `[填写]` 或明显空缺，先通过项目文件推断。
3. 推断失败时询问用户。
4. 不得在未知测试命令、构建命令或包管理器时直接进入开发。
