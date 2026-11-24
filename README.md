# plumb

**Advisory pull request review that stays silent unless it is sure — and gets better from what
reviewers do with its comments.**

plumb is part of the Vizzori family: [loam](https://github.com/ybotok/loam) is the ground —
architecture and requirements as checked files — and plumb is the plumb line that checks what is
built on it.

> **Status: requirements only.** No code yet. The first feature, FEAT-1, is written and passes
> `loam validate`; nothing is implemented, verified or archived.

## What plumb is for

Most AI reviewers post a lot and are acted on rarely: in open-source review bots, code changed after
only 0.9–19.2% of valid AI comments, against 60% of human ones. plumb is built around what the
evidence says works:

- **Few comments, each one verified.** A finding names the changed lines, a concrete failure
  scenario and the evidence an independent verification step checked. No praise, no walkthroughs,
  no style nits unless the team asks for them.
- **No repeats.** Each push is reviewed incrementally; a finding already made, resolved or
  dismissed never comes back.
- **Advice, not a gate.** plumb never approves, blocks or merges, and a review that did not happen
  is never shown as a clean one.
- **A core with a contract.** plumb runs as a daemon with an API. An integrator — a CI job, a bot,
  a platform app — sends it the code and whatever requirements exist, from a tracker ticket to a
  loam or OpenSpec feature, and shows its results. plumb knows no code host, follows no link and
  publishes nothing; its only way out is the model gateway.
- **Each project's own rules.** Rules come in layers — built-in core, organization packs, project,
  path scopes, learned rules — and a convention such as value objects versus thin DTOs is checked
  only where a project declared it.
- **Self-improving, with proof.** plumb records what happened to every finding, turns repeated,
  similar dismissals into rules that can only quiet it down — after a critic, a replay and shadow
  mode — reports its addressed rate next to the human baseline, and adopts a new way of reviewing
  only after a replay on stored requests shows it is no worse.

## Repository layout

| Path | What it holds |
|---|---|
| [`loam-docs/`](loam-docs/) | Requirements and architecture, governed by loam |
| [`loam-docs/features/FEAT-1-precise-advisory-pull-request-review/`](loam-docs/features/FEAT-1-precise-advisory-pull-request-review/) | FEAT-1: intent with its decisions, the C4 delta (seven bounded contexts), the API contract (OpenAPI, 15 operations), 40 requirements, 18 architecture obligations, five flows |
| [`research/`](research/) | The November 2026 research on open-source AI code review the requirements rest on: the report (in Russian) and six topic notes |
| `.claude/` | loam's slash commands and Agent Skills, and plumb's own architecture skills, agents and boundary check |
| `loam.json` | Binds this repository to the service id `plumb` |

## Working with the requirements

Requires Node.js 22.22.3 or newer and the `loam` CLI on `PATH` (or `npx loam` once it is a
devDependency).

```bash
loam status            # what is in flight and what is owed
loam validate --all    # the gate CI runs
loam show FEAT-1       # the feature, joined for review
python3 .claude/skills/architecture-boundaries/scripts/check-boundaries.py   # needs the LikeC4 CLI
```

In Claude Code the lifecycle runs through `/loam-feature`, `/loam-implement FEAT-1 plumb`,
`/loam-check FEAT-1`, `/loam-verify FEAT-1` and `/loam-ship FEAT-1`.

Start a review of FEAT-1 with its [intent](loam-docs/features/FEAT-1-precise-advisory-pull-request-review/intent.md):
its decisions table records what was settled and why, and one question — the implementation
language — is still open.

To look at the architecture, start the LikeC4 preview of the feature's delta (from this repository's
root, with LikeC4 installed):

```bash
npx likec4 start loam-docs/features/FEAT-1-precise-advisory-pull-request-review
```

## License

[MIT](LICENSE).
