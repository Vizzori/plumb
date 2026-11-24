# loam problem report: the c4.uncovered hint for an internal edge suggests a cover that blankets every internal edge

- Recorded: 2026-11-23T18:10:44Z
- Classification: loam-product
- Status: open
- Repository role: combined
- loam version: 0.2.0-alpha.20
- Entry point: `loam validate --feature <FEAT>` (CLI), while authoring a feature through `/loam-feature`
- Side effects observed: none known — `validate` is read-only, and the reproduction ran in a throwaway docs repo outside the project

## Summary

For an edge between two elements inside one service — the modular-monolith shape loam supports —
`c4.uncovered` prints the fix `add 'Covers: <svc> -> <svc>'`. Every internal edge of the service
gets the same fix text. Following it once, for an obligation about ONE edge, covers EVERY internal
edge of the service: the other edges stop being reported, and the run reads as fully covered while
no requirement accounts for them. The internal-edge coverage check turns vacuous exactly when the
hint is followed.

The precise spelling already works: `Covers: svc_app.a -> svc_app.b` resolves and covers that edge
only. The hint never suggests it.

Hypothesis, not proven: the hint is built from the endpoints' resolved service names, which
collapse to the same service for an internal edge, and the matcher reads `<svc> -> <svc>` as every
edge from the first service to the second, as the authoring guidance documents for cross-service
edges ("the kind is read past … it covers every edge from the first service to the second").

## Expected

- For an internal edge, the hint names that edge precisely, by element path, so following it
  covers that edge and no other.
- A `Covers:` line that matches more than one internal edge is either refused for internal edges or
  reported — for example "`app -> app` covers 3 internal edges" — so coverage cannot pass vacuously.

## Actual

Step 1 of the reproduction, elements covered but no edge:

```text
⚠ delta adds edge app → app ("A asks B") but no arch requirement covers it — add 'Covers: app -> app' to a specs/<svc>/arch.spec.md delta  (c4.uncovered)
⚠ delta adds edge app → app ("B asks C") but no arch requirement covers it — add 'Covers: app -> app' to a specs/<svc>/arch.spec.md delta  (c4.uncovered)
⚠ delta adds edge app → app ("C asks A") but no arch requirement covers it — add 'Covers: app -> app' to a specs/<svc>/arch.spec.md delta  (c4.uncovered)
```

Step 2, the single obligation ("A reaches B with a timeout") given `Covers: … app -> app` as the
hint says: no `c4.uncovered` remains; `summary.warnings` drops from 5 to 2 (the two left are not
about coverage). "B asks C" and "C asks A" read as covered although nothing covers them.

Step 3, the same obligation with `Covers: … svc_app.a -> svc_app.b`: "B asks C" and "C asks A"
are still reported — the precise spelling behaves as expected.

## Minimal safe reproduction

In an empty directory, with neutral stand-ins:

```bash
loam init --docs . --create
loam new FEAT-1 --title "Repro" --new-service app
rm features/FEAT-1-repro/specs/app/openapi.yaml
```

`features/FEAT-1-repro/delta.likec4`:

```likec4
specification {
  element softwareSystem
  element container
  relationship calls
  tag FEAT-1
}
model {
  svc_app = softwareSystem 'app' {
    #FEAT-1
    description 'Repro service'
    metadata { service 'app' }
    a = container 'A' { #FEAT-1 }
    b = container 'B' { #FEAT-1 }
    c = container 'C' { #FEAT-1 }
  }
  svc_app.a -[calls]-> svc_app.b 'A asks B' { #FEAT-1 }
  svc_app.b -[calls]-> svc_app.c 'B asks C' { #FEAT-1 }
  svc_app.c -[calls]-> svc_app.a 'C asks A' { #FEAT-1 }
}
```

`specs/app/spec.md`: frontmatter `owner`, `# app`, a `## Purpose`, and one ADDED requirement
(`Requirement-ID: APP-WORKS`) with one Given/When/Then scenario.

`specs/app/arch.spec.md`: the same frame and one ADDED requirement, "A reaches B with a timeout"
(`Requirement-ID: ARCH-A-B`), with one scenario about A and B, and its `Covers:` line set to:

1. `Covers: app, svc_app.a, svc_app.b, svc_app.c` — three identical hints
2. `Covers: app, svc_app.a, svc_app.b, svc_app.c, app -> app` — no coverage warning at all
3. `Covers: app, svc_app.a, svc_app.b, svc_app.c, svc_app.a -> svc_app.b` — two warnings remain

Run `loam validate --feature FEAT-1` after each.

## Machine contract

- Exit code 0 in all three steps; `c4.uncovered` is severity `warn`.
- Envelope: `contractVersion` `1.0`, `ok` `true`, `command` `validate`, `valid` `true`.
- Step 1: three findings `targets[0].findings[7..9]` with `code` `c4.uncovered`, `subject` `app`,
  `locations` `[{ "path": "features/FEAT-1-repro", "role": "scope" }]`, `details` `[]`; the
  message carries the fix text quoted under Actual. The finding names the edge only by its label
  in the message — no structured field identifies which edge it is.
- Step 2: no finding with `code` `c4.uncovered`; `summary.warnings` 2.

## Doctor and status evidence

In the project where the problem surfaced: `loam doctor --json` healthy, one finding,
`doctor.service-unknown` (expected: the service is introduced by an unarchived feature);
`reports.next` `001`; write path clean (no lock, no intent, no temps). `loam status --json`: one
feature in flight; `next` codes `next.feature`, `next.fleet-gate`.

## Files changed or write state

No project file was changed by the reproduction; it ran in a temporary directory outside the
project. The project's own feature uses the precise spelling and validates with no warnings.

## Workaround

Write each internal edge in `Covers:` by element path (`svc_x.a -> svc_x.b`), one per edge, and
ignore the spelling the hint suggests.

## Missing evidence

- Whether `archive`, `verify` or the done-check read the blanket cover the same way — not tried;
  `archive` is a writer.
- Whether a cross-service pair with several edges between the same two services should also warn
  when one `a -> b` line covers obligations written about a single edge — out of scope here.

## Sanitization

The reproduction uses neutral stand-ins (`app`, `A`, `B`, `C`); no names from the project appear.
No credentials or environment values were involved. Paths are repository-relative.
