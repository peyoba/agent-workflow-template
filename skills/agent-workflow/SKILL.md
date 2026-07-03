---
name: agent-workflow
description: Install or run a lightweight multi-agent engineering workflow for software projects. Use when Codex, Claude Code, or another coding agent is asked to install Agent Workflow, add reusable AGENTS.md workflow rules, start a new task with intake/risk classification/spec/task-card handoffs, enforce TDD and verification gates, or package a project with .agent-workflow templates and scripts/workflow.py.
---

# Agent Workflow

Use this skill to install or operate the Agent Workflow template in a software project.

## Quick Start

1. Read the target project's existing `AGENTS.md`, `Agent.md`, README, package files, and current task request.
2. If the project does not have Agent Workflow installed, copy the template files listed in `README.md` and `QUICKSTART.md` without overwriting existing user files.
3. Run `python3 scripts/workflow.py doctor` from the target project root.
4. If `PROJECT_PROFILE.md` still contains placeholders, infer safe values from local project files and ask about anything that cannot be determined.
5. Start work from `.agent-workflow/WORKFLOW.md`, `.agent-workflow/SKILLS.md`, `.agent-workflow/STATE_RULES.md`, and `.agent-workflow/state.md`.

## Required Files

An installed project should include:

- `AGENTS.md` or `Agent.md`
- `PROJECT_PROFILE.md`
- `.agent-workflow/WORKFLOW.md`
- `.agent-workflow/SKILLS.md`
- `.agent-workflow/STATE_RULES.md`
- `.agent-workflow/state.md`
- `.agent-workflow/agents/`
- `.agent-workflow/templates/`
- `scripts/workflow.py`

## Task Flow

For new feature work, bug fixes, and refactors:

1. Execute the Superpowers bootstrap described in `INSTALL_SUPERPOWERS.md`.
2. Run intake and risk classification before implementation.
3. Generate or update the SPEC and task card.
4. Wait for user confirmation of scope and tasks before editing code.
5. Use test-driven development for implementation.
6. Record handoffs, verification evidence, and delivery report paths under `.agent-workflow/`.

Use `python3 scripts/workflow.py assess-risk "<task>"` to recommend `L1`, `L2`, or `L3`.
Use `python3 scripts/workflow.py new-task "<title>" --level auto --summary "<summary>"` to create initial workflow artifacts.

## Safety Rules

- Do not overwrite an existing `AGENTS.md`, `Agent.md`, `.agent-workflow/`, `scripts/`, or `tests/` path without showing the conflict and getting confirmation.
- Do not enter implementation before SPEC and task list confirmation unless the user explicitly overrides the workflow.
- Do not claim completion until verification commands have been run and their output has been read.
- Treat login, permissions, payments, database writes, secrets, external APIs, prompts, deployment, and production changes as at least `L3`.
