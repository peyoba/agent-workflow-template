"""Path helpers for workflow commands."""

from pathlib import Path


def relative(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()
