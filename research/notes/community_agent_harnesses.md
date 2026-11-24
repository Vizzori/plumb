# Community / open-source general-purpose coding-agent harnesses used for AI code review (state as of 23 Nov 2026)

Method note: repo metadata (stars, license, archived flag, last push, renames) was pulled from the GitHub REST API on 2026-11-22 (UTC). Issue/PR data comes from the GitHub search API and the issue pages. "Vendor claim" marks statements from a project's own docs or marketing that I could not check independently. Anything dated 2023–2024 is marked HISTORICAL.

---

## 1. OpenCode (now anomalyco/opencode, formerly sst/opencode): GitHub agent, PR-review use, model flexibility, complaints

### Takeaway
OpenCode is the largest OSS harness (about 228.6k stars) and has the most complete built-in GitHub integration: `opencode github install`, `/opencode` or `/oc` mentions in PR and line comments, and an action that reviews every PR. It works with any `provider/model`. Its main gap for review is that it does not post native inline review comments: the feature request was auto-closed by the stale bot. Users also report problems with review-thread replies, triggers, bot identity, and "stuck" runs. The repo moved from `sst` to the `anomalyco` org. The client is MIT-licensed, but the default GitHub-App token flow and the paid Zen/Go model gateways are hosted services.

### Cited Findings
**Repo, license, move**
- `sst/opencode` now redirects to `anomalyco/opencode`. As of 2026-11-22: 228,569 stars, 31,058 forks, MIT license, created 2025-04-30, last push 2026-11-22. — [GitHub API: repos/sst/opencode](https://api.github.com/repos/sst/opencode); [repo](https://github.com/anomalyco/opencode)
- "Anomaly" (GitHub `anomalyco`) is described as the company behind SST. I found no official announcement or date for the move. — [bmannconsulting note](https://bmannconsulting.com/notes/anomaly/)
- OpenCode 2 is being built on a long-lived `v2` branch. In July 2026 the legacy `packages/opencode` package was removed from that branch and `packages/llm` was renamed to `packages/ai`, so downstream forks face a migration. This comes from a downstream fork's description of the upstream. — [Kilo-Org/kilocode#12887 (2026-08-05)](https://github.com/Kilo-Org/kilocode/issues/12887)

**GitHub agent / review features (official docs)**
- `opencode github install` installs the GitHub App, creates the workflow and sets up secrets. Manual setup is the `opencode-agent` GitHub App plus `.github/workflows/opencode.yml`. — [OpenCode GitHub docs](https://opencode.ai/docs/github/)
- Trigger phrases default to `/opencode,/oc` and can be changed. Supported events: `issue_comment`, `pull_request_review_comment` (mention on specific diff lines), `issues`, `pull_request` (for automatic reviews), `schedule`, `workflow_dispatch`. — [OpenCode GitHub docs](https://opencode.ai/docs/github/)
- In a line comment, the agent receives the file, the lines and the surrounding diff context automatically, for example `/oc add error handling here`. For change requests it commits to the same PR. — [OpenCode GitHub docs](https://opencode.ai/docs/github/)
- The automatic-review example triggers on `opened, synchronize, reopened, ready_for_review`. Without a `prompt`, the action reviews the PR by default. The docs warn that fork PRs normally get a read-only token and no secrets. — [OpenCode GitHub docs](https://opencode.ai/docs/github/)
- `model` is required as `provider/model`, and `variant` sets reasoning effort. By default the action exchanges an OIDC token for an OpenCode GitHub App token via `https://api.opencode.ai`, a hosted service. `use_github_token: true` avoids the app and the hosted exchange. — [OpenCode GitHub docs](https://opencode.ai/docs/github/)
- An issue (2026-04-30) asks the GitHub action to reuse the prompt of the TUI `/review` command, which implies a built-in local `/review` exists. — [anomalyco/opencode#25095](https://github.com/anomalyco/opencode/issues/25095)

**Complaints and limits specific to review (GitHub issues)**
- **No native inline review comments.** Opened 2026-02-17 with 20 👍. All feedback lands in "a single big comment", and the `gh api` workaround is called fragile. The stale bot auto-closed it on 2026-04-18 with no linked PR. On 2026-05-25 a user noted inline comments were still unsupported. — [#13918](https://github.com/anomalyco/opencode/issues/13918)
- The action replies in the PR conversation instead of the review thread that triggered it (2026-07-17, 5 👍). An earlier request asked it to reply in review comment threads (2026-05-10). — [#37560](https://github.com/anomalyco/opencode/issues/37560); [#26691](https://github.com/anomalyco/opencode/issues/26691)
- Trigger gaps: `pull_request_review` (the review body) is not a supported trigger event. Reported 2025-08-22, 2026-07-20 and 2026-09-20. — [#2152](https://github.com/anomalyco/opencode/issues/2152); [#37867](https://github.com/anomalyco/opencode/issues/37867); [#50247](https://github.com/anomalyco/opencode/issues/50247)
- With a PAT, the review is posted as the PAT owner instead of a bot identity (2026-06-25). — [#33735](https://github.com/anomalyco/opencode/issues/33735)
- Bot-authored PRs cannot be reviewed because `assertPermissions` fails for non-collaborator actors (2026-08-19). — [#43532](https://github.com/anomalyco/opencode/issues/43532)
- The summary commit is not conventional-commit-safe, so a failed hook turns a completed review into a failed run (2026-09-18). — [#49754](https://github.com/anomalyco/opencode/issues/49754)
- Reaction removal ignores the provided custom token (2026-09-08). — [#47967](https://github.com/anomalyco/opencode/issues/47967)
- Reliability: "OpenCode Github Agent Stuck!" (2025-11-24, 23 comments). `/opencode` raises an error in GitHub Actions (2025-09-11, 24 comments). — [#4672](https://github.com/anomalyco/opencode/issues/4672); [#2549](https://github.com/anomalyco/opencode/issues/2549)
- Provider friction in CI: how to use the Copilot provider in the action (2025-07-26, 28 comments). All Gemini requests failed because of an `anyOf` schema in a `github_create_pull_request_review` tool (2026-02-21). — [#1341](https://github.com/anomalyco/opencode/issues/1341); [#14509](https://github.com/anomalyco/opencode/issues/14509)
- A community PR, "Add multi-provider code review to GitHub Action" (2026-01-09), was closed. — [PR #7404](https://github.com/anomalyco/opencode/pull/7404)

**Independent user reports of OpenCode as a CI reviewer**
- Martin Alderson (2026-02-26) runs OpenCode in CI in Docker with `openai/gpt-5.3-codex` through a ChatGPT subscription. The review is written to `report.md` and posted as one PR comment.
  - He calls the output "genuinely useful" rather than noisy, helped by a conservative prompt: verify before flagging, skip style, flag only at 90%+ confidence. Marginal cost is "effectively zero".
  - Downsides: OpenAI OAuth tokens expire after 14 days, the ToS position is unclear, and Codex CLI failed in his sandbox (no Landlock), which is why he switched to OpenCode. — [martinalderson.com](https://martinalderson.com/posts/using-opencode-in-cicd-for-ai-pull-request-reviews/)
- Shadowsong27 (2026-05-10) runs a reusable action on a self-hosted runner that calls `opencode run` with the diff and posts a comment, with GPT via ChatGPT subscription auth.
  - Problems: rapid pushes flood the PR with stale reviews and burn quota, and the stateless reviewer repeats the same flags on every push.
  - Quota exhaustion is indistinguishable from model or network errors, and prompt injection from diffs is a concern. — [shadowsong27 blog](https://shadowsong27.github.io/2026/05/ai-log-2-adding-an-ai-pr-reviewer-to-my-agent-harness/)
- Hugging Face publishes a guide to running OpenCode in GitHub Actions for code review with open-weight models (e.g., GLM-4.5) through HF Inference Providers. This is from a search-result summary; I did not open the page. — [HF docs](https://huggingface.co/docs/inference-providers/guides/github-actions-code-review)

**Model flexibility and the paid layer**
- OpenCode Go is a $10/month subscription, with Go Plus at $40/month per docs as summarized by search. OpenCode Zen is a pay-as-you-go gateway over a curated model list. The OSS client still works with your own keys and local models. — [OpenCode Go docs](https://opencode.ai/docs/go/); [llmgateway pricing explainer (third-party)](https://llmgateway.io/blog/opencode-go-pricing)
- Subscription-auth fragility: per secondary sources, OpenCode 1.3.0 (≈2026-03-19, PR #18186 "Remove anthropic references per legal requests") removed the bundled Claude Pro/Max OAuth plugin. Anthropic said in Feb 2026 that subscriptions may not be used in third-party harnesses. — [x-cmd blog (secondary)](https://www.x-cmd.com/ja/blog/260320); [timetobuildbob blog (secondary)](https://timetobuildbob.github.io/blog/why-anthropic-sent-a-cease-and-desist-to-opencode-and-what-it-means-for-agents); [The Register, 2026-02-20](https://www.theregister.com/2026/02/20/anthropic_clarifies_ban_third_party_claude_access)
- Broader complaints, brief because security is covered elsewhere:
  - A July 2026 "Stop Using OpenCode" post by Luke Wren on RCE and permission bypass reportedly reached about 256 points on HN. This is secondary and in Japanese. — [labmemo.com](https://labmemo.com/?p=54107)
  - Reports of multi-GB RAM and 100% CPU (Mar 2026), also secondary. — [towardsai.net](https://pub.towardsai.net/opencode-just-dethroned-claude-code-with-172-000-stars-i-ran-both-and-its-78-slower-508961c12959)

### Inferences
- In practice OpenCode reviews are "agent writes a summary comment" unless users script `gh api` themselves. That is the biggest functional gap against dedicated bots: line-anchored comments that can be resolved one by one, and suggestion blocks.
- The cluster of 2026 issues (triggers, threads, identity, bot PRs, hook failures) shows the GitHub agent is actively used for review but still rough at the edges of GitHub's PR model.
- Subscription-based CI review (ChatGPT or Claude OAuth) is cheap but legally and operationally fragile. API keys or Zen/Go are the stable path.

### Gaps
- No official date for the sst → anomalyco move.
- No public data on review precision or false-positive rates for OpenCode-based review.
- I could not verify the claim that Apache Doris `doris-website` uses an `opencode-review.yml` workflow: the URL appeared in search results but the fetch returned 404.

---

## 2. OpenHands (OpenHands/OpenHands, formerly All-Hands-AI/OpenHands): GitHub/GitLab, PR review, headless/CI, Cloud vs OSS, complaints

### Takeaway
OpenHands has the most review-specific OSS tooling of the general harnesses. A `pr-review` GitHub Action/plugin (MIT, in `OpenHands/extensions`) is built on the Software Agent SDK. It posts inline comments with severity labels and can submit APPROVE or REQUEST_CHANGES, and in 2026 it gained sub-agent delegation, supply-chain checks, prompt fencing and acceptance checks. The org-wide "Automation" reviewer and the GitLab integration live in OpenHands Cloud, and the `enterprise/` directory is source-available. Known weaknesses: no automatic re-review on new pushes, some trigger gaps, and line and suggestion-block handling that needed fixes.

### Cited Findings
**Repo and licensing**
- `All-Hands-AI/OpenHands` now redirects to `OpenHands/OpenHands`, with 94,064 stars and an MIT license as of 2026-11-22. — [GitHub API](https://api.github.com/repos/All-Hands-AI/OpenHands)
- Everything is MIT except the `enterprise/` directory. That code is source-available, and running it beyond one month requires a paid license. A self-hosted "Cloud" Helm chart is offered under a Polyform Free Trial license (30-day trial). — [OpenHands enterprise docs (via search summary)](https://docs.openhands.dev/enterprise); [OpenHands blog on self-hosted Cloud](https://www.openhands.dev/blog/openhands-cloud-self-hosted-secure-convenient-deployment-of-ai-software-development-agents)
- `OpenHands/extensions` ("Public registry for OpenHands extensions"): MIT, 185 stars, created 2025-11-24. `OpenHands/software-agent-sdk`: MIT, 1,418 stars. — [GitHub search API](https://github.com/OpenHands/extensions); [GitHub API](https://github.com/OpenHands/software-agent-sdk)

**PR-review workflow (official docs; vendor description)**
- It is a GitHub Actions workflow built on the Software Agent SDK. The plugin now lives at `OpenHands/extensions/plugins/pr-review`, replacing the old `software-agent-sdk/.github/actions/pr-review` path. Reviews arrive in about 2–3 minutes. — [OpenHands code-review docs](https://docs.openhands.dev/openhands/usage/use-cases/code-review)
- Triggers: a non-draft PR is opened, a draft is marked ready, the `review-this` label is added, or `openhands-agent` is requested as a reviewer. Pushing new commits does not re-trigger a review. — [same](https://docs.openhands.dev/openhands/usage/use-cases/code-review)
- It uses two skills, `/codereview` and `/github-pr-review`. Comments carry 🔴 Critical, 🟠 Important, 🟡 Suggestion or 🟢 Nit labels, line references and fix suggestions, and the review can be APPROVE, REQUEST_CHANGES or COMMENT. The old `review-style` input (standard or "roasted") is deprecated because the two styles were merged. — [same](https://docs.openhands.dev/openhands/usage/use-cases/code-review)
- Models:
  - `llm-model` defaults to `anthropic/claude-sonnet-4-5-20250929`, and comma-separated models enable A/B comparison. `llm-base-url` takes custom endpoints or proxies.
  - An experimental ACP mode delegates to ACP agents such as Codex ACP or Claude agent ACP and should run only on trusted self-hosted runners. — [same](https://docs.openhands.dev/openhands/usage/use-cases/code-review)
- Security design:
  - It uses `pull_request_target` so fork PRs work, and only users with write access can trigger via label or reviewer request.
  - API keys are passed as SDK secrets rather than environment variables, to make exfiltration by malicious fork PRs harder. — [same](https://docs.openhands.dev/openhands/usage/use-cases/code-review)
- **Cloud-only part:** "OpenHands Automation" (org-wide, event-driven) requires a GitHub App install, a team org and a bot account. It does not re-review on new pushes and does not auto-trigger for first-time contributors. — [same](https://docs.openhands.dev/openhands/usage/use-cases/code-review)
- Also offered: a prebuilt "GitHub PR Review Assistant" in Agent Canvas and a `setup-pr-review` skill. These come from search results; I did not open them. — [Agent Canvas page](https://docs.openhands.dev/openhands/usage/agent-canvas/prebuilt/github-pr-review); [SDK PR-review guide](https://docs.openhands.dev/sdk/guides/github-workflows/pr-review)
- GitLab support is Cloud-based: you mention `@openhands` on merge requests to ask questions, request updates or get explanations. The PR-review plugin docs do not mention GitLab. — [OpenHands GitLab docs](https://docs.openhands.dev/openhands/usage/cloud/gitlab-installation)

**Development trajectory (primary: PRs)**
- OpenHands dogfoods the reviewer on its own repo:
  - "Add PR Review by OpenHands workflow" (2026-02-06)
  - consolidation and migration to the extensions action (2026-02-09 and 2026-02-18)
  - "ci: run PR review on fork PRs" (2026-04-23)
  - "Add PR review bot triage guidelines" (2026-05-13)
  — [#12784](https://github.com/OpenHands/OpenHands/pull/12784); [#12801](https://github.com/OpenHands/OpenHands/pull/12801); [#12917](https://github.com/OpenHands/OpenHands/pull/12917); [#14109](https://github.com/OpenHands/OpenHands/pull/14109); [#14410](https://github.com/OpenHands/OpenHands/pull/14410)
- Extension PRs in 2026:
  - restrict the workflow to collaborators (2026-02-20)
  - sub-agent delegation for file-level reviews (2026-04-13), on by default from 2026-04-23
  - ACP backend mode (2026-04-24)
  - supply-chain checks for dependency changes (2026-05-04)
  - "fence untrusted prompt content" (2026-05-20)
  - "teach agent how suggestion blocks actually work" (2026-06-02)
  - "independent acceptance checks" (2026-09-13)
  — [#65](https://github.com/OpenHands/extensions/pull/65); [#164](https://github.com/OpenHands/extensions/pull/164); [#205](https://github.com/OpenHands/extensions/pull/205); [#210](https://github.com/OpenHands/extensions/pull/210); [#226](https://github.com/OpenHands/extensions/pull/226); [#252](https://github.com/OpenHands/extensions/pull/252); [#293](https://github.com/OpenHands/extensions/pull/293); [#572](https://github.com/OpenHands/extensions/pull/572)
- HISTORICAL:
  - "DogFood: Use OpenDevin to review PR" (2024-04-19)
  - "Feature: PR Review" (2024-11-23)
  - "Implement AI PR description & code reviews" (2025-06-25)
  — [#1223](https://github.com/OpenHands/OpenHands/pull/1223); [#5219](https://github.com/OpenHands/OpenHands/issues/5219); [#9338](https://github.com/OpenHands/OpenHands/issues/9338)

**Complaints and limits**
- An `@openhands` mention inside a formal PR review (Review changes → Comment/Approve) does not trigger the agent, while the same mention in a normal comment does. Opened 2026-01-20, closed "not planned" 2026-06-03. — [#12513](https://github.com/OpenHands/OpenHands/issues/12513)
- HISTORICAL (2025-04-16): the resolver ignored line numbers when addressing PR review comments. — [#7877](https://github.com/OpenHands/OpenHands/issues/7877)
- The docs themselves note that new pushes do not re-trigger review, large PRs are slow, and team review requests are not matched by default. — [OpenHands code-review docs](https://docs.openhands.dev/openhands/usage/use-cases/code-review)

### Inferences
- OpenHands is the clearest case of a general harness that grew a dedicated reviewer: it now has severity tiers, inline comments, verdicts, sub-agents and acceptance checks. Its 2026 PR stream (suggestion blocks, prompt fencing, collaborator gating) reads like a list of problems that DIY harness reviewers hit.
- The OSS/paid split is clean for per-repo use: the MIT action plus your own LLM key. Org-wide automation, GitLab and enterprise deployment push users toward Cloud or the source-available `enterprise/` code.

### Gaps
- No independent quality or false-positive measurements for the OpenHands reviewer.
- I could not confirm whether the PR-review plugin supports GitLab MRs outside Cloud. Hodor (Section 6) fills that gap on top of the SDK.

---

## 3. Continue (continuedev/continue): `cn` CLI, "AI checks" / Continuous AI, OSS vs Hub/paid

### Takeaway
Continue repositioned around source-controlled "AI checks": markdown-defined agents that run on every PR and report as GitHub status checks with suggested diffs. They are powered by the OSS (Apache-2.0) `cn` CLI, which can also run checks locally (`cn check`) without an account. The hosted parts are the GitHub App runner, Hub-configured checks and the Mission Control metrics dashboard. Adoption signals are modest (44 points on the Show HN), and at least one open bug shows stale results being re-posted on new commits.

### Cited Findings
- Repo: 36,535 stars, Apache-2.0, active as of 2026-11-22. — [GitHub API](https://api.github.com/repos/continuedev/continue)
- Show HN, "Continue – Source-controlled AI checks, enforceable in CI": 44 points and 7 comments. The page shows "9 months ago", so roughly Feb 2026.
  - Each check is a markdown file in `.continue/checks/` and shows up as a GitHub status check. Checks are agents that can read and write files, run bash and use a browser. A failing check offers a one-click diff, and passing checks stay silent.
  - The author says the checks are powered by an open-source CLI, with a hosted dashboard (Mission Control) for metrics and public links. — [HN item 47049848](https://news.ycombinator.com/item?id=47049848)
- HN commenters:
  - One called it an "Interesting rebrand" of the local coding-assistant project, and the author confirmed the VS Code extension is still maintained.
  - Another asked how it differs from GitHub's `gh-aw` (agentic workflows). The author pointed to the local experience, accept/reject UX, and metrics on suggestion and merge rates. — [HN item 47049848](https://news.ycombinator.com/item?id=47049848)
- `cn check` (repo skill doc):
  - It runs checks against the diff with the base branch. Flags: `--agent` (local file or Hub slug), `--base`, `--fix` (apply patches), `--patch`, `--fail-fast`, `--format json` for CI.
  - Hub-configured checks need `cn login`, and local-only agents need no auth. This doc places local checks in `.continue/agents/*.md`, which conflicts with `.continue/checks/` in the HN post and docs; the layout may have been renamed. — [cn-check SKILL.md](https://raw.githubusercontent.com/continuedev/continue/HEAD/skills/cn-check/SKILL.md)
- Docs issue "Document recent CLI features (hooks, ai-sdk, cn checks, MCP Apps, skills)" (2026-03-24) shows `cn checks` shipped by about March 2026. — [continue#11758](https://github.com/continuedev/continue/issues/11758)
- **Complaint:** PR checks do not create fresh agent sessions on PR updates, so stale task IDs re-post to new commits. Reported 2026-05-12 against `cn` 1.5.45 with the org-level GitHub App; still open, 10 comments. — [continue#12382](https://github.com/continuedev/continue/issues/12382)
- Pricing, third-party and not verified: Team is reported at $20/seat/month with $10 in credits per seat, alongside Starter and Company tiers. The official pricing URL returned 404 when fetched. — [aitoolsatlas](https://aitoolsatlas.ai/tools/continue/pricing); [costbench](https://www.costbench.com/software/ai-coding-assistants/continue/)

### Inferences
- Continue's design is closer to a policy/linting gate (pass/fail status check plus patch) than to a conversational reviewer. That suits teams that want "rules as code" enforcement. It is not an inline-comment reviewer.
- What is OSS: the CLI and the check definitions, which can run fully local or in your own CI. What is hosted: the GitHub App runner, Hub checks and the metrics dashboard.

### Gaps
- I could not fetch official pricing or the current checks docs (several docs URLs returned 404, possibly due to restructuring). Pricing is from third parties only.
- No independent user reports on check quality or noise beyond the HN thread.

---

## 4. Kilo Code, Roo Code, Cline: review features and what is OSS vs cloud-only

### Takeaway
- **Kilo** has the most productized reviewer among the VS Code-lineage agents: the hosted "Kilo Code Reviewer" (GitHub and GitLab, strictness levels, REVIEW.md, sub-agents) plus a local `/review` in the MIT-licensed CLI/extension. The CLI is now an OpenCode fork. Its issue tracker shows silent-success failures, BYOK billing bugs and runaway token loops.
- **Roo Code** is gone. The extension shut down on 2026-05-15 and the repo is archived. Its cloud "PR Reviewer" (BYOK, hosted) is now history, and the team moved to Roomote.
- **Cline** offers no hosted reviewer. It ships a documented, security-conscious GitHub Actions sample for the Apache-2.0 CLI (summary comment only) and an SDK example with a review-plus-judge pipeline, but the CLI has gone through frequent breaking versions (2.x → 3.x → 4.0 native) in 2026.

### Cited Findings
**Kilo Code**
- `Kilo-Org/kilocode`: MIT, 28,087 stars, active as of 2026-11-22. A separate `Kilo-Org/kilo` repo (created 2026-01-26) is archived, last pushed 2026-02-24. — [GitHub API](https://api.github.com/repos/Kilo-Org/kilocode); [GitHub API](https://api.github.com/repos/Kilo-Org/kilo)
- Kilo CLI 1.0 is "built on the OpenCode server as its open-source foundation". Kilo says it will upstream fixes. A third-party source dates the launch to 2026-02-05. — [Kilo blog repost on DEV](https://dev.to/kilocode/kilo-cli-10-built-for-kilo-speed-5amk); [morphllm comparison (third-party)](https://www.morphllm.com/comparisons/kilo-code-vs-opencode)
- Kilo tracks OpenCode's core: "7.5.x (opencode core)", and a plan to migrate Kilo to OpenCode 2 (2026-08-05). — [kilocode#13772](https://github.com/Kilo-Org/kilocode/issues/13772); [kilocode#12887](https://github.com/Kilo-Org/kilocode/issues/12887)
- Code Reviewer launched on Product Hunt on 2026-01-27. — [Product Hunt launch](https://www.producthunt.com/products/kilocode/launches/kilo-code-reviewer)
- Code Reviewer features (vendor docs):
  - Platforms and triggers: GitHub App and GitLab (OAuth or PAT). Reviews run on PR/MR open or update for selected repos, and bot PRs such as Dependabot or Renovate are skipped.
  - Strictness and focus: Strict, Balanced or Lenient, plus focus areas.
  - REVIEW.md: read from the base branch, truncated at 10,000 characters.
  - Sub-agents: none for tiny diffs, up to 6 for large ones. They are read-only, and the main reviewer verifies their findings.
  - Output: inline comments plus a summary, with severity tags. The agent checks that comments target valid diff lines and "avoids duplicate comments" (mechanism not described).
  — [Kilo Code Reviews docs](https://kilo.ai/docs/automate/code-reviews/overview)
- Pricing and limits:
  - The docs say compute and review time are free during a limited beta, but credits are still consumed for model reasoning. Concurrency is 1 review if the balance is ≤$5, 3 if higher, and 20 for organizations.
  - The product page now says reviews are free with "Kilo Auto" or a free model.
  - A third-party review says the free tier covers specific free models only. These sources conflict. — [Kilo docs](https://kilo.ai/docs/automate/code-reviews/overview); [kilo.ai/code-reviewer](https://kilo.ai/code-reviewer); [makerstack review (third-party)](https://makerstack.co/reviews/kilo-code-reviewer-review/)
- Local reviews: `/review` in VS Code or the CLI can review uncommitted changes, a branch, a worktree, a commit or a PR, and does not count toward cloud limits. — [Kilo docs](https://kilo.ai/docs/automate/code-reviews/overview)
- **Complaints (GitHub issues):**
  - The GitHub Code Review check run reports success even when output-limit exhaustion prevented any review from being posted (2026-08-17). It was closed "not_planned" on 2026-10-17. — [kilocode#13153](https://github.com/Kilo-Org/kilocode/issues/13153)
  - Hosted Code Reviews fail with "insufficient credits" when using a ChatGPT BYOK connection (2026-10-25, open). — [kilocode#15468](https://github.com/Kilo-Org/kilocode/issues/15468)
  - Sub-agent reasoning loop in the review workflow (2026-09-17, open). — [kilocode#14218](https://github.com/Kilo-Org/kilocode/issues/14218)
  - "Ask and Code Review mode edits the files" (2026-08-18). — [kilocode#13189](https://github.com/Kilo-Org/kilocode/issues/13189)
  - The review check fails with `SandboxError: Container is starting` (2026-05-11). — [kilocode#10160](https://github.com/Kilo-Org/kilocode/issues/10160)
  - "Review only checks against master" (2026-02-25). — [kilocode#6278](https://github.com/Kilo-Org/kilocode/issues/6278)
  - "Maximum review time" (2026-08-15). — [kilocode#13147](https://github.com/Kilo-Org/kilocode/issues/13147)
  - "v2: port the Kilo /review command" (2026-10-29), a sign of re-platforming churn. — [kilocode#15598](https://github.com/Kilo-Org/kilocode/issues/15598)
  - Token burn, harness-wide: the OpenCode-core rebuild has no per-turn step, error or cost cap. One looping session cost $626.34, with 1.877B cache-read tokens over 3,673 steps in 14.7 hours (2026-09-04). — [kilocode#13772](https://github.com/Kilo-Org/kilocode/issues/13772)

**Roo Code**
- `RooCodeInc/Roo-Code` is archived (archived=true, last push 2026-05-15, 24,238 stars, Apache-2.0). — [GitHub API](https://api.github.com/repos/RooCodeInc/Roo-Code)
- The README says the extension was shut down on May 15 and points users to "ZooCode" (a community fork) and Cline. Billing questions go to the company. — [Roo-Code README](https://github.com/RooCodeInc/Roo-Code)
- Secondary sources say the shutdown was announced on 2026-04-21 and that the team is refocusing on "Roomote". Roo's own cloud page now says the team is launching something new and links to Roomote. — [vibecodehq (secondary)](https://vibecodehq.pages.dev/blog/roo-code-shuts-down-roomote-cloud-agent-may-2026); [morphllm (secondary)](https://www.morphllm.com/roo-code); [roocode.com/cloud](https://roocode.com/cloud)
- HISTORICAL product (2025–early 2026): Roo Code Cloud's "PR Reviewer" cloud agent monitored repos and posted PR comments with BYOK models. A separate "PR Fixer" was invoked via `@roomote`. These were vendor docs. — [Roo Cloud Agents docs](https://docs.roocode.com/roo-code-cloud/cloud-agents); [roocode.com/reviewer](https://roocode.com/reviewer)

**Cline**
- `cline/cline`: Apache-2.0, 71,823 stars, active as of 2026-11-22. — [GitHub API](https://api.github.com/repos/cline/cline)
- Official CLI PR-review sample:
  - Structure: two jobs. A read-only `review` job runs Cline and uploads `review.md`. A `post` job with only `pull-requests: write` publishes it as a single COMMENT review, so the agent can never approve a PR.
  - Inline comments require extra work: write JSON and post via the reviews API.
  - The sample skips drafts, forks and Dependabot. Install is `npm install -g cline`, unpinned, and the run is `cline --auto-approve true`.
  - Stated risks: the review job can run any shell command and reach the internet. Hooks are taken from the base branch. Do not use `pull_request_target`. — [Cline docs: GitHub PR review](https://docs.cline.bot/cli/samples/github-pr-review)
- Headless piping, e.g. `gh pr diff 123 | cline -y "Review this PR"`, per the CLI docs as summarized by search. Cline CLI 2.0 (headless stdout mode) is dated 2026-02-13 by a secondary source. — [Cline CLI docs](https://docs.cline.bot/cline-cli); [ByteIota (third-party)](https://byteiota.com/cline-cli-run-your-ai-coding-agent-in-github-actions/)
- Cline dogfoods it: "add cline pr review as a github workflow" was merged 2026-01-13. A follow-up fix, "use 'cline task --yolo' instead of 'cline --yolo'" (2026-02-05), shows a CLI flag change breaking the workflow. "Add real PR dashboard to code review bot example" (2026-05-16). — [cline#8434](https://github.com/cline/cline/pull/8434); [cline#9120](https://github.com/cline/cline/pull/9120); [cline#10812](https://github.com/cline/cline/pull/10812)
- Cline SDK review agent (Cline blog, 2026-08-26):
  - Two passes. A reviewer calls `record_finding` per changed line, then a stricter "judge" run keeps only findings worth posting.
  - A deterministic driver posts one batched COMMENT review. It falls back to summary-only when a comment lands outside the diff hunk.
  - A denylist `tool-guard` blocks edits and dangerous shell commands.
  - The example uses OpenRouter `moonshotai/kimi-k3`, and the provider and model are configurable. — [Cline blog](https://cline.bot/blog/building-a-code-review-agent-with-cline-sdk)
- **CLI stability complaints:**
  - "Cline CLI start failed … instance not found in registry" (2025-10-21, 13 comments, 7 👍) and "Unable to run cline cli in linux" (2025-10-19). — [cline#7011](https://github.com/cline/cline/issues/7011); [cline#6973](https://github.com/cline/cline/issues/6973)
  - Bedrock profile auth broken in CLI 3.0.2 (2026-05-14, 25 comments) and Azure AI Foundry auth broken in 3.0.15 (2026-06-03). — [cline#10770](https://github.com/cline/cline/issues/10770); [cline#11237](https://github.com/cline/cline/issues/11237)
  - Missing npm platform package for 3.0.34 (2026-06-30). Cline 4.0.0 native CLI binary path error (2026-06-27). Crash-loop on pre-AVX CPUs (2026-09-11). — [cline#11998](https://github.com/cline/cline/issues/11998); [cline#11908](https://github.com/cline/cline/issues/11908); [cline#14066](https://github.com/cline/cline/issues/14066)
  - Cline hangs when `gh` commands succeed but return nothing (2025-12-04), which matters for gh-driven review scripts. — [cline#7898](https://github.com/cline/cline/issues/7898)

### Inferences
- Kilo's reviewer is effectively OpenCode-based review packaged as a hosted service with a free or credit model. The local `/review` is OSS, while the cloud orchestration, concurrency and billing are proprietary hosted services. Its bugs (silent green checks, BYOK billing, loops) are the typical failure modes of putting an agent harness behind a PR check.
- The Roo Code shutdown is a cautionary data point: a popular OSS agent (24k stars) with a hosted PR-reviewer add-on shut down within months. Teams that depend on vendor-hosted review layers on top of OSS clients carry continuity risk.
- Cline's sample is the most explicit about safe CI patterns (split read and write jobs, COMMENT-only), but its review quality depends entirely on the user's prompt. CLI churn makes pinning versions mandatory.

### Gaps
- I did not verify whether any part of Kilo's cloud reviewer orchestration is open source. One issue refers to a "published implementation" of a balance-check function, but I could not locate it.
- Roo's own 2026-04-21 announcement post was not found. The date is from secondary sources.
- I found no paid Cline review tier. I did not verify Cline's current Teams or Enterprise pricing in this pass.

---

## 5. Goose, Aider, Crush, SWE-agent / mini-swe-agent

### Takeaway
- **Goose** (now under the Linux Foundation's Agentic AI Foundation) gained a real local review command in 2026. `goose review` runs per-check sub-agents from `.agents/checks/*.md` with severity filtering, and its flags mirror `amp review`. CI usage is a documented `goose run` workflow that posts a single PR comment. A "goose bot" hosted reviewer PR was not merged.
- **Aider** has no review feature. It is scriptable (`--message`) but effectively in maintenance mode: last feature release Aug 2025, last push May 2026, and a community fork exists.
- **Crush** is source-available (FSL-1.1-MIT, not OSI) and has a maturing `crush run` headless mode, but no review features.
- **SWE-agent / mini-swe-agent** are research harnesses with no review features. They appear in only tiny community review experiments.

### Cited Findings
**Goose**
- `block/goose` now redirects to `aaif-goose/goose` (Apache-2.0, 56,871 stars, active as of 2026-11-22). — [GitHub API](https://api.github.com/repos/block/goose)
- The Linux Foundation formed the Agentic AI Foundation (AAIF) on 2025-12-09 with goose, MCP and AGENTS.md as founding projects. — [LF press release](https://www.linuxfoundation.org/press/linux-foundation-announces-the-formation-of-the-agentic-ai-foundation); [The Register, 2025-12-09](https://www.theregister.com/2025/12/09/linux_foundation_agentic_ai_foundation/)
- `goose review` (man page):
  - It reviews the working tree vs HEAD, or a `[RANGE]` such as `main...HEAD`.
  - It discovers `**/.agents/checks/*.md` sub-agent reviewers and `**/.agents/REVIEW.md` scoped prompt overrides, and runs one `goose run` subprocess per check (at most 4 in parallel).
  - Flags include `--severity` (default medium), `--model`, `--provider`, `--override-model`, `--turn-limit`, `--checks-only`, `--dry-run`, `-f` and `-c`.
  - Several flags mirror `amp review` "for drop-in compatibility". — [goose-review(1) man page](https://www.mankier.com/1/goose-review)
- Origin and related PRs:
  - "feat(cli): add `goose review` local code review command" (2026-05-08). — [goose#9114](https://github.com/aaif-goose/goose/pull/9114)
  - "Add goose review --format json with session attribution" (2026-06-02, closed without merge). It cites an internal `sq-agents` need for cost and session export in multi-check reviews. — [goose#9567](https://github.com/aaif-goose/goose/pull/9567)
  - "feat: added goose bot for automated code reviews" proposed a hosted switchboard/webhook bot for GitHub PRs. Opened 2026-05-20, closed without merge on 2026-07-15. — [goose#9341](https://github.com/aaif-goose/goose/pull/9341)
- Security hardening around review:
  - "Some safety features for reviewing untrusted code" (2026-03-14). — [goose#7893](https://github.com/aaif-goose/goose/pull/7893)
  - "fix(review): disable repository diff helpers" (2026-08-27, open). — [goose#11617](https://github.com/aaif-goose/goose/pull/11617)
  - "fix: avoid following untracked review symlinks" (2026-08-05). — [goose#10995](https://github.com/aaif-goose/goose/pull/10995)
- CI/CD docs: headless `goose run --instructions` inside a GitHub Actions workflow that collects the diff via `gh`, installs a pinned CLI and posts the result with `gh pr comment` as a single comment. There is no official Action, and the docs admit the output filtering via grep is fragile. — [goose CI/CD tutorial](https://goose-docs.ai/docs/tutorials/cicd)
- Recipes are YAML packages of instructions, prompts and parameters. A "code-review" recipe is listed among the examples, and `goose run --recipe` runs one headless. This is from a search-result summary. — [goose recipes docs](https://goose-docs.ai/docs/guides/recipes/session-recipes)
- Community guide, "Building effective prompts and workflows for code review with goose", tracked from a 2025-09-23 issue. — [goose#4720](https://github.com/aaif-goose/goose/issues/4720); [DEV post](https://dev.to/lymah/building-effective-prompts-and-workflows-for-code-review-with-goose-51m1)

**Aider**
- `Aider-AI/aider`: Apache-2.0, 50,220 stars. The last push was 2026-05-22, six months before this snapshot. — [GitHub API](https://api.github.com/repos/Aider-AI/aider)
- PyPI shows 0.86.0 (2025-08-09), 0.86.1 (2025-08-13) and 0.86.2 (2026-02-12), with no release since. — [PyPI aider-chat history](https://pypi.org/project/aider-chat/#history)
- A community fork, `aider-ce` (cecli), ships frequent releases and says Aider has been "painfully slow in receiving updates" (from a search-result summary). — [PyPI aider-ce](https://pypi.org/project/aider-ce/0.92.0/)
- Scripting: `--message/-m` or `--message-file` run a single instruction and exit, with `--yes`, `--no-auto-commits` and `--dry-run`. The Python API "is not officially supported". The scripting page has no CI guidance. — [Aider scripting docs](https://aider.chat/docs/scripting.html)
- A GitHub search of Aider issue and PR titles for "code review" returned 0 results, so I found no review feature or official review workflow. — [GitHub search](https://github.com/Aider-AI/aider/issues?q=%22code+review%22+in%3Atitle)

**Crush (charmbracelet/crush)**
- 29,164 stars. The GitHub API reports the license as NOASSERTION. The actual license is FSL-1.1-MIT: source-available, it forbids "Competing Use", and each version converts to MIT two years after release. — [GitHub API](https://api.github.com/repos/charmbracelet/crush); [LICENSE.md](https://github.com/charmbracelet/crush/blob/main/LICENSE.md)
- Headless evolution:
  - Request for `--provider/--model` flags on `crush run` (2025-10-31). — [crush#1354](https://github.com/charmbracelet/crush/issues/1354)
  - "run Crush as an ACP server" (2026-01-05). — [crush#1769](https://github.com/charmbracelet/crush/pull/1769)
  - `crush run --model` (2026-01-15). — [crush#1889](https://github.com/charmbracelet/crush/pull/1889)
  - "continue non-interactive sessions" (2026-03-12). — [crush#2401](https://github.com/charmbracelet/crush/pull/2401)
- Open rough edges:
  - a `--no-tools` flag for single invocations (2026-08-23) — [crush#3621](https://github.com/charmbracelet/crush/issues/3621)
  - "print the whole answer in crush run" (2026-11-11) — [crush#4270](https://github.com/charmbracelet/crush/pull/4270)
- I found no review command, GitHub App or PR integration.

**SWE-agent / mini-swe-agent**
- SWE-agent: MIT, 20,854 stars. mini-swe-agent: MIT, 9,967 stars. Both pushed 2026-11-16. — [GitHub API](https://api.github.com/repos/SWE-agent/SWE-agent); [GitHub API](https://api.github.com/repos/SWE-agent/mini-swe-agent)
- mini-swe-agent v2:
  - Design: "some 100 lines of python" and bash only, with no tool-calling interface.
  - Models: anything via litellm, OpenRouter or Portkey.
  - Claims: over 74% on SWE-bench Verified (a project claim). The README recommends it as the default over SWE-agent and does not mention code review. — [mini-swe-agent README](https://github.com/SWE-agent/mini-swe-agent)
- Community adaptations are tiny:
  - `yuki-uix/pr-review-agent` (0 stars, Aug 2026): "Read-only, evidence-based PR review agent built on mini-swe-agent".
  - `trkaplan/local-harness-bench` (0 stars, Nov 2026) benchmarks Pi, opencode and mini-swe-agent on a local Qwen model. — [GitHub](https://github.com/yuki-uix/pr-review-agent); [GitHub](https://github.com/trkaplan/local-harness-bench)

### Inferences
- `goose review` is the most "review-native" local CLI among the OSS harnesses: checks-as-markdown, severity threshold, parallel per-check sub-agents. Mirroring `amp review` suggests a cross-tool convention for local review is forming. The PR-bot layer is still DIY, posting a single comment.
- Aider's dormancy and the community fork mean it is a poor base for new review pipelines in 2026, although its `--message` scripting still works.
- Crush's FSL license makes it unsuitable as the basis of a commercial review service, though internal use is allowed.
- mini-swe-agent's minimalism (bash only, linear history) makes it easy to fork into a read-only reviewer, but there is no community traction for that use.

### Gaps
- I did not confirm the merge status of goose#9114 via the API (rate-limited). The command's presence in distro man pages (openSUSE Tumbleweed) shows it shipped.
- No user reports found on `goose review` quality.
- No 2025–2026 Aider review workflows of note found.

---

## 6. Other OSS harnesses with review traction, and OSS projects that build review workflows on top of harnesses

### Takeaway
Outside the big harnesses, review-on-harness projects are numerous but small. The notable ones:
- the official OpenHands `pr-review` plugin (185 stars)
- `mr-karan/hodor` (117 stars; OpenHands SDK; GitHub and GitLab)
- Kilo Code Reviewer (hosted, on an OpenCode fork)
- many single-digit-star actions on OpenCode, OpenHands, mini-swe-agent or Cline

A 2026 pattern is "skills/plugins" packs that add review workflows to several harnesses at once (OpenCode, Pi, Codex, Claude Code), plus multi-harness orchestrators with cross-model review. Vendor-backed OSS CLIs (Qwen Code, Gemini CLI, Codex CLI) are out of scope here.

### Cited Findings
**Review projects built on harnesses (stars as of 2026-11-22)**
- `OpenHands/extensions` (pr-review plugin): MIT, 185 stars. — [GitHub](https://github.com/OpenHands/extensions)
- `mr-karan/hodor`: "Agentic code reviewer for GitHub PRs and GitLab MRs", MIT, 117 stars, created 2025-11-05, pushed 2026-11-09.
  - It is built on the OpenHands Agent SDK, supports any LiteLLM model, a custom gateway and self-hosted GitLab, and posts results with `--post`.
  - Each review runs in an isolated temporary workspace, with token and cost reporting (README, read via the fork). — [GitHub (original)](https://github.com/mr-karan/hodor); [README via fork rhnvrm/hodor](https://github.com/rhnvrm/hodor)
- `pgup-ai/jbot-review-action`: MIT, 5 stars, created 2026-06. "Open-source AI code review in your own GitHub Actions — bring an OpenCode gateway key or a CLI subscription". — [GitHub](https://github.com/pgup-ai/jbot-review-action)
- `wende/agentic-pr-review` (1 star, 2026-07): OpenHands-based PR reviews "with follow-up awareness", which targets the dedup-across-pushes gap. — [GitHub](https://github.com/wende/agentic-pr-review)
- `gutierrezje/diffowl` (10 stars, MIT, 2026-05): "Local AI code review from your terminal". A search summary says it runs OpenCode locally; I did not verify this. — [GitHub](https://github.com/gutierrezje/diffowl)
- `Shadowsong27/gh-actions-commons`: a reusable `opencode run` PR-review action described in the author's blog (2026-05-10). — [blog](https://shadowsong27.github.io/2026/05/ai-log-2-adding-an-ai-pr-reviewer-to-my-agent-harness/)
- Cline SDK review-agent example: review plus judge, then a batched COMMENT review (2026-08-26). — [Cline blog](https://cline.bot/blog/building-a-code-review-agent-with-cline-sdk)

**Cross-harness review skills and orchestrators (2026)**
- `waybarrios/opencode-power-pack` (559 stars, 2026-04): 55 skills including code review and security audit for Claude Code, Codex, OpenCode 1 and 2, and Pi. — [GitHub](https://github.com/waybarrios/opencode-power-pack)
- `persiyanov/herdr-reviewr` (1,016 stars, 2026-06): lets a human review an agent's diff in a terminal pane and send comments back to Claude Code, Codex, OpenCode or Pi. This is human review of agent output, not a PR bot. — [GitHub](https://github.com/persiyanov/herdr-reviewr)
- `the-open-engine/zeroshot` (2,219 stars, 2025-12): a multi-agent graph harness in which "separate agents review and test the work". — [GitHub](https://github.com/the-open-engine/zeroshot)

**Other harnesses, for context**
- Qwen Code: 30,868 stars, Apache-2.0. It is vendor-backed (Alibaba) and out of scope. — [GitHub API](https://api.github.com/repos/QwenLM/qwen-code)
- Plandex: 15,931 stars, no push since 2025-10-03, so effectively dormant. — [GitHub API](https://api.github.com/repos/plandex-ai/plandex)
- "Pi" is repeatedly named as a supported harness in 2026 review tooling (see power-pack, herdr-reviewr, local-harness-bench). I could not fetch its metadata. — [herdr-reviewr](https://github.com/persiyanov/herdr-reviewr)

### Inferences
- Real-world "review on a general harness" in late 2026 clusters around OpenCode (largest user base; its GitHub agent is the default DIY path) and OpenHands (most complete OSS reviewer). Hodor is the most credible independent OSS project, notably for GitLab users.
- The ecosystem is converging on a few shared primitives: markdown "checks" or REVIEW.md files (goose, Kilo, Continue), severity thresholds, and judge or verification passes (Cline SDK, Kilo sub-agent verification, OpenHands acceptance checks).

### Gaps
- Star counts of the small projects show they exist, not that anyone uses them. I found no download or usage data.
- No metadata for the Pi harness (API query failed).

---

## 7. Cross-cutting: what a harness gives vs a dedicated bot, what is missing, and maturity/stability complaints

### Takeaway
General harnesses give review agents real repo exploration, shell and test execution, sub-agents, any-model choice (including subscriptions and open-weight or local models), self-hosting, and the same tool locally and in CI. What they usually lack, unless a project like OpenHands or Kilo has built it, is the PR-native layer: inline, line-anchored comments and suggestion blocks, replies in threads, state across pushes (dedup or incremental re-review), severity filtering, and reliable failure signalling. The dominant complaints are DIY fragility (triggers, identity, flags changing between CLI versions), duplicate or stale comments on every push, silent failures, token or quota burn, and weak small local models.

### Cited Findings
**What harness-based review adds (vs a dedicated bot)**
- Whole-repo context: the OpenHands reviewer "analyzes changes in the context of the whole repository" (paraphrase of the docs). — [OpenHands docs](https://docs.openhands.dev/openhands/usage/use-cases/code-review)
- Tools: Continue checks are agents that can read and write files, run bash and use a browser. — [HN 47049848](https://news.ycombinator.com/item?id=47049848)
- Verification passes: OpenHands extensions added "independent acceptance checks" (2026-09-13). Kilo's main reviewer verifies sub-agent findings. Cline's SDK example uses a judge pass. — [OpenHands extensions#572](https://github.com/OpenHands/extensions/pull/572); [Kilo docs](https://kilo.ai/docs/automate/code-reviews/overview); [Cline blog](https://cline.bot/blog/building-a-code-review-agent-with-cline-sdk)
- Cost and control: no per-seat, per-repo or per-PR fees, any CI (including self-hosted or Bitbucket), and the prompt under your control. — [Martin Alderson, 2026-02-26](https://martinalderson.com/posts/using-opencode-in-cicd-for-ai-pull-request-reviews/)
- The same tool works locally and in CI: `goose review`, Kilo `/review`, `cn check`. — [goose man page](https://www.mankier.com/1/goose-review); [Kilo docs](https://kilo.ai/docs/automate/code-reviews/overview); [cn-check SKILL.md](https://raw.githubusercontent.com/continuedev/continue/HEAD/skills/cn-check/SKILL.md)

**What is typically missing (evidence)**
- Inline, line-anchored comments:
  - OpenCode posts one big comment. — [#13918](https://github.com/anomalyco/opencode/issues/13918)
  - The Cline sample posts a single comment, and inline comments need extra plumbing. — [Cline docs](https://docs.cline.bot/cli/samples/github-pr-review)
  - The goose CI tutorial posts a single `gh pr comment`. — [goose docs](https://goose-docs.ai/docs/tutorials/cicd)
  - Cline's SDK falls back to summary-only when a comment lands outside the diff hunk. — [Cline blog](https://cline.bot/blog/building-a-code-review-agent-with-cline-sdk)
  - OpenHands needed a fix to teach the agent how suggestion blocks work (2026-06-02). — [extensions#293](https://github.com/OpenHands/extensions/pull/293)
- State across pushes and dedup:
  - Rapid pushes produce stale reviews and repeated flags. — [shadowsong27, 2026-05-10](https://shadowsong27.github.io/2026/05/ai-log-2-adding-an-ai-pr-reviewer-to-my-agent-harness/)
  - Continue re-posts stale task results to new commits. — [continue#12382](https://github.com/continuedev/continue/issues/12382)
  - OpenHands does not re-review on push at all. — [OpenHands docs](https://docs.openhands.dev/openhands/usage/use-cases/code-review)
- Thread and trigger UX:
  - OpenCode replies outside review threads, and review bodies are not a trigger. — [#37560](https://github.com/anomalyco/opencode/issues/37560); [#50247](https://github.com/anomalyco/opencode/issues/50247)
  - OpenHands ignores mentions made in formal reviews. — [OpenHands#12513](https://github.com/OpenHands/OpenHands/issues/12513)
- Severity filtering exists only where it was built: OpenHands 🔴/🟠/🟡/🟢 labels, `goose review --severity`, Kilo Strict/Balanced/Lenient. Generic OpenCode, Cline and Aider setups rely on prompt wording. — [OpenHands docs](https://docs.openhands.dev/openhands/usage/use-cases/code-review); [goose man page](https://www.mankier.com/1/goose-review); [Kilo docs](https://kilo.ai/docs/automate/code-reviews/overview)
- Silent failure and observability:
  - A Kilo check stays green while no review is posted. — [kilocode#13153](https://github.com/Kilo-Org/kilocode/issues/13153)
  - Quota exhaustion looks the same as other errors. — [shadowsong27](https://shadowsong27.github.io/2026/05/ai-log-2-adding-an-ai-pr-reviewer-to-my-agent-harness/)
  - goose CI output filtering is fragile. — [goose docs](https://goose-docs.ai/docs/tutorials/cicd)

**Maturity and stability complaints**
- Token burn and runaway loops: Kilo's OpenCode-core loop cost $626.34 (2026-09-04), and a sub-agent reasoning loop appears in Kilo's review workflow (2026-09-17). — [kilocode#13772](https://github.com/Kilo-Org/kilocode/issues/13772); [kilocode#14218](https://github.com/Kilo-Org/kilocode/issues/14218)
- Breaking CLI changes:
  - Cline's PR-review workflow broke on a flag change (2026-02-05), followed by auth and packaging breakages in 3.x and 4.0. — [cline#9120](https://github.com/cline/cline/pull/9120); [cline#10770](https://github.com/cline/cline/issues/10770); [cline#11998](https://github.com/cline/cline/issues/11998)
  - The OpenHands action moved repos twice (SDK → extensions), and docs warn that older guides point to stale paths. — [OpenHands docs](https://docs.openhands.dev/openhands/usage/use-cases/code-review)
  - OpenCode 2 is coming on a v2 branch. — [kilocode#12887](https://github.com/Kilo-Org/kilocode/issues/12887)
- Platform discontinuation: the Roo Code extension and its cloud reviewer shut down (2026-05-15). — [Roo-Code README](https://github.com/RooCodeInc/Roo-Code)
- Subscription-auth risk: Anthropic barred third-party harness use of subscriptions (Feb 2026), OpenCode removed its Claude Pro/Max plugin (Mar 2026, secondary sources), and ChatGPT OAuth tokens expire every 14 days. — [The Register](https://www.theregister.com/2026/02/20/anthropic_clarifies_ban_third_party_claude_access); [x-cmd (secondary)](https://www.x-cmd.com/ja/blog/260320); [Martin Alderson](https://martinalderson.com/posts/using-opencode-in-cicd-for-ai-pull-request-reviews/)
- Local-model quality and logistics: a community guide says small models (about 3B) give generic or wrong review comments and suggests a 14B-class model at Q4 as the practical minimum. GitHub-hosted runners cannot reach a local Ollama, so a self-hosted runner is needed. This is from a search-result summary; the post date was not verified. — [DEV (pickuma)](https://dev.to/pickuma/automate-python-code-reviews-with-free-local-llms-and-github-actions-o54)
- Security (brief; covered by another researcher):
  - Cline's docs say an auto-approved review job can run any shell command. — [Cline docs](https://docs.cline.bot/cli/samples/github-pr-review)
  - OpenHands warns about `pull_request_target` and key exfiltration. — [OpenHands docs](https://docs.openhands.dev/openhands/usage/use-cases/code-review)
  - goose is hardening its review diff helpers. — [goose#11617](https://github.com/aaif-goose/goose/pull/11617)
  - There was the "Stop Using OpenCode" criticism (Jul 2026, secondary). — [labmemo](https://labmemo.com/?p=54107)

#### Repo snapshot (GitHub API, fetched 2026-11-22 UTC)
| Harness | Canonical repo (renamed from) | Stars | License | Status | Review features (summary) | Hosted/paid layer |
|---|---|---|---|---|---|---|
| OpenCode | anomalyco/opencode (sst/opencode) | 228,569 | MIT | very active | GitHub agent `/oc`, auto PR review action, TUI `/review`; no native inline comments | OpenCode GitHub App token exchange (api.opencode.ai); Zen/Go gateways |
| OpenHands | OpenHands/OpenHands (All-Hands-AI/OpenHands) | 94,064 | MIT + source-available `enterprise/` | very active | MIT `pr-review` plugin with inline comments, severity, verdicts, sub-agents | Cloud Automation (org-wide), GitLab via Cloud, Enterprise |
| Cline | cline/cline | 71,823 | Apache-2.0 | active | CLI + documented PR-review workflow (summary comment), SDK review example | none review-specific found |
| Goose | aaif-goose/goose (block/goose) | 56,871 | Apache-2.0 | active (AAIF/LF) | `goose review` (checks, severity), CI tutorial, recipes | none (goose-bot PR unmerged) |
| Aider | Aider-AI/aider | 50,220 | Apache-2.0 | maintenance (last push 2026-05-22) | none; `--message` scripting | none |
| Continue | continuedev/continue | 36,535 | Apache-2.0 | active | AI checks as GitHub status checks; `cn check` local | GitHub App runner, Hub, Mission Control, Team plan |
| Crush | charmbracelet/crush | 29,164 | FSL-1.1-MIT (source-available) | active | none; `crush run` headless | n/a |
| Kilo Code | Kilo-Org/kilocode | 28,087 | MIT | very active | local `/review`; hosted Code Reviewer (GitHub/GitLab) | Code Reviewer in Kilo Cloud; credits |
| Roo Code | RooCodeInc/Roo-Code | 24,238 | Apache-2.0 | ARCHIVED (shut down 2026-05-15) | HISTORICAL: Cloud PR Reviewer | discontinued |
| SWE-agent | SWE-agent/SWE-agent | 20,854 | MIT | active (research) | none | none |
| mini-swe-agent | SWE-agent/mini-swe-agent | 9,967 | MIT | active (research) | none | none |
Sources: [GitHub API](https://api.github.com) per-repo calls listed in the sections above.

### Inferences
- A general harness is a good review engine but a poor review product. Teams that choose it get depth (tests, exploration, any model, low cost) and must rebuild the PR-native layer (anchoring, dedup, severity, thread replies, failure signalling). The projects that invested in that layer (OpenHands extensions, Kilo, Cline SDK example, goose review) are where harness-based review matured in 2026.
- A plausible decision rule for the report: use a harness when you need self-hosting, model freedom or execution-based verification. Use a dedicated bot when you need polished PR UX and incremental reviews.

### Gaps
- I found no independent, quantitative comparison (precision, recall or noise) of harness-based review vs dedicated bots in 2025–2026. The user reports here are qualitative.
- Reddit threads (r/LocalLLaMA, r/ChatGPTCoding) were not surfaced by search in this pass, so local-model review quality rests on one community guide.
