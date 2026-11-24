# Vendor-backed coding-agent CLIs used for AI code review (Codex CLI, Gemini CLI / Qwen Code, Claude Code GitHub Action and others), state as of 2026-11-23

Method note: repo stats come from the GitHub REST API, queried 2026-11-23. Prompts and workflows were read straight from shallow clones of each repo's default branch on 2026-11-23. Issue dates and titles come from GitHub search. Community reports come from HN (via Algolia), vendor docs and blogs. Reddit's API returned HTTP 403, so Reddit is covered only second-hand. Vendor numbers are labelled as claims.

## 1. OpenAI Codex: the OSS Codex CLI `/review`, `openai/codex-action`, and the proprietary Codex cloud GitHub reviews

### Takeaway
OpenAI has the most complete review stack, but it is split in two. The open-source part (Apache-2.0) is the Codex CLI `/review` command and the `openai/codex-action` CI wrapper. The `/review` prompt is public: it tags findings P0–P3, adds a confidence score and a patch-correctness verdict, and ties rules to AGENTS.md. The PR bot most people mean by "Codex review" (`@codex review` or automatic reviews) is a proprietary ChatGPT/Codex cloud feature running proprietary GPT-5.x-Codex models. OpenAI says these models were trained for precision over recall (its own claim). Users praise the low noise of `/review` but report reliability and usage-limit problems with the cloud GitHub integration in 2026: fork PRs ignored, stuck reviews, noisy progress comments, and false "usage limit" errors.

### Cited Findings

#### What is open source and what is not (as of 2026-11-23)
- `openai/codex`: Apache-2.0, 136,138 stars, created 2025-04-13, latest release `rust-v0.171.0` on 2026-11-20. — [GitHub repo](https://github.com/openai/codex)
- `openai/codex-action`: Apache-2.0, 1,310 stars, created 2025-10-01, last push 2026-11-18. It has no GitHub Release objects and is consumed as `openai/codex-action@v1`. — [GitHub repo](https://github.com/openai/codex-action), [README](https://github.com/openai/codex-action/blob/main/README.md)
- The hosted GitHub review (`@codex review`, automatic review) is part of Codex cloud / ChatGPT plans, not the OSS repo. API-key users get "No cloud-based features (GitHub code review, Slack, etc.)". — [Codex pricing page (redirect target of developers.openai.com/codex/pricing)](https://learn.chatgpt.com/docs/pricing)
- The models are proprietary. OpenAI says it trained a dedicated agentic reviewer "as part of gpt-5-codex and gpt-5.1-codex-max" (vendor statement, 2025-12-01). — [OpenAI, "A Practical Approach to Verifying Code at Scale"](https://openai.com/safety-alignment/scaling-code-verification/)
- Naming trap: Codex also has an "auto-review"/Guardian feature that reviews tool-approval requests, not code. Issue [#21928](https://github.com/openai/codex/issues/21928) (2026-05-09) reports that this approval reviewer fails on Azure/Foundry because the `codex-auto-review` model "is not deployable". Do not confuse it with PR review.

#### How CLI `/review` works under the hood (read from source, 2026-11-23)
- Four review targets: `uncommittedChanges`, `baseBranch`, `commit` (sha + optional title) and `custom` (free-form instructions). — [ReviewTarget.ts](https://github.com/openai/codex/blob/main/codex-rs/app-server-protocol/schema/typescript/v2/ReviewTarget.ts)
- For a base branch, Codex computes the merge-base and tells the model to run `git diff <merge_base_sha>`. For uncommitted work it covers staged, unstaged and untracked files. Every prompt asks for "prioritized, actionable findings". — [review_request.rs](https://github.com/openai/codex/blob/main/codex-rs/prompts/src/review_request.rs)
- The review runs as a separate sub-agent with its own context and with the approval policy forced to "never". The model is the `review_model` config value if set, otherwise the session model. — [tasks/review.rs](https://github.com/openai/codex/blob/main/codex-rs/core/src/tasks/review.rs), [config/mod.rs (`review_model`)](https://github.com/openai/codex/blob/main/codex-rs/core/src/config/mod.rs)
- The review system prompt (rubric) allows flagging only bugs that:
  - were introduced by the change (pre-existing bugs are excluded);
  - are discrete and actionable;
  - do not rely on unstated assumptions;
  - can be shown to affect other code (speculation is not enough).
- Rubric rules for comments: at most one paragraph, code snippets of three lines or fewer, no flattery, severity not overstated. On volume, if nothing qualifies the model should "prefer outputting no findings". — [rubric.md](https://github.com/openai/codex/blob/main/codex-rs/prompts/templates/review/rubric.md)
- Prioritisation: each title is tagged [P0]–[P3]. P0 means "drop everything", reserved for issues that do not depend on assumptions about inputs. Each finding has a numeric `priority`, a `confidence_score` (0–1) and a `code_location` that must overlap the diff. The JSON output also carries `overall_correctness` ("patch is correct/incorrect") and `overall_confidence_score`. — [rubric.md](https://github.com/openai/codex/blob/main/codex-rs/prompts/templates/review/rubric.md)
- AGENTS.md integration (the rubric's "Repository Rule Attribution" section):
  - The reviewer reads root and scoped instruction files in precedence order: `AGENTS.override.md`, then `AGENTS.md`, then configured fallback names. The more specific file wins.
  - A finding backed by a rule must cite the instruction file and the smallest supporting line range.
  - The rubric also says not to invent findings just because a rule file exists.
  - Source: [rubric.md](https://github.com/openai/codex/blob/main/codex-rs/prompts/templates/review/rubric.md)
- OpenAI reviews its own repo with codex-action using a label-triggered prompt. The prompt asks for a 1–2 sentence summary plus a short review in a "friendly tone". — [.github/codex/labels/codex-review.md](https://github.com/openai/codex/blob/main/.github/codex/labels/codex-review.md)

#### `openai/codex-action`: how it is deployed in CI
- The action installs the Codex CLI and starts a "secure proxy to the Responses API", so the API key is held by the proxy. It needs an OpenAI key or an Azure OpenAI key; there is no ChatGPT-subscription auth. — [README](https://github.com/openai/codex-action/blob/main/README.md); subscription auth requested in [#27](https://github.com/openai/codex-action/issues/27) (2025-10-07, open, 33 reactions)
- The reference "PR bot" uses two jobs:
  - The Codex job has `contents: read`, checks out the PR merge commit, fetches base and head refs, and runs `codex exec` with a prompt. The prompt uses `git log base...head` and asks for concise feedback.
  - A second job with `pull-requests: write` posts `final-message` with `actions/github-script`.
  - Source: [README](https://github.com/openai/codex-action/blob/main/README.md)
- Hardening inputs:
  - `permission-profile` (`:workspace` or `:read-only`).
  - `safety-strategy`, default `drop-sudo` (alternative `unprivileged-user`).
  - `allow-users`, `allow-bots` and `allow-bot-users`; by default only users with write access can trigger.
  - `output-schema` for structured output, plus `model` and `effort`.
  - The `:workspace` profile has no network access, so dependencies must be installed before the Codex step if it should build or test.
  - Source: [README](https://github.com/openai/codex-action/blob/main/README.md)
- The README itself points teams to the cloud reviewer first: "While Codex cloud offers a powerful code review tool… build your own… if you want more control." — [README](https://github.com/openai/codex-action/blob/main/README.md)
- codex-action complaints:
  - [#28](https://github.com/openai/codex-action/issues/28) (2025-10-07): how to use Azure OpenAI.
  - [#32](https://github.com/openai/codex-action/issues/32) (2025-10-09): GitHub Enterprise support.
  - [#48](https://github.com/openai/codex-action/issues/48) (2025-11-04): API base URL override.
  - [#49](https://github.com/openai/codex-action/issues/49) (2025-11-04): bots/GitHub Apps could not trigger reviews.
  - [#66](https://github.com/openai/codex-action/issues/66) (2026-01-15): a new Codex version broke the action.
  - [#75](https://github.com/openai/codex-action/issues/75) (2026-03-17): the action suddenly could not read git log/diff.
  - [#150](https://github.com/openai/codex-action/issues/150) (2026-08-21): v1.12 Linux run never returns after the turn; the job dies on timeout even though output was written.
  - [#169](https://github.com/openai/codex-action/issues/169) (2026-08-31): CLI 0.150.1 still hangs after the final output.

#### Codex cloud GitHub reviews (proprietary hosted feature)
- Setup: connect the repo in Codex, then turn on "Automatic review", or set a personal "Review trigger".
- A `@codex review` comment gets a 👀 reaction and then "a standard GitHub code review". Focus text is allowed, e.g. "@codex review for issues in the database migration".
- "Codex flags only P0 and P1 issues" in GitHub reviews.
- Repo rules live in an AGENTS.md `## Code Review Rules` section. Nested AGENTS.md files add per-service rules on top of the root ones. OpenAI advises starting with 2–3 concise rules and leaving lint and format checks to CI.
- A separate Security Review (research preview) is triggered by `@codex security review`.
- Source for all of the above: [Codex GitHub integration docs (redirect target of developers.openai.com/codex/cloud/code-review)](https://learn.chatgpt.com/docs/third-party/github)
- Usage: reviews run through GitHub are tracked as a separate "Code Review usage" bucket; local reviews count toward general usage. Plus lists "automatic code review"; API-key users get no cloud review. The page gives no per-plan review counts. — [Codex pricing](https://learn.chatgpt.com/docs/pricing)
- At launch (2025-09-15) automatic reviews ran when a PR moved from draft to ready. Users could then ask Codex in the same thread to implement fixes. — [OpenAI, "Introducing upgrades to Codex"](https://openai.com/index/introducing-upgrades-to-codex/)

#### OpenAI's claims about review-tuned models (vendor claims, not independently verified)
- 2025-09-15: GPT-5-Codex "has been trained specifically for code review". Comments were evaluated by experienced engineers on recent commits from popular OSS repos and were judged "less likely to be incorrect or unimportant". Codex reviews the "vast majority" of OpenAI PRs, "catching hundreds of issues every day". OpenAI says it reasons over the codebase and runs code and tests, unlike static analysis. — [OpenAI blog](https://openai.com/index/introducing-upgrades-to-codex/)
- Chart figures reported by the press for the same launch: incorrect comments 13.7% (GPT-5 high) vs 4.4% (GPT-5-Codex); high-impact comments about 39% vs about 52%. — [eWeek](https://www.eweek.com/news/openai-gpt-5-codex-update/), [The New Stack](https://thenewstack.io/openai-launches-a-new-gpt-5-model-for-its-codex-coding-agent/). I could not read the numbers off OpenAI's page, as the chart appears to be an image.
- 2025-12-01 alignment post (vendor):
  - "Precision is more important for usability than recall." OpenAI accepted "modestly reduced recall in exchange for high signal quality and developer trust".
  - More than 100k external PRs per day were reviewed as of Oct 2025.
  - 52.7% of comments led to a code change.
  - Over 80% of reactions to comments were positive.
  - Codex commented on 36% of fully Codex-generated PRs.
  - Diff-only review is fastest but misses context. Adding repo access and code execution "caught more critical issues and raised fewer false alarms".
  - GPT-5.1-Codex improves recall and precision over GPT-5.
  - Recall drops faster on model-generated code when the thinking budget is cut.
  - OpenAI also warns against treating a clean review as a guarantee.
  - Source: [OpenAI alignment blog](https://openai.com/safety-alignment/scaling-code-verification/)

#### Independent user reports: praise
- [#5547](https://github.com/openai/codex/issues/5547) (2025-10-23, 87 reactions, open): "`/review` is just amazing". The isolated context is praised and it "rarely flags non-issues". The request is to make the number of issues configurable.
- HN, 2026-10-11: `codex /review` often "comes back satisfied on the first shot"; the team does one LLM review round. — [HN comment](https://news.ycombinator.com/item?id=50038462)
- HN, 2026-07-09: having Codex review Claude-written code finds important gaps, and the reverse also works. — [HN comment](https://news.ycombinator.com/item?id=48849267)
- HN, 2026-09-14: "remarkably good results" running recent OpenAI models in the codex-rs harness on a built checkout of the PR. The models use the shell to understand the repo; there are some false positives and negatives; the commenter says the harness matters more than the model. — [HN comment](https://news.ycombinator.com/item?id=49705452)

#### Complaints, with dates and links
- Missed bugs: in a planted-fault "canary" PR with five faults, Codex review found three and missed a bug and a security hole, for the second time in a row. — [HaakTuah/barkstreet-snakes #528](https://github.com/HaakTuah/barkstreet-snakes/issues/528) (2026-11-06)
- Reviews that never end: with `@codex review` on a codebase of any size, asking for things to fix always yields more findings, so review loops may not terminate. — [HN comment](https://news.ycombinator.com/item?id=49134039) (2026-08-01)
- Fork PRs: `@codex review` silently ignores PRs from forks, while same-repo PRs work; fork reviews reportedly worked until 2026-09-20. — [#47577](https://github.com/openai/codex/issues/47577) (2026-09-23, 33 reactions, open)
- Stuck reviews: a manual `@codex review` stayed "Running" after 👀 and no review was submitted. — [#55890](https://github.com/openai/codex/issues/55890) (2026-10-21, closed). Older case: Codex only reacted with 👀 and posted nothing. — [#3808](https://github.com/openai/codex/issues/3808) (2025-09-17)
- Noise from progress comments: a new top-level "Codex Review Summary" status comment creates notification and automation noise; before, the flow was 👀 followed by the review. — [#42478](https://github.com/openai/codex/issues/42478) (2026-09-03, open)
- Usage limits: `@codex review` is blocked with a usage-limit error while the linked dashboard shows quota available and zero review activity. — [#31001](https://github.com/openai/codex/issues/31001) (2026-07-03, 16 comments, open)
- General quota anger in the same period (not review-specific):
  - [#14593](https://github.com/openai/codex/issues/14593) "Burning tokens very fast" (2026-03-13, 630 comments).
  - [#28879](https://github.com/openai/codex/issues/28879): rate-limit cost per token jumped about 10–20x (2026-06-18).
- Configurability and missing features:
  - Custom-instructions input for code review: [#10874](https://github.com/openai/codex/issues/10874) (2026-02-06, 31 reactions).
  - Review of draft PRs: [#40721](https://github.com/openai/codex/issues/40721) (2026-08-25).
  - Reviews surfaced as GitHub Check Runs: [#27691](https://github.com/openai/codex/issues/27691) (2026-06-11).
  - Automatic review not triggering on GitHub-native stacked PRs: [#42698](https://github.com/openai/codex/issues/42698) (2026-09-04).
  - No org-wide automatic-review policy: [#61318](https://github.com/openai/codex/issues/61318) (2026-11-13).
- CLI `/review` reliability: `/review` hung on "Starting MCP servers (1/2): codex_apps". — [#18792](https://github.com/openai/codex/issues/18792) (2026-04-21, closed)
- Refusals that hit security review:
  - Codex Security refused defensive review of legacy DSA code. — [HN comment](https://news.ycombinator.com/item?id=49095084) (2026-07-29)
  - Codex refused to run its own tests over a cybersecurity false positive. — [HN comment](https://news.ycombinator.com/item?id=49679642) (2026-09-13)

### Inferences
- OpenAI's design (P0–P3 tags, "prefer no findings", and only P0/P1 posted in GitHub) explicitly targets the noise complaint. Users largely back this for CLI `/review`. 2026 complaints shift from noise to operations: triggers, forks, quotas, progress-comment noise.
- What OSS adopters get: the reviewer prompt, the review loop and the CI plumbing are inspectable and forkable. The best-tuned behaviour still depends on proprietary GPT-5.x-Codex models via API key (billed per token), since codex-action has no subscription auth.
- The cloud reviewer is billed through ChatGPT plans with a separate "Code Review usage" bucket, so cost is opaque per PR. That opacity is a plausible source of the confusion in #31001.

### Gaps
- No independent, systematic precision/recall numbers for Codex review were found; the evidence is OpenAI's own numbers plus anecdotes.
- No authoritative per-PR latency figures for Codex cloud reviews were found.
- Per-plan review quotas are not published on the pricing page (checked 2026-11-23).
- I could not confirm whether a non-interactive `codex review`/`codex exec review` subcommand exists for CI: it was not found in the CLI source files I grepped. codex-action uses `codex exec` with a prompt.

## 2. Google Gemini CLI (`run-gemini-cli` PR review, code-review extension), Qwen Code, and the proprietary Gemini Code Assist GitHub app

### Takeaway
Gemini CLI and its review add-ons are Apache-2.0 and still maintained (Gemini CLI v0.70.0 on 2026-11-19). In 2026, however, Google moved consumers to a new Antigravity CLI that the community describes as closed-source. Since 2026-06-18 Gemini CLI serves only enterprise Code Assist users and paid API keys. The Gemini Code Assist GitHub review app stopped taking new consumer installs on the same date. The `run-gemini-cli` review workflow is essentially diff-centric. It fetches the diff through the GitHub MCP server, may comment only on changed lines, and its issue tracker shows recurring "runs but posts nothing" failures. Qwen Code, a Gemini CLI fork, built the most elaborate open-source `/review` pipeline of any tool here (up to about 16 parallel agents, verification, build and test, worktree isolation), with long runtimes as the trade-off.

### Cited Findings

#### OSS status and the 2026 Gemini CLI → Antigravity CLI transition
- `google-gemini/gemini-cli`: Apache-2.0, 108,998 stars, created 2025-04-17, latest `v0.70.0` on 2026-11-19. — [GitHub repo](https://github.com/google-gemini/gemini-cli)
- Google blog, 2026-05-19:
  - Gemini CLI "will stop serving requests" on 2026-06-18 for Google AI Pro/Ultra and free Code Assist individual users.
  - Enterprise Code Assist Standard/Enterprise and "Code Assist for GitHub" via Google Cloud are unchanged.
  - Gemini CLI stays usable through paid Gemini API and Gemini Enterprise Agent Platform keys.
  - Antigravity CLI (Go, sharing the Antigravity 2.0 harness) is available from 2026-05-19.
  - For consumer orgs, the Gemini Code Assist GitHub app takes no new installs from 2026-06-18, and existing requests stop "in the following weeks".
  - The post does not state Antigravity CLI's license; it links github.com/google-antigravity/antigravity-cli only as a feedback forum.
  - Source: [Google Developers Blog](https://developers.googleblog.com/an-important-update-transitioning-gemini-cli-to-antigravity-cli/)
- The Gemini CLI README banner (Nov 2026) reads "Enterprise Code Assist only" and "No free tier or Google AI plans". — [README](https://github.com/google-gemini/gemini-cli/blob/main/README.md)
- Community reaction:
  - "They had Gemini CLI as open-source… then moved to closed-source Antigravity CLI." — [HN](https://news.ycombinator.com/item?id=50160142) (2026-10-20)
  - "Google's Antigravity bait and switch" thread. — [HN](https://news.ycombinator.com/item?id=48223697) (2026-05-21)
  - Issue "Antigravity CLI is a massive downgrade from Gemini CLI for developers" — [#27858](https://github.com/google-gemini/gemini-cli/issues/27858) (2026-06-12, 21 reactions)
  - Secondary write-ups also call Antigravity a closed-source Go binary that can use Gemini, Claude and GPT-OSS models (not verified against Google docs). — [Virtualization Review, 2026-05-19](https://virtualizationreview.com/articles/2026/05/19/google-moves-gemini-cli-into-antigravity-cli-as-agent-platform-expands.aspx), [The New Stack](https://thenewstack.io/gemini-cli-antigravity-replacement/)
- Conflict: the `run-gemini-cli` README (commit of 2026-11-19) still says to get an AI Studio key "with generous free-of-charge quotas". — [run-gemini-cli README](https://github.com/google-github-actions/run-gemini-cli/blob/main/README.md). This contradicts Google's "paid … API keys" wording above. Whether free-tier keys still work in CI is unclear.

#### `google-github-actions/run-gemini-cli`: PR-review workflow and internals
- Apache-2.0, 2,131 stars, created 2025-07-11, latest release `v0.1.22` on 2026-04-24 (no release since the transition), last push 2026-11-19. — [repo](https://github.com/google-github-actions/run-gemini-cli)
- It ships four workflow templates: Dispatch, Issue Triage, PR Review and Assistant. Reviews can also be triggered on demand with `@gemini-cli /review`. `GEMINI.md` supplies project instructions. — [README](https://github.com/google-github-actions/run-gemini-cli/blob/main/README.md)
- The review workflow combines the code-review extension with the GitHub MCP server:
  - Data comes from `pull_request_read.get`, `get_files` and `get_diff`.
  - Comments may touch only `+`/`-` lines; comments on context lines are "strictly forbidden".
  - Command substitution `$(...)` is banned, and PR text is treated as data (anti-prompt-injection).
  - Severities are 🔴 Critical, 🟠 High, 🟡 Medium and 🟢 Low.
  - The model must not comment on dates or license headers, and must not post duplicate comments.
  - Source: [gemini-review.toml](https://github.com/google-github-actions/run-gemini-cli/blob/main/examples/workflows/pr-review/gemini-review.toml)
- The PR-review README advertises severity-ranked feedback, "positive highlights", custom instructions and a failure-notification comment. Fork support is not built in; there is a section on extending to forks, including via `pull_request_target`. — [PR review README](https://github.com/google-github-actions/run-gemini-cli/blob/main/examples/workflows/pr-review/README.md)
- The repo carries PR-review evals ([evals/pr-review.eval.ts](https://github.com/google-github-actions/run-gemini-cli/blob/main/evals/pr-review.eval.ts)). Users asked for README docs on running them in [#463](https://github.com/google-github-actions/run-gemini-cli/issues/463) (2026-02-12).
- Complaints (2025 items are early-launch history):
  - [#134](https://github.com/google-github-actions/run-gemini-cli/issues/134) (2025-08-07): PR review often fails with "Could not parse tool response".
  - [#137](https://github.com/google-github-actions/run-gemini-cli/issues/137) (2025-08-07) and [#277](https://github.com/google-github-actions/run-gemini-cli/issues/277) (2025-09-13): the review runs but no comment is posted.
  - [#151](https://github.com/google-github-actions/run-gemini-cli/issues/151) (2025-08-08): the model confuses line numbers and the old/new sides of diffs.
  - [#132](https://github.com/google-github-actions/run-gemini-cli/issues/132) (2025-08-07): fallback to gemini-2.5-flash not respected; requests still go to Pro.
  - [#123](https://github.com/google-github-actions/run-gemini-cli/issues/123) (2025-08-06): 401 with Workload Identity Federation.
  - [#258](https://github.com/google-github-actions/run-gemini-cli/issues/258) (2025-09-03) and [#497](https://github.com/google-github-actions/run-gemini-cli/issues/497) (2026-04-03, open): Cloud Code Private API error with Code Assist + WIF.
  - [#337](https://github.com/google-github-actions/run-gemini-cli/issues/337) (2025-09-30): freezes at startup in sandbox mode.
  - [#213](https://github.com/google-github-actions/run-gemini-cli/issues/213) (2025-08-21, open): request to show token usage in the comment.
  - [#425](https://github.com/google-github-actions/run-gemini-cli/issues/425) (2025-12-16, 19 comments, open): the PR-review workflow fails for missing repository/PR context.
  - [#519](https://github.com/google-github-actions/run-gemini-cli/issues/519) (2026-05-14, open): "silent success" with zero review output when several auth methods are set.

#### Gemini CLI code-review extension (official, Apache-2.0)
- `gemini-cli-extensions/code-review`: 537 stars, created 2025-09-09, last push 2026-03-10, no releases. It is built "by the authors of the Gemini Code Assist GitHub App". `/code-review` reviews the current branch. `/pr-code-review` reviews a PR through the GitHub MCP server, configured with `REPOSITORY`, `PULL_REQUEST_NUMBER` and `ADDITIONAL_CONTEXT`. Requires Gemini CLI ≥ 0.4.0. — [repo/README](https://github.com/gemini-cli-extensions/code-review)
- Internals: a `code-review-commons` skill holds the persona and constraints. The flow creates a pending review, adds `[SEVERITY]` comments with optional `suggestion` blocks, then submits. — [pr-code-review.toml](https://github.com/gemini-cli-extensions/code-review/blob/main/commands/pr-code-review.toml)
- Issues:
  - [#16](https://github.com/gemini-cli-extensions/code-review/issues/16) (2025-12-27): reviews the repo instead of the diff.
  - [#17](https://github.com/gemini-cli-extensions/code-review/issues/17) (2026-01-07): asks to focus only on branch/remote changes.
  - [#12](https://github.com/gemini-cli-extensions/code-review/issues/12) (2025-10-09): asks for precise diff parsing.
  - [#22](https://github.com/gemini-cli-extensions/code-review/issues/22) (2026-03-12): no GitLab support.
  - [#4](https://github.com/gemini-cli-extensions/code-review/issues/4) (2025-09-24): asks for other source-control support.
- Sibling `gemini-cli-extensions/security` (Apache-2.0, 794 stars, `v0.5.0` on 2026-04-01) "finds vulnerabilities in your code changes and pull requests". — [repo](https://github.com/gemini-cli-extensions/security)
- The Gemini CLI team dogfoods review skills in its own repo: `.gemini/skills/code-reviewer`, `async-pr-review`, `review-duplication`, and the command `.gemini/commands/oncall/pr-review.toml`. — [gemini-cli .gemini/skills](https://github.com/google-gemini/gemini-cli/tree/main/.gemini/skills)

#### Contrast: Gemini Code Assist GitHub app (proprietary)
- `/gemini review` and `/gemini summary` commands; `.gemini/config.yaml` supports:
  - `comment_severity_threshold`;
  - `max_review_comments` (default −1, unlimited);
  - `pull_request_opened` toggles for the help message, summary and review;
  - `include_drafts` (default true);
  - plus `.gemini/styleguide.md`.
  - Source: [Google docs: customize Gemini Code Assist on GitHub](https://developers.google.com/gemini-code-assist/docs/customize-gemini-behavior-github)
- 2025 user note (historical): Gemini Code Assist adds many PR comments, which can "blow the context window" of an agent reading the PR. — [HN](https://news.ycombinator.com/item?id=45387723) (2025-09-26)
- Consumer availability ends from 2026-06-18; enterprise via Google Cloud continues. — [Google blog](https://developers.googleblog.com/an-important-update-transitioning-gemini-cli-to-antigravity-cli/)

#### Qwen Code (QwenLM/qwen-code, Gemini CLI fork)
- Apache-2.0, 30,868 stars, created 2025-06-26, latest `v0.28.4` on 2026-11-22. — [repo](https://github.com/QwenLM/qwen-code)
- It is based on Gemini CLI v0.8.2 and has diverged since Qwen Code v0.1. It supports OpenAI, Anthropic, Gemini and Qwen APIs, plus local Ollama/vLLM models, switchable at runtime. — [README](https://github.com/QwenLM/qwen-code/blob/main/README.md)
- `/review` (vendor docs, Nov 2026):
  - Targets: local diff, PR (number or URL), or a file.
  - Flags: `--comment` (inline PR comments; forces high effort), `--fix`, `--resume`.
  - `--effort low|medium|high`:
    - `low`: inline passes, no subagents, unverified, findings capped at 10.
    - `high`: up to about 16–19 parallel agents (correctness ×5 variants, security, quality ×3, performance, tests, three "attacker/3am-oncall/maintainer" personas, build & test). Then sharded verification (≤8 findings per verifier) and iterative "reverse audit" until two dry rounds.
  - Large PRs (>500 source lines or >3,200 diff lines) switch to ~400-line territory chunks, plus invariant agents for heavily rewritten files.
  - Runs in an isolated git worktree with dependencies installed.
  - Every finding must state a concrete failure scenario. Low-confidence findings are never posted.
  - Source: [docs/users/features/code-review.md](https://github.com/QwenLM/qwen-code/blob/main/docs/users/features/code-review.md)
- Repo-specific rules come from `.qwen/review-rules.md`, `.github/copilot-instructions.md`, the AGENTS.md `## Code Review` section, the QWEN.md `## Code Review` section, and a `.qwen/review-context.json` manifest. — [code-review.md](https://github.com/QwenLM/qwen-code/blob/main/docs/users/features/code-review.md)
- Runtime is long by design. The docs mention "five ~90-minute rounds" that do not fit a 6-hour CI ceiling. Default deadlines are 8, 12 or 16 hours depending on diff size. — [code-review.md](https://github.com/QwenLM/qwen-code/blob/main/docs/users/features/code-review.md)
- QwenLM reviews its own PRs with it: the workflow uses `pull_request_target`, comment and review events, `review`/`resolve` commands, dry-run vs comment modes, and a timeout. — [qwen-code-pr-review.yml](https://github.com/QwenLM/qwen-code/blob/main/.github/workflows/qwen-code-pr-review.yml)
- Design docs show an "Aone" provider (Alibaba's internal code platform) alongside GitHub. — [docs/design/2026-08-15-review-aone-provider.md](https://github.com/QwenLM/qwen-code/blob/main/docs/design/2026-08-15-review-aone-provider.md)
- `QwenLM/qwen-code-action` (a structural clone of run-gemini-cli): 43 stars, `v0.1.1` on 2025-12-05, last push 2026-08-03. — [repo](https://github.com/QwenLM/qwen-code-action)
- Issues:
  - [#2346](https://github.com/QwenLM/qwen-code/issues/2346) (2026-03-13): origin of the bundled `/review` skill.
  - [#12193](https://github.com/QwenLM/qwen-code/issues/12193) (2026-09-18): the "reviewed" skip anchor is not scoped by PR or base ref.
  - [#13586](https://github.com/QwenLM/qwen-code/issues/13586) (2026-10-07): no Bitbucket support.
  - [#15447](https://github.com/QwenLM/qwen-code/issues/15447) (2026-10-24): review-pr checks fail after a completed review on CI hosts.
  - [#15507](https://github.com/QwenLM/qwen-code/issues/15507) (2026-10-25): need to protect the reviewed worktree from in-place edits during review.

### Inferences
- As of Nov 2026 the open-source Gemini review path (Gemini CLI + run-gemini-cli + code-review extension) is in maintenance or uncertain status for non-enterprise users. The action has had no release since April 2026, and Google's consumer focus moved to a closed CLI. New adopters should check auth and quota before building on it.
- run-gemini-cli review is mostly diff-only: it fetches the diff via MCP, the comment scope is restricted to changed lines, and fork support is not built in. It therefore sits closer to "diff bot" than "agentic reviewer", even though the agent technically has tools.
- Qwen Code is the most model-agnostic OSS harness here, with the most ambitious review pipeline. The cost is complexity and multi-hour runtimes; I found no independent quality reports.

### Gaps
- I found no independent quality evaluation (precision, false-positive rate) of run-gemini-cli or the Gemini code-review extension, and no HN/Reddit threads specifically about them (an HN Algolia search returned zero comments).
- Whether free AI Studio keys still work with Gemini CLI in CI after 2026-06-18 is unresolved: the README and Google's blog conflict.
- I could not verify Antigravity CLI's license from a Google primary source.
- I found no usage numbers (installs, reviews per day) for any Gemini or Qwen review path.

## 3. Anthropic: `claude-code-action` (MIT) on top of the proprietary Claude Code CLI, `claude-code-security-review`, review plugins and commands, and the managed "Code Review" service

### Takeaway
Anthropic's open-source review surface consists of thin or plugin layers: the MIT GitHub Action, the MIT security-review Action and Apache-2.0 review plugins. All of them execute the proprietary Claude Code CLI with proprietary Claude models. Since 2026-03-09 (GA 2026-10-15) Anthropic also sells a managed multi-agent "Code Review" service for Team and Enterprise. Users criticise it mainly for price: about $15–25 per review at launch (vendor figure), token-billed, and by default triggered on every push.

Complaints about the Action, 2025–2026:
- **Comments:** no sticky or updated comments, and stale context from old or bot comments.
- **Tool permissions:** allowed-tools setup is confusing.
- **Fork PRs:** fork PRs break the action.
- **Stability:** a long series of crashes after SDK or CLI updates.

The security-review Action appears unmaintained: no release, last push 2026-02-11, and its false-positive filter silently disabled by a retired model ID.

### Cited Findings

#### Licensing and OSS status (as of 2026-11-23)
- Claude Code CLI is proprietary: "© Anthropic PBC. All rights reserved," with use under Anthropic's Commercial Terms. The GitHub API detects no license. The repo has 156,678 stars; latest release `v2.1.330` on 2026-11-20. — [LICENSE.md](https://github.com/anthropics/claude-code/blob/main/LICENSE.md), [repo](https://github.com/anthropics/claude-code)
- `anthropics/claude-code-action`: MIT, 10,049 stars, created 2025-05-19, last push 2026-11-21. It ships as a `v1` major tag with v1.0.x patch tags; for example v1.0.218 is cited in [#1817](https://github.com/anthropics/claude-code-action/issues/1817). It is built on `claude-code-base-action` (MIT mirror, 1,062 stars). — [repo](https://github.com/anthropics/claude-code-action), [base-action](https://github.com/anthropics/claude-code-base-action)
- The Action "executes entirely on your own GitHub runner". Auth options are an Anthropic API key or WIF, Bedrock, Vertex AI or Microsoft Foundry. The quickstart is `/install-github-app`, which requires repo admin and direct Anthropic API access. — [README](https://github.com/anthropics/claude-code-action/blob/main/README.md)
- Anthropic plugins now live in `anthropics/claude-plugins-official`; the `claude-code` repo marketplace only lists them. The `code-review` plugin is Apache-2.0. — [plugins/README.md](https://github.com/anthropics/claude-code/blob/main/plugins/README.md), [marketplace.json](https://github.com/anthropics/claude-code/blob/main/.claude-plugin/marketplace.json), [plugin LICENSE](https://github.com/anthropics/claude-plugins-official/blob/main/plugins/code-review/LICENSE)
- Anthropic itself calls the Action the "lighter weight" option that "remains open source", while the managed Code Review is the deeper, pricier one. — [Claude blog, 2026-03-09](https://claude.com/blog/code-review)

#### How review works in `claude-code-action`
- The canonical auto-review workflow:
  - Triggers on `pull_request: [opened, synchronize]` with a prompt.
  - Inline comments go through `mcp__github_inline_comment__create_inline_comment` (`confirmed: true`).
  - Tools are allowlisted with `--allowedTools "mcp__github_inline_comment__create_inline_comment,Bash(gh pr comment:*),Bash(gh pr diff:*),Bash(gh pr view:*)"`.
  - `track_progress: true` adds a checkbox progress comment.
  - Source: [docs/solutions.md](https://github.com/anthropics/claude-code-action/blob/main/docs/solutions.md), [examples/pr-review-comprehensive.yml](https://github.com/anthropics/claude-code-action/blob/main/examples/pr-review-comprehensive.yml)
- Documented limits:
  - It "cannot submit formal GitHub PR reviews" or approve PRs.
  - It acts by updating a single initial comment.
  - For fork PRs it pushes to a `pr-N` branch in your repo, and the fork branch is not updated.
  - In the default "auto mode", a tool call outside the allow rules can still run if a "safety review" passes it; `--permission-mode acceptEdits` gives a strict list.
  - Source: [docs/capabilities-and-limitations.md](https://github.com/anthropics/claude-code-action/blob/main/docs/capabilities-and-limitations.md)
- Anthropic dogfoods multi-agent review in the Action repo: `.claude/agents/{code-quality,documentation-accuracy,performance,security-code}-reviewer.md`, `.claude/commands/review-pr.md` and `.github/workflows/claude-review.yml`. — [repo tree](https://github.com/anthropics/claude-code-action/tree/main/.claude)

#### `claude-code-security-review` (MIT)
- 7,055 stars, created 2025-08-04, last push 2026-02-11, no releases; the README uses `@main`. — [repo](https://github.com/anthropics/claude-code-security-review)
- It runs a Claude Code security analysis of PR changes, followed by a "False Positive Filtering" stage (`findings_filter.py` plus a Claude API client). The default model is `claude-opus-4-1-20250805`. A `run-every-commit` option comes with a warning that it may increase false positives. — [README](https://github.com/anthropics/claude-code-security-review/blob/main/README.md)
- The README says the Action is "not hardened against prompt injection attacks" and should review only trusted PRs, with approval required for external contributors. — [README](https://github.com/anthropics/claude-code-security-review/blob/main/README.md)
- Claude Code ships a `/security-review` slash command with the same analysis. Teams customise it by copying `security-review.md` into `.claude/commands/`. — [README](https://github.com/anthropics/claude-code-security-review/blob/main/README.md)
- Issues:
  - [#139](https://github.com/anthropics/claude-code-security-review/issues/139) (2026-09-07), [#69](https://github.com/anthropics/claude-code-security-review/issues/69) (2026-02-19) and [#88](https://github.com/anthropics/claude-code-security-review/issues/88) (2026-03-25): `validate_api_access()` hardcodes the retired `claude-3-5-haiku-20241022`, which silently disables false-positive filtering or returns 404.
  - [#45](https://github.com/anthropics/claude-code-security-review/issues/45) (2025-10-13): "Make a release".
  - [#37](https://github.com/anthropics/claude-code-security-review/issues/37) (2025-08-25): action pinning.
  - [#42](https://github.com/anthropics/claude-code-security-review/issues/42) (2025-09-23): the cache prevents re-runs after fixes.
  - [#4](https://github.com/anthropics/claude-code-security-review/issues/4) (2025-08-07, 33 reactions): Bedrock auth.
  - [#3](https://github.com/anthropics/claude-code-security-review/issues/3) (2025-08-07): Max-subscription support.

#### Code-review plugins and the built-in `/code-review`
- `code-review` plugin (author Boris Cherny; Apache-2.0), command flow:
  1. A Haiku agent checks eligibility and skips closed, draft, trivial or already-reviewed PRs.
  2. A Haiku agent collects the relevant CLAUDE.md paths.
  3. A Sonnet agent summarises the PR.
  4. Four parallel reviewers run: two Sonnet CLAUDE.md-compliance agents and two Opus bug agents (one diff-only, one on the introduced code).
  5. A validation subagent checks each flagged issue (Opus for bugs, Sonnet for CLAUDE.md), and unvalidated issues are dropped.
  6. With `--comment`, findings are posted as inline comments; committable suggestions are allowed only when they fully fix the issue.
  - It carries an explicit false-positive exclusion list: pre-existing issues, linter-catchable issues, pedantic nits, silenced rules.
  - Source: [commands/code-review.md](https://github.com/anthropics/claude-plugins-official/blob/main/plugins/code-review/commands/code-review.md)
- The plugin README still describes 0–100 confidence scoring with an 80 threshold and a git-blame/history agent. The current command prompt uses validation subagents instead, so the docs have drifted from the prompt. — [README](https://github.com/anthropics/claude-plugins-official/blob/main/plugins/code-review/README.md) vs [command](https://github.com/anthropics/claude-plugins-official/blob/main/plugins/code-review/commands/code-review.md)
- `pr-review-toolkit` plugin: agents `code-reviewer`, `code-simplifier`, `comment-analyzer`, `pr-test-analyzer`, `silent-failure-hunter` and `type-design-analyzer`, plus `/review-pr`. — [plugin dir](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/pr-review-toolkit)
- Plugin feature request: post findings as resolvable PR review threads. — [claude-plugins-official #1708](https://github.com/anthropics/claude-plugins-official/issues/1708) (2026-05-05)
- The built-in `/code-review` is a bundled skill in the proprietary CLI (Nov 2026 docs):
  - `/review` is an alias.
  - Effort levels run from `low` (most confident findings, fewer false positives) to `max`.
  - `ultra` sends the review to a cloud "Ultrareview". That needs a claude.ai account and is unavailable on Bedrock, Vertex or Foundry and for ZDR, HIPAA or CMEK orgs. A `claude ultrareview` subcommand serves CI.
  - Flags: `--fix`, `--comment` (GitHub inline comments, or a single GitLab MR note via `glab` from v2.1.257), `--max-findings`.
  - It follows CLAUDE.md, not REVIEW.md.
  - Source: [Claude Code docs: /code-review](https://code.claude.com/docs/en/code-review-local)
- Built-in command complaints:
  - [#13960](https://github.com/anthropics/claude-code/issues/13960) (2025-12-14): the built-in `/review` stopped working and users were told to install a plugin instead.
  - [#63048](https://github.com/anthropics/claude-code/issues/63048) (2026-05-28): a silent fallback to `main...HEAD` reviews other people's commits, and the JSON-only output is hard to read.
  - [#79560](https://github.com/anthropics/claude-code/issues/79560) (2026-07-20): `/code-review` refused invocation from another skill.
  - [#79282](https://github.com/anthropics/claude-code/issues/79282) (2026-07-20): asks to let Claude run `/code-review` on its own again. The docs say this works again since v2.1.246.

#### Managed "Code Review" for Claude Code (proprietary)
- Launch, 2026-03-09 (research preview, Team and Enterprise). Several agents search in parallel, then findings are verified and ranked. Vendor figures:
  - Reviews are token-billed, "generally average $15–25", and take about 20 minutes on average.
  - Internally, the share of PRs with substantive comments rose from 16% to 54%.
  - On PRs over 1,000 lines, 84% get findings (average 7.5); on PRs under 50 lines, 31% (average 0.5).
  - Engineers marked fewer than 1% of findings incorrect.
  - Source: [Claude blog](https://claude.com/blog/code-review), [TechCrunch](https://techcrunch.com/2026/03/09/anthropic-launches-code-review-tool-to-check-flood-of-ai-generated-code/)
- GA on 2026-10-15:
  - Quick, Standard (default) and Deep levels per repo.
  - Vendor claim of "about 3x faster": roughly 20 minutes down to 6–10 minutes.
  - At least $10k in credits for eligible Enterprise orgs that claim them by 2027-01-15.
  - Source: [Claude blog (GA)](https://claude.com/blog/code-review-is-now-generally-available)
- How it works per the docs (Nov 2026):
  - Find, Verify, Rank, Post, run on Anthropic infrastructure.
  - Read-only repo access; it does not build or run code.
  - Output: inline comments, a summary, and a "Claude Code Review" check run that never concludes as a failure. "A review never approves or blocks the pull request".
  - Triggers: once on open, after every push, or manual (`@claude review` / `@claude review always`).
  - Drafts and forks are skipped automatically.
  - `REVIEW.md` is read only from the base branch, never from the PR. There is no model choice.
  - Supports GitHub, GHES and GHE Cloud with data residency. Not available to ZDR, HIPAA or CMEK orgs.
  - Source: [docs: Code Review](https://code.claude.com/docs/en/code-review)
- Billing: there is "no flat per-review price"; reviews are billed through usage credits, separate from plan usage. Repos added from the admin page start at "After every push", which multiplies cost by the number of pushes. Org spend caps apply, and reviews are skipped with a budget comment when money runs out. — [docs: costs](https://code.claude.com/docs/en/code-review-costs)

#### User praise for the Anthropic options
- An independent agency blog (2025-10-15) switched from BugBot to the Claude GitHub Action. It found the Action noticeably better at catching real bugs and simple to set up, and caught bugs before QA over three months on a Claude Pro plan. — [madewithlove blog](https://madewithlove.com/blog/why-i-switched-from-bugbot-to-claude-for-code-reviews/)
- HN, 2026-03-10: a commenter ran a similar parallel-agent workflow with validators internally. They report a 20% reduction in time-to-merge at similar cost, with far more comments than other bots. — [HN](https://news.ycombinator.com/item?id=47324174)

#### Complaints, with dates and links
- Cost of the managed service (launch HN thread, 2026-03-09/10; [thread](https://news.ycombinator.com/item?id=47313787)):
  - 2,000 PRs a week at $15–25 comes to about $30–50k per week. — [comment](https://news.ycombinator.com/item?id=47323800)
  - Suspicion that the price is subsidised and could rise sharply. — [comment](https://news.ycombinator.com/item?id=47316398)
  - A DIY workflow costing about $0.04 per review across 200+ PRs. — [comment](https://news.ycombinator.com/item?id=47317279)
  - LLM reviewers "tend to always produce findings". — [comment](https://news.ycombinator.com/item?id=47319842)
  - A tool that flags the same count on clean and broken code is "a random number generator with a UI". — [comment](https://news.ycombinator.com/item?id=47370832) (2026-03-13)
- A team that tried "the new very expensive claude code review" found "it was slow and expensive" and preferred Copilot code review. — [HN](https://news.ycombinator.com/item?id=47643811) (2026-04-04)
- Billing bug: Code Review reports the overage limit reached when spend is $0 of $250. — [claude-code #39678](https://github.com/anthropics/claude-code/issues/39678) (2026-03-27, 18 comments, open)
- A competitor-run benchmark (Qodo, Mar 2026; not neutral) reported Claude Code Review recall of 52% vs 60–71% for Qodo, at similar precision. — [dev.to write-up](https://dev.to/nnennandukwe/we-benchmarked-claudes-code-review-tool-heres-what-the-data-shows-35b9)
- Action: progress, sticky and duplicated comments:
  - [#37](https://github.com/anthropics/claude-code-action/issues/37) (2025-05-23, open): update PR comments instead of adding new ones.
  - [#207](https://github.com/anthropics/claude-code-action/issues/207) (2025-06-26, open): reuse the existing comment on new pushes.
  - [#419](https://github.com/anthropics/claude-code-action/issues/419) (2025-08-06, open, 36 reactions): sticky comment for review mode.
  - [#705](https://github.com/anthropics/claude-code-action/issues/705) (2025-11-28): `use_sticky_comment` fails with `pull_request_target`.
  - [#60](https://github.com/anthropics/claude-code-action/issues/60) (2025-05-27, open, 92 reactions): inline comments for reviews.
  - [#731](https://github.com/anthropics/claude-code-action/issues/731) (2025-12-09): cannot reply in existing inline threads.
  - The madewithlove blog (2025-10-15) reports that re-running on every push would "quickly flood the conversation with noise", and default reviews were picky about null checks.
- Action: stale context: reviews are "heavily biased" by outdated and bot comments and repeat already-fixed issues. — [#590](https://github.com/anthropics/claude-code-action/issues/590) (2025-09-25, open)
- Action: permissions and allowed-tools pain:
  - Claude "does not understand that it does have the correct bash permissions". — [#74](https://github.com/anthropics/claude-code-action/issues/74) (2025-05-28, 28 comments)
  - Request for a read-only mode that disables commits. — [#1415](https://github.com/anthropics/claude-code-action/issues/1415) (2026-06-16)
  - "Workflow validation failed" in reusable workflows. — [#443](https://github.com/anthropics/claude-code-action/issues/443) (2025-08-12, 53 comments)
- Action: fork PRs:
  - "couldn't find remote ref" on fork PRs. — [#223](https://github.com/anthropics/claude-code-action/issues/223) (2025-07-02), [#821](https://github.com/anthropics/claude-code-action/issues/821) (2026-01-14; `branch.ts` doesn't use `refs/pull/*/head`)
  - Cannot run under `pull_request_target`. — [#347](https://github.com/anthropics/claude-code-action/issues/347) (2025-07-28)
  - Open design discussion on fork support. — [#939](https://github.com/anthropics/claude-code-action/issues/939) (2026-02-13)
  - HN, 2026-04-14: the Action is "pretty buggy", forked-repo PRs do not work, and API-only billing makes it expensive compared to a subscription. — [HN](https://news.ycombinator.com/item?id=47772912)
- Action: reliability regressions in 2026:
  - SDK crashes: [#852](https://github.com/anthropics/claude-code-action/issues/852) (2026-01-22), [#853](https://github.com/anthropics/claude-code-action/issues/853) (2026-01-22, exits after about 150 ms with $0 cost), [#892](https://github.com/anthropics/claude-code-action/issues/892) (2026-02-02), [#911](https://github.com/anthropics/claude-code-action/issues/911) (2026-02-08), [#965](https://github.com/anthropics/claude-code-action/issues/965) (2026-02-23: pinned-SHA workaround stopped working).
  - No output from PR review: [#944](https://github.com/anthropics/claude-code-action/issues/944) (2026-02-14, 31 reactions).
  - Bun "directory mismatch" crash: [#1205](https://github.com/anthropics/claude-code-action/issues/1205) (2026-04-10).
  - `plugin_marketplaces` install fails: [#1290](https://github.com/anthropics/claude-code-action/issues/1290) (2026-05-06, 60 reactions).
  - Installer leaves no launcher on ubuntu-latest, so every run fails: [#1817](https://github.com/anthropics/claude-code-action/issues/1817) (2026-09-08).
- Action: auth and cost visibility:
  - Max-subscription use: [#4](https://github.com/anthropics/claude-code-action/issues/4) (2025-05-19, 79 reactions).
  - Refresh tokens for Max subscribers: [#727](https://github.com/anthropics/claude-code-action/issues/727) (2025-12-08).
  - Cost report: [#59](https://github.com/anthropics/claude-code-action/issues/59) (2025-05-26, open).
  - Possible false-positive account bans in intensive review loops on Pro/Max, where review → fix → re-review cycles come from GitHub IPs: [#641](https://github.com/anthropics/claude-code-action/issues/641) (2025-10-25).

### Inferences
- "Open-source Claude review" in practice means MIT/Apache glue (Action, plugins, prompts) around a closed CLI and closed models. Teams can read and fork the orchestration and prompts, but not the harness, which limits auditability and self-hosting compared with Codex CLI or Qwen Code.
- The managed service fixes several Action pain points: one consolidated review with inline threads and a check run, no allowed-tools setup, forks and drafts skipped safely, verification before posting. The price is a per-review cost that is high relative to DIY Action runs. Its "After every push" default and token billing make spend scale with push count; at $15–25 per review, a 5-push PR could cost about $75–125 (inference from vendor figures).
- The security-review Action looks effectively unmaintained as of Nov 2026: last push February 2026, a default model from 2025, and its FP filter broken by a retired model ID.

### Gaps
- No primary-source statement was found on whether `claude-code-action` officially supports subscription OAuth tokens as of Nov 2026. Issues #4/#727 and the 2026-04-14 HN comment conflict, and the README auth list (API key/WIF, Bedrock, Vertex, Foundry) does not mention it.
- No independent measurements of `claude-code-action` per-PR cost or latency were found beyond anecdotes. DIY write-ups claim about $0.02–0.04 per small PR, e.g. [HN](https://news.ycombinator.com/item?id=47317279); one per-PR figure surfaced only through a search snippet and was not verified.
- A widely cited Reddit thread ("Who's gonna pay $15–25 per PR…") is known only second-hand from a paywalled Medium post, because Reddit blocked automated access: [levelup.gitconnected.com](https://levelup.gitconnected.com/anthropic-wants-25-per-pull-request-devs-are-losing-their-minds-over-claude-code-review-55dbbaca4996).

## 4. Other vendor-backed CLIs with explicit review features (late 2026): GitHub Copilot CLI, Amazon Q Developer CLI / Kiro CLI, Mistral Vibe, Google Antigravity CLI

### Takeaway
Of the other vendor CLIs, only GitHub Copilot CLI ships a first-class review command (`/review`, plus an experimental `/security-review`), and it is not open source. Amazon's successor Kiro CLI is closed-source, and the old OSS Q Developer CLI is in maintenance; no review command was found in either. Mistral Vibe is Apache-2.0, but I found no dedicated review feature in it. Google's Antigravity CLI is reported closed-source.

### Cited Findings
- GitHub Copilot CLI is not OSS. The repo `github/copilot-cli` (11,454 stars, `v1.0.114` on 2026-11-18) is under a custom "GitHub Copilot CLI License" that allows installing, running and redistributing unmodified copies only. GitHub's API reports the license as NOASSERTION. — [LICENSE.md](https://github.com/github/copilot-cli/blob/main/LICENSE.md)
- Copilot CLI's `/review [PROMPT]` runs a built-in code-review agent on local changes. — [GitHub docs: agentic code review](https://docs.github.com/en/copilot/how-tos/copilot-cli/use-copilot-cli/agentic-code-review), [command reference](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-command-reference)
- An experimental `/security-review` arrived 2026-06-10. — [changelog](https://github.blog/changelog/2026-06-10-dedicated-security-review-command-now-available-in-copilot-cli/)
- Copilot CLI went GA on 2026-06-23. — [changelog](https://github.blog/changelog/2026-06-23-github-copilot-cli-is-now-generally-available/)
- Copilot code review can be requested from the `gh` CLI since 2026-03-11. — [changelog](https://github.blog/changelog/2026-03-11-request-copilot-code-review-from-github-cli/)
- Copilot CLI review complaints:
  - Built-in agents (explore, task, code-review) do not inherit custom instructions. — [#1990](https://github.com/github/copilot-cli/issues/1990) (2026-03-11)
  - `agentStop` firing on subagent turns makes `/review` never finish. — [#3894](https://github.com/github/copilot-cli/issues/3894) (2026-06-23)
  - Code-review task agents can mutate the shared parent worktree. — [#4195](https://github.com/github/copilot-cli/issues/4195) (2026-07-20)
  - An explicit code-review subagent model override is ignored. — [#4462](https://github.com/github/copilot-cli/issues/4462) (2026-08-12)
  - "Copilot encountered an error and was unable to review this pull request". — [#3529](https://github.com/github/copilot-cli/issues/3529) (2026-05-26)
- GitHub's own ReviewBench (Oct 2026, vendor-run with Microsoft) puts Copilot code review first at 40.1% "grounded F1". The New Stack notes the ranking differs on Martian's leaderboard. — [The New Stack](https://thenewstack.io/github-reviewbench-code-review/)
- A user found Copilot PR reviews leave "beside-the-point semantic nits" but sometimes spot useful things. — [HN](https://news.ycombinator.com/item?id=48535063) (2026-06-15)
- Amazon:
  - `aws/amazon-q-developer-cli`: 1,985 stars, Apache-2.0 per GitHub's API (some secondary sources say MIT/Apache dual), last release `v1.19.7` on 2025-11-17. — [repo](https://github.com/aws/amazon-q-developer-cli)
  - Its README calls the successor Kiro CLI closed-source; the OSS repo gets only critical security fixes. — [Q CLI README](https://raw.githubusercontent.com/aws/amazon-q-developer-cli/main/README.md), [Kiro migration guide](https://kiro.dev/docs/cli/migrating-from-q/)
  - Kiro CLI is licensed as "AWS Content" under the AWS Customer Agreement and AWS IP License. — [kiro.dev/license](https://kiro.dev/license/)
  - I found no review-specific command in either CLI in search results.
- Mistral Vibe (`mistralai/mistral-vibe`): Apache-2.0, 5,455 stars, created 2025-12-08, `v3.1.4` on 2026-11-20. No review command or skill appears in the repo tree (skills are style, CI and async helpers) or in issues matching "review". — [repo](https://github.com/mistralai/mistral-vibe)
- Google Antigravity CLI (`agy`) replaced consumer Gemini CLI from 2026-05-19/06-18. Community and secondary sources call it closed-source and multi-model. — See Section 2 sources ([Google blog](https://developers.googleblog.com/an-important-update-transitioning-gemini-cli-to-antigravity-cli/), [HN](https://news.ycombinator.com/item?id=50160142)).

### Inferences
- In late 2026 the "OSS vendor CLI with built-in review" niche comes down to Codex CLI (`/review`) and Qwen Code (`/review`). The Gemini CLI path is weakened by its access changes, and Claude Code, Copilot CLI and Kiro are closed harnesses.
- Copilot CLI is the main proprietary competitor for teams already paying for GitHub Copilot. Its open issues mirror the OSS tools' problems: instruction inheritance, model override, and worktree mutation by review subagents.

### Gaps
- I did not verify whether Kiro CLI added a review command after launch; no source was found.
- Mistral Vibe: no evidence of review usage. It may be used via generic prompts, but I found no reports.
- I found no first-party statement of Antigravity CLI's license.

## 5. Cross-cutting: agentic vs diff-only review, setup effort and per-PR cost/latency, repo-specific guidance files, vendor lock-in (plus a brief security pointer)

### Takeaway
Vendors themselves argue that repo access, and ideally execution, beats diff-only review: OpenAI explicitly says so, and Qwen runs builds and tests. In practice, though, most CI deployments are diff-centric or read-only. run-gemini-cli limits comments to diff lines, the Claude Action examples use a depth-1 checkout plus `gh pr diff`, codex-action's default profile has no network, and Anthropic's managed review reads code but never runs it. Independent evidence on quality is thin and points to non-determinism and "always finds something" noise. Cost ranges from cents (DIY API runs) to $15–25 or more per review (Anthropic managed). Repo-specific guidance is converging on AGENTS.md, with vendor-specific files (CLAUDE.md, REVIEW.md, GEMINI.md, QWEN.md, `.gemini/config.yaml`) still in use. Every OSS harness except Qwen Code is effectively tied to its vendor's models.

### Cited Findings

#### Agentic vs diff-only
- OpenAI (vendor, 2025-12-01): diff-only is fastest but "often misses" codebase context and dependency interactions. Repo access plus code execution caught more critical issues with fewer false alarms. — [OpenAI alignment blog](https://openai.com/safety-alignment/scaling-code-verification/)
- Anthropic's managed review reads "the diff and the surrounding code, without building or running your code". — [docs](https://code.claude.com/docs/en/code-review)
- Qwen Code `/review` high effort includes a Build & Test agent and runs in a worktree with dependencies installed. Cross-repo PRs drop to a "lightweight", diff-only mode with no build or test. — [docs](https://github.com/QwenLM/qwen-code/blob/main/docs/users/features/code-review.md)
- Gemini's reference review prompt fetches the diff via MCP and forbids comments outside changed lines. — [gemini-review.toml](https://github.com/google-github-actions/run-gemini-cli/blob/main/examples/workflows/pr-review/gemini-review.toml)
- The Claude Action examples check out with `fetch-depth: 1` and allow only `gh pr diff/view/comment` plus the inline-comment MCP. — [pr-review-comprehensive.yml](https://github.com/anthropics/claude-code-action/blob/main/examples/pr-review-comprehensive.yml)
- codex-action's recommended `:workspace` profile has no network, so builds and tests need pre-installed dependencies. — [README](https://github.com/openai/codex-action/blob/main/README.md)
- Independent observation of non-determinism: on a PR where the same missing-guard pattern appeared five times, the AI reviewer flagged two sites. Re-running it on the identical commit flagged one site, at a different line. The author contrasts PR bots with an agent in a full checkout that greps every instance, and concedes the sample is one PR. — [HN post](https://news.ycombinator.com/item?id=49746110) (2026-09-17), [author follow-up](https://news.ycombinator.com/item?id=49752398) (2026-09-18)
- A practitioner design: run the same review agents both as a PR webhook bot and as an MCP tool the local agent calls before pushing, so false positives are cheap to dismiss with full context. — [HN](https://news.ycombinator.com/item?id=49729438) (2026-09-16)
- Benchmarks (likely covered by another researcher):
  - An independent academic benchmark, SWRBench, reportedly puts the best system near F1 ≈ 19% (known only from a secondary summary). — [Atlas summary](https://laoujin.github.io/Atlas/research/2026-06-09-ai-assisted-code-review-in-2026-landscape-tools-evidence-and-limits/evaluation-rubrics-and-benchmarks/)
  - Vendor-run boards (GitHub ReviewBench; Martian results as written up by CodeRabbit) disagree on rankings. — [The New Stack](https://thenewstack.io/github-reviewbench-code-review/), [CodeRabbit write-up](https://www.coderabbit.ai/ja/blog/coderabbit-tops-martian-code-review-benchmark)

#### Setup effort, per-PR cost and latency
- Codex cloud: a toggle in the Codex settings plus `@codex review`, included in ChatGPT plans with a separate "Code Review usage" bucket and no per-PR price. API-key users get no cloud review. — [docs](https://learn.chatgpt.com/docs/third-party/github), [pricing](https://learn.chatgpt.com/docs/pricing)
- codex-action: you write the workflow yourself (the two-job pattern above) and pay API tokens. — [README](https://github.com/openai/codex-action/blob/main/README.md)
- claude-code-action: `/install-github-app` quickstart (repo admin, direct API only); others follow a manual or cloud-provider setup. Cost is API tokens; users asked for cost reporting in [#59](https://github.com/anthropics/claude-code-action/issues/59) (2025-05-26). — [README](https://github.com/anthropics/claude-code-action/blob/main/README.md)
- Anthropic managed review:
  - At launch: about $15–25 and about 20 minutes per review. — [Claude blog](https://claude.com/blog/code-review) (2026-03-09)
  - At GA: 6–10 minutes (vendor claim). — [GA blog](https://claude.com/blog/code-review-is-now-generally-available) (2026-10-15)
  - Default trigger is every push. — [costs doc](https://code.claude.com/docs/en/code-review-costs)
  - A user called it "slow and expensive". — [HN](https://news.ycombinator.com/item?id=47643811) (2026-04-04)
- DIY: one commenter reports about $0.04 per review over 200+ PRs with their own workflow. — [HN](https://news.ycombinator.com/item?id=47317279) (2026-03-09)
- Qwen `/review` high effort: multi-hour runs by design (8–16-hour default deadlines, about 90-minute rounds on huge diffs). — [docs](https://github.com/QwenLM/qwen-code/blob/main/docs/users/features/code-review.md)
- Gemini run-gemini-cli: needs an API key or WIF/Vertex and workflow files. Token usage is not reported in PR comments ([#213](https://github.com/google-github-actions/run-gemini-cli/issues/213), 2025-08-21). — [README](https://github.com/google-github-actions/run-gemini-cli/blob/main/README.md)

#### Repo-specific guidance (AGENTS.md / CLAUDE.md / GEMINI.md / other)
- Codex:
  - The CLI rubric uses `AGENTS.override.md`, then `AGENTS.md`, then fallbacks, with rule citations required. — [rubric.md](https://github.com/openai/codex/blob/main/codex-rs/prompts/templates/review/rubric.md)
  - The cloud reviewer reads the AGENTS.md `## Code Review Rules` section, nested per directory. — [docs](https://learn.chatgpt.com/docs/third-party/github)
  - OpenAI (vendor) says the precision/recall trade-off can be steered with AGENTS.md. — [alignment blog](https://openai.com/safety-alignment/scaling-code-verification/)
- Claude:
  - CLAUDE.md is used by the CLI, the Action and the plugin. — [code-review command](https://github.com/anthropics/claude-plugins-official/blob/main/plugins/code-review/commands/code-review.md), [docs](https://code.claude.com/docs/en/code-review-local)
  - `REVIEW.md` is used only by the managed service and only from the base branch. — [docs](https://code.claude.com/docs/en/code-review)
  - As of Nov 2026, Claude Code loads `AGENTS.md` as project instructions when there is no CLAUDE.md (default) or alongside it, via the built-in `agents-md` mod. — [mods/README.md](https://github.com/anthropics/claude-code/blob/main/mods/README.md)
  - The AGENTS.md request had been hugely popular. — [#6235](https://github.com/anthropics/claude-code/issues/6235) (2025-08-21, 6,693 reactions)
- Gemini:
  - GEMINI.md by default; `context.fileName` can list `AGENTS.md`. — [docs/cli/gemini-md.md](https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/gemini-md.md)
  - The Code Assist app uses `.gemini/config.yaml` and `styleguide.md`. — [Google docs](https://developers.google.com/gemini-code-assist/docs/customize-gemini-behavior-github)
- Qwen: `.qwen/review-rules.md`, `copilot-instructions.md`, and the AGENTS.md or QWEN.md "## Code Review" sections. — [docs](https://github.com/QwenLM/qwen-code/blob/main/docs/users/features/code-review.md)
- Copilot CLI: the built-in code-review agent does not inherit custom instructions. — [#1990](https://github.com/github/copilot-cli/issues/1990) (2026-03-11)

#### Vendor lock-in
- codex-action: OpenAI or Azure OpenAI only, through a Responses API proxy. — [README](https://github.com/openai/codex-action/blob/main/README.md)
- claude-code-action: Claude models only, via Anthropic, Bedrock, Vertex or Foundry. — [README](https://github.com/anthropics/claude-code-action/blob/main/README.md)
- run-gemini-cli: Gemini only (Gemini API, Vertex, Code Assist). — [README](https://github.com/google-github-actions/run-gemini-cli/blob/main/README.md)
- Qwen Code: OpenAI, Anthropic, Gemini, Qwen and local models. — [README](https://github.com/QwenLM/qwen-code/blob/main/README.md)
- Managed services (Codex cloud, Claude Code Review, Gemini Code Assist app, Copilot code review) offer no model choice; Claude's docs say so explicitly. — [Claude docs](https://code.claude.com/docs/en/code-review)
- An HN commenter argues harnesses should be OSS and models treated as commodities, criticising closed Claude Code and the move to closed Antigravity. — [HN](https://news.ycombinator.com/item?id=48493927) (2026-06-11)
- Practitioners commonly use cross-vendor review, e.g. Codex reviewing Claude's output, to offset single-model blind spots. — [HN](https://news.ycombinator.com/item?id=48849267) (2026-07-09), [HN](https://news.ycombinator.com/item?id=50136955) (2026-10-18)

#### Security pointer (covered in depth by another researcher)
- Aikido's "PromptPwnd" showed prompt injection via issue and PR text into AI agents running in GitHub Actions and GitLab CI, covering Gemini CLI, Claude Code and Codex setups. — [Aikido](https://aikido.dev/blog/promptpwnd-github-actions-ai-agents)
- Wiz notes that relaxed bot gates (`allowed_bots: "*"` in claude-code-action, `allow-bots: true` in codex-action) let attackers act through a GitHub App. — [Wiz](https://www.wiz.io/ja-jp/blog/github-actions-security-ai-powered-actions-vulnerabilities)
- The CSA research note (2026-05-03) cites "Comment and Control" exploitation of the Claude Code Security Review Action, the Gemini CLI Action and the Copilot agent. — [CSA](https://labs.cloudsecurityalliance.org/research/csa-research-note-ai-github-actions-security-20260503-csa-st/)
- Academic paper "GitInject". — [arXiv 2606.09935](https://arxiv.org/html/2606.09935)
- A blog author claims the Claude Code action leaked secrets from `/proc/self/environ` (unverified). — [HN](https://news.ycombinator.com/item?id=48718983) (2026-06-29)
- The claude-code-security-review README itself warns it is not hardened against prompt injection. — [README](https://github.com/anthropics/claude-code-security-review/blob/main/README.md)

### Inferences
- The "agentic advantage" is mostly realised locally: Codex `/review` on a full checkout, Claude `/code-review`, Qwen `/review` with build and test. In CI the defaults keep checkouts shallow, tools allowlisted and the network off for security reasons, so many deployed bots behave like diff reviewers with a few extra reads.
- Cost spans about three orders of magnitude: cents for DIY API runs on small PRs, tens of dollars for managed multi-agent reviews, and multi-hour compute for Qwen's high effort. Trigger policy (every push vs once vs on request) is the biggest cost lever and also the main noise lever.
- AGENTS.md is becoming the cross-vendor convention: Codex natively, Claude Code via the 2026 mod, Gemini via `context.fileName`, Qwen via an AGENTS.md section. A single AGENTS.md "Code Review" section therefore gives reasonable portability, while REVIEW.md, `.gemini/config.yaml` and `.qwen/review-rules.md` remain vendor-specific.

### Gaps
- No independent head-to-head comparison of Codex `/review`, claude-code-action, run-gemini-cli and Qwen `/review` on the same PR set was found as of 2026-11-23.
- No systematic latency or cost survey across these OSS harnesses was found; the evidence is vendor docs and anecdotes.
- Reddit could not be read directly (HTTP 403 on the JSON API), so the r/ChatGPTCoding, r/ClaudeAI, r/OpenAI, r/GoogleGeminiAI and r/ExperiencedDevs sentiment is under-represented. The only Reddit-sourced claim is second-hand.
