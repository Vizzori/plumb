---
owner: ybotok
---

# plumb — architecture

## Purpose

plumb is one daemon made of seven bounded contexts, and these are the obligations that keep them
apart. Intake is the contract edge: it authenticates, validates, has the archive record what it
accepted and hands the work to its owner, and it keeps nothing. Archive owns the immutable record
of everything accepted, file blobs included. Review owns findings, the Rule registry owns rules and
configuration, Outcomes owns what happened to each finding, Tuning owns what is learned from
outcomes and is started only by its own scheduler, and the Model gateway owns the only way out of
plumb.

Each context owns its store — its own database schema, reachable only through its own repository's
database role. A context is entered only through its port and left only through its own client for
each dependency, and the dependencies point one way. The review engine runs nothing it reads, and
every learned rule takes the same path from evidence to effect — through the rule registry, which
alone switches anything.

## ADDED Requirements

### Requirement: Intake is the only way in, and it decides nothing
Requirement-ID: ARCH-CONTRACT-BOUNDARY

Nothing reaches plumb except through the published contract, and the edge that serves it holds
no state and no rule.

- Intake SHALL authenticate every call — integration operations with the project's integration key, maintainer operations with its maintainer key, rule packs with an organization key — and SHALL scope every command to the calling project.
- Intake SHALL validate every message against the published contract version and refuse one that fails with a stable error code.
- Intake SHALL hold no store and no business rule: its dispatcher has the archive record each accepted message, then hands it to the context that owns the work.
- Intake SHALL relay an owning context's refusal unchanged, and SHALL answer the state of a change by joining what Review and Outcomes return for it by finding identity.
- Keys SHALL be kept only as hashes, in the daemon's deployment secrets, with up to two active keys per role and project, so that a key can be rotated without downtime.

Covers: svc_plumb.intake, svc_plumb.intake.http, svc_plumb.intake.dispatcher, integrator -> svc_plumb.intake.http, maintainer -> svc_plumb.intake.http, svc_plumb.intake.http -> svc_plumb.intake.dispatcher

#### Scenario: One project's key cannot read another project's review
- **Given** a review stored for project A
- **When** the integrator calls intake with project B's key to fetch that review
- **Then** intake answers that no such review exists for the project

#### Scenario: Intake relays the registry's refusal
- **Given** a project configuration that extends a rule pack version which was never published
- **When** a maintainer registers it through intake
- **Then** the rule registry refuses it with the error code for an unknown pack version
- **And** intake relays that refusal unchanged and the archive records the configuration as refused

### Requirement: Every store belongs to one context
Requirement-ID: ARCH-DATA-OWNERSHIP

There is no shared database: what a context knows, it keeps, and others have to ask.

- Each store SHALL belong to exactly one context, and only that context's repository SHALL read or write it.
- Another context SHALL get that data only by asking the owner's port.
- Each context's store SHALL be a database schema of its own, read and written through a database role that only that context's repository holds; snapshot file blobs SHALL live in object storage that only the Archive repository can reach.

Covers: svc_plumb.archive.store, svc_plumb.archive.blobs, svc_plumb.review.store, svc_plumb.rules.store, svc_plumb.outcomes.store, svc_plumb.tuning.store, svc_plumb.gateway.store, svc_plumb.archive.repo, svc_plumb.review.repo, svc_plumb.rules.repo, svc_plumb.outcomes.repo, svc_plumb.tuning.repo, svc_plumb.gateway.repo, svc_plumb.archive.repo -> svc_plumb.archive.store, svc_plumb.archive.repo -> svc_plumb.archive.blobs, svc_plumb.review.repo -> svc_plumb.review.store, svc_plumb.rules.repo -> svc_plumb.rules.store, svc_plumb.outcomes.repo -> svc_plumb.outcomes.store, svc_plumb.tuning.repo -> svc_plumb.tuning.store, svc_plumb.gateway.repo -> svc_plumb.gateway.store

#### Scenario: A component reading another context's store fails the boundary check
- **Given** the C4 model of plumb
- **When** a component of Tuning is drawn reading the finding ledger directly
- **Then** the boundary check fails and names the ownership rule and that relationship

#### Scenario: Outcomes gets findings by asking Review
- **Given** the outcome recorder needs the findings returned for a change
- **When** it asks for them
- **Then** the request goes from its review client to the review port
- **And** only the ledger repository of Review reads the finding ledger

### Requirement: Contexts meet only at ports, through clients, in one direction
Requirement-ID: ARCH-PORTS-ONLY

Every crossing between contexts is visible, named and one-way.

- A call from one context to another SHALL leave through the caller's client for that context — for intake, its dispatcher — and SHALL enter through the callee's port.
- Context dependencies SHALL point one way: intake to archive, review, outcomes and rules; tuning to outcomes, archive, review, rules and the model gateway; outcomes to archive, review, rules and the model gateway; review to archive, rules and the model gateway.
- Tuning SHALL be started only by its own scheduler; no other context calls it.

Covers: svc_plumb.archive.port, svc_plumb.review.port, svc_plumb.rules.port, svc_plumb.outcomes.port, svc_plumb.review.rulesClient, svc_plumb.review.archiveClient, svc_plumb.outcomes.archiveClient, svc_plumb.outcomes.reviewClient, svc_plumb.outcomes.rulesClient, svc_plumb.tuning.outcomesClient, svc_plumb.tuning.archiveClient, svc_plumb.tuning.reviewClient, svc_plumb.tuning.rulesClient, svc_plumb.intake.dispatcher -> svc_plumb.archive.port, svc_plumb.intake.dispatcher -> svc_plumb.review.port, svc_plumb.intake.dispatcher -> svc_plumb.outcomes.port, svc_plumb.intake.dispatcher -> svc_plumb.rules.port, svc_plumb.review.rulesClient -> svc_plumb.rules.port, svc_plumb.review.archiveClient -> svc_plumb.archive.port, svc_plumb.outcomes.archiveClient -> svc_plumb.archive.port, svc_plumb.outcomes.reviewClient -> svc_plumb.review.port, svc_plumb.outcomes.rulesClient -> svc_plumb.rules.port, svc_plumb.tuning.outcomesClient -> svc_plumb.outcomes.port, svc_plumb.tuning.archiveClient -> svc_plumb.archive.port, svc_plumb.tuning.reviewClient -> svc_plumb.review.port, svc_plumb.tuning.rulesClient -> svc_plumb.rules.port

#### Scenario: A call into another context's internals fails the boundary check
- **Given** the C4 model of plumb
- **When** a component of the rule registry is drawn calling the gate of the review engine
- **Then** the boundary check fails, naming the port rule and the dependency cycle between review and rules

### Requirement: The archive keeps every accepted message as it came
Requirement-ID: ARCH-IMMUTABLE-RECORDS

Exact replays and honest audits both depend on knowing precisely what plumb was given.

- The dispatcher SHALL have every accepted request, snapshot and feedback event recorded in the archive, as an immutable, content-addressed record, before any context starts work on it.
- The archive SHALL never change a record. A refusal by the owning context SHALL be appended as a record of its own, and replays and outcome derivation SHALL skip refused records.
- The archive SHALL store each file blob once by its digest, SHALL keep requests, snapshot manifests and feedback events for good, and SHALL remove a blob only when no request pinned for a replay sample references it and it is older than the retention period, appending a removal record.
- Every result SHALL name the records it was computed from.

Covers: svc_plumb.archive, svc_plumb.archive.port -> svc_plumb.archive.repo

#### Scenario: A result names the record of its request
- **Given** a review request that intake accepted and the archive port recorded
- **When** the review completes
- **Then** the result names the digest of that archived request

### Requirement: The review engine is a function of its inputs
Requirement-ID: ARCH-PURE-ENGINE

What the engine returns depends on nothing it was not given.

- The review engine SHALL compute a result only from the request it was handed, the snapshot files that request names, the effective rules and parameters, the model responses, and the findings already returned for the change before this revision.
- The review engine SHALL write nothing but its results — review results, audit results and follow-ups — and only through its ledger repository.
- A replay job SHALL return its result to the caller, SHALL start no audit and SHALL write nothing.

Covers: svc_plumb.review, svc_plumb.review.triage, svc_plumb.review.anchor, svc_plumb.review.port -> svc_plumb.review.triage, svc_plumb.review.port -> svc_plumb.review.repo, svc_plumb.review.anchor -> svc_plumb.review.repo

#### Scenario: The same inputs give the same result
- **Given** one request, one configuration version, the recorded model responses and the findings returned for the change before its revision
- **When** the review port starts a replay of it twice
- **Then** both results are identical
- **And** the anchor writes nothing through the ledger repository

### Requirement: Code is read, never run
Requirement-ID: ARCH-NO-EXECUTION

Running a repository's own tools is how hosted reviewers have been taken over; plumb does not do it.

- plumb SHALL NOT execute code, build scripts, tests, linters or tool configuration from a request or a snapshot.
- The review engine SHALL read snapshot files only through its archive client, as text.

Covers: svc_plumb.review.reviewers, svc_plumb.review.auditor, svc_plumb.review.reviewers -> svc_plumb.review.archiveClient, svc_plumb.review.verifier -> svc_plumb.review.archiveClient, svc_plumb.review.auditor -> svc_plumb.review.archiveClient

#### Scenario: A linter configuration in a snapshot is not run
- **Given** a snapshot that contains a linter configuration file which loads code from the repository
- **When** the reviewers and the auditor read the snapshot through the archive client
- **Then** no process runs that configuration file

### Requirement: Audits run apart from reviews
Requirement-ID: ARCH-ASYNC-AUDIT

An audit can take long; a review result never waits for one.

- Audits SHALL run as jobs separate from review jobs, whether the review port or triage starts them.
- The auditor SHALL hand its area to the same reviewers and verification as a review, without a diff.
- The auditor SHALL run one audit for all escalations of the same area within the coalescing window, finding an earlier one through the ledger repository.

Covers: svc_plumb.review.port -> svc_plumb.review.auditor, svc_plumb.review.triage -> svc_plumb.review.auditor, svc_plumb.review.auditor -> svc_plumb.review.reviewers, svc_plumb.review.auditor -> svc_plumb.review.repo

#### Scenario: Triage starts an audit without holding the review
- **Given** a review whose triage reaches the audit threshold
- **When** triage starts an area audit and the auditor hands the area to the reviewers
- **Then** the review result is written before the audit finishes

### Requirement: The model gateway is the only way out
Requirement-ID: ARCH-SINGLE-EGRESS

No component reaches a model except through its own context's model client and the gateway.

- Only the gateway's provider adapters SHALL open network connections, and only to configured model providers.
- Every other context SHALL reach a model only through its own model client and the gateway's port.
- Every model request SHALL carry its job id, its step, the provider, model and connection profile that the effective parameters name for that step, the job's limits and whether it is a replay; the gateway SHALL refuse a request that lacks any of them, SHALL fail fast on an unsupported provider, and SHALL never fall back to a default silently.
- A connection profile SHALL be defined only in the gateway's deployment configuration, as an endpoint and a reference to a secret that the provider adapters resolve at call time.
- Provider credentials SHALL be held only by the provider adapters, and SHALL NOT appear in a log, an error, a result or a string rendering.

Covers: svc_plumb.gateway, svc_plumb.gateway.port, svc_plumb.gateway.router, svc_plumb.gateway.providers, svc_plumb.review.modelClient, svc_plumb.outcomes.modelClient, svc_plumb.tuning.modelClient, svc_plumb.gateway.port -> svc_plumb.gateway.router, svc_plumb.gateway.router -> svc_plumb.gateway.providers, svc_plumb.gateway.providers -> llm, svc_plumb.review.modelClient -> svc_plumb.gateway.port, svc_plumb.outcomes.modelClient -> svc_plumb.gateway.port, svc_plumb.tuning.modelClient -> svc_plumb.gateway.port, svc_plumb.review.triage -> svc_plumb.review.modelClient, svc_plumb.review.contextReader -> svc_plumb.review.modelClient, svc_plumb.review.reviewers -> svc_plumb.review.modelClient, svc_plumb.review.verifier -> svc_plumb.review.modelClient, svc_plumb.outcomes.classifier -> svc_plumb.outcomes.modelClient, svc_plumb.tuning.miner -> svc_plumb.tuning.modelClient, svc_plumb.tuning.critic -> svc_plumb.tuning.modelClient

#### Scenario: A request without a connection profile is refused
- **Given** a model request from the review engine's model client that names its step, provider and model but no connection profile
- **When** it reaches the model port
- **Then** the gateway refuses it with the error code for a missing profile
- **And** nothing is sent to the model provider

#### Scenario: An unsupported provider fails fast
- **Given** a project configuration that names a provider family the gateway has no adapter for
- **When** the provider router receives a request for it
- **Then** the request fails at once with the error code for an unsupported provider
- **And** no other provider is tried

### Requirement: Limits are enforced and every call recorded at the gateway
Requirement-ID: ARCH-LIMITS-AT-GATEWAY

Spend and determinism are decided in one place.

- The budget guard SHALL check the job's token, step, time and spend limits against the job's spend so far before a request leaves — for review, audit, replay and learning jobs alike.
- The gateway SHALL record every request, response, token count and cost in its call log.
- During a replay under the active configuration, the gateway SHALL answer from the recorded response instead of calling the provider.

Covers: svc_plumb.gateway.budget, svc_plumb.gateway.port -> svc_plumb.gateway.budget, svc_plumb.gateway.port -> svc_plumb.gateway.repo, svc_plumb.gateway.budget -> svc_plumb.gateway.repo

#### Scenario: A spent review sends nothing more to the model provider
- **Given** a review whose spend has reached its limit
- **When** the model port receives another request for that review and the budget guard reads the spend so far
- **Then** the request is refused before it leaves
- **And** the call log records the refusal with the limit that caused it

### Requirement: Provider errors are retried within the job's limits, and only some of them
Requirement-ID: ARCH-GATEWAY-RETRIES

A transient provider failure does not fail a review, and a permanent one does not burn its budget.

- On a rate limit or a server error, the provider adapters SHALL retry with exponential backoff up to the configured number of attempts, and only while the job's limits allow.
- On any other error, the provider adapters SHALL fail at once with a typed error naming the provider and the cause.
- The call log SHALL record every attempt.

Covers: svc_plumb.gateway.providers, svc_plumb.gateway.providers -> llm

#### Scenario: A rate limit is retried
- **Given** a model provider that answers the first attempt with a rate limit and the second with a response
- **When** the provider adapters send a request for a job that allows three attempts
- **Then** the request succeeds on the second attempt
- **And** the call log records both attempts

#### Scenario: A rejected request is not retried
- **Given** a model provider that rejects a request as malformed
- **When** the provider adapters send it
- **Then** the request fails at once with a typed error naming the provider and the cause

### Requirement: One pipeline, verification before the gate
Requirement-ID: ARCH-PIPELINE-ORDER

Every candidate takes the same path, so no shortcut can skip verification.

- The review engine SHALL take every candidate through triage, context reading, proposal, verification, the gate and placement, in that order.
- No candidate SHALL reach the gate without a verification result.

Covers: svc_plumb.review.contextReader, svc_plumb.review.verifier, svc_plumb.review.triage -> svc_plumb.review.contextReader, svc_plumb.review.contextReader -> svc_plumb.review.reviewers, svc_plumb.review.reviewers -> svc_plumb.review.verifier, svc_plumb.review.verifier -> svc_plumb.review.gate, svc_plumb.review.gate -> svc_plumb.review.anchor

#### Scenario: An unverified candidate never reaches the result
- **Given** a candidate whose verification request failed
- **When** triage hands over the request, the context reader the change with its expectations, the reviewers the candidates and the verifier the confirmed findings
- **Then** the candidate never reaches the gate
- **And** the result counts it as dropped unverified

### Requirement: A finding keeps one identity across revisions
Requirement-ID: ARCH-FINDING-IDENTITY

Never repeating a finding depends on knowing that two findings are the same one.

- plumb SHALL give every finding an identity derived from its file, the normalized code it concerns, its category and its claim, so that the identity survives line shifts caused by unrelated edits.
- The finding ledger SHALL be the only record the gate consults, through the ledger repository, to decide whether a finding was already returned for the change before this revision.

Covers: svc_plumb.review.gate, svc_plumb.review.gate -> svc_plumb.review.repo

#### Scenario: A shifted line does not create a duplicate
- **Given** a finding returned for line 40 of a file
- **When** a later revision inserts ten lines above it and leaves the code it concerns unchanged
- **Then** the gate finds the finding's identity in the ledger as already returned
- **And** the result does not contain it again

### Requirement: The rule registry alone reads and changes configuration
Requirement-ID: ARCH-RULE-RESOLUTION

Which rule applied to which file, and every switch of a rule or a configuration, has one owner.

- The rule registry SHALL be the only context that reads or changes rules and configuration, and its layer resolver SHALL apply the layers in one fixed order.
- Rule states and configuration versions SHALL change only through the registry's rule lifecycle: Tuning proposes, the registry switches.
- Every result SHALL record the configuration version and the rule pack versions it was computed under.
- The rule lifecycle SHALL refuse, and the layer resolver SHALL drop, any learned rule that would add a check, apply to a protected category, or apply outside the project it was learned in.
- A rule candidate SHALL be registered in the registry before its replay, and the resolver SHALL answer a replay with the active rules plus that candidate.
- Outcomes and Tuning SHALL read the parameters and explicit rules they need only through their rules clients.

Covers: svc_plumb.rules, svc_plumb.rules.resolver, svc_plumb.rules.lifecycle, svc_plumb.rules.port -> svc_plumb.rules.resolver, svc_plumb.rules.port -> svc_plumb.rules.lifecycle, svc_plumb.rules.resolver -> svc_plumb.rules.repo, svc_plumb.rules.lifecycle -> svc_plumb.rules.repo, svc_plumb.review.triage -> svc_plumb.review.rulesClient, svc_plumb.review.reviewers -> svc_plumb.review.rulesClient, svc_plumb.review.gate -> svc_plumb.review.rulesClient, svc_plumb.outcomes.classifier -> svc_plumb.outcomes.rulesClient, svc_plumb.tuning.miner -> svc_plumb.tuning.rulesClient, svc_plumb.tuning.critic -> svc_plumb.tuning.rulesClient

#### Scenario: A result records the versions it used
- **Given** a project that extends rule pack `base` version 2 under configuration version 5
- **When** triage, the reviewers and the gate ask the rules client for the effective rules of a file
- **Then** the result records configuration version 5 and pack `base` version 2

#### Scenario: A learned rule that would silence security is refused
- **Given** a candidate that would withhold findings in the security category
- **When** the rule critic registers it through the rules client
- **Then** the rule lifecycle refuses it with the error code for a protected category

### Requirement: Projects never mix
Requirement-ID: ARCH-PROJECT-ISOLATION

One project's code and conventions never shape another project's review.

- plumb SHALL NOT combine records of two projects in one model request, one rule or one statistic.
- Published rule packs SHALL be the only data that projects share.
- Every record SHALL carry its organization and its project.
- The rule miner SHALL compare a finding only with findings of the same project, and the gateway SHALL reuse a recorded response only for a request of the same project.

Covers: plumb, svc_plumb.tuning.miner, svc_plumb.tuning.store, svc_plumb.outcomes.store, svc_plumb.gateway.store

#### Scenario: A rule learned in one project stays there
- **Given** a rule learned in project B that withholds requests for value objects
- **When** plumb reviews a change in project A, which declares value objects
- **Then** the rule is not applied

### Requirement: Outcomes come from facts; reply classes are recorded as derived
Requirement-ID: ARCH-OUTCOMES-FROM-FACTS

What plumb learns from is what people did, which a model cannot invent.

- The outcome recorder SHALL derive touched and unanswered from revisions and closures, confirmed addressed from the review engine's findings for the final revision, and dismissed from the replies and thread states of maintainers and members.
- A reply's class SHALL be recorded as derived by the reply classifier, together with the reply text, so that it can be derived again.

Covers: svc_plumb.outcomes, svc_plumb.outcomes.port, svc_plumb.outcomes.recorder, svc_plumb.outcomes.classifier, svc_plumb.outcomes.port -> svc_plumb.outcomes.recorder, svc_plumb.outcomes.port -> svc_plumb.outcomes.repo, svc_plumb.outcomes.recorder -> svc_plumb.outcomes.classifier, svc_plumb.outcomes.recorder -> svc_plumb.outcomes.archiveClient, svc_plumb.outcomes.recorder -> svc_plumb.outcomes.reviewClient, svc_plumb.outcomes.recorder -> svc_plumb.outcomes.repo

#### Scenario: An outcome carries its evidence
- **Given** a finding whose lines changed in revision D
- **When** the outcomes port hands over the closure, and the outcome recorder reads the later revisions through its archive client and the findings of the final revision through its review client
- **Then** the outcome store holds the outcome confirmed addressed, with revision D and the final review as its evidence

### Requirement: A dispute reaches the verifier once
Requirement-ID: ARCH-REVERIFY-ONCE

A reply with an argument gets one more verification, through the review port, and no debate.

- The reply classifier SHALL ask the review engine, through its review client, to verify a finding disputed with an argument.
- The review port SHALL accept one re-verification per finding and refuse every further one, whoever asks.
- The verifier SHALL write the outcome of that verification through the ledger repository as a follow-up on the finding, and nothing else for it.

Covers: svc_plumb.outcomes.classifier -> svc_plumb.outcomes.reviewClient, svc_plumb.review.port -> svc_plumb.review.verifier, svc_plumb.review.verifier -> svc_plumb.review.repo

#### Scenario: A second dispute of the same finding is not verified again
- **Given** a finding the verifier already checked once more after a maintainer's dispute
- **When** the reply classifier asks the review port, through its review client, to verify it again after a second dispute
- **Then** the review port refuses the re-verification
- **And** the finding keeps its first follow-up as its only one

### Requirement: No rule takes effect without a critic and a replay
Requirement-ID: ARCH-LEARNING-PIPELINE

Every learned rule takes the same path from evidence to effect.

- Tuning SHALL take every rule candidate from the rule miner through the rule critic to the replayer, in that order.
- No rule SHALL reach shadow mode without a critic verdict and a replay result.
- The scheduler SHALL start rule mining, the shadow-mode tally, rule revisits and depth calibration; nothing else starts them.
- On each sweep the promoter SHALL collect reported missed defects from Outcomes and ask the registry to send every rule they match back to shadow mode; Outcomes never calls Tuning.

Covers: svc_plumb.tuning, svc_plumb.tuning.scheduler, svc_plumb.tuning.miner, svc_plumb.tuning.critic, svc_plumb.tuning.scheduler -> svc_plumb.tuning.miner, svc_plumb.tuning.scheduler -> svc_plumb.tuning.promoter, svc_plumb.tuning.miner -> svc_plumb.tuning.outcomesClient, svc_plumb.tuning.miner -> svc_plumb.tuning.repo, svc_plumb.tuning.miner -> svc_plumb.tuning.critic, svc_plumb.tuning.critic -> svc_plumb.tuning.replayer

#### Scenario: A candidate the critic rejects is never replayed
- **Given** a candidate the rule miner formed from dismissals it read through its outcomes client
- **When** the rule critic rejects it as broader than its evidence
- **Then** the replayer is never asked to replay it

### Requirement: Replays never reach a change, and the registry makes every switch
Requirement-ID: ARCH-REPLAY-ISOLATION

plumb experiments on its history, and every switch it makes can be traced and undone.

- Replays SHALL run on archived requests through the review port, and their results SHALL never appear in a change's state or start an audit.
- The replayer SHALL pin its sample in the archive for as long as the sample is in use, and unpin it after.
- The promoter SHALL only ask the rule registry, through its rules client, for a rule state or configuration switch that names the replay result it rests on; the registry records and makes the switch.
- The promoter SHALL ask for no activation until the shadow-mode tally, read from the review engine through its review client, covers the configured number of reviews.

Covers: svc_plumb.tuning.replayer, svc_plumb.tuning.promoter, svc_plumb.tuning.replayer -> svc_plumb.tuning.archiveClient, svc_plumb.tuning.replayer -> svc_plumb.tuning.reviewClient, svc_plumb.tuning.replayer -> svc_plumb.tuning.repo, svc_plumb.tuning.replayer -> svc_plumb.tuning.promoter, svc_plumb.tuning.promoter -> svc_plumb.tuning.rulesClient, svc_plumb.tuning.promoter -> svc_plumb.tuning.repo, svc_plumb.tuning.promoter -> svc_plumb.tuning.reviewClient, svc_plumb.tuning.promoter -> svc_plumb.tuning.outcomesClient

#### Scenario: A replay shows up nowhere but in its own result
- **Given** the replayer reads 200 archived requests through its archive client and asks for replays under a candidate configuration through its review client
- **When** it hands the replay results to the promoter
- **Then** no change's state shows a finding from the replay
- **And** the promoter's switch request names the replay result it rests on
