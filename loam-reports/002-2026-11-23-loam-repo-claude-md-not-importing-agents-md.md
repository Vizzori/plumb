# loam problem report: loam's own repository fails its own doctor.agents-md-shadowed check

- Recorded: 2026-11-23T18:24:00Z
- Classification: project-data
- Status: open
- Repository role: docs (loam's self-model under `meta/`, run from the loam repository)
- loam version: 0.2.0-alpha.20
- Entry point: `loam doctor` (CLI), run read-only in the loam repository's `meta/`
- Side effects observed: none known

## Summary

loam's root `CLAUDE.md` points to `AGENTS.md` with a markdown link and prose ("Read AGENTS.md")
but does not import it. `loam doctor`, run against loam's own self-model, warns about exactly this:
`doctor.agents-md-shadowed`. The binary is right — the repository is the one out of line. It
matters beyond loam itself: a project that copies the CLAUDE.md shape from loam's repository, as
the project where this surfaced did, inherits the same warning and the same orientation gap.

## Expected

loam's own repository passes its own doctor without `doctor.agents-md-shadowed`: its `CLAUDE.md`
imports the orientation, for example with a line `@AGENTS.md`.

## Actual

```text
loam doctor — healthy
    ⚠ doctor.agents-md-shadowed: <home>/loam/CLAUDE.md sits in the docs repo or above it and does not import AGENTS.md. Claude Code reads AGENTS.md only when no CLAUDE.md, .claude/CLAUDE.md or CLAUDE.local.md is in the working directory or above it, so a Claude Code session here starts without loam's orientation.
```

## Minimal safe reproduction

In a checkout of the loam repository at 0.2.0-alpha.20:

```bash
cd meta && loam doctor
```

## Machine contract

Exit code 0; doctor reports `healthy` with the warning `doctor.agents-md-shadowed`, whose fix is to
add `@AGENTS.md` to the named `CLAUDE.md`. Not collected: the JSON envelope for this run.

## Doctor and status evidence

The finding above is the doctor evidence. `loam status` was not run in the loam repository.

## Files changed or write state

None; `doctor` is read-only and nothing in the loam repository was edited.

## Workaround

Add the line `@AGENTS.md` to the root `CLAUDE.md`, keeping the prose pointer if wanted.

## Missing evidence

- The `--json` envelope of the doctor run.
- Whether any of loam's own tests or release checks run `doctor` against the self-model; if they
  do, they tolerate this warning today.

## Sanitization

The home directory is replaced with `<home>`. No credentials or environment values were involved.
