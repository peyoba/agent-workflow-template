from pathlib import Path

from tests.workflow_test_helpers import REPO_ROOT


def section_value(markdown: str, heading: str) -> str:
    marker = f"## {heading}"
    start = markdown.index(marker) + len(marker)
    rest = markdown[start:].strip()
    next_heading = rest.find("\n## ")
    if next_heading == -1:
        return rest.strip()
    return rest[:next_heading].strip()


def test_l3_real_verification_examples_match_template_gate() -> None:
    example_paths = sorted((REPO_ROOT / ".agent-workflow" / "examples").glob("*/08-verification*.md"))
    assert example_paths

    for path in example_paths:
        markdown = path.read_text(encoding="utf-8")

        assert "## 证据门" in markdown, path
        assert "| 检查项 | 命令或证据 | 结果 |" in markdown, path
        assert "## 未验证项" in markdown, path
        assert section_value(markdown, "结论") in {"PASS", "FAIL", "BLOCKED"}, path
