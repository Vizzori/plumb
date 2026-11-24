---
name: documentation-writing
description: >-
  Use when writing or editing plumb's loam documents — intent.md, spec.md, arch.spec.md,
  openapi.yaml, the C4 model and flows, ADRs — or the repository README. Enforces concrete
  behavior over abstract intent, one home per fact, and honest UNKNOWN entries.
---

# Skill: Documentation writing

plumb's requirements and architecture live in `loam-docs/`. They describe concrete behavior,
not abstract intent: every rule, flow, invariant and scenario says what actually happens.

## Concrete behavior

- Name the actor or context that acts, the object or state it changes, and the trigger.
- Describe the visible result, and every rejected, degraded or recovery state with its reason
  and error code.
- Add an example wherever a phrase could be read two ways.
- In the C4 model every element and relationship has a description that meets these rules; a
  bare technology label is not a description.

## Forbidden without expansion

"handled gracefully", "safe retry", "consistent state", "proper validation", "eventually",
"integrity is preserved". If such a phrase is useful as a summary, follow it at once with the
objects, states, codes and outcomes that define it.

## UNKNOWN entries

An unknown states the missing decision, why it matters, the practical options and the
recommended next step. In a loam feature it is a row in `## Open questions` with its default.

## One home per fact

- `spec.md` — what plumb accepts, returns and refuses, as Given / When / Then.
- `arch.spec.md` — boundaries, ownership, retries, idempotency, limits, data obligations, each
  with `Covers:` naming the model objects it accounts for.
- `openapi.yaml` — the contract: payloads, required fields, every status a caller can get.
- `delta.likec4` — contexts, components, stores and the edges between them.
- `specs/plumb/usecases/` — one flow per promise that crosses several components.
- `adrs/` — one decision per record, with the options compared.

## The completeness bar

Someone must be able to answer, without opening the code: what plumb accepts and returns per
operation; every refusal and its code; what each context stores and for how long; what it
retries and within what limit; what happens when the model provider is down or over quota; and
why the shape is what it is. Where the documents cannot answer, that gap is an open question.
