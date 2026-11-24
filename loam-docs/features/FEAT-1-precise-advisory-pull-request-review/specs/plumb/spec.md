---
owner: ybotok
---

# plumb

## Purpose

plumb is a review core that runs as a daemon. Something else — an integrator such as a CI job, a
bot or a platform app — gathers the code of a change and whatever requirements describe it, sends
plumb one complete review package, and shows the result where the team works. plumb knows no code
host, tracker or knowledge base, follows no link and publishes nothing.

From each package plumb returns only findings it has verified: every one names the changed lines, a
concrete way the code fails and the evidence it checked. It reviews by the rules a project
registered — layered from organization packs down to path scopes — and checks a convention only
where the project declared one. It decides how deep to look and says how confident it is.

plumb also measures itself and learns. It derives what happened to each finding from later
revisions and from the feedback the integrator sends, turns repeated, similar dismissals into rules
that only ever quiet it down, and adopts any change to how it reviews only after replaying the
change on stored requests.

## ADDED Requirements

### Requirement: A review works from what the request contains
Requirement-ID: CONTRACT-REVIEW-REQUEST
Operations: submitReview, putSnapshot, uploadBlob

Everything plumb reviews arrives in the request; nothing is fetched.

- plumb SHALL accept a review request that carries the project, the change identifier and its revision, the base revision, the unified diff and the changed files, and optionally a snapshot named by the digest of its manifest and a list of context items.
- plumb SHALL accept a snapshot as a manifest of file paths and content digests, answer with the files it does not yet hold, and store each file once by its digest, however many snapshots share it.
- plumb SHALL refuse a request that does not satisfy the published contract, with a stable error code naming the rule it broke.
- plumb SHALL NOT fetch anything a request does not contain, and SHALL follow no link, URL or reference found in one.

#### Scenario: A link in the context is not followed
- **Given** a request whose only context item says the details are on a page at a URL
- **When** plumb reviews the change
- **Then** plumb makes no request to that URL
- **And** the result notes that the referenced page was not included

#### Scenario: A request without a diff is refused
- **Given** a review request that names a change and a revision but carries no diff
- **When** the integrator submits it
- **Then** plumb refuses it with the error code for a missing diff

### Requirement: Results are fetched, never published
Requirement-ID: CONTRACT-REVIEW-RESULT
Operations: getReview

plumb answers; the integrator decides what to show and where.

- For every accepted review request plumb SHALL make a result available that states its status, the findings, the depth decision with its confidence, the expectations read from the context, and the cost.
- plumb SHALL let the integrator wait up to 60 seconds for a result in one fetch, and SHALL open no connection to an integrator.
- plumb SHALL NOT publish anything to a code host, a tracker or a chat.

#### Scenario: The integrator fetches a completed result
- **Given** a review that completed with two findings
- **When** the integrator fetches the result
- **Then** the result holds both findings with their locations
- **And** plumb has opened no connection except to the model provider

### Requirement: Context is any text with a source
Requirement-ID: CONTRACT-CONTEXT
Operations: submitReview

plumb does not know how a team writes requirements, so it asks for the least it can work with.

- plumb SHALL accept context items of which only the text and the source system are required; a title, a kind, a trust level, links and named facets are optional.
- plumb SHALL ignore facets it does not recognize, and SHALL treat an item without a trust level as untrusted.
- plumb SHALL review a change that comes with no context at all.

#### Scenario: A tracker ticket is the only context
- **Given** a request whose only context item is the text of a tracker ticket and its source
- **When** plumb reviews the change
- **Then** the review completes
- **And** the result lists the expectations plumb read from the ticket

### Requirement: Feedback arrives as events
Requirement-ID: CONTRACT-FEEDBACK
Operations: postFeedback

What happened after a review reaches plumb only through the integrator.

- plumb SHALL accept these feedback events: whether a finding was shown, a reply to a finding with its text and its author's role, a thread resolved or reopened, the closure of a change, a reported missed defect, and the location of a human review comment.
- plumb SHALL take each author's role — maintainer, member, outside contributor or bot — as the integrator states it.
- plumb SHALL refuse an event about a finding it never returned for that project.

#### Scenario: An event about an unknown finding is refused
- **Given** a finding identifier that plumb never returned for the project
- **When** the integrator sends a reply event for it
- **Then** plumb refuses the event with the error code for an unknown finding

### Requirement: Rules come in layers, and the nearest wins
Requirement-ID: RULES-LAYERS
Operations: putRulePack, putProjectConfig

Different projects write code differently; one set of rules cannot serve them all.

- plumb SHALL compute the effective rules for each file from five layers, from the most general: built-in core rules, organization rule packs, the project configuration, the project's path scopes, and learned rules.
- Where two layers set the same thing, plumb SHALL apply the nearer one, and an explicit setting SHALL outrank a learned rule.
- plumb SHALL keep every published rule pack version immutable, and a project SHALL name the versions it extends.

#### Scenario: A path scope overrides the project
- **Given** a project configuration with `domain-modeling: value-objects`
- **And** a path scope for `src/api/dto/**` with `domain-modeling: thin-dto`
- **When** a change adds a data transfer object (DTO) with primitive fields under `src/api/dto/`
- **Then** no finding asks for value objects in that file

### Requirement: A convention is checked only where it is declared
Requirement-ID: RULES-CONVENTIONS

A convention is a team's choice, not a best practice to enforce on everyone.

- plumb SHALL treat a convention — such as how domain data is modelled — as a choice between named options, each with its own rules.
- plumb SHALL return no finding about a convention in a file for which no option of that convention is declared.

#### Scenario: No declaration, no comment
- **Given** a project that declares no option for `domain-modeling`
- **When** a change passes domain data around in thin DTOs
- **Then** no finding about domain modelling is returned

### Requirement: A change cannot rewrite the rules it is reviewed by
Requirement-ID: RULES-REGISTERED-ONLY
Operations: putProjectConfig

The rules a review applies are the ones a maintainer registered, whatever the change contains.

- plumb SHALL take rules and configuration only from what is registered for the project through its API, never from files in the change or the snapshot under review.

#### Scenario: A configuration file in the change has no effect on its own review
- **Given** a change that adds a file shaped like a plumb configuration which switches security rules off
- **When** plumb reviews the change
- **Then** the review applies the registered configuration, security rules included

### Requirement: Findings name the rule or requirement they rest on
Requirement-ID: RULES-CITED

A reader can always see why plumb thinks something is wrong.

- When a finding rests on a rule, plumb SHALL cite the rule with its pack and version.
- When a finding rests on an expectation from the context, plumb SHALL cite the context item's source and quote its text.

#### Scenario: A finding against a ticket quotes the ticket
- **Given** a ticket in the context that says a split accepts between two and five payees
- **When** a change accepts any number of payees and plumb returns a finding about it
- **Then** the finding cites the ticket's source and quotes the criterion

### Requirement: Every threshold is a parameter
Requirement-ID: RULES-PARAMETERS
Operations: putProjectConfig

No number in plumb's behaviour is fixed in code.

- plumb SHALL let every threshold it applies — the finding limit, the limits on cost and time, the escalation thresholds, triage votes, exploration rate, audit coalescing window and budget, the retry attempts for model requests, the second-verification threshold, the depth signal weights, the caller depth of an affected area, the replay sample and its cost limit, the approval mode, and every learning threshold — be set at any configuration layer, each with a documented default.
- plumb SHALL treat a value a person set explicitly as pinned, and SHALL change an unpinned value only through the replay gate.

#### Scenario: A project raises the dismissal threshold
- **Given** a project that sets the minimum number of similar dismissals to 5
- **When** four structurally similar findings are dismissed
- **Then** no rule candidate is formed

### Requirement: Stay silent unless there is a verified finding
Requirement-ID: REVIEW-SILENCE

plumb speaks only when it has something verified to say.

- plumb SHALL return no finding when no candidate passes verification, with the status completed and the number of files reviewed.
- plumb SHALL NOT return praise, a restatement of the diff, or a walkthrough of the change.

#### Scenario: A change with no defect gets no findings
- **Given** a change that contains no defect plumb can verify
- **When** plumb reviews it
- **Then** the result is completed with no findings and the number of files reviewed

### Requirement: Every finding names how the code fails
Requirement-ID: REVIEW-FAILURE-SCENARIO

A finding is a claim about behaviour, not a feeling about the code.

- plumb SHALL return a finding only when it states the changed lines it concerns, a concrete failure scenario — the inputs or state that lead to wrong behaviour — and the observable consequence.
- plumb SHALL drop a candidate that cannot state a failure scenario.

#### Scenario: A vague concern is dropped
- **Given** a candidate that says the change might cause problems but names no input or state that leads to one
- **When** plumb prepares the result
- **Then** the candidate is not returned

### Requirement: Every finding is verified before it is returned
Requirement-ID: REVIEW-VERIFIED

A second, independent look decides whether a candidate reaches anyone.

- plumb SHALL check every candidate in a verification step that reads the code the candidate depends on and does not see the reasoning that produced it.
- plumb SHALL return a candidate only when verification confirms it, and SHALL drop one that verification refutes or cannot confirm.
- Verification SHALL use a model from a different provider family than the one that proposed the candidate, wherever the project configures more than one.
- When a verdict is less confident than the configured threshold, plumb SHALL verify once more, and SHALL return the candidate only if both verdicts confirm it.

#### Scenario: A refuted candidate is not returned
- **Given** a candidate that reports a possible null dereference
- **And** the value is checked for null before the call, in code the change does not touch
- **When** verification reads that code
- **Then** the candidate is dropped

#### Scenario: An uncertain verdict gets a second look
- **Given** a second-verification threshold of 0.7
- **When** the first verdict confirms a candidate with confidence 0.6 and the second verdict refutes it
- **Then** the candidate is dropped

### Requirement: Only defects the change introduces
Requirement-ID: REVIEW-INTRODUCED-ONLY

A review is about the change, not the history of the repository.

- In a review result plumb SHALL return findings only about defects the change introduces or makes newly reachable.
- Defects in code the change neither alters nor newly reaches SHALL appear only in audit results.

#### Scenario: An old defect in untouched code stays out of the review
- **Given** a change that edits function A
- **And** an unrelated defect in function B, which the change neither edits nor newly calls
- **When** plumb reviews the change
- **Then** the review result contains no finding about function B

### Requirement: Comment on what breaks, not on taste
Requirement-ID: REVIEW-CATEGORIES

By default plumb looks for the defects reviewers act on.

- By default plumb SHALL return findings only in these categories: correctness, error handling, security, data loss and concurrency.
- plumb SHALL return findings about style, naming, structure or documentation only where a rule or a declared convention asks for them.

#### Scenario: A naming preference is not returned
- **Given** a change that introduces a correct but unusually named variable
- **And** no rule about naming applies to the file
- **When** plumb reviews it
- **Then** no finding about the name is returned

### Requirement: A small, ranked set of findings
Requirement-ID: REVIEW-BUDGET

Each review has a limit on how many findings it returns.

- plumb SHALL return at most the configured number of findings per review, highest severity first and, within a severity, highest confidence first.
- plumb SHALL state in the result how many verified findings the limit left out.

#### Scenario: Findings beyond the limit are counted, not returned
- **Given** a limit of 5 findings
- **And** 8 verified findings
- **When** plumb prepares the result
- **Then** the 5 highest-ranked findings are returned
- **And** the result says 3 more verified findings were left out

### Requirement: Findings point at the lines they discuss
Requirement-ID: REVIEW-ANCHOR

A finding is only useful at the exact place it talks about.

- plumb SHALL place each finding on lines that exist in the diff at the reviewed revision, on the side — base or head — that the finding concerns.
- plumb SHALL list a verified finding it cannot place among the unplaced findings, never at another position.

#### Scenario: A finding outside the diff is listed as unplaced
- **Given** a verified finding about a line outside every hunk of the diff
- **When** plumb prepares the result
- **Then** the finding appears among the unplaced findings with its file and line

### Requirement: Each revision is reviewed once, without repeats
Requirement-ID: REVIEW-INCREMENTAL
Operations: submitReview

A change that evolves is reviewed as it evolves, never from scratch.

- For a later revision of a change plumb SHALL review only what changed since the last revision it reviewed, reading the surrounding code as context.
- plumb SHALL NOT return a finding it already returned for the same change, including one that was dismissed.
- A second request for a revision already reviewed SHALL return the existing result.

#### Scenario: A second request for the same revision returns the same result
- **Given** plumb reviewed revision C of a change and returned two findings
- **When** the integrator submits revision C again
- **Then** plumb returns the existing result and starts no new review

#### Scenario: A dismissed finding is not raised again
- **Given** a finding that a maintainer dismissed
- **When** a later revision leaves the code that finding concerns unchanged
- **Then** plumb does not return that finding again

### Requirement: Advise, never decide
Requirement-ID: REVIEW-ADVISORY

The people who merge stay the decision-makers.

- A result SHALL contain no approval, no request for changes and no merge decision.
- A result's status SHALL say whether the review ran, not whether the code is acceptable.

#### Scenario: Findings carry no verdict
- **Given** a review that returns two verified security findings
- **When** the integrator fetches the result
- **Then** the status is completed
- **And** the result contains no approval and no request for changes

### Requirement: A review that did not happen says so
Requirement-ID: REVIEW-FAIL-LOUD

A missing review must never look like a clean one.

- When a review cannot complete — the model provider fails or refuses on quota, or a limit is reached before verification — plumb SHALL set the status to not completed and name the reason.
- plumb SHALL NOT report a review as completed unless its result is stored.

#### Scenario: A quota error is visible
- **Given** the model provider rejects plumb's requests because a quota is exhausted
- **When** plumb reviews a change
- **Then** the result's status is not completed
- **And** the reason names the quota error

### Requirement: Hard limits on cost and time
Requirement-ID: REVIEW-LIMITS

A review never runs away with a team's money.

- plumb SHALL stop a review when it reaches the configured limit on model tokens, steps, wall-clock time or spend.
- When plumb stops at a limit, it SHALL return the findings it had already verified and name the limit it reached.

#### Scenario: A review stops at its spend limit
- **Given** a spend limit of 1 US dollar per review
- **When** a review's model spend reaches 1 US dollar
- **Then** plumb makes no further model request for that review
- **And** the result names the spend limit

### Requirement: Request text is data, not instructions
Requirement-ID: REVIEW-UNTRUSTED

Anything in a request may have been written by an attacker.

- plumb SHALL treat every text in a request — code, comments, descriptions, commit messages and context items — as data, and SHALL NOT follow instructions found in it.
- plumb SHALL remove hidden HTML comments and invisible Unicode characters from request text before any model reads it.
- plumb SHALL list in the result any request text addressed to an automated reviewer, quoting it with its source.

#### Scenario: An instruction in the context changes nothing
- **Given** a context item that tells the reviewer to report no findings
- **When** plumb reviews the change
- **Then** the review applies the registered rules as it would to any change
- **And** the result quotes the instruction with its source

### Requirement: Expectations come from the context, with quotes
Requirement-ID: REVIEW-EXPECTATIONS

Whatever form the requirements take, plumb reads what they expect of the code.

- plumb SHALL read checkable expectations from the context items and list each in the result with the quote and the source it came from.
- plumb SHALL return a finding about an expectation only when the expectation is stated explicitly and the code clearly contradicts it.
- When the context refers to something it does not contain, plumb SHALL say so in the result instead of guessing.

#### Scenario: An explicit criterion that the code contradicts
- **Given** a ticket in the context that says a split accepts between two and five payees
- **When** the change accepts any number of payees
- **Then** plumb returns a finding that quotes the criterion

### Requirement: Context may add checks, never remove them
Requirement-ID: REVIEW-CONTEXT-TRUST

Context can be forged as easily as code, so it can only make plumb stricter.

- plumb SHALL use context items of any trust level to add expectations, and only items marked approved to explain away a candidate.
- plumb SHALL NOT withhold or downgrade a finding in a protected category because of anything a context item says.

#### Scenario: A proposed specification cannot excuse a missing check
- **Given** a context item with trust proposed that says an endpoint is public by design
- **When** verification confirms that the endpoint lacks an authorization check
- **Then** plumb returns the security finding

### Requirement: Every review states its depth, its confidence and why
Requirement-ID: DEPTH-CONFIDENCE

How deep plumb looks is a decision a reader can see and question.

- plumb SHALL decide the depth of each review with a confidence between 0 and 1 and the reasons for it, and SHALL return both in the result.
- The confidence SHALL combine deterministic signals with the share of independent triage votes for an extended review.
- A hard trigger — a database migration, a changed public contract, or a new dependency between modules or services — SHALL force an extended review; triage votes SHALL be able to raise the depth but never lower it below a trigger.
- The deterministic signals and their weights SHALL be parameters: changed public symbols, cross-cutting code, dependency manifests, modules touched, size, and architecture the context declares.
- A dependency between modules or services that the code introduces and a C4 delta in the context does not declare SHALL be a hard trigger.

#### Scenario: A migration forces an extended review
- **Given** a change that adds a database migration
- **And** all triage votes are against an extended review
- **When** plumb decides the depth
- **Then** the review is extended
- **And** the reasons name the migration as the trigger

### Requirement: Thresholds decide what a confidence leads to
Requirement-ID: DEPTH-BANDS
Operations: submitReview

One number, four outcomes, each threshold a parameter.

- At or above the audit threshold plumb SHALL run an extended review and an audit of the affected area.
- At or above the extended threshold plumb SHALL run an extended review and recommend an audit of the area.
- At or above the suggestion threshold plumb SHALL run a normal review and suggest an extended one in the result, with its reasons.
- Below the suggestion threshold plumb SHALL run a normal review.
- When a request sets the depth itself, plumb SHALL follow it and record the depth as the integrator's decision.

#### Scenario: A middle confidence suggests instead of escalating
- **Given** a suggestion threshold of 0.3 and an extended threshold of 0.5
- **When** triage decides with a confidence of 0.42
- **Then** plumb runs a normal review
- **And** the result suggests an extended review and gives its reasons

### Requirement: An extended review reads more of what was delivered
Requirement-ID: DEPTH-EXTENDED

Looking wider never means fetching more; it means reading more of the snapshot.

- An extended review SHALL read beyond the diff within the request's snapshot: the call sites of changed public symbols, the dependencies between the modules involved, and the context items about architecture.
- When an extended review is due and the request has no snapshot, plumb SHALL review what it has and state in the result that an extended review needs a snapshot.

#### Scenario: An extended review without a snapshot says what it lacks
- **Given** a change that changes a public contract and a request without a snapshot
- **When** plumb reviews it
- **Then** the result states that an extended review needs a snapshot
- **And** the findings come from the diff and the changed files alone

### Requirement: Audits on request
Requirement-ID: AUDIT-REQUEST
Operations: submitAudit, getAudit

Whole-project review belongs to audits, not to somebody's pull request.

- plumb SHALL audit a snapshot on request — the whole project, the areas changed since the last audit, or named areas — and return the findings as an audit result.
- plumb SHALL keep audit findings out of every review result.

#### Scenario: A nightly audit covers what changed since the last one
- **Given** an audit last run on revision R1
- **When** the integrator submits an audit of revision R2 for the areas changed since the last audit
- **Then** plumb audits only the areas that differ between R1 and R2
- **And** returns the findings as an audit result

### Requirement: An area audit when escalation calls for it
Requirement-ID: AUDIT-ON-ESCALATION

A large architectural change is checked against the project, not only against its diff.

- When a review's confidence reaches the audit threshold and the request has a snapshot, plumb SHALL audit the affected area without delaying the review result.
- The affected area SHALL be the architecture components the context names for the changed paths and their neighbours one hop out; without such facets, the changed symbols and their callers to the configured depth, found by parsing the snapshot; for a language plumb cannot parse, the top-level modules the change touches and the modules that import them.
- plumb SHALL run one audit for several escalations of the same area within the configured coalescing window.

#### Scenario: The review result does not wait for the audit
- **Given** a review whose confidence reaches the audit threshold and whose request has a snapshot
- **When** plumb completes the review
- **Then** the review result is available while the area audit is still running
- **And** the result says that an audit of the area has started

### Requirement: A disputed finding is checked once more
Requirement-ID: DIALOG-REVERIFY
Operations: postFeedback, getChange

A reply with an argument deserves a second look, not a debate.

- When a maintainer or member replies to a finding with an argument against it, plumb SHALL verify the finding once more with the reply as added context.
- plumb SHALL record the result on the change as a follow-up — withdrawn, with a short explanation, or upheld, with its evidence — for the integrator to show.
- plumb SHALL NOT verify the same finding a third time.

#### Scenario: A finding withdrawn after a good argument
- **Given** a finding about a missing null check
- **When** a maintainer replies that the value is validated in the caller and names the caller
- **And** the second verification confirms it
- **Then** the change's state shows the finding as withdrawn with a short explanation

### Requirement: Every returned finding gets an outcome
Requirement-ID: LEARN-OUTCOMES
Operations: postFeedback, getChange

What happens to a finding is the only honest measure of whether it helped.

- plumb SHALL record one outcome for every returned finding: touched, when the lines it points at or their enclosing function changed in a later revision; confirmed addressed, when it was touched and the final revision of the change no longer produces a finding with the same identity; dismissed, when a maintainer or member rejected it in a reply or resolved its thread without a code change; or unanswered, when the change closed with none of these.
- plumb SHALL ignore replies and thread states from outside contributors and bots.

#### Scenario: A fix counts as confirmed addressed
- **Given** a finding that points at lines 40 to 42 of a file
- **When** a later revision alters those lines, the review of the final revision no longer produces the finding, and the change is merged
- **Then** the finding's outcome is confirmed addressed

#### Scenario: A refactor that keeps the defect is only touched
- **Given** a finding that points at lines 40 to 42 of a file
- **When** a later revision reformats the enclosing function and the review of the final revision still produces the finding
- **Then** the finding's outcome is touched, not confirmed addressed

#### Scenario: An outside contributor cannot dismiss a finding
- **Given** a returned security finding
- **When** the change's author, whom the integrator reports as an outside contributor, replies that it is wrong
- **Then** the finding's outcome is not dismissed

### Requirement: What a reply means decides what is learned
Requirement-ID: LEARN-REPLIES

"Not critical" and "not relevant" are different answers and teach different things.

- plumb SHALL classify each reply from a maintainer or member as agreed, false positive, true but minor, a convention of this place, later, or a question.
- A false positive or a convention of this place SHALL count towards withholding rules; true but minor SHALL count only towards downgrading rules; later and questions SHALL count towards neither.

#### Scenario: "Not critical" downgrades but never withholds
- **Given** four replies classified true but minor to similar findings
- **When** plumb forms rule candidates
- **Then** any candidate from them downgrades such findings
- **And** none withholds them

### Requirement: The usefulness figure is measured, not claimed
Requirement-ID: LEARN-METRIC
Operations: getReport

A team sees in one figure, with its counts, whether plumb is worth its findings.

- plumb SHALL report, per project and per category, the share of returned findings whose outcome is confirmed addressed over a rolling window, with the counts behind the share and the count of findings only touched.
- When the integrator reports human review comments, plumb SHALL report the same share for them, measured the same way, as the baseline.

#### Scenario: The report shows the share and its counts
- **Given** 40 findings returned in the window, of which 22 were confirmed addressed
- **When** a maintainer reads the report
- **Then** it shows 55% confirmed addressed, from 22 of 40 findings

### Requirement: Rule candidates come from repeated, similar dismissals
Requirement-ID: LEARN-RULE-CANDIDATES

A pattern, not a single complaint, is what plumb learns from.

- plumb SHALL form a rule candidate when the structurally similar dismissals in one project reach the configured minimum, from at least the configured number of distinct people, within the configured window.
- plumb SHALL compare dismissals in two stages: first group them by category or rule, path scope and the syntax shape of the lines, then compare the meaning of the claims inside a group by embedding, against the configured threshold — never by wording alone.

#### Scenario: A candidate is no wider than its evidence
- **Given** three dismissed findings about null checks in DTO mappers under `src/api/dto/`, from two maintainers
- **When** plumb forms a candidate from them
- **Then** the candidate covers null checks in DTO mappers under `src/api/dto/` only

### Requirement: A critic and a replay before any rule takes effect
Requirement-ID: LEARN-RULE-VALIDATION

A rule that hides real defects is worse than noise.

- A rule critic SHALL reject a candidate that is broader than its evidence, conflicts with an explicit rule, or touches a protected category.
- plumb SHALL replay every candidate the critic accepts on stored requests, and SHALL reject or narrow it when it would have withheld a finding that was later addressed at or above the configured severity.

#### Scenario: A candidate that would have hidden a real defect is rejected
- **Given** a candidate that, on stored requests, would have withheld one finding that was later addressed with severity high
- **When** the replay finishes
- **Then** the candidate is rejected or narrowed so that it no longer withholds that finding

### Requirement: Shadow mode, activation and review of learned rules
Requirement-ID: LEARN-RULE-LIFECYCLE
Operations: listRules, decideRule

A learned rule earns its place and keeps having to.

- A validated candidate SHALL first run in shadow mode for the configured number of reviews, recording what it would have withheld without withholding anything.
- After shadow mode, a rule that only downgrades findings within a path scope or a layer SHALL activate by itself; a rule that withholds findings, or covers the whole project, SHALL wait for a maintainer's decision. A project MAY make every rule wait, or none.
- plumb SHALL return an active rule to shadow mode after the configured number of days, and at once when a reported missed defect matches it.
- plumb SHALL list every rule with its status and provenance.

#### Scenario: A withholding rule waits for a maintainer
- **Given** the default, risk-based approval mode
- **When** a rule that withholds findings completes shadow mode
- **Then** the rule's status is awaiting decision
- **And** it withholds nothing until a maintainer accepts it

#### Scenario: A narrow downgrade activates by itself
- **Given** the default, risk-based approval mode
- **When** a rule that only downgrades findings under `src/api/dto/**` completes shadow mode
- **Then** the rule becomes active without a maintainer's decision

### Requirement: Learned rules can only quiet plumb down
Requirement-ID: LEARN-RULE-EFFECTS

Learning must never become a way to switch safety off.

- A learned rule SHALL only withhold or downgrade findings, and SHALL NOT add a check.
- A learned rule SHALL NOT apply to a protected category. The protected categories — security, data loss and concurrency by default — SHALL change only through an explicit configuration change, and security and data loss SHALL stay protected whatever a configuration says.
- A learned rule SHALL apply only in the project it was learned in.

#### Scenario: Dismissals do not silence a security finding
- **Given** three dismissed findings about building SQL by string concatenation
- **When** a later revision introduces the same pattern and verification confirms it
- **Then** plumb returns the finding

### Requirement: A new way of reviewing must beat the current one on history
Requirement-ID: LEARN-GATE
Operations: listConfigurations, activateConfiguration

plumb improves by trying changes on stored requests, never on live ones.

- plumb SHALL switch to a new configuration — prompts, models, thresholds or rules — only after replaying it on a sample of stored requests with known outcomes: stratified by category and size, of the configured size, with every reported miss in it, and within the configured cost limit.
- The candidate SHALL lose no confirmed addressed finding of high or critical severity and add no miss, and SHALL improve the utility — confirmed addressed, less the configured weight of dismissed and of missed findings — by at least the configured amount, with the lower bound of its bootstrap interval above zero.
- plumb SHALL keep every previous configuration, and SHALL make any of them active again when a maintainer asks.

#### Scenario: A candidate configuration that adds noise is rejected
- **Given** a candidate configuration that, on stored requests, returns the same addressed findings as the active one and four more that were dismissed
- **When** the replay finishes
- **Then** the active configuration stays in use
- **And** the replay result names the four extra findings

#### Scenario: A trade worth making is accepted
- **Given** a candidate configuration that, on the replay sample, adds five confirmed addressed findings and one dismissed finding, loses no high or critical finding and adds no miss
- **When** the replay finishes and the gain holds across the bootstrap
- **Then** the candidate becomes the active configuration

#### Scenario: A maintainer returns to an earlier configuration
- **Given** configuration 7 is active and configuration 6 preceded it
- **When** a maintainer makes configuration 6 active
- **Then** the next review runs under configuration 6

### Requirement: Learn from what was missed
Requirement-ID: LEARN-MISSED
Operations: postFeedback

Silence is only a virtue when nothing was there to find.

- plumb SHALL accept a report that a reviewed change contained a defect plumb did not return, with its file and lines.
- plumb SHALL add each reported miss to the stored requests that replays use, and count it as missed for every configuration that does not find it.

#### Scenario: A reported miss joins the replay set
- **Given** a merged change that plumb reviewed without findings
- **When** a maintainer reports a defect in it that plumb did not return
- **Then** the next replay includes that change
- **And** counts the defect as missed for every configuration that does not find it

### Requirement: The depth confidence is calibrated on outcomes
Requirement-ID: LEARN-DEPTH-CALIBRATION

A confidence is only worth its number if the number comes true.

- plumb SHALL record every depth decision with its confidence and whether the extended review or audit it led to returned a finding that was later addressed.
- plumb SHALL recalibrate each project's escalation thresholds from those records through the replay gate, unless a person pinned them.
- plumb SHALL give the configured share of normal reviews an extended review in shadow mode, recorded but never returned, to measure what triage misses.

#### Scenario: An exploratory extended review is recorded, not returned
- **Given** an exploration rate of 5%
- **When** a normal review is chosen for exploration
- **Then** plumb also runs an extended review of the same request
- **And** the result returned to the integrator contains only the normal review's findings

### Requirement: Any model, chosen per step
Requirement-ID: MODEL-CHOICE

No team is locked into one model vendor.

- plumb SHALL let a project choose, for each step that uses a model — triage, reading context, proposing, verifying, classifying replies, criticising rules and comparing findings — the provider, the model and the connection profile, including self-hosted endpoints, through configuration alone.
- A connection profile SHALL be named in the project configuration and defined only in the model gateway's deployment configuration, as an endpoint and a reference to a secret the gateway resolves itself, so that no endpoint credential ever passes through the contract or is stored by plumb.

#### Scenario: Different models for proposing and verifying
- **Given** a configuration that names one provider's model for proposing and a self-hosted model for verifying
- **When** plumb reviews a change
- **Then** candidates are proposed by the first model and verified by the self-hosted one
