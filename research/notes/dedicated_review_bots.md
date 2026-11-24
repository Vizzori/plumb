# Dedicated open-source AI code-review bots and apps (state as of 2026-11-23)

## Q1. Qodo PR-Agent: architecture, platforms, models, config, paid vs OSS, governance and health, recurring complaints

### Takeaway
PR-Agent is no longer a Qodo product. Qodo handed it to a community GitHub org, The-PR-Agent, on 2026-04-23. It now has 16.6k stars, a release every 1–2 weeks and only 14 open issues. Its license has changed three times: Apache-2.0 → AGPL-3.0 (June 2025) → Apache-2.0 (June 2026) → MIT (August 2026). Technically it is still a non-agentic prompt pipeline over the diff, with one LLM call per command in the simple case. It has good diff compression, "dynamic context" and very broad platform and model coverage. The complaints keep coming back to the same things: duplicate comments on re-runs, large PRs being truncated, local models breaking, inline comments landing on the wrong line on specific platforms, and configuration sprawl. The community has fixed many of these during 2026.

### Cited Findings

#### Method note for stats
- Star, fork and issue counts below come from the GitHub REST API and github.com pages, retrieved 2026-11-23. Release dates come from GitHub release pages and Atom feeds, and from PyPI upload history. A request to `qodo-ai/pr-agent` now redirects to `The-PR-Agent/pr-agent` — [GitHub repo](https://github.com/The-PR-Agent/pr-agent)

#### Identity, governance, license, health
- As of 2026-11-23: 16,564 stars, 2,239 forks, created 2023-07-05, last push 2026-11-22. The repo description says it is "The Original Open-Source PR Reviewer" and adds "This project is not the Qodo free tier." — [GitHub repo](https://github.com/The-PR-Agent/pr-agent)
- Open items as of 2026-11-23: 14 open issues; the API's open count of 50 includes about 36 open PRs. That is very low for a project this size, and suggests active triage — [GitHub issue search](https://github.com/The-PR-Agent/pr-agent/issues?q=is%3Aissue%20is%3Aopen)
- Handoff: Qodo's blog post of 2026-04-23 announces the move from qodo-ai/pr-agent to the community-owned The-PR-Agent org, which it describes as independent of Qodo. Qodo's stated reasons:
  - its investment is focused on its enterprise platform;
  - PR-Agent had fallen behind the Qodo platform.
- Governance after the handoff:
  - Naor Peled is the first external maintainer.
  - Ofir Friedman, a Qodo contributor, stays on the core team.
  - Naor Peled, Ofir Friedman and Dana Fine form a governance committee.
  - Moving to an external foundation is being explored but not committed.
  - The release pipeline is being rebuilt.
  - Source: [Qodo blog, 2026-04-23](https://www.qodo.ai/blog/qodo-is-handing-pr-agent-over-to-the-community/)
- The current README says:
  - Qodo donated PR-Agent; it is now "fully community-owned" and open to more maintainers.
  - Docs moved to docs.pr-agent.ai.
  - Qodo Merge ("Qodo 1.0") evolved into Qodo 2.0, a separate AI code-review platform.
  - Qodo is listed as the Gold Sponsor.
  - Sponsorship goes through Naor Peled's GitHub Sponsors.
  - The project is described as in the process of being donated to a foundation.
  - Source: [README](https://github.com/The-PR-Agent/pr-agent/blob/main/README.md)
- License history, verified from the LICENSE file at each tag:
  - Apache-2.0 at v0.26 (2024-12-30), v0.28 (2025-03-28) and v0.29 (2025-05-17) — [v0.29 LICENSE](https://github.com/The-PR-Agent/pr-agent/blob/v0.29/LICENSE)
  - AGPL-3.0 from v0.30 (2025-06-21) through v0.35.0 (2026-05-14) — [v0.30 LICENSE](https://github.com/The-PR-Agent/pr-agent/blob/v0.30/LICENSE)
  - Apache-2.0 again at v0.36.0 (2026-06-01) and v0.38.0 — [v0.36.0 LICENSE](https://github.com/The-PR-Agent/pr-agent/blob/v0.36.0/LICENSE)
  - MIT ("Copyright (c) 2026 The PR Agent") from v0.40.0 (2026-08-18) to today; PyPI also lists MIT — [v0.40.0 LICENSE](https://github.com/The-PR-Agent/pr-agent/blob/v0.40.0/LICENSE), [PyPI](https://pypi.org/project/pr-agent/)
  - Conflict: Qodo's handoff post says the project returns to Apache 2.0. The repo did that in June 2026, then moved again to MIT by August 2026. I found no announcement explaining the MIT switch — [Qodo blog](https://www.qodo.ai/blog/qodo-is-handing-pr-agent-over-to-the-community/)
- Late-2025 slowdown under Qodo:
  - v0.31 shipped on 2025-11-06 and v0.32 not until 2026-02-22, a gap of about 3.5 months — [v0.31](https://github.com/The-PR-Agent/pr-agent/releases/tag/v0.31), [v0.32](https://github.com/The-PR-Agent/pr-agent/releases/tag/v0.32)
  - By v0.31 (Nov 2025) the README already called PR-Agent a "legacy" project kept up by the community, said it was looking for more maintainers, and called it a separate product from Qodo Merge — [v0.31 README](https://github.com/The-PR-Agent/pr-agent/blob/v0.31/README.md)
- PyPI publishing gap: per the PyPI upload history, version 0.3.0 was uploaded 2025-06-21 and nothing more until 0.34.1 on 2026-05-02. The v0.43.0 notes say "PyPI releases are back" and that 0.40–0.42 were backfilled — [PyPI history](https://pypi.org/project/pr-agent/#history), [v0.43.0 notes](https://github.com/The-PR-Agent/pr-agent/releases/tag/v0.43.0)
- Release cadence after the handoff, per PyPI and GitHub:
  - 0.34.1 on 2026-05-02, 0.35.0 on 05-14, 0.36.0 on 06-01, 0.37–0.39 in June–July.
  - 0.40–0.42 published on 08-18 (backfill).
  - 0.43 on 08-22, 0.44 on 08-30, 0.45 on 09-05, 0.46 on 09-21, 0.47 on 10-02, 0.48 on 10-16, 0.49 on 10-25, 0.50 on 11-07.
  - That is about 17 minor versions in 6 months — [Releases](https://github.com/The-PR-Agent/pr-agent/releases)
- Docker images moved: releases 0.34.2+ publish to `pragent/pr-agent`. The old `codiumai/pr-agent` namespace is a frozen archive up to v0.31 — [README](https://github.com/The-PR-Agent/pr-agent/blob/main/README.md)
  - A user reported on 2026-04-04 that `codiumai/pr-agent:0.33` and `:0.34` images did not match their source tags — [#2306](https://github.com/The-PR-Agent/pr-agent/issues/2306)
- Conflicting third-party claim: an independent Dec 2025 blog says pr-agent was "archived in November 2025" and that Qodo had moved toward closed source and SaaS — [happyassassin.net, 2025-12-16](https://www.happyassassin.net/posts/2025/12/16/a-half-assed-assessment-of-open-source-ai-code-review-tools/). I could not confirm an archive. v0.32 was released from the same repo on 2026-02-22 — [v0.32](https://github.com/The-PR-Agent/pr-agent/releases/tag/v0.32)
- Analyst risk view (Futurum, 2026-04-23):
  - possible fragmentation and slower consensus;
  - possible competing forks;
  - no commercial support, which could slow enterprise uptake;
  - open questions about security and roadmap stability.
  - Futurum gives no adoption numbers — [Futurum](https://futurumgroup.com/insights/qodo-hands-pr-agent-to-the-community-will-open-governance-accelerate-ai-code-review/)
- Forks: no significant competing fork surfaced. Examples found:
  - Writesonic/qodo-pr-agent, a copy archived 2025-06-21 — [GitHub](https://github.com/Writesonic/qodo-pr-agent)
  - a one-off PyPI fork `pr-agent-patched` 0.3.2 (2026-02-09), published during the PyPI gap — [PyPI](https://pypi.org/project/pr-agent-patched/)
  - The maintainers are crowdsourcing a list of adopters in an open issue — [#3778](https://github.com/The-PR-Agent/pr-agent/issues/3778)

#### Architecture: is it agentic?
- Commands (run as PR comments or from the CLI):
  - /describe, /review, /improve, /ask, ask-on-code-lines
  - /add_docs, /generate_labels, /similar_issue, /help, /update_changelog
  - /help_docs, disabled since v0.36.1 because of a credential-exposure issue
  - Sources: [README](https://github.com/The-PR-Agent/pr-agent/blob/main/README.md), [Supported platforms](https://docs.pr-agent.ai/overview/supported_platforms/)
- Cost model: per the README, simple /review and /ask requests can be a single LLM call; retries, fallbacks and larger reviews need more calls — [README](https://github.com/The-PR-Agent/pr-agent/blob/main/README.md)
- PR compression for diffs that don't fit in one prompt:
  - drop binary and non-code files;
  - order files by the repo's main languages;
  - for large PRs, keep additions over deletions (deletion-only hunks are removed, deleted files become a list);
  - count tokens with tiktoken, packing the largest files first within each language;
  - list the files that don't fit under "other modified files", then hard-stop at the token limit.
  - Small PRs get 5 extra context lines before each hunk and 1 after by default — [Compression strategy docs](https://docs.pr-agent.ai/core-abilities/compression_strategy/)
- "Dynamic context" gives asymmetric context (more lines before a change than after). It can extend up to the enclosing function or class, which is a structural hint, not repository exploration — [Dynamic context docs](https://docs.pr-agent.ai/core-abilities/dynamic_context/)
- Large-PR chunking for /review is opt-in:
  - `enable_large_pr_chunking` (default false) splits the diff into up to `max_number_of_calls` chunks (default 3) and merges the results;
  - `num_max_findings` defaults to 6;
  - the JSON output lists `files_not_reviewed` and `files_partially_reviewed`.
  - Source: [/review docs](https://docs.pr-agent.ai/commands/review/); chunking added in v0.45.0 (2026-09-05) — [v0.45.0 notes](https://github.com/The-PR-Agent/pr-agent/releases/tag/v0.45.0)
- 2026 additions to /review: a merge recommendation driven by deterministic checks plus a model veto, and a risk rating that can take structural facts from a build-graph tool (e.g., Nx, Bazel) as an input file — [/review docs](https://docs.pr-agent.ai/commands/review/)
- "Agent skills" are not tool use:
  - SKILL.md files are discovered on the host and their text is injected into the /review, /describe and /ask prompts, under a token budget.
  - `skills.paths` is host-only, so a malicious repo cannot point it at files like ~/.ssh.
  - Source: [Agent skills docs](https://docs.pr-agent.ai/core-abilities/agent_skills/)
- Other context sources:
  - repo context files (AGENTS.md);
  - ticket context: native issues on GitHub/GitLab, work items on Azure DevOps, Jira/Asana/Linear integrations elsewhere;
  - local and global metadata.
  - Source: [Supported platforms](https://docs.pr-agent.ai/overview/supported_platforms/). Jira ticket context was added in v0.46.0 (#2420) — [v0.46.0 notes](https://github.com/The-PR-Agent/pr-agent/releases/tag/v0.46.0)
- Modes without a git host: local branch compare, plain-diff from stdin, and a "MOSAICO" A2A server that other agents can call with a PR URL or diff — [Supported platforms](https://docs.pr-agent.ai/overview/supported_platforms/)
- There is no repository-exploration or tool loop. A request for code-graph support has been open since 2026-07-03 with 15 comments — [#2499](https://github.com/The-PR-Agent/pr-agent/issues/2499)

#### Git platforms
- Full matrix: GitHub, GitLab, Bitbucket Cloud, Bitbucket Server, Azure DevOps and Gitea all support describe/review/improve/ask, CLI and app/webhook.
  - Ask-on-code-lines works only on GitHub, GitLab and Azure DevOps.
  - Similar Issues is GitHub-only.
  - Action/pipeline runners exist for GitHub, GitLab, Bitbucket Cloud and Azure DevOps.
- Gerrit and AWS CodeCommit are registered providers with reduced support:
  - no ask-on-lines;
  - labels and changelog are posted as comments;
  - Gerrit has no installation page yet.
  - Source: [Supported platforms (as of 2026-11-23)](https://docs.pr-agent.ai/overview/supported_platforms/)

#### Model support (LiteLLM) and local models
- Any model reachable through LiteLLM: OpenAI, Anthropic, Gemini, DeepSeek, Mistral, Azure OpenAI, Bedrock, Vertex, Databricks, OpenRouter, Ollama, vLLM, and others — [README](https://github.com/The-PR-Agent/pr-agent/blob/main/README.md), [Changing a model](https://docs.pr-agent.ai/usage-guide/changing_a_model/)
- Ollama setup requires `custom_model_max_tokens`, `duplicate_prompt_examples=true` and raising `OLLAMA_CONTEXT_LENGTH`. The docs say local open-source models suit experimentation (mainly /ask) and are not suitable for production-level code analysis; this note is dated "as of January 2025" — [Changing a model](https://docs.pr-agent.ai/usage-guide/changing_a_model/)
- v0.49.0 (2026-10-25) changed the default model to `gpt-6.1-sol`, with `gpt-6-luna` as fallback. That shows the defaults track current commercial models and change between releases — [v0.49.0 notes](https://github.com/The-PR-Agent/pr-agent/releases/tag/v0.49.0)

#### Configuration
- Layering: `.pr_agent.toml` on the repo's default branch, an org-level global config repo (`global_settings_repo`) and an external config URL. Local overrides global, and global overrides the external URL — [Configuration options](https://docs.pr-agent.ai/usage-guide/configuration_options/)
- Per-directory `.pr_agent.toml` for monorepos arrived in v0.46.0 (2026-09-21) — [v0.46.0 notes](https://github.com/The-PR-Agent/pr-agent/releases/tag/v0.46.0)
- Each tool takes `extra_instructions`, for example `[pr_reviewer] extra_instructions = "..."` — [/review docs](https://docs.pr-agent.ai/commands/review/)
- Security hardening has steadily moved settings to host-only (repo files and comments can no longer set them). Examples:
  - `extra_config_url` (v0.47.0) — [v0.47.0](https://github.com/The-PR-Agent/pr-agent/releases/tag/v0.47.0)
  - `litellm.extra_headers` (v0.49.0) — [v0.49.0](https://github.com/The-PR-Agent/pr-agent/releases/tag/v0.49.0)
  - GitHub pacing/retries, custom labels and `max_number_of_calls` (v0.50.0) — [v0.50.0](https://github.com/The-PR-Agent/pr-agent/releases/tag/v0.50.0)
- Breaking upgrade changes in autumn 2026:
  - v0.47.0: the GitHub Action now fails when a tool fails, and comment commands need a leading "/" on GitLab and Bitbucket — [v0.47.0](https://github.com/The-PR-Agent/pr-agent/releases/tag/v0.47.0)
  - v0.48.0: `pip install pr-agent` no longer installs git-provider SDKs (use extras such as `pr-agent[github]`), and Docker images run as non-root — [v0.48.0](https://github.com/The-PR-Agent/pr-agent/releases/tag/v0.48.0)
- Config confusion is acknowledged: an issue from 2026-09-08 found 82 of 292 configuration keys undocumented — [#3179](https://github.com/The-PR-Agent/pr-agent/issues/3179)

#### What was or is held back for the paid product
- Historical, per the v0.29 README of 2025-05-17, these features were marked as Qodo Merge-only:
  - ticket context; "best practices"; PR chat; suggestion tracking; CI feedback (/checks);
  - /add_docs; custom labels; /analyze; /similar_code; /custom_prompt; /test; /implement; /scan_repo_discussions;
  - auto-approve; static code analysis; global/wiki configuration; interactive PR actions;
  - impact evaluation; code validation; auto best practices.
  - The paid tier also offered hosting, zero data retention and priority support.
  - Source: [v0.29 README](https://github.com/The-PR-Agent/pr-agent/blob/v0.29/README.md)
- Several of those now exist in the community PR-Agent (Nov 2026): Add Docs, Generate Labels, ticket context, and an org-level global config repo — [Supported platforms](https://docs.pr-agent.ai/overview/supported_platforms/), [Configuration options](https://docs.pr-agent.ai/usage-guide/configuration_options/)
- Qodo's current proprietary offering, Qodo 2.0 code review:
  - multi-agent review that is aware of the full repo and its history;
  - Merge Risk; cross-repository conflict detection;
  - requirement gaps against a linked spec; UX deviations against a linked Figma design;
  - fix remediation; CI failure feedback; "skill insights".
  - Qodo's docs still mention `.pr_agent.toml` for shaping reviews.
  - Source: [Qodo docs (as of 2026-11-23)](https://docs.qodo.ai/code-review)
  - The old qodo-merge-docs.qodo.ai domain now redirects there — [redirect check](https://qodo-merge-docs.qodo.ai/)
- Qodo offers a free tier for open-source projects ("supported by Google") — [Qodo OSS page](https://www.qodo.ai/solutions/open-source/). The PR-Agent README says explicitly that the repo is not that offering — [README](https://github.com/The-PR-Agent/pr-agent/blob/main/README.md)

#### Recurring complaints (all issues are in The-PR-Agent/pr-agent; dates are when opened)
- **Duplicate or re-posted comments on re-runs**
  - [#2037](https://github.com/The-PR-Agent/pr-agent/issues/2037), 2025-09-22, 15 comments: request for persistent inline comments so re-runs stop creating duplicates.
  - [#2184](https://github.com/The-PR-Agent/pr-agent/issues/2184), 2026-01-27: asks whether suggestions from the previous push can be remembered.
  - [#3654](https://github.com/The-PR-Agent/pr-agent/issues/3654), 2026-09-23: proposes semantic dedup (show the model its earlier findings) instead of text hashes.
  - Fixes: v0.45.0 "preserve findings across review reruns" — [v0.45.0](https://github.com/The-PR-Agent/pr-agent/releases/tag/v0.45.0); GitLab content-based auto-resolve of fixed threads in v0.46.0 — [v0.46.0](https://github.com/The-PR-Agent/pr-agent/releases/tag/v0.46.0)
- **Large PRs and token limits**
  - [#2042](https://github.com/The-PR-Agent/pr-agent/issues/2042), 2025-09-24: fails to process large PRs with multi-model configs.
  - [#2527](https://github.com/The-PR-Agent/pr-agent/issues/2527), 2026-07-16: request to chunk large diffs for describe, review and improve.
  - [#2978](https://github.com/The-PR-Agent/pr-agent/issues/2978), 2026-09-01: /review had no large-diff chunking.
  - [#4947](https://github.com/The-PR-Agent/pr-agent/issues/4947), 2026-11-14: raise the self-review prompt budget from 32k to 256k tokens.
- **Wrong or low-value suggestions**
  - [#1743](https://github.com/The-PR-Agent/pr-agent/issues/1743), 2025-05-07: Java suggestion wrongly flags a possible NPE inside an `instanceof` expression.
  - [#3014](https://github.com/The-PR-Agent/pr-agent/issues/3014), 2026-09-03: code suggestions break brackets and forget imports.
  - [#1963](https://github.com/The-PR-Agent/pr-agent/issues/1963), 2025-07-29: suggestions seem capped at 3.
  - Historical (HN, 2024-09-10): a user whose company used Codium on internal repos saw nothing beyond lint-level suggestions, though the PR summaries were useful — [HN thread](https://news.ycombinator.com/item?id=41500840)
- **Local models (Ollama/vLLM)**
  - [#535](https://github.com/The-PR-Agent/pr-agent/issues/535), 2023-12-18: request for Ollama support (historical).
  - [#1422](https://github.com/The-PR-Agent/pr-agent/issues/1422), 2024-12-28: authenticated Ollama instance.
  - [#1521](https://github.com/The-PR-Agent/pr-agent/issues/1521), 2025-02-06: no model works with Ollama + deepseek-r1.
  - [#1623](https://github.com/The-PR-Agent/pr-agent/issues/1623), 2025-03-14: unable to make it work with locally hosted Ollama models.
  - [#1932](https://github.com/The-PR-Agent/pr-agent/issues/1932), 2025-07-11: Ollama model names split incorrectly.
  - [#2287](https://github.com/The-PR-Agent/pr-agent/issues/2287), 2026-03-25: regression where provider-specific auth was overridden by `litellm.api_key`.
- **Breakage with new or commercial models**
  - [#2576](https://github.com/The-PR-Agent/pr-agent/issues/2576), 2026-07-29, 20 comments: GPT-5.6-Terra silently fails.
  - [#1901](https://github.com/The-PR-Agent/pr-agent/issues/1901), 2025-06-27: Bedrock response parsing fails.
  - [#461](https://github.com/The-PR-Agent/pr-agent/issues/461) and [#373](https://github.com/The-PR-Agent/pr-agent/issues/373), 2023 (historical): "Failed to parse AI prediction" YAML errors.
- **Inline anchoring and platform-specific posting bugs**
  - [#2410](https://github.com/The-PR-Agent/pr-agent/issues/2410), 2026-05-26: GitLab inline suggestions not posted to the Changes tab.
  - [#2642](https://github.com/The-PR-Agent/pr-agent/issues/2642), 2026-08-13: Azure DevOps inline suggestions silently orphaned when the file path doesn't match.
  - [#3285](https://github.com/The-PR-Agent/pr-agent/issues/3285), 2026-09-10: Bitbucket Cloud multi-line comments collapse onto their first line.
  - [#3739](https://github.com/The-PR-Agent/pr-agent/issues/3739), 2026-09-27: unresolved inline positions drop GitHub review findings.
  - [#2110](https://github.com/The-PR-Agent/pr-agent/issues/2110), 2025-11-20: wrong inline suggestion formatting in Azure DevOps.
  - [#592](https://github.com/The-PR-Agent/pr-agent/issues/592), 2024-01-13 (historical): CLI fails when a comment falls outside the diff hunk.
  - Fix: v0.42.0 anchors GitLab inline comments to the latest diff version — [v0.42.0](https://github.com/The-PR-Agent/pr-agent/releases/tag/v0.42.0)
- **Platform setup pain (historical)**
  - [#171](https://github.com/The-PR-Agent/pr-agent/issues/171), 2023-08-03, 47 comments: GitLab installation guide request.
  - [#1150](https://github.com/The-PR-Agent/pr-agent/issues/1150), 2024-08-16: Bitbucket Cloud pipeline errors.
  - [#1200](https://github.com/The-PR-Agent/pr-agent/issues/1200), 2024-09-06: Azure DevOps pipeline error.
- **Packaging and config**
  - [#2217](https://github.com/The-PR-Agent/pr-agent/issues/2217), 2026-02-17: pip package throws NameError.
  - [#3507](https://github.com/The-PR-Agent/pr-agent/issues/3507), 2026-09-19: every install pulls every provider SDK (fixed via extras in v0.48.0).
  - [#3179](https://github.com/The-PR-Agent/pr-agent/issues/3179): undocumented config keys.
  - [#4444](https://github.com/The-PR-Agent/pr-agent/issues/4444), 2026-10-28, open: refuse config overrides in PR comments by default.
- **No learning from feedback**
  - [#2075](https://github.com/The-PR-Agent/pr-agent/issues/2075), 2025-10-21, closed: feature request to learn from accepted suggestions and reactions.
- **Security (brief; covered elsewhere)**
  - /help_docs disabled pending a credential-exposure fix — [#2445](https://github.com/the-pr-agent/pr-agent/issues/2445)
  - Model output reaches PR comments unsanitized, open — [#4999](https://github.com/The-PR-Agent/pr-agent/issues/4999)
  - v0.44.0 requires signed GitHub webhooks and escapes attacker-controlled webhook fields — [v0.44.0](https://github.com/The-PR-Agent/pr-agent/releases/tag/v0.44.0)

#### Independent assessment
- Fedora QA engineer Adam Williamson (2025-12-16) rated pr-agent the most mature of the OSS tools he examined:
  - broad forge and LiteLLM support;
  - simple, documented standalone deployment (pip/container);
  - weaknesses: primitive tests (many commented out, ~24% coverage).
  - He planned to fork it to add Forgejo support — [happyassassin.net](https://www.happyassassin.net/posts/2025/12/16/a-half-assed-assessment-of-open-source-ai-code-review-tools/)
- Empirical industrial study of PR-Agent at Beko (pointer only; covered by another researcher) — [arXiv 2412.18531](https://arxiv.org/abs/2412.18531)

### Inferences
- PR-Agent's core design has not changed since 2023: it fits the diff into one prompt per command, with compression and heuristics. The 2026 community work went into robustness (chunking, dedup, anchoring fixes), security hardening (host-only settings, webhook secrets) and packaging, not into agentic repo exploration. It remains a diff-centric reviewer with optional extra context. The open #2499 request (code graph) and the opt-in-only chunking support this reading.
- The "held back for paid" question has changed meaning. The tools are no longer an open core and a paid tier of one product. They are two products: a community-owned MIT tool, and a separate proprietary Qodo 2.0 whose differentiators are cross-repo and full-history context, spec and Figma checks, and remediation.
- The license churn (AGPL in mid-2025, then Apache, then MIT in 2026) and the PyPI and Docker discontinuities matter for enterprises: pinned images or packages from 2025 may be stale or mismatched (#2306).
- Very fast release cadence plus frequent breaking changes (v0.47–v0.50) means a self-hosted deployment needs ongoing upgrade work, which partly undercuts the "simple deployment" strength.

### Gaps
- I found no public statement explaining the Apache → MIT relicense (between v0.38.0 and v0.40.0, i.e., summer 2026).
- I could not verify whether qodo-ai/pr-agent was briefly archived in November 2025, as the happyassassin blog claims. Releases continued in Feb 2026.
- I did not confirm whether the current OSS /improve still runs a separate "self-reflection" scoring call; the old docs path now returns a stub.
- I found no Reddit threads with first-hand 2025–2026 PR-Agent experiences; the search returned only docs and marketing write-ups.
- I found no adoption numbers (installs or orgs) from the project or from Futurum.

## Q2. Kodus AI / Kody: architecture, license, self-hosting, cloud vs OSS split, maturity, complaints

### Takeaway
Kodus (kodustech/kodus-ai, 1.6k stars, created March 2025) is the most feature-rich self-hostable OSS reviewer. It builds a persistent AST/code graph of the repo, its review agents have sandboxed file tools, it applies plain-language "Kody Rules", and it has memories, metrics and a CLI. It is open core, though: AGPL-3.0 plus a source-available "Enterprise Code" license, with community limits enforced in the software. Its own public issues are unusually candid about quality:
- its reaction-based learning loop was switched off;
- regex rule detectors got a 44.6% thumbs-down rate;
- Kody posted only about 13–15% of the valid bugs the team found with Claude Code.

### Cited Findings
- As of 2026-11-23: 1,646 stars, 209 forks, created 2025-03-28, last push 2026-11-22, about 172 open issues. GitHub's license field shows NOASSERTION because of the dual license — [GitHub repo](https://github.com/kodustech/kodus-ai), [issue search](https://github.com/kodustech/kodus-ai/issues?q=is%3Aissue%20is%3Aopen)
- Release cadence is very high. On 2026-11-22 alone there were several tags, including 2.2.18, web-1.2.15 and "Self-Hosted Release 2.2.12" — [Releases](https://github.com/kodustech/kodus-ai/releases)
- License:
  - code outside `ee/` directories and `.ee.` files is AGPL-3.0;
  - `ee` code is under the Kodus Enterprise Code License.
  - Under that license, self-hosted community users may run the unmodified enterprise code for community features (code review, BYOK) in production, within limits the software enforces. They may not modify it, bypass the limits, use Enterprise-only features or offer it as a hosted service.
  - Source: [license.md](https://github.com/kodustech/kodus-ai/blob/main/license.md), [license_ee.md](https://github.com/kodustech/kodus-ai/blob/main/license_ee.md)
- Tier split, per the README table:
  - **OSS (free; self-hosted or Kodus-hosted):** BYOK, unlimited PRs and users, up to 10 Kody Rules, up to 3 active plugins, Kody Memory. No Cockpit/engineering metrics, no priority queue, no SSO/RBAC/audit logs, Discord-only support.
  - **Teams:** $10/dev monthly or $8/dev annual, plus tokens.
  - **Enterprise:** custom pricing; SSO, RBAC, audit, SOC 2.
  - Self-host on a VM needs at least 2 CPU, 8 GB RAM and 60 GB disk, with Docker. The README also offers a "Request a trial license" link.
  - Source: [README](https://github.com/kodustech/kodus-ai/blob/main/README.md)
- Platforms: GitHub, GitLab, Bitbucket, Azure DevOps and Forgejo, including self-managed GitLab and Forgejo. Models: BYOK with OpenAI, Anthropic, Gemini, Vertex, Novita or any OpenAI-compatible endpoint, including self-hosted models — [README](https://github.com/kodustech/kodus-ai/blob/main/README.md)
- Architecture: a NestJS monorepo with:
  - `apps/api` for orchestration, Kody Rules and integrations;
  - `apps/worker` for review execution and queues;
  - `apps/webhooks` for ingestion;
  - `apps/web`, a Next.js dashboard;
  - `libs/llm`, the BYOK abstraction.
  - Source: [README](https://github.com/kodustech/kodus-ai/blob/main/README.md)
- Code graph and sandbox:
  - Kodus parses the whole repo into an AST graph (functions, classes, files, imports, calls) using `@kodus/kodus-graph`, stores it in Postgres and rebuilds it incrementally on merges.
  - At review time it parses only the touched files and gives the agent a focused subgraph.
  - The sandbox also gives review agents search, read-file and list-directory tools.
  - Sandbox modes: `local` (default for self-host), E2B (a paid isolation option), and `none` (no AST graph or cross-file context).
  - Source: [Kodus docs, Sandbox & AST Graph](https://docs.kodus.io/how_to_deploy/en/deploy_kodus/sandbox)
- Rules engine:
  - Kody Rules are plain-language rules scoped to an org, repo or path.
  - Production telemetry shows three delivery paths: the generalist LLM agent, rules checked by an LLM judge, and "T0" regex detectors.
  - Source: [README](https://github.com/kodustech/kodus-ai/blob/main/README.md), [#1831](https://github.com/kodustech/kodus-ai/issues/1831)
- Self-hosted instances send one anonymous daily heartbeat of aggregated counters; opt out with `KODUS_TELEMETRY_DISABLED=true` — [README](https://github.com/kodustech/kodus-ai/blob/main/README.md)
- Learning from feedback is partly marketing:
  - Issue #1863 (opened 2026-09-05, closed 2026-09-16) says the documented 👍/👎 "reinforcement learning" loop no longer ran. Reviews use only the agent pipeline; reactions are recorded but don't affect later reviews.
  - The team turned it off on purpose because bare reactions gave low-quality signal, and rewrote the docs to point to Memories, Kody Rules and Automatic Rules Generation.
  - Source: [#1863](https://github.com/kodustech/kodus-ai/issues/1863)
- Quality telemetry the vendor published itself (production data, 2026-08-04 to 2026-09-01, 65 orgs):
  - thumbs-down rate: 1.8% for generalist LLM suggestions (39,130 delivered), 6.2% for LLM-judged Kody Rules (18,171), 44.6% for T0 regex detectors (887);
  - implementation rates: 53% / 46% / 32%;
  - cause: regex detectors published every match without LLM confirmation or language scope (e.g., a Ruby-only rule firing on non-Ruby files).
  - Fixed via PR #1864 (closed 2026-09-07) — [#1831](https://github.com/kodustech/kodus-ai/issues/1831)
- A companion issue's title attributes 38% of thumbs-down to suggestions with empty, identical or truncated "improvedCode" (2026-09-02, closed) — [#1833](https://github.com/kodustech/kodus-ai/issues/1833)
- Recall gap versus general agents:
  - The issue author (sartorijr92, apparently a Kodus team member: assignee and author of all updates) wrote (2026-11-05) that customers find more bugs with Claude Code, Codex and others.
  - On the team's own PRs, Kody posted about 13% of the valid bugs found with Claude Code; a later study found about 15% of 229 valid in-diff bugs.
  - Most of the missed bugs needed context outside the changed file.
  - Experiments (a "siblings" agent, code execution, fuzzing) are still undecided; the issue is open — [#2411](https://github.com/kodustech/kodus-ai/issues/2411)
- Complaints, mostly from self-hosters:
  - [#62](https://github.com/kodustech/kodus-ai/issues/62), 2025-05-28: cannot select a repository to automate.
  - [#68](https://github.com/kodustech/kodus-ai/issues/68), 2025-06-03: maximum context length exceeded.
  - [#267](https://github.com/kodustech/kodus-ai/issues/267), 2025-09-26: 502 on creating an organization.
  - [#1836](https://github.com/kodustech/kodus-ai/issues/1836), 2026-09-02, open: rule configuration not working.
  - [#1849](https://github.com/kodustech/kodus-ai/issues/1849), 2026-09-03, open: the GitHub check stays IN_PROGRESS forever when a review fails internally.
  - [#1845](https://github.com/kodustech/kodus-ai/issues/1845), 2026-09-03, open: fine-tuning embeddings are hardcoded to api.openai.com, so self-hosted BYOK can't supply them.
  - [#1844](https://github.com/kodustech/kodus-ai/issues/1844), 2026-09-03, open: the PR-summary path has no BYOK fallback.
  - [#1871](https://github.com/kodustech/kodus-ai/issues/1871), 2026-09-06, open: OpenRouter reviews fail after a passing connection test, with no diagnostics.
  - [#2583](https://github.com/kodustech/kodus-ai/issues/2583), 2026-11-17, open: "Ultra review" for paid BYOK teams gets one review from three of their models.
- Independent view (2025-12-16): Kodus is actively developed and has broad forge and model support. But it is TypeScript, deployment looks complex (local use documented only for development), and the author disliked its review style, calling the project "a sloppy vibe". Not recommended — [happyassassin.net](https://www.happyassassin.net/posts/2025/12/16/a-half-assed-assessment-of-open-source-ai-code-review-tools/)
- Community traction on HN is minimal: Show HN on 2025-04-03 got 3 points and 0 comments; a second Show HN on 2026-05-07 got 4 points — [HN 43572816](https://news.ycombinator.com/item?id=43572816), [HN 48049508](https://news.ycombinator.com/item?id=48049508)

### Inferences
- Kodus is agentic and uses a code graph and file tools, while PR-Agent is not. The vendor's own data shows that this alone does not close the recall gap to general coding agents (about 13–15%). It also shows that precision problems came mostly from the cheapest deterministic path (regex detectors), not from the LLM.
- "Open source" in Kodus's marketing means open core. A real share of the features (rule counts, plugins, metrics, SSO) is enforced by enterprise-licensed code that self-hosters may not modify. Teams with strict open-source requirements should treat it as source-available plus AGPL.
- Publishing internal telemetry in public issues is a strength for transparency, and a rare source of real precision and recall numbers in this category. They are still vendor-measured.

### Gaps
- The license of `@kodus/kodus-graph` (the npm AST parser) was not verified.
- I found no independent benchmark of Kodus. Its "less noise" claims are vendor claims, apart from its own telemetry.
- The exact community limits enforced in self-hosted mode beyond rules and plugins (e.g., Kody Memory size) were not verified.

## Q3. The long tail: per-tool profiles

### Takeaway
Most first-generation (2023) "send the diff to GPT" bots are now stale or gone:
- ai-codereviewer: last commit Dec 2023;
- CodeRabbit's ai-pr-reviewer: archived in 2024 and now returns 404;
- codedog: archived;
- anc95's ChatGPT-CodeReview: maintenance trickle only.

The projects still alive in 2026 moved toward optional agent modes that explore the repo:
- Shippie (agent loop + MCP);
- Nikita-Filonov/ai-review (ReAct shell exploration, six platforms);
- sunmh207/AI-Codereview-Gitlab (agentic mode, Chinese IM integrations, paid Pro);
- Gito (high-confidence filtering, GitHub-first).

Bito's "open-source" agent is a thin wrapper that needs a Bito account key. Gerrit has a maintained but low-activity plugin family. reviewdog and Danger have no maintained LLM add-on.

### Cited Findings

#### Shippie (mattzcarey/shippie, formerly Code Review GPT)
- As of 2026-11-23: 2,533 stars, 241 forks, MIT, created 2023-07-06, about 31 open issues+PRs. Last release v0.21.2 (2026-06-23); the latest main-branch commit in the Atom feed is 2026-07-02, while the API shows a push on 2026-10-21. Before 0.21 the previous release was v0.20.0 (2025-08-01) — [GitHub](https://github.com/mattzcarey/shippie), [Releases](https://github.com/mattzcarey/shippie/releases)
- Approach (2026):
  - an agent loop on the "flue" + "pi" frameworks that reads the diff, explores the codebase with developer tools and posts focused comments;
  - acts as an MCP client;
  - runs in GitHub Actions, GitLab CI, Node or Cloudflare;
  - on-demand `/shippie review`;
  - rules via AGENTS.md/CLAUDE.md and Agent Skills.
  - Providers: Anthropic, OpenAI, OpenRouter, Cloudflare Workers AI.
  - Source: [README](https://github.com/mattzcarey/shippie/blob/main/README.md)
- Low issue traffic since mid-2025 (9 issues since 2025-06-01). Open bug [#522](https://github.com/mattzcarey/shippie/issues/522), 2026-10-07: changed files with non-ASCII names are silently skipped. Older complaints are mostly 2023–24 setup failures, e.g., [#205](https://github.com/mattzcarey/shippie/issues/205) (doesn't run on Ubuntu 22.04/Node 18, 2023-08-21) and [#323](https://github.com/mattzcarey/shippie/issues/323) (missing @gitbeaker/rest module, 2024-01-29) — [issue search](https://github.com/mattzcarey/shippie/issues?q=is%3Aissue+created%3A%3E2025-06-01)
- An open RFC (2026-06-22) proposes `shippie eval` to benchmark reviews against human reviews, so no built-in quality evaluation exists yet — [#471](https://github.com/mattzcarey/shippie/issues/471)

#### Gito (Nayjest/Gito, formerly ai-code-review)
- As of 2026-11-23: 476 stars, 45 forks, MIT, created 2025-04-30, about 63 open issues+PRs. Latest release v4.5.0 (2026-09-05); about monthly releases in July–Sept 2026 — [GitHub](https://github.com/Nayjest/Gito), [Releases](https://github.com/Nayjest/Gito/releases)
- Positioning: it detects "high-confidence, high-impact" issues with parallelized LLM calls. It is vendor-agnostic, including local models, and stateless/client-side with no intermediary server. It can react to PR comments (e.g., asked to fix an issue) and supports post-processing scripts to filter issues.
  - Platforms: GitHub supported; GitLab beta; Bitbucket planned.
  - Integrations: Jira and Linear.
  - Known limitation: it cannot modify `.github/workflows` files when asked to fix something, because of GITHUB_TOKEN restrictions.
  - Source: [README](https://github.com/Nayjest/Gito/blob/main/README.md)
- Complaints:
  - [#135](https://github.com/Nayjest/Gito/issues/135), 2025-08-24: additional commits cause the same issues to be flagged again.
  - [#244](https://github.com/Nayjest/Gito/issues/244), 2026-03-29, open: bad JSON from the LLM breaks parsing.
  - [#132](https://github.com/Nayjest/Gito/issues/132) and [#141](https://github.com/Nayjest/Gito/issues/141), 2025: crashes (TypeError/AttributeError).
  - [#217](https://github.com/Nayjest/Gito/issues/217), open: no conversation context when replying to comments.
  - [#220](https://github.com/Nayjest/Gito/issues/220), open: feedback is not posted as native GitHub PR Reviews.
  - [#260](https://github.com/Nayjest/Gito/issues/260), 2026-05-19: request to use Claude Code instead of an API key.

#### ai-codereviewer (now villesau/ai-codereviewer; formerly aidar-freeed and freeedcom)
- `freeedcom/ai-codereviewer` redirects to `villesau/ai-codereviewer` (checked via the GitHub API on 2026-11-23). As of that date: 1,049 stars, 848 forks (a very high fork ratio, i.e., people fork to customise), MIT. Last commit 2023-12-19, last push 2024-08-19, last release 2023-12-02 ("Support gpt-4-1106-preview"). Stale — [GitHub](https://github.com/villesau/ai-codereviewer)
- Approach: a GitHub Action that takes the PR diff, filters excluded globs, sends chunks to the OpenAI API (default GPT-4) and posts review comments. Diff-only, OpenAI-only — [README](https://github.com/villesau/ai-codereviewer/blob/main/README.md)
- Complaints, all still open:
  - [#34](https://github.com/villesau/ai-codereviewer/issues/34), 2023-12-09: GitHub rejects comments ("review thread path is invalid"), a line/path anchoring failure.
  - [#56](https://github.com/villesau/ai-codereviewer/issues/56), 2024-03-29: JSON failures with gpt-4-0125-preview.
  - [#21](https://github.com/villesau/ai-codereviewer/issues/21), 2023-08-10: "Workflow failed".
  - [#96](https://github.com/villesau/ai-codereviewer/issues/96), 2024-10-21: is the Gemini API supported?
  - [#98](https://github.com/villesau/ai-codereviewer/issues/98), 2024-11-04: proposal to batch requests per file.

#### ChatGPT-CodeReview (anc95/ChatGPT-CodeReview)
- As of 2026-11-23: 4,482 stars, 470 forks, ISC license, created 2023-02-11, about 61 open issues+PRs. Last commit 2026-08-10 (a fix to keep reviews aligned with rebased diffs). Releases: v1.0.22 (2025-08-04), v1.0.23 (2026-02-07), v1.0.24 (2026-07-14), i.e., a slow trickle — [GitHub](https://github.com/anc95/ChatGPT-CodeReview), [Releases](https://github.com/anc95/ChatGPT-CodeReview/releases)
- Approach: a GitHub App ("cr-gpt") or GitHub Action that reviews changed files on PR open and re-reviews on push. Supports OpenAI-compatible endpoints, Azure deployments and GitHub Models, with a configurable output language. The README says the hosted app is for testing only, rate-limited and may be unstable, and recommends self-deploying — [README](https://github.com/anc95/ChatGPT-CodeReview/blob/main/README.md)
- Complaints, mostly old and unanswered:
  - [#115](https://github.com/anc95/ChatGPT-CodeReview/issues/115), 2023-07-09, open, and [#30](https://github.com/anc95/ChatGPT-CodeReview/issues/30), 2023-02-23, open: GitLab integration requests.
  - [#67](https://github.com/anc95/ChatGPT-CodeReview/issues/67), 2023-04-09, open: API-key configuration errors.
  - [#110](https://github.com/anc95/ChatGPT-CodeReview/issues/110), 2023-06-15, open: "no target label attached".
  - [#42](https://github.com/anc95/ChatGPT-CodeReview/issues/42), 2023-03-17, open: request to skip removed and renamed files.

#### coderabbitai/ai-pr-reviewer (archived OSS predecessor of CodeRabbit)
- Status:
  - On 2026-11-23, github.com/coderabbitai/ai-pr-reviewer and its former name fluxninja/openai-pr-reviewer both return HTTP 404 (direct request), so the repo is deleted or private.
  - ecosyste.ms records list it as archived, previously named coderabbitai/openai-pr-reviewer and fluxninja/openai-pr-reviewer, with last push 2024-02-28; search snippets of GitHub mirrors give archive date 2024-03-06 — [ecosyste.ms record](https://awesome.ecosyste.ms/projects/github.com%2Fcoderabbitai%2Fai-pr-reviewer)
  - Conflict: the happyassassin blog says it was archived in November 2023 — [happyassassin.net](https://www.happyassassin.net/posts/2025/12/16/a-half-assed-assessment-of-open-source-ai-code-review-tools/)
- Historical approach: a TypeScript GitHub Action ("summarizer and reviewer with chat"), GitHub- and OpenAI-only. Per the same blog: barely any tests, no standalone deployment documented, and the Action no longer maintained, so the author rejected it — [happyassassin.net](https://www.happyassassin.net/posts/2025/12/16/a-half-assed-assessment-of-open-source-ai-code-review-tools/)

#### sunmh207/AI-Codereview-Gitlab (plus mimo-x/Code-Review-GPT-Gitlab)
- As of 2026-11-23: 1,878 stars, 412 forks, Apache-2.0, created 2024-11-14, last commit 2026-10-08, latest release 1.5.1 (2026-06-29) — [GitHub](https://github.com/sunmh207/AI-Codereview-Gitlab)
- Approach and features:
  - a webhook service (Python + SQLite) triggered by GitLab MR or push events that writes review notes back;
  - also supports GitHub and Gitea;
  - models: DeepSeek, ZhipuAI, OpenAI, Anthropic, Qwen, Ollama;
  - pushes results to DingTalk, WeCom and Feishu;
  - daily commit reports and a dashboard;
  - selectable "review styles" (professional, sarcastic, gentlemanly, humorous).
  - An optional Agentic Review mode gives the LLM `read_file` and a sandboxed read-only shell (ls/cat/grep/git log) with a 30-second timeout, and falls back to diff-only on any failure.
  - Source: [README](https://github.com/sunmh207/AI-Codereview-Gitlab/blob/main/README.md); deep-review feature merged for v1.5.0 (2026-06-25) — [Releases](https://github.com/sunmh207/AI-Codereview-Gitlab/releases)
- Open-core split: a paid "Pro" edition (Vue + Java + MySQL) adds:
  - per-project prompts, project templates and custom review rules;
  - deeper whole-project and history analysis;
  - HTML reports, member analytics and @-mentions in IM below a score threshold;
  - RBAC and a configuration UI; Gitee support.
  - Source: [doc/pro.md](https://github.com/sunmh207/AI-Codereview-Gitlab/blob/main/doc/pro.md)
- Complaints:
  - [#10](https://github.com/sunmh207/AI-Codereview-Gitlab/issues/10), 2025-02-08: can the whole project be used as context? (the diff-only limitation)
  - [#85](https://github.com/sunmh207/AI-Codereview-Gitlab/issues/85), 2025-04-09, open: push events stopped being reviewed after updating to 1.3.6.
  - [#33](https://github.com/sunmh207/AI-Codereview-Gitlab/issues/33), 2025-03-10: empty review log.
  - [#91](https://github.com/sunmh207/AI-Codereview-Gitlab/issues/91) and [#129](https://github.com/sunmh207/AI-Codereview-Gitlab/issues/129), 2025: per-project prompts, which are now a Pro feature.
- Related: mimo-x/Code-Review-GPT-Gitlab (817 stars, MIT, last commit 2026-11-16, no tagged releases) is a GitLab MR reviewer for DeepSeek and other models — [GitHub](https://github.com/mimo-x/Code-Review-GPT-Gitlab)

#### Nikita-Filonov/ai-review
- As of 2026-11-23: 611 stars, Apache-2.0. Latest release v1.5.0 (2026-11-21), after v1.0.0 (2026-09-20); very active — [GitHub](https://github.com/Nikita-Filonov/ai-review), [Releases](https://github.com/Nikita-Filonov/ai-review/releases)
- Approach:
  - a CI tool with inline, context (cross-file), summary and reply modes;
  - an optional "agent mode", an iterative ReAct loop that runs `ls/cat/rg/git` to explore the repo before reviewing;
  - customizable prompts; YAML/JSON/ENV config; runs fully client-side.
  - Platforms: GitHub, GitLab, Bitbucket Cloud, Bitbucket Server, Azure DevOps, Gitea.
  - Models: OpenAI, Claude, Gemini, Ollama, Bedrock, OpenRouter, Azure OpenAI.
  - Funded through Boosty donations.
  - Source: [README](https://github.com/Nikita-Filonov/ai-review/blob/main/README.md)
- Complaints:
  - [#59](https://github.com/Nikita-Filonov/ai-review/issues/59), 2026-02-03: recursive reply loop with the inline-reply tag.
  - [#29](https://github.com/Nikita-Filonov/ai-review/issues/29), 2025-11-06: a false-positive result when it failed to fetch data from GitLab.
  - [#40](https://github.com/Nikita-Filonov/ai-review/issues/40), 2025-12-03, open: Bedrock integration problems.
  - [#12](https://github.com/Nikita-Filonov/ai-review/issues/12), 2025-10-08: GitLab CI does not work with CI_JOB_TOKEN.
  - [#53](https://github.com/Nikita-Filonov/ai-review/issues/53), 2026-01-08: Gitea inline comments missing (since added).

#### Gerrit plugins
- The upstream Gerrit plugin `plugins/ai-code-review` is based on Amarula's ChatGPT plugin, generalized to other providers. Supported `aiType` values: ChatGPT (default), Ollama, AzureOpenAI and Generic (any endpoint and auth header).
  - It comments on new patch sets and can optionally vote; users can follow up by @-mentioning it or with `/review`.
  - Java/Maven.
  - Recent commits: 2026-04-01 ("Bump version to 3.13.0"), 2025-09-12 and 2025-07-22, so low but ongoing maintenance.
  - Source: [gerrit.googlesource.com plugin](https://gerrit.googlesource.com/plugins/ai-code-review/), [commit log](https://gerrit.googlesource.com/plugins/ai-code-review/+log/refs/heads/master)
- Amarula's original repo, amarula/chatgpt-code-review-gerrit-plugin, now redirects to amarula/reviewai-gerrit-plugin: 65 stars, last commit 2026-11-18, active. `amarula/gerrit-ai-code-review` returns 404 — [GitHub](https://github.com/amarula/reviewai-gerrit-plugin)
- Origin context: a Gerrit Summit 2024 hackathon proposed generalizing the plugin so on-prem or private models could be used — [Gerrit summit notes](https://gerrit.googlesource.com/summit/2024/+show/master/lightning-talks/hackathon-ai-code-review-plugin.md)
- PR-Agent also lists Gerrit as a reduced-support provider — [PR-Agent supported platforms](https://docs.pr-agent.ai/overview/supported_platforms/)

#### Bito "AI Code Review Agent" (gitbito/CodeReviewAgent)
- As of 2026-11-23: 69 stars, MIT, last commit 2025-11-13, no releases. Stale as a public repo — [GitHub](https://github.com/gitbito/CodeReviewAgent)
- What is open: scripts and Docker wrapper for running Bito's agent self-hosted (CLI, webhooks, GitHub Actions) on GitHub, GitLab and Bitbucket — [README](https://github.com/gitbito/CodeReviewAgent/blob/main/README.md)
- What is not: the self-hosted prerequisites require a **Bito Access Key** (a Bito account) alongside a GitHub classic PAT or GitLab token. It is an OSS wrapper around a proprietary service. OWASP Dependency-Check is built in, and a Snyk token is optional — [Bito prerequisites](https://docs.bito.ai/ai-code-reviews-in-git/install-run-as-a-self-hosted-service/prerequisites)
- A separate repo, gitbito/bitoai (298 stars, last push 2025-08-22), is Bito's general product repo — [GitHub](https://github.com/gitbito/bitoai)

#### LLM add-ons for reviewdog / Danger
- reviewdog (9.8k stars) is a generic linter-to-PR-comment runner with no official LLM integration. The common pattern is a DIY script that sends the diff to an LLM (e.g., local Ollama) and emits reviewdog-format diagnostics — [reviewdog](https://github.com/reviewdog/reviewdog), [DEV tutorial](https://dev.to/jovan_chan_9500711396d4e6/ai-code-review-setup-with-reviewdog-and-local-llm-16cb)
- Danger (5.7k stars): I found no maintained, widely used LLM plugin — [danger/danger](https://github.com/danger/danger)

### Inferences
- The long tail splits by generation:
  - **2023 "GPT-on-diff" Actions** (ai-codereviewer, ChatGPT-CodeReview, ai-pr-reviewer, codedog) are stale, archived or deleted.
  - **2025–26 survivors** added optional agent modes (repo exploration via shell or file tools), multi-platform support and reply threads.
  - Even so, most keep diff-only as the default, because of cost and latency and because agent modes can fail. sunmh207, for example, falls back to diff-only.
- Open-core monetization is common even among small tools: sunmh207 has a paid Pro, Bito needs a proprietary key, and Kodus has enterprise code. Fully free, single-maintainer projects (Gito, ai-review, Shippie) rely on donations or sponsorship and have small contributor bases.
- The high fork-to-star ratio of ai-codereviewer (848/1,049) suggests teams treat these simple bots as templates to copy and modify rather than as maintained dependencies.

### Gaps
- I could not identify notable maintained forks of coderabbitai/ai-pr-reviewer. The canonical repo now returns 404, and the GitHub API rate limit blocked fork listing.
- The license of vercel-labs/openreview and Agent-Field/pr-af could not be detected from the repo pages (see Q4).
- For Shippie I found no independent user reports from 2025–26.

## Q4. Other dedicated OSS review tools with >1k stars or notable 2025–2026 traction

### Takeaway
The biggest 2026 entrant is Alibaba's OpenCodeReview: 55k stars, Apache-2.0, very active. It is a CLI and agent-skill reviewer that combines a deterministic pipeline with a tool-using agent, and it has CI integrations for GitHub, GitLab, GitFlic and Gerrit. Smaller 2026 entrants share a pattern: agentic review in a sandbox (Vercel OpenReview, now dormant), multi-agent verification (PR-AF), or a code index plus learning loop (Mira). A new sub-genre reviews the coding agent's changes before push (openqodex). Most benchmark claims in this space are vendor-run.

### Cited Findings
- **alibaba/open-code-review (OpenCodeReview, `ocr`)**
  - Stats as of 2026-11-23: 55,354 stars, Apache-2.0, release v1.14.1 on 2026-11-22, near-daily releases — [GitHub](https://github.com/alibaba/open-code-review), [Releases](https://github.com/alibaba/open-code-review/releases)
  - Origin (vendor claim): Alibaba's internal official AI review assistant for about two years, used by tens of thousands of developers.
  - Design: a hybrid of deterministic engineering and an agent.
    - Deterministic parts: file selection, bundling related files into sub-agents with isolated context, and template-based rule matching.
    - Separate comment-positioning and "reflection" modules check location and content accuracy.
    - The agent can read whole files and search the codebase.
  - Modes: native (OCR calls the model) and delegation (the host coding agent, e.g., Claude Code or Codex, does the review following OCR's pipeline).
  - CI/CD docs cover GitHub Actions, GitLab CI, GitFlic CI and Gerrit.
  - Source: [README](https://github.com/alibaba/open-code-review/blob/main/README.md)
  - Vendor-run benchmark: 50 repos, 200 PRs, 1,505 annotated issues. Alibaba claims higher precision and F1 than Claude Code on the same model at about 1/9 of the tokens, and openly states recall is lower — [README](https://github.com/alibaba/open-code-review/blob/main/README.md)
  - Its README also names general agents' review failure modes: skipped files on big changes, "position drift" (wrong lines) and unstable quality — [README](https://github.com/alibaba/open-code-review/blob/main/README.md)
  - Press coverage started by June–July 2026, e.g., [Silenceper, 2026-07-31](https://silenceper.com/en/article/2026-07-31-opencodereview-ai-code-review/) and [GIGAZINE](https://www.gigazine.net/gsc_news/en/20260607-open-code-review)
- **vercel-labs/openreview**
  - 1,714 stars. Beta: an internal Vercel experiment.
  - Design: mention @openreview on a GitHub PR; it runs Claude Sonnet 4.6 via the AI SDK in a Vercel Sandbox with full repo access. It can run linters, formatters and tests, post suggestion blocks, and commit fixes. Uses Vercel Workflow; extensible "skills".
  - Activity: the last commit was 2026-03-06, and all recent commits fall in 2026-03-05/06, so it looks dormant. Requires Vercel infrastructure.
  - Source: [GitHub](https://github.com/vercel-labs/openreview), [HN 2026-03-17](https://news.ycombinator.com/item?id=47413785)
- **openqodex/openqodex**
  - 1,198 stars, Apache-2.0, active (last commit 2026-11-22).
  - Design: reviews the coding agent's change before push, inside Claude Code, Codex, Cursor, Cline and Goose.
    - Fresh reviewer processes (on the user's own Claude Code or Codex login) check the change.
    - A script verifies every quoted evidence line against the code, and verifiers confirm or refute each candidate finding.
    - Scanners (gitleaks, semgrep) and an osv.dev lockfile check run alongside.
    - A local code graph (TS/JS/Python/Go/Ruby/Java) supplies callers, callees and importers; it is exposed via MCP.
  - A hosted PR-review product, "Qodex", is linked. It appears unrelated to Qodo; not verified.
  - Source: [GitHub](https://github.com/openqodex/openqodex)
- **Agent-Field/pr-af**
  - 668 stars, active (last commit 2026-11-13); no license detected on the repo page.
  - Design: a multi-agent review plan with focused reviewer agents, findings grounded in code evidence, and a challenge pass.
  - Claims to be the #1 open-source reviewer on Martian Code-Review-Bench (golden recall 0.706 with GLM-5.2 across 42 tools, 38 PRs). This is a self-reported benchmark claim.
  - Source: [GitHub](https://github.com/Agent-Field/pr-af)
- **miracodeai/mira**
  - 419 stars, Apache-2.0, active (last commit 2026-11-16).
  - Claims every feature is self-hostable with "no paid tier".
  - Features:
    - a full-repo code index;
    - a learning loop that turns rejected comments and human review patterns into rules;
    - noise controls: confidence thresholds, dedup, a self-critique pass, per-PR caps;
    - cross-PR conflict detection; OSV CVE scanning; a dashboard.
  - Platforms: GitHub, GitLab, Forgejo/Codeberg, Bitbucket Cloud.
  - Claims best precision on Martian Code Review Bench (self-reported).
  - Source: [GitHub](https://github.com/miracodeai/mira)
- Other repos with >1k stars, adjacent rather than PR bots:
  - HexmosTech/git-lrc: 1,494 stars, "micro AI code reviews" on git commit, license NOASSERTION — [GitHub](https://github.com/HexmosTech/git-lrc)
  - appleboy/CodeGPT: 1,502 stars, MIT, Go CLI for commit messages and brief code review, v1.8.0 on 2026-09-28 — [GitHub](https://github.com/appleboy/CodeGPT)
  - tirth8205/code-review-graph: 32,904 stars, MIT, a local code-intelligence graph exposed over MCP/CLI to give AI tools review context; a context provider, not a bot — [GitHub](https://github.com/tirth8205/code-review-graph)
- Smaller active GitHub Actions:
  - hustcer/deepseek-review: 397 stars, MIT, Nushell-based, v1.22 on 2026-11-10 — [GitHub](https://github.com/hustcer/deepseek-review)
  - cirolini/genai-code-review: 372 stars, MIT, last commit 2026-09-21 — [GitHub](https://github.com/cirolini/genai-code-review)
  - presubmit/ai-reviewer: 187 stars, MIT, last commit 2026-09-14; PR summaries, title generation, Q&A — [GitHub](https://github.com/presubmit/ai-reviewer)
- Stale or archived:
  - codedog-ai/codedog: 190 stars, archived, last commit 2025-04-25 — [GitHub](https://github.com/codedog-ai/codedog)
  - sturdy-dev/codereview.gpt: 608 stars, browser-extension reviewer, last push 2024-08-12 — [GitHub](https://github.com/sturdy-dev/codereview.gpt)
- Topic-search context: `topic:ai-code-review` returned 1,131 repos on 2026-11-23. Many of the top results are "review skills" for coding agents (Claude Code/Codex) rather than PR bots, which reflects a 2026 shift toward in-agent review — [GitHub topic](https://github.com/topics/ai-code-review)
- An independent blog (2025-12-16) preferred Red Hat's "ai-code-review" (Juanje Ojeda; Gemini/Anthropic/Ollama; Forgejo support in progress) over Kodus and ai-pr-reviewer, with pr-agent as co-favourite — [happyassassin.net](https://www.happyassassin.net/posts/2025/12/16/a-half-assed-assessment-of-open-source-ai-code-review-tools/)

### Inferences
- OCR's star count (55k in a few months) is an outlier driven by Alibaba's brand and agent-skill distribution. It is, though, the clearest example of the "deterministic scaffolding + agent + verification" design that other 2026 entrants (openqodex, PR-AF, Mira) also use, in contrast to PR-Agent's single-prompt design.
- Benchmark claims from Alibaba, PR-AF and Mira are vendor-run or self-reported on public benchmarks (Martian Code Review Bench). They should be labelled as claims; empirical evaluation is covered by another researcher.

### Gaps
- Licenses of vercel-labs/openreview and Agent-Field/pr-af were not confirmed.
- The exact date OCR was open-sourced was not confirmed: press URLs range from June to September 2026, and the repo creation date wasn't retrieved because of API rate limits.
- Independent user reports on OCR, Mira, PR-AF and openqodex were not found beyond the vendors' own material.

## Q5. Cross-cutting patterns: abandonment, architectural limits, what users actually like

### Takeaway
The category has split in two:
- **Simple diff-in, comments-out bots (2023 vintage).** Mostly abandoned. They share the same failure modes: noise, wrong line anchors, JSON or parse failures, duplicates on re-push, and no cross-file context.
- **2026-generation tools.** They add repo exploration (tools, sandboxes, code graphs) and, increasingly, deterministic verification steps.

The tools users and maintainers rate well (PR-Agent, Kodus to a degree, OCR) are distinguished by:
- maintenance velocity;
- broad platform and model support with simple self-hosting;
- explicit noise controls.

Even agentic OSS reviewers still trail general coding agents on recall, per Kodus's own data.

### Cited Findings
- **Effectively abandoned, deleted or dormant (as of 2026-11-23):**
  - villesau/ai-codereviewer: last commit 2023-12-19 — [GitHub](https://github.com/villesau/ai-codereviewer)
  - coderabbitai/ai-pr-reviewer: archived in 2024, now 404 — [ecosyste.ms](https://awesome.ecosyste.ms/projects/github.com%2Fcoderabbitai%2Fai-pr-reviewer)
  - codedog: archived — [GitHub](https://github.com/codedog-ai/codedog)
  - sturdy-dev/codereview.gpt: last push 2024-08 — [GitHub](https://github.com/sturdy-dev/codereview.gpt)
  - gitbito/CodeReviewAgent: last commit 2025-11 — [GitHub](https://github.com/gitbito/CodeReviewAgent)
  - vercel-labs/openreview: no commits since 2026-03-06 — [GitHub](https://github.com/vercel-labs/openreview)
  - Slow trickle: anc95/ChatGPT-CodeReview (2–3 releases/yr) — [Releases](https://github.com/anc95/ChatGPT-CodeReview/releases); Shippie (one release cycle in 2026) — [Releases](https://github.com/mattzcarey/shippie/releases)
- **Diff-only context and no repo exploration is the default limit:**
  - PR-Agent works from the diff plus heuristics (dynamic context, AGENTS.md, tickets), and its code-graph request is open — [Dynamic context](https://docs.pr-agent.ai/core-abilities/dynamic_context/), [#2499](https://github.com/The-PR-Agent/pr-agent/issues/2499)
  - ai-codereviewer sends diff chunks — [README](https://github.com/villesau/ai-codereviewer/blob/main/README.md)
  - An AI-Codereview-Gitlab user asked for whole-project context — [#10](https://github.com/sunmh207/AI-Codereview-Gitlab/issues/10)
  - Kodus found most bugs Kody missed needed context outside the changed file — [#2411](https://github.com/kodustech/kodus-ai/issues/2411)
- **2026 responses to that limit:**
  - Agent loops with shell or file tools: Shippie, ai-review agent mode, sunmh207 agentic mode, Kodus sandbox tools.
  - Sandboxes that run linters and tests: OpenReview.
  - Code graphs or indexes: Kodus kodus-graph, openqodex graph, Mira index, code-review-graph.
  - Sources: [Shippie](https://github.com/mattzcarey/shippie), [ai-review](https://github.com/Nikita-Filonov/ai-review), [sunmh207](https://github.com/sunmh207/AI-Codereview-Gitlab), [Kodus docs](https://docs.kodus.io/how_to_deploy/en/deploy_kodus/sandbox), [OpenReview](https://github.com/vercel-labs/openreview), [openqodex](https://github.com/openqodex/openqodex), [Mira](https://github.com/miracodeai/mira)
- **Missing verification steps are the second limit; newer tools add them:**
  - OCR: comment-positioning and reflection modules — [OCR](https://github.com/alibaba/open-code-review)
  - openqodex: evidence-line checking plus verifiers — [openqodex](https://github.com/openqodex/openqodex)
  - PR-AF: a challenge pass — [PR-AF](https://github.com/Agent-Field/pr-af)
  - Mira: a self-critique pass and confidence thresholds — [Mira](https://github.com/miracodeai/mira)
  - Kodus: "deterministic evidence" work item (closed 2026-09-01) — [#1825](https://github.com/kodustech/kodus-ai/issues/1825)
  - PR-Agent: a merge recommendation gated by deterministic checks — [/review docs](https://docs.pr-agent.ai/commands/review/)
- **Shared failure modes across tools:**
  - Duplicates on re-push: [PR-Agent #2037](https://github.com/The-PR-Agent/pr-agent/issues/2037), [Gito #135](https://github.com/Nayjest/Gito/issues/135)
  - Anchoring and position errors: [ai-codereviewer #34](https://github.com/villesau/ai-codereviewer/issues/34), [PR-Agent #3739](https://github.com/The-PR-Agent/pr-agent/issues/3739); OCR's README calls general agents' version of this "position drift" — [OCR](https://github.com/alibaba/open-code-review)
  - Unparseable LLM output: [Gito #244](https://github.com/Nayjest/Gito/issues/244), [ai-codereviewer #56](https://github.com/villesau/ai-codereviewer/issues/56), [PR-Agent #461](https://github.com/The-PR-Agent/pr-agent/issues/461)
  - Large-diff truncation: [PR-Agent #2978](https://github.com/The-PR-Agent/pr-agent/issues/2978), [Kodus #68](https://github.com/kodustech/kodus-ai/issues/68)
  - Local-model fragility: [PR-Agent #1623](https://github.com/The-PR-Agent/pr-agent/issues/1623) and the [docs warning](https://docs.pr-agent.ai/usage-guide/changing_a_model/)
- **Noise is the dominant UX problem:**
  - Kodus measured 1.8% thumbs-down on LLM suggestions versus 44.6% on unconfirmed regex-rule findings — [#1831](https://github.com/kodustech/kodus-ai/issues/1831)
  - Historical (2024-12): Greptile's widely discussed post (257 HN points) on stopping nitpicks. After prompt tweaks failed, they filtered using similarity to past rejected comments. Vendor blog — [HN](https://news.ycombinator.com/item?id=42451968), [Greptile blog](https://www.greptile.com/blog/make-llms-shut-up)
- **Learning from feedback is rarer and weaker than marketed:**
  - Kodus switched off its reaction-based loop (Sept 2026) — [#1863](https://github.com/kodustech/kodus-ai/issues/1863)
  - PR-Agent has no learning loop — [#2075](https://github.com/The-PR-Agent/pr-agent/issues/2075)
  - Mira claims rules synthesized from rejected comments (unverified) — [Mira](https://github.com/miracodeai/mira)
- **What distinguishes tools people choose:**
  - The independent reviewer picked pr-agent for maturity, breadth of forge and model support, and simple documented deployment, and rejected Kodus partly for deployment complexity and review style — [happyassassin.net](https://www.happyassassin.net/posts/2025/12/16/a-half-assed-assessment-of-open-source-ai-code-review-tools/)
  - PR-Agent's 16.6k stars versus at most a few thousand for any other dedicated PR bot (excluding OCR) — [GitHub](https://github.com/The-PR-Agent/pr-agent)
  - Users value AI PR descriptions and summaries more than review suggestions (historical, 2024) — [HN](https://news.ycombinator.com/item?id=41500840)
- **Commercial pull:** the strongest projects' original backers moved value into proprietary platforms:
  - Qodo → Qodo 2.0, while PR-Agent was donated — [Qodo blog](https://www.qodo.ai/blog/qodo-is-handing-pr-agent-over-to-the-community/)
  - CodeRabbit's OSS predecessor was archived and is now gone — [ecosyste.ms](https://awesome.ecosyste.ms/projects/github.com%2Fcoderabbitai%2Fai-pr-reviewer)
  - Kodus and sunmh207 run open-core tiers — [Kodus license](https://github.com/kodustech/kodus-ai/blob/main/license.md), [sunmh207 Pro](https://github.com/sunmh207/AI-Codereview-Gitlab/blob/main/doc/pro.md)

### Inferences
- The best predictor of whether a dedicated OSS review bot is still usable in late 2026 is not its star count but whether it has an active maintainer group tracking fast-changing model APIs. Model-specific breakages (e.g., PR-Agent #2576, Bedrock parsing #1901) recur, and stale bots break silently.
- The architectural frontier moved from "better prompt over the diff" to "context acquisition + verification":
  - exploring the repo or querying a graph to find cross-file impact;
  - then checking evidence and positions deterministically before posting.
- Tools stuck at single-shot diff review (PR-Agent at its core, the 2023 Actions) can be tuned for noise but are structurally limited on recall for bugs that span files.
- A second 2026 trend: review is moving into the coding agent itself (agent skills, pre-push reviewers like openqodex, OCR's delegation mode). That partly makes PR-time bots less central, and blurs the line with general-purpose coding agents (covered by other researchers).

### Gaps
- There is no independent, cross-tool benchmark of OSS PR bots run on the same PRs in this research; the empirical-study researcher covers that.
- Systematic user-satisfaction data (surveys, Reddit threads) for specific OSS bots in 2025–26 was not found. Most evidence is from GitHub issues and one independent blog.
- Notable maintained forks of the deleted coderabbitai/ai-pr-reviewer could not be enumerated.
