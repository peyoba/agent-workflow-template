"""Risk assessment for workflow task levels."""

from __future__ import annotations

import argparse
from dataclasses import dataclass


@dataclass(frozen=True)
class RiskAssessment:
    level: str
    reasons: list[str]


RISK_RULES = [
    (
        "L3",
        "security",
        [
            "security",
            "auth",
            "login",
            "permission",
            "role",
            "admin",
            "administrator",
            "oauth",
            "jwt",
            "session",
            "安全",
            "登录",
            "权限",
            "管理员",
            "会话",
            "认证",
        ],
    ),
    (
        "L3",
        "payment",
        [
            "payment",
            "checkout",
            "billing",
            "invoice",
            "subscription",
            "stripe",
            "refund",
            "order status",
            "transaction",
            "支付",
            "结账",
            "账单",
            "订阅",
            "退款",
            "订单状态",
            "订单",
            "交易",
        ],
    ),
    (
        "L3",
        "api key",
        [
            "api key",
            "apikey",
            "secret",
            "token",
            "credential",
            "password",
            ".env",
            "env var",
            "environment variable",
            "密钥",
            "令牌",
            "凭证",
            "密码",
            "环境变量",
        ],
    ),
    (
        "L3",
        "database",
        ["database", "migration", "schema", "sql", "delete", "write", "db", "数据库", "迁移", "数据表", "删除", "写入", "保存"],
    ),
    (
        "L3",
        "deployment",
        ["deploy", "deployment", "production", "ci/cd", "release", "rollback", "部署", "生产", "发布", "回滚"],
    ),
    (
        "L3",
        "external api",
        [
            "webhook",
            "callback",
            "external api",
            "external service",
            "third-party",
            "llm",
            "openai",
            "anthropic",
            "ark",
            "search api",
            "prompt",
            "crawler",
            "web scrape",
            "外部 api",
            "外部服务",
            "第三方",
            "大模型",
            "搜索 api",
            "搜索",
            "prompt",
            "提示词",
            "爬虫",
            "回调",
        ],
    ),
    (
        "L2",
        "core behavior",
        ["feature", "workflow", "refactor", "api", "cli", "integration", "state", "功能", "工作流", "重构", "集成", "状态"],
    ),
    (
        "L2",
        "data handling",
        ["cache", "file", "upload", "download", "import", "export", "report", "缓存", "文件", "上传", "下载", "导入", "导出", "报告"],
    ),
    (
        "L2",
        "test impact",
        ["bug", "fix", "test", "validation", "parser", "error handling", "修复", "测试", "校验", "解析", "错误处理"],
    ),
]


def assess_risk(text: str) -> RiskAssessment:
    normalized = text.lower()
    matched_levels: list[str] = []
    reasons: list[str] = []

    for level, reason, keywords in RISK_RULES:
        if any(keyword in normalized for keyword in keywords):
            matched_levels.append(level)
            reasons.append(reason)

    if "L3" in matched_levels:
        return RiskAssessment("L3", sorted(set(reasons)))
    if "L2" in matched_levels:
        return RiskAssessment("L2", sorted(set(reasons)))
    return RiskAssessment("L1", ["small scoped change"])


def format_assessment_reason(assessment: RiskAssessment) -> str:
    return "自动风险评分：{}。".format(", ".join(assessment.reasons))


def run_assess_risk(args: argparse.Namespace) -> int:
    assessment = assess_risk(args.text)
    print(f"Recommended level: {assessment.level}")
    print("Reasons:")
    for reason in assessment.reasons:
        print(f"- {reason}")
    return 0
