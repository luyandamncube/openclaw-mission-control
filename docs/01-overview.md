# Overview

Mission Control is the **web UI + HTTP API** for operating OpenClaw.

It’s where you manage **boards**, **tasks**, **agents**, **approvals**, and (optionally) **gateway connections**.

## Problem statement

OpenClaw can execute work (tools/skills) and converse across channels, but real operations need a place to:

- **Coordinate** work across people + agents (what’s next, what’s blocked, who owns what)
- **Track evidence** of what happened (commands run, links, logs, artifacts)
- **Control risk** (approvals, guardrails, isolation)
- **Operate reliably** (deployment, configuration, troubleshooting)

Mission Control provides that control plane.

## Who uses it

- **Maintainers / operators**: keep Mission Control + gateways healthy, deploy upgrades, respond to incidents.
- **Contributors**: develop backend/frontend changes, run tests, ship docs.
- **Automation authors**: define agent identities, skills, and task workflows.

## Key concepts (glossary-lite)

- **Board**: a workspace containing tasks, memory, and agents.
- **Task**: a unit of work on a board (status + comments/evidence).
- **Agent**: an automated worker that can execute tasks and post evidence.
- **Approval**: a structured “allow/deny” checkpoint for risky actions.
- **Gateway**: the OpenClaw runtime host that executes tools/skills and runs heartbeats/cron.
- **Heartbeat**: periodic agent check-in loop for incremental work.
- **Cron job**: scheduled execution (recurring or one-shot), often isolated from conversational context.

## Out of scope

- Not a general-purpose project management suite (we optimize for AI-assisted operations, not every PM feature).
- Not a full observability platform (we integrate with logs/metrics rather than replacing them).
- Not a secrets manager (we reference secret sources; don’t store secrets in docs/tasks/comments).

## Where to go next

- Want it running? → [Quickstart](02-quickstart.md)
- Want to contribute? → [Development](03-development.md)
- Want to understand internals? → [Architecture](05-architecture.md)
- Operating it? → [Ops / runbooks](09-ops-runbooks.md)
