---
name: architecture-boundaries
description: >-
  Use when designing or changing plumb's architecture — the C4 model in loam-docs, a new bounded
  context, a new dependency, a store, or code that crosses a context boundary. Enforces contexts
  that own their data, one way in per context, one way out per dependency, and model access only
  through the model gateway. Run its boundary check before loam validate.
---

# Skill: Architecture boundaries

plumb is one deployable daemon made of bounded contexts. Each context is a C4 `container` in the
plumb model; its parts are `component`s; its store is a `database` nested inside it. The rules
below hold for the model and for the code that implements it.

## The rules

1. **A context owns its data.** Every store sits inside exactly one context. Only that
   context's repository component (`repo`) reads or writes it. Nothing else touches it — another
   context asks the owner's port. There is no shared database.
2. **One way in.** A context is entered only through its port component (`port`). Every edge
   from another context targets that port, never an internal component. The one exception is
   the contract edge: external actors enter `intake.http`.
3. **One way out per dependency.** A call leaves a context only through that context's adapter
   for the dependency: `<target>Client` for another context, `repo` for its own store,
   `providers` for the model provider. Domain and application components call their own
   adapters, never another context.
4. **The model provider is reached only through the model gateway.** Only
   `gateway.providers` talks to a provider. Every other context calls `gateway.port` through its
   own `modelClient`. Each request names its step, provider, model and connection profile —
   there is no hidden default and no silent fallback; an unsupported provider fails fast.
   Provider credentials live only in the provider adapters and never appear in a log, an error,
   a result or a string rendering.
5. **Dependencies point one way.** Context dependencies form a directed acyclic graph:
   `intake → archive, review, outcomes, rules`; `outcomes → archive, review, rules, gateway`;
   `tuning → outcomes, archive, review, rules, gateway`; `review → archive, rules, gateway`.
   Tuning has no port: only its own scheduler starts it, and no context calls it. A new edge that closes a cycle is a design question for the user,
   not a detail to decide in passing.
6. **The edge holds no business rule.** `intake` parses, validates, records and dispatches; it
   holds no store and decides nothing a domain component should.
7. **Inside a context:** inbound edge → application → domain, with infrastructure (repositories,
   clients, provider adapters) behind ports the application owns. The domain is free of
   transport, persistence and framework types; identities and domain values are typed value
   objects or tiny types, never bare strings or numbers.

## Writing it in C4

- Name ports `port`, repositories `repo`, adapters to another context `<context>Client`, stores
  `store`. The boundary check relies on these names.
- Give every element and relationship a concrete description: who does what to which object,
  triggered by what, with what result. A technology label is not a description.
- The fleet landscape carries plumb's element and its outbound edges, never its internals.
- A flow enters every context at its port, never straight at an internal component; inside a
  context it shows only the components the promise needs.

## Check

```bash
python3 .claude/skills/architecture-boundaries/scripts/check-boundaries.py
loam validate --feature <FEAT>
```

The script exports each feature's model with the LikeC4 CLI — `likec4` on `PATH`, or the path
in `LIKEC4_BIN` — and checks rules 1–5 on every relationship. It prints the context dependency
graph, exits non-zero and names each violation with its rule. The one exception it knows is
`intake.dispatcher`, the contract edge's single way out. A violation is fixed in the model, or
argued in an ADR that names the trade — never waived in chat.
