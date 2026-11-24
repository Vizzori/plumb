# Working in the plumb repository

plumb is an advisory pull request reviewer. Its requirements and architecture live in
[`loam-docs/`](loam-docs/) and are governed by loam; [`loam-docs/AGENTS.md`](loam-docs/AGENTS.md)
is the protocol for that directory and wins wherever this file is silent. This file holds only the
rules for every task; details live in skills and agents.

## Workflow

- **Resume with `loam status --json`.** Its ordered `next[]` is the work queue.
- **Requirements change only through a feature** (`/loam-feature`), never by editing living
  documents by hand. FEAT-1 introduces the `plumb` service; until it archives, its
  `specs/plumb/` files are the service's documents.
- **Design before code.** Form the testable design skeleton (`testable-design-skeleton`, or the
  `service-designer` agent) before implementing non-trivial logic.
- **Build with `/loam-implement FEAT-1 plumb`**, one task at a time, and record evidence with
  `/loam-verify FEAT-1`. Archive only after the code is merged.
- **Never run `loam vouch`.** Vouching is a person's act.
- **Open questions are the owner's.** FEAT-1's intent.md lists them with the default that gets
  built if nobody answers; do not answer them on the owner's behalf.
- **Background is in [`research/`](research/)**: why each requirement exists, with sources.

## Architecture guardrails

plumb is one daemon made of bounded contexts: Intake, Archive, Review engine, Rule registry,
Outcomes, Tuning and Model gateway (`architecture-boundaries` has the rules and the check).

- A context owns its store; only its own repository touches it. There is no shared database.
- A context is entered only through its port and left only through its own client for each
  dependency. Context dependencies point one way; a new cycle is a question for the user.
- The model provider is reached only through the Model gateway, and every model request names
  its step, provider, model and connection profile. Provider credentials never leave the
  gateway's provider adapters and never appear in logs, errors or results.
- Intake parses, validates, records and dispatches; it holds no store and no business rule.
- Domain code is free of transport and persistence types; identities and domain values are
  typed value objects or tiny types. No generic `*Service`, `*Manager`, `*Util` or `*Helper`.
- Every C4 element and relationship has a concrete description (`documentation-writing`).

Before any architecture change is accepted, run:

```bash
python3 .claude/skills/architecture-boundaries/scripts/check-boundaries.py   # LikeC4 on PATH or LIKEC4_BIN
loam validate --feature FEAT-1
```

## Skills and agents

| Need | Use |
|---|---|
| Change the C4 model, add a context, a store or a dependency | skill `architecture-boundaries` |
| Design a change before code | skill `testable-design-skeleton`, agent `service-designer` |
| Write or edit loam documents | skill `documentation-writing` |
| Make an implicit safety rule explicit and testable | agent `invariant-architect` |
| Independent check of the design before it is accepted | agent `architecture-validator` (read-only) |
| Anything in the loam lifecycle | the `/loam-*` commands and skills |

Every `loam` command assumes the binary is on `PATH`; where the repository installs it as a
devDependency, run `npx loam …` instead.
