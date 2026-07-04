#!/usr/bin/env python3
"""CLI helpers for the reusable agent workflow template."""

from __future__ import annotations

import argparse
import sys
from datetime import date
from pathlib import Path

from workflow_lib.doctor import run_doctor
from workflow_lib.metadata import DEFAULT_REASON
from workflow_lib.risk import run_assess_risk
from workflow_lib.tasks import run_new_task


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="workflow",
        description="Agent workflow helper commands.",
    )
    subcommands = parser.add_subparsers(dest="command", required=True)

    doctor = subcommands.add_parser("doctor", help="Check workflow template wiring.")
    doctor.add_argument("--project-root", default=".", help="Project root to inspect.")
    doctor.add_argument(
        "--mode",
        choices=["auto", "template", "installed"],
        default="auto",
        help="Check template package files or installed-project workflow files.",
    )

    new_task = subcommands.add_parser("new-task", help="Create task workflow artifacts.")
    new_task.add_argument("title", help="Task title.")
    new_task.add_argument("--level", choices=["auto", "L1", "L2", "L3"], default="L2")
    new_task.add_argument("--reason", default=DEFAULT_REASON)
    new_task.add_argument("--summary", default="由主 Agent 在 intake_hook 中补充。")
    new_task.add_argument("--date", default=date.today().isoformat())
    new_task.add_argument("--project-root", default=".", help="Project root to modify.")
    new_task.add_argument("--force", action="store_true", help="Overwrite existing generated files.")
    new_task.add_argument(
        "--allow-downgrade",
        action="store_true",
        help="Allow an explicit L1/L2 level even when risk assessment recommends L3.",
    )

    assess_risk = subcommands.add_parser("assess-risk", help="Recommend L1/L2/L3 from task text.")
    assess_risk.add_argument("text", help="Task description to assess.")
    assess_risk.add_argument("--project-root", default=".", help="Project root, accepted for CLI consistency.")

    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    if args.command == "doctor":
        return run_doctor(Path(args.project_root).resolve(), args.mode)
    if args.command == "assess-risk":
        return run_assess_risk(args)
    if args.command == "new-task":
        return run_new_task(args)
    raise ValueError(f"Unsupported command: {args.command}")


if __name__ == "__main__":
    raise SystemExit(main())
