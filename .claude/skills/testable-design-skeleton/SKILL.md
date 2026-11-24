---
name: testable-design-skeleton
description: >-
  Use before implementing non-trivial logic in plumb. Produce a minimal testable design
  skeleton — the bounded context, the domain/application/infrastructure split, value objects,
  policies, ports and adapters, the behavior points, and which scenario each test level covers.
---

# Skill: Testable design skeleton

Good tests cannot be written after the fact if the code is one large procedural class. Before
implementing non-trivial logic, form a minimal skeleton so the code is testable, readable and
split by responsibility. This is not big architecture documentation and not DDD theatre — it is
just enough structure to make the behavior testable.

## Order

1. Understand the requirement: the loam requirement and its scenarios are the input.
2. Name the bounded context it belongs to (`architecture-boundaries`).
3. Extract the local behavior scenarios as Given / When / Then.
4. Form the skeleton: domain objects, value objects, policies, the application use case, and
   the ports and adapters for every dependency — each with the module it lands in (context
   first, layer inside).
5. Name the public methods that are the behavior points.
6. Decide what tests each scenario — unit, component or contract.
7. Write the tests first; implement only after the user approves them.

## Placement

- Business rules live in domain objects, value objects and policies — not in a mapper, an
  adapter, a repository or a generic handler.
- A use case coordinates the scenario (accept a command → call the domain → save → publish
  through a port); it does not hold the business logic.
- Every dependency hides behind a port the use case owns; adapters implement it.
- Infrastructure never leaks into the domain.

## Example split (review: verify a candidate)

- `Finding` — aggregate guarding the finding's states (candidate, confirmed, dropped, returned).
- `FindingIdentity`, `FailureScenario`, `LineRange` — value objects with their invariants.
- `VerificationPolicy` — domain policy: what counts as confirmed, refuted or unconfirmed.
- `VerifyCandidatesUseCase` — application use case for one review.
- `ModelPort`, `FindingLedger` — ports; `GatewayModelClient`, `LedgerRepository` — adapters.

Unit tests cover the domain types, the policy, and the use case with fake ports. Component tests
cover the adapters and the contract boundary.

## Signs of a good skeleton

- The bounded context is clear and each type has one responsibility.
- No type has more than 4 collaborators; a fifth is a question for the user.
- No generic `*Service`, `*Manager`, `*Util` or `*Helper` types.
- Public methods take at most 3 parameters; constructors at most 4.
- Business terms from the spec appear in the code, and most unit tests need no database,
  network or model.

If code is hard to unit-test, that is a design signal, not a test problem.
