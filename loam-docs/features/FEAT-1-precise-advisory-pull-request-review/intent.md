---
feature: FEAT-1
title: Precise advisory pull request review
status: proposed
owner: ybotok
---

# Precise advisory pull request review

## Why

AI review bots were meant to take load off human reviewers. In practice most of them add to it.
The research behind plumb ([open-source AI code review, November 2026](../../../research/2026-11-23-oss-ai-code-review.md))
found the same picture across tools:

- **Their comments are mostly ignored.** Across 16 open-source review GitHub Actions in 178
  repositories, code changed after only 0.9–19.2% of valid AI comments, against 60% of human ones
  (arXiv 2508.18771). On the SWR-Bench benchmark of real pull requests the best approach scores an
  F1 of about 19%.
- **The same complaints recur in every tracker:** the whole diff re-reviewed on every push,
  duplicate comments, comments on the wrong lines, green checks with no review behind them,
  breakage when a model changes, and no memory of what a team already rejected.
- **What works is the machinery around the model, not the model.** Uber, ByteDance, Atlassian and
  Greptile reached 40–75% of comments addressed only by verifying findings, suppressing what nobody
  acts on, deduplicating across pushes and filtering with what developers actually did (Greptile:
  19% to 55% addressed). Rules matter as much: without its 219-rule taxonomy, ByteDance's precision
  fell from 57% to 17%. Filters trained on real outcomes are the one lever almost no open-source
  tool has.
- **A reviewer is an attack surface.** Crafted pull request text made AI reviewers miss
  re-introduced vulnerabilities in 32 of 33 attempts (arXiv 2603.18740), and a hosted reviewer that
  ran a repository's linter configuration exposed a key with write access to about a million
  repositories.

Teams also differ: one models domain data with value objects, another with thin data transfer
objects (DTOs); one keeps requirements in loam, another in OpenSpec, a knowledge base or a single
tracker ticket. A reviewer that hard-codes one practice is wrong for everyone else.

plumb exists to be the reviewer those findings describe, and nothing more: a review core with a
contract. It returns few findings, each verified and placed on the line it discusses; reviews by
the rules each project registered; never repeats itself; never decides; cannot be steered by what
it reads; and becomes measurably better over time, adopting a change to how it reviews only when a
replay on stored requests proves it.

## Scope

One new service, **plumb**: a daemon made of seven bounded contexts — Intake (the contract edge,
which keeps nothing), Archive, Review engine, Rule registry, Outcomes, Tuning (started only by its
own scheduler) and Model gateway. Each owns its store, is entered only through its port and left
only through its own client for each dependency; the model provider is reached only through the
Model gateway. Its boundary is the
contract in
[specs/plumb/openapi.yaml](specs/plumb/openapi.yaml): review and audit requests in, results out,
feedback in, rules and the report for maintainers.

Deliberately out of scope, because they belong to whoever integrates plumb:

- Talking to code hosts — GitHub, GitLab, Bitbucket, Gerrit — and publishing anything there.
- Gathering context: following links, reading trackers, knowledge bases or specification tools.
- Deciding which human roles exist; plumb takes the role the integrator states.
- Scheduling: nightly audits are requests the integrator sends.
- A user interface, a CLI client, and committing fixes on anyone's behalf.

Also out of scope: running the code under review — builds, tests or its linters — and blocking,
approving or merging anything.

## How to read this feature

One new service, plumb. Read [specs/plumb/spec.md](specs/plumb/spec.md) first — what an
integrator and a maintainer get from plumb — then [specs/plumb/openapi.yaml](specs/plumb/openapi.yaml),
the contract, and [specs/plumb/arch.spec.md](specs/plumb/arch.spec.md), the obligations that keep it
safe and honest. The pictures are the views in [delta.likec4](delta.likec4): `feat_1` shows who
talks to plumb, `feat_1_plumb` the seven contexts with the stores each one owns, and one view per
context shows its inside. Five flows under [specs/plumb/usecases/](specs/plumb/usecases/)
walk through them step by step: a review of one revision, feedback becoming outcomes, a disputed
finding, an escalation that starts an area audit, and a learned rule earning its place.

## Business requirements and what keeps them

| Business requirement | Kept by | Where |
|---|---|---|
| plumb works with any integration and any requirements practice | CONTRACT-REVIEW-REQUEST, CONTRACT-REVIEW-RESULT, CONTRACT-CONTEXT, CONTRACT-FEEDBACK, ARCH-CONTRACT-BOUNDARY | spec.md, openapi.yaml, arch.spec.md |
| Each project reviews by its own rules, and a change cannot rewrite them | RULES-LAYERS, RULES-CONVENTIONS, RULES-REGISTERED-ONLY, RULES-CITED, ARCH-RULE-RESOLUTION | spec.md, arch.spec.md |
| Every number in plumb's behaviour is configurable | RULES-PARAMETERS | spec.md |
| Each part of plumb owns its data and is reached only through its port | ARCH-CONTRACT-BOUNDARY, ARCH-DATA-OWNERSHIP, ARCH-PORTS-ONLY | arch.spec.md |
| A reviewer gets few findings, and each one is worth reading | REVIEW-SILENCE, REVIEW-FAILURE-SCENARIO, REVIEW-VERIFIED, REVIEW-INTRODUCED-ONLY, REVIEW-CATEGORIES, REVIEW-BUDGET, ARCH-PIPELINE-ORDER | spec.md, arch.spec.md |
| A finding points exactly where the problem is | REVIEW-ANCHOR | spec.md |
| A new revision never brings back a finding already made | REVIEW-INCREMENTAL, ARCH-FINDING-IDENTITY | spec.md, arch.spec.md |
| The requirements of a change are checked, whatever form they take | REVIEW-EXPECTATIONS, REVIEW-CONTEXT-TRUST | spec.md |
| People stay the decision-makers, and a missing review never looks clean | REVIEW-ADVISORY, REVIEW-FAIL-LOUD | spec.md |
| Cost and time stay bounded | REVIEW-LIMITS, ARCH-SINGLE-EGRESS, ARCH-LIMITS-AT-GATEWAY, ARCH-GATEWAY-RETRIES | spec.md, arch.spec.md |
| plumb looks as deep as the change needs, and says how sure it is | DEPTH-CONFIDENCE, DEPTH-BANDS, DEPTH-EXTENDED, AUDIT-REQUEST, AUDIT-ON-ESCALATION, ARCH-ASYNC-AUDIT | spec.md, arch.spec.md |
| A disputed finding gets one honest second look | DIALOG-REVERIFY, ARCH-REVERIFY-ONCE, uc_dispute | spec.md, arch.spec.md, usecases/dispute.likec4 |
| It improves by itself, and proves each improvement | LEARN-OUTCOMES, LEARN-REPLIES, LEARN-METRIC, LEARN-RULE-CANDIDATES, LEARN-RULE-VALIDATION, LEARN-RULE-LIFECYCLE, LEARN-GATE, LEARN-MISSED, LEARN-DEPTH-CALIBRATION, ARCH-OUTCOMES-FROM-FACTS, ARCH-LEARNING-PIPELINE, ARCH-REPLAY-ISOLATION | spec.md, arch.spec.md |
| Learning can never switch safety off | LEARN-RULE-EFFECTS, REVIEW-CONTEXT-TRUST | spec.md |
| Safe to feed with attacker-controlled text | REVIEW-UNTRUSTED, ARCH-NO-EXECUTION, ARCH-SINGLE-EGRESS, ARCH-PURE-ENGINE, ARCH-IMMUTABLE-RECORDS, ARCH-PROJECT-ISOLATION | spec.md, arch.spec.md |
| No lock-in to one model vendor | MODEL-CHOICE, ARCH-SINGLE-EGRESS | spec.md, arch.spec.md |

## Decisions

Answered on 2026-11-24 from the options compared for each question. Each decision is already
written into the requirements, the contract or the model named beside it.

| ID | Decision | Applied in |
|---|---|---|
| Q1 | PostgreSQL with one schema per context, each read and written only through its own repository's database role; snapshot file blobs in object storage that only Archive reaches | ARCH-DATA-OWNERSHIP; `archive.blobs` |
| Q2 | Results are fetched, and a fetch may wait up to 60 seconds (long polling). plumb never calls an integrator back; webhooks, if ever needed, come as a Notifier context of their own | CONTRACT-REVIEW-RESULT; `wait` in openapi.yaml |
| Q3 | A snapshot is a manifest of paths and content digests, and each file is uploaded once (`putSnapshot`, `uploadBlob`). Requests, manifests and feedback are kept for good; a blob is removed only when no pinned replay request references it and it is older than 90 days | CONTRACT-REVIEW-REQUEST, ARCH-IMMUTABLE-RECORDS |
| Q4 | The verifier uses a model of a different provider family than the proposer; a verdict below 0.7 confidence gets a second sample and both must confirm. Calibration on outcomes follows once about 200 outcomes per project exist | REVIEW-VERIFIED |
| Q5 | Expert starting weights as parameters — public symbols 0.3, cross-cutting code 0.3, dependency manifests 0.2, modules touched 0.15, size 0.05, declared architecture 0.3; a dependency the code adds and a C4 delta in the context does not declare is a hard trigger; per-project calibration after about 200 decisions | DEPTH-CONFIDENCE, LEARN-DEPTH-CALIBRATION |
| Q6 | The architecture components the context names for the changed paths and their neighbours; otherwise the changed symbols and their callers to depth 2, found by parsing; otherwise top-level modules and their importers | AUDIT-ON-ESCALATION |
| Q7 | Two levels: touched (the lines or their enclosing function changed) and confirmed addressed (the final revision no longer produces the finding); the usefulness figure counts confirmed addressed only | LEARN-OUTCOMES, LEARN-METRIC, ARCH-OUTCOMES-FROM-FACTS |
| Q8 | Two stages: deterministic groups by category or rule, path scope and syntax shape, then embedding similarity of claims inside a group, starting at 0.85 and tuned by replay | LEARN-RULE-CANDIDATES |
| Q9 | A hard floor — no confirmed addressed high or critical finding lost, no new miss — then utility (addressed − 0.5 × dismissed − 2 × missed) up by at least 1 with its bootstrap lower bound above zero, on a stratified sample of 300 with every reported miss, within a spend limit per replay | LEARN-GATE |
| Q10 | Risk-based: a downgrade within a path or a layer activates by itself; a withholding rule, or one covering the whole project, waits for a maintainer; the mode is a parameter | LEARN-RULE-LIFECYCLE |
| Q11 | Security, data loss and concurrency by default; security and data loss can never be removed | LEARN-RULE-EFFECTS |
| Q12 | One daemon per organization; every record carries its organization and project, so a multi-tenant daemon later is a migration, not a rewrite | ARCH-PROJECT-ISOLATION |
| Q13 | Never in plumb. Requiring an acknowledgement of critical or high findings before merge is the integrator's policy, fed by plumb's severities | REVIEW-ADVISORY |
| Q15 | Keys live in the daemon's deployment secrets as hashes only, with up to two active keys per role and project for rotation without downtime; short-lived OIDC tokens from CI come later, as a feature of their own | ARCH-CONTRACT-BOUNDARY |
| Q16 | The gateway's deployment configuration defines each connection profile as an endpoint and a reference to a secret (a vault or a cloud secret manager) that the gateway resolves itself; a project only names a profile | ARCH-SINGLE-EGRESS, MODEL-CHOICE |
| Q17 | Learning splits into Outcomes (per event) and Tuning (on schedule, entered only by its scheduler); Tuning pulls reported misses from Outcomes, so the dependencies stay acyclic | `outcomes`, `tuning` in delta.likec4; ARCH-PORTS-ONLY, ARCH-LEARNING-PIPELINE |

## Open questions

| ID | Question | Blocks | Owner | Current default |
|---|---|---|---|---|
| Q14 | Which language and runtime is plumb written in? TypeScript keeps one stack with loam and the best model SDKs; Java 21+ carries the owner's own layering rules and ArchUnit tests over unchanged | all requirements | ybotok | TypeScript on Node.js 22 or newer, like loam |
