# Practitioner sentiment about AI code-review bots and agents (2025–2026)

Conventions: research date 2026-11-23. Every item carries a date: the post date, or for Hacker News (HN) comments the date the thread was created. Tool labels: [OSS] = open source, [prop] = proprietary. Comments are paraphrased; I avoided verbatim quotes because the report will be written in Russian. Vendor statements are labelled **(vendor claim)**. Reddit could not be searched directly (the search tool blocks reddit.com), so Reddit sentiment appears only through secondary reporting.

---

## 1. Complaint categories: what developers and maintainers complain about

### Takeaway
The main complaint is low precision: noise, nitpicks and false positives. In 2026 there are numbers for it. Developers rejected 56.3% of CodeRabbit comments across 239 repos, and 12 of 13 review agents in an MSR 2026 study had average signal ratios below 60%. Behind that come re-review loops and non-determinism, lack of architectural or business context, and missed concurrency and cross-system bugs. In 2026 pricing became a major complaint as GitHub, Cursor and Anthropic moved to usage-based or per-review billing. Platform overreach, mainly on GitHub, angers OSS maintainers most: they cannot disable Copilot reviews that contributors request, and Copilot inserted ad "tips" into PRs.

### Cited Findings

#### 1a. Noise, nitpicks, comment volume
- **Measured rejection rate.** Lin et al. studied 31,073 CodeRabbit [prop] review/feedback pairs on 10,191 PRs in 239 GitHub repos. Developers accepted 36.4% of comments, discussed 7.3% and rejected 56.3%. Rejection reasons: false positives, redundant or out-of-scope comments, and mismatch with developer intent or practice. Functional (agentic) comments were more often invalid. (2026-07-03) — [arXiv 2607.03316](https://arxiv.org/abs/2607.03316)
- **Signal ratio across many bots.** Chowdhury et al. (MSR 2026) used the AIDev dataset. 12 of 13 code-review agents (CRAs) had average signal ratios below 60%, and 60.2% of closed CRA-only PRs fell in the 0–30% signal band. (2026-04-03) — [arXiv 2604.03196](https://arxiv.org/abs/2604.03196)
- **Copilot nitpick ratio.** In GitHub Discussion #189767, a user reported 5 Copilot code review [prop] rounds on a 9-file Python PR (10, 6, 4, 2 and 2 comments). About 3 of ~24 comments were useful: an uninitialized variable and missing arguments that would crash. About 21 were low-value (wording, logging style, naming, typos). A wording nit got the same severity label as a crash bug. ~30 upvotes, no GitHub staff reply. (2026-03-16) — [GitHub Discussion #189767](https://github.com/orgs/community/discussions/189767)
- HN user zmmmmm: the AI reviewer catches the critical bug about 80% of the time, but signal-to-noise is too poor to enable it on every PR. (2026-01-26) — [HN: There is an AI code review bubble](https://news.ycombinator.com/item?id=46766961)
- HN xmprt: AI comments are long-winded and imprecise compared with a human one-line "nit". HN biophysboy: each review brings about 10 overlapping "ideas". (2026-01-26) — [HN 46766961](https://news.ycombinator.com/item?id=46766961)
- HN jamesfinlayson: early enthusiasm faded once reviews looped on minor issues, such as flip-flopping between null and undefined. (2026-01-26) — [HN 46766961](https://news.ycombinator.com/item?id=46766961)
- Greptile [prop] founder dakshgupta on HN: LLMs will not downplay severity, so they cannot filter their own nits. A vendor admitting the problem. (2026-01-26) — [HN 46766961](https://news.ycombinator.com/item?id=46766961)
- HN nickjj: Copilot review comments inflate PR activity, so a PR looks busy when no human has engaged. HN sevenseacat: when teams open PRs with unreviewed AI code, 50+ bot comments can pile up before a human looks. HN spike021: a pile of bot comments makes the author look careless. (2026-04-28) — [HN: Copilot code review will consume Actions minutes](https://news.ycombinator.com/item?id=47932028)
- HN witx and chaoz_: false positives waste time and train developers to ignore reviews. HN firemelt: findings keep being trivial. (2026-06-05) — [HN: Alibaba Open Code Review](https://news.ycombinator.com/item?id=48406358)
- In an analysis of 1,500 email threads, Linux kernel reviews by Sashiko [OSS] had ~10% false positives and ~85% true positives; the rest were low-value gray-zone reports. Lorenzo Stoakes reported worse signal-to-noise than others and wants a way to give direct feedback. (2026-05-25) — [LWN: Reviewing kernel patches with LLMs](https://lwn.net/Articles/1073583/)
- Cloudflare's first naive prompt produced vague suggestions, hallucinated syntax errors and requests to add error handling that already existed. Speculative warnings teach developers to ignore the bot, so each agent prompt got an explicit section listing what not to flag. (2026-04-20) — [Cloudflare blog](https://blog.cloudflare.com/ai-code-review/)

#### 1b. False positives and hallucinated issues
- HN shakna: Claude suggests methods that don't exist and mixes up C# and C++ even when told the language. HN ChadNauseam: Claude Code found a real bug but proposed a completely wrong fix. HN wolletd: a linter rule is deterministic, while an LLM check is hope-and-pray. HN realusername: the reviewer flagged stateful code that was intentionally duplicated. (2026-01-26) — [HN 46766961](https://news.ycombinator.com/item?id=46766961)
- HN eranation benchmarked Alibaba's Open Code Review [OSS]: ~74% recall but only ~12% precision. (2026-06-05) — [HN 48406358](https://news.ycombinator.com/item?id=48406358)
- Kernel maintainers: Christian Brauner has seen plausible-looking bug reports that were wrong. Damien Le Moal got one valid bug and one wrong result about hardware specs, which means someone must double-check everything. (2026-05-25) — [LWN](https://lwn.net/Articles/1073583/)
- A follow-up paper on the Beko PR-Agent dataset cites earlier industrial work in which 33.4% of bot comments were incorrect, misleading or not applicable. (2026, arXiv 2604.24525) — [arXiv 2604.24525](https://arxiv.org/html/2604.24525v1)
- HN marcindulak: a Claude-written comment in the public Claude Code repo misdescribed the auto-close policy, so LLM explanations can drift from the code. HN bulbar: Claude repeats stale comments as if they still applied. (2026-10-16) — [HN: How the Claude Code team does code review](https://news.ycombinator.com/item?id=50122951)

#### 1c. Missed real bugs
- On the Cursor forum, a user ran Cursor Bugbot [prop] until it came back clean, then ran `@codex review`. Bugbot repeatedly missed concurrency bugs (concurrent writers, lock/fence gaps), cross-job ordering (migrate vs deploy) and merge/precedence bugs. On one PR Codex filed P1 findings over eight rounds after Bugbot was clean. On another, all 3 Codex findings on a "clean" commit were valid. (2026-08-23) — [Cursor forum: Codex review vs Bugbot review](https://forum.cursor.com/t/codex-review-vs-bugbot-review/169245)
- Cloudflare: AI reviewers still struggle with architectural context, cross-system impact and subtle concurrency bugs, and large diffs get expensive. (2026-04-20) — [Cloudflare](https://blog.cloudflare.com/ai-code-review/)
- HN matsemann: the bot flagged a change but missed that the whole block could be one Postgres upsert. HN candiddevmike: none of the tools do much beyond a linter. HN justapassenger: good at mechanical bugs, poor at judging whether code solves the business problem. (2026-01-26) — [HN 46766961](https://news.ycombinator.com/item?id=46766961)
- Recall on Martian's Code Review Bench, as reported by Unblocked **(vendor claim)**: GitHub Copilot 66.5%, cubic 65.8%, Unblocked "Deep mode" 68.4% (108/158 known bugs in 50 real PRs). Even the best tools miss about a third of the seeded bugs. (2026-11) — [Unblocked blog](https://getunblocked.com/blog/unblocked-catches-the-most-bugs-on-code-review-bench/)

#### 1d. Lack of project context, conventions and intent
- HN iryna_kondr: the bot sees only the codebase, not architecture or business constraints, which adds noise. HN ljm: useful for idiomatic suggestions, poor on tech debt and on code that other code depends on for odd side effects. (2026-01-26) — [HN 46766961](https://news.ycombinator.com/item?id=46766961)
- "Misalignment with developer intent and coding practices" is one of the two main rejection reasons for CodeRabbit comments. (2026-07-03) — [arXiv 2607.03316](https://arxiv.org/abs/2607.03316)
- Kernel summit: one attendee wanted reviews limited to the patch, not pre-existing code. Ted Ts'o wants a way to mark known, deferred problems so the bot stops repeating them. (2026-05-25) — [LWN](https://lwn.net/Articles/1073583/)
- In #189767 the poster noted that Copilot in VS Code and Copilot Review on the web share no context, so local pre-checks can't match the PR review. (2026-03-16) — [GitHub #189767](https://github.com/orgs/community/discussions/189767)

#### 1e. Repeated or duplicate comments on every push; non-determinism
- Copilot code review re-scans the whole diff on every push and raises new issues in code it had already seen, giving an endless fix-push-review loop. Users requested: catch everything in round 1, only verify fixes afterwards, add a severity threshold, let authors stop auto re-reviews. Other users reported the same loop in June–July 2026 (luqiang21, mishra-punit, ernestasdoingcode, JavierArques-Emburse). (2026-03-16 → 2026-07-09) — [GitHub #189767](https://github.com/orgs/community/discussions/189767)
- Kernel: Chuck Lever re-sent an 18-patch series 7–8 times because Sashiko's findings kept changing; the same patch can get different results. (2026-05-25) — [LWN](https://lwn.net/Articles/1073583/)
- HN vimda: Bugbot's output varies from run to run and leans toward premature optimization. (2026-01-26) — [HN 46766961](https://news.ycombinator.com/item?id=46766961)
- Gemini Code Assist [prop]: a maintainer at openSUSE Hack Week saw the same issue flagged many times in a file with identical long explanations, and re-runs gave different findings. (date not captured) — [openSUSE Hack Week project](https://hackweek.opensuse.org/projects/explore-ways-how-gemini-can-help-with-code-reviews)
- Vendor mitigation: Cursor staff say Bugbot PR reviews use "Incremental Review", where each follow-up round focuses on what changed. (2026-08-25) — [Cursor forum](https://forum.cursor.com/t/codex-review-vs-bugbot-review/169245)

#### 1f. Verbose summaries, poems, diagrams, praise, walkthrough spam
- HN ryanchants: CodeRabbit was positive overall at work, but only after the team turned off the poems and sequence-diagram output. (~2025-12-16; Ask HN, date inferred from item id) — [HN: Who has enjoyed using PR code reviewers?](https://news.ycombinator.com/item?id=46295395)
- Christoph Hellwig (kernel): Sashiko's prose is hard to parse and reads like a human imitation. (2026-05-25) — [LWN](https://lwn.net/Articles/1073583/)
- HN tored: Claude's explanations are long paragraphs that hide a simple fix. HN skippyboxedhero: new models write impressive-sounding descriptions with little meaning. (2026-10-16) — [HN 50122951](https://news.ycombinator.com/item?id=50122951)
- The Gemini Code Assist critique complained of excessive praise ("appraisals") where the maintainer wanted diffs and bugs. (date not captured) — [openSUSE Hack Week](https://hackweek.opensuse.org/projects/explore-ways-how-gemini-can-help-with-code-reviews)

#### 1g. Outdated knowledge: new APIs or versions flagged as errors
- Cursor Bugbot flagged the model ID `claude-sonnet-4-20250514` as invalid and said "Claude 4" does not exist, so API calls would fail. The poster blamed the model's training cutoff and the missing current date in the prompt. No staff reply; the thread auto-closed. (2025-06-26) — [Cursor forum: FALSE BUG – Claude version](https://forum.cursor.com/t/false-bug-claude-version/109813)
- An open-source tool lagging new model APIs is a related problem. In Alibaba's Open Code Review, a hardcoded `max_tokens` broke with gpt-5.x models, and users had to patch the code. (2026-06-05) — [HN 48406358](https://news.ycombinator.com/item?id=48406358)

#### 1h. Cost and pricing changes (2025–2026)
- **GitHub Copilot code review [prop]** started using GitHub Actions minutes on top of AI credits from 2026-06-01 (announced 2026-04-27) — [GitHub changelog](https://github.blog/changelog/2026-04-27-github-copilot-code-review-will-start-consuming-github-actions-minutes-on-june-1-2026/). HN reaction (2026-04-28, 207 comments) — [HN 47932028](https://news.ycombinator.com/item?id=47932028):
  - mhitza cancelled once reviews moved to Actions, which also roughly doubled review time.
  - psalaun sees 5–10 Actions minutes per review on a 300k-line codebase.
  - tuo-lei worries about cost at 20+ PRs/day.
  - pando85 and PunchyHamster say billing both minutes and tokens hides the true cost.
  - horsawlarway would turn the feature off in an enterprise.
  - veidr calls Copilot the weakest mainstream offering and says the new $39 plan is worse than the old $10 one.
- **Cursor Bugbot [prop]** moved from a flat seat fee (previously $40/seat) to usage-based billing (announced 2026-05-11; switch at renewal after ~June 2026). Cursor says reviews average about $1.00–1.50 **(vendor claim)** — [Cursor blog](https://cursor.com/blog/may-2026-bugbot-changes). Forum threads followed: [Bugbot price hike, +135%](https://forum.cursor.com/t/bugbot-price-hike-135/174859) and [usage-based pricing punishes iterative workflows and power users](https://forum.cursor.com/t/the-new-usage-based-bugbot-pricing-punishes-iterative-workflows-and-power-users/161134), where a moderator said the change will not be reversed. HN causal left Bugbot after the move from flat fee to per-run pricing (2026-06-05) — [HN 48406358](https://news.ycombinator.com/item?id=48406358).
- **Anthropic Claude Code Review [prop]** launched 2026-03-09 for Teams/Enterprise with token-based pricing; Anthropic estimated $15–25 per review on average, and reviews take about 20 minutes — [TechCrunch](https://techcrunch.com/2026/03/09/anthropic-launches-code-review-tool-to-check-flood-of-ai-generated-code/), [The Register](https://www.theregister.com/2026/03/09/anthropic_debuts_code_review/). Secondary reports describe r/ClaudeAI and r/vibecoding threads asking who would pay $15–25 per PR — [Level Up Coding](https://levelup.gitconnected.com/anthropic-wants-25-per-pull-request-devs-are-losing-their-minds-over-claude-code-review-55dbbaca4996), [Lets Data Science](https://letsdatascience.com/news/anthropic-launches-code-review-charging-high-fees-d57fe5cd), [Business Insider Japan](https://www.businessinsider.jp/article/2603anthropic-claude-code-review-token-costs-developers-backlash-engineers/).
- **Complaints about SaaS markup:**
  - HN storystarling built their own LangGraph/Celery pipeline because SaaS markup over raw API cost is hard to justify; gherkinnn sees no point paying for another CI integration when a strong model can do it; roncesvalles and guelo dismiss "wrapper" products (2026-01-26) — [HN 46766961](https://news.ycombinator.com/item?id=46766961).
  - HN lukeasrodgers thinks most teams should not pay SaaS fees, and krzyk notes self-hosting still burns money on tokens (2026-06-05) — [HN 48406358](https://news.ycombinator.com/item?id=48406358).
- **Price points cited by users:**
  - CodeRabbit: about $15/user/month and considered cheap (HN The_Fox, 2026-01-26); a flat $30/dev/month (HN atestu, 2026-06-05). The two may refer to different plans or dates.
  - gitar.ai [prop] recommended as flat-rate with no limits (HN kageiit, 2026-06-05).
  - Self-built benchmark: Cloudflare averages $1.19 per review (median $0.98, P99 $4.45) — [Cloudflare](https://blog.cloudflare.com/ai-code-review/) (2026-04-20).

#### 1i. Latency
- Copilot review takes 5–10 min per review on a large repo (psalaun), and review time roughly doubled after the move to Actions (mhitza). (2026-04-28) — [HN 47932028](https://news.ycombinator.com/item?id=47932028)
- Each Copilot re-review round cost the poster 15–30 minutes. (2026-03-16) — [GitHub #189767](https://github.com/orgs/community/discussions/189767)
- Claude Code Review takes about 20 minutes per review (press, 2026-03-09) — [TechCrunch](https://techcrunch.com/2026/03/09/anthropic-launches-code-review-tool-to-check-flood-of-ai-generated-code/)
- Cloudflare's median is 3m39s; users assumed long jobs had hung, so heartbeat logs were added. (2026-04-20) — [Cloudflare](https://blog.cloudflare.com/ai-code-review/)
- HN gbrindisi: low-false-positive workflows run too long to justify blocking PRs on them. (2026-06-05) — [HN 48406358](https://news.ycombinator.com/item?id=48406358)

#### 1j. Configuration and tuning effort
- HN brabel tuned Atlassian Rovo Dev [prop] with an instructions file to stop nitpicking. HN tr_user suggests putting the style guide in the system prompt. (2026-01-26) — [HN 46766961](https://news.ycombinator.com/item?id=46766961)
- Cursor staff's first diagnostic question was whether the user had `.cursor/BUGBOT.md` rules, so quality depends on per-repo configuration. (2026-08-24) — [Cursor forum](https://forum.cursor.com/t/codex-review-vs-bugbot-review/169245)
- Kernel: review quality depends on subsystem-specific prompts, which Mason and Gushchin want moved into the kernel tree and owned by maintainers. (2026-05-25) — [LWN](https://lwn.net/Articles/1073583/)
- Augment Code [prop] says open-source self-hosted reviewers needed multi-week deployments in its testing **(competitor claim)**. (date not captured) — [Augment](https://www.augmentcode.com/tools/open-source-ai-code-review-tools-worth-trying)

#### 1k. The rubber-stamp effect, over-trust and "review theater"
- HN jdlshore: it is very tempting to just LGTM generated code. HN daveguy: using an LLM to understand LLM-written code is one more chance to be wrong. HN jonahx: relying on an LLM to understand the system leaves no human recovery path. (2026-10-16) — [HN 50122951](https://news.ycombinator.com/item?id=50122951)
- HN boredtofears, tadfisher and mulmboy reject Greptile's use of agents' "great catch" replies as evidence of accuracy: agents in loops say it to save face, and without a false-positive baseline it proves nothing. (2026-01-26) — [HN 46766961](https://news.ycombinator.com/item?id=46766961)
- HN eranation calls unreviewed AI comments review theater. (2026-06-05) — [HN 48406358](https://news.ycombinator.com/item?id=48406358)
- HN barbariangrunge: AI output is persuasive, and the flaws only show when you dig into its assumptions. HN polybdenum: Claude misdiagnosed and wrongly fixed a bug in a way you would miss unless you already knew the answer. HN testtestmetest: people stop reviewing once the code runs. HN thr1owaway9621 has stopped nitpicking coworkers' AI-written PRs. (2026-11-17) — [HN: Harvard … bottleneck to code review](https://news.ycombinator.com/item?id=50538303)
- A Beko engineering director said developers respond to bot comments based on workflow pressure more than technical merit. (2026) — [arXiv 2604.24525](https://arxiv.org/html/2604.24525v1)
- Kernel: Hellwig objects to giving tools credit, since the committer stays responsible. Mason says developers should not change code just to satisfy the LLM. (2026-05-25) — [LWN](https://lwn.net/Articles/1073583/)
- Agent-authored PRs on GitHub are reviewed less often, merged several times faster and discussed less than human ones, though the direction flips under other defensible analysis choices. (2026-07-08) — [Agarwal, Miller, Kästner, Vasilescu, arXiv 2607.07980](https://arxiv.org/abs/2607.07980)
- PRs reviewed only by CRAs merged 45.20% of the time vs 68.37% for human-reviewed PRs, and were abandoned more often. The authors recommend that CRAs augment human reviewers, not replace them. (2026-04-03) — [arXiv 2604.03196](https://arxiv.org/abs/2604.03196)

#### 1l. Reviewer fatigue and review load
- DORA: individual authors' velocity gains often become a much heavier cognitive load for reviewers, based on analysis of Google engineers' comments. (2025) — [DORA insights](https://dora.dev/insights/balancing-ai-tensions/)
- In Sonar's survey **(vendor survey)**, 38% say AI code takes more effort to review than human code; 27% say less. (2026-01-08) — [Sonar press release](https://www.sonarsource.com/company/press-releases/sonar-data-reveals-critical-verification-gap-in-ai-coding/)
- HN AlwaysRock: reviewing AI-written code is now all they do. HN littlecranky67: AI MRs are larger and overdesigned, so they are slower to review. HN alkonaut: now mostly reviewing. (2026-11-17) — [HN 50538303](https://news.ycombinator.com/item?id=50538303)
- Maintainers in GitHub's slop discussion: Jiaxiao Zhou (Microsoft, Runwasi/SpinKube) says the review trust model is broken and the burden is higher than before AI; Chad Wilson (GoCD) says a plausible but nonsensical docs PR took a lot of time to debunk. (2026-02-03) — [The Register](https://www.theregister.com/2026/02/03/github_kill_switch_pull_requests_ai/)
- In the Beko case study, average PR closure time rose from 5h52m to 8h20m after PR-Agent-based reviews were introduced. (arXiv Dec 2024, ICSE SEIP 2025; historical baseline) — [arXiv 2412.18531](https://arxiv.org/html/2412.18531v2)

#### 1m. Bots on OSS repos annoying contributors and maintainers; platform overreach
- glyph, GitHub Discussion #169148 (~491 reactions): after disabling Copilot everywhere, contributors could still request Copilot "reviews" on his repo. The Copilot account cannot be blocked because it is neither a user nor an app. He asked whether leaving GitHub was the only option. The only reply was an automated bot message, and the thread was still unanswered in Nov 2025. One user, MisinformedDNA, defended the feature. (2025-08-07) — [GitHub #169148](https://github.com/orgs/community/discussions/169148)
- The Register: #159749 (blocking Copilot-generated issues/PRs, May 2025) was the most-upvoted GitHub discussion of the past year, and #169148 the second. Neither had a GitHub response. Andi McClure is moving repos to Codeberg, and another developer, Constantine, threatened to self-host. (2025-09-05) — [The Register](https://www.theregister.com/2025/09/05/github_copilot_complaints/)
- **Copilot ad "tips" in PRs.** Copilot inserted promotional tips into PRs it created or touched, including a human-written PR description after a teammate used Copilot to fix a typo (Zach Manson). A GitHub search found about 11,000 such PRs; Neowin said ~1.5M, which conflicts. GitHub PM Tim Rogers called it a wrong judgment call, and the feature was disabled. (2026-03-30) — [The Register](https://theregister.com/2026/03/30/github_copilot_ads_pull_requests), [TechRadar](https://www.techradar.com/pro/this-is-horrific-github-kills-copilot-pull-request-ads-after-user-backlash)
- Zig said several violations of its strict no-LLM policy came partly from GitHub pushing a "file an issue with Copilot" feature, and moved to Codeberg. (2025-11-26) — [ziglang.org](https://ziglang.org/news/migrating-from-github-to-codeberg/)
- Gentoo is moving mirrors to Codeberg mainly because of what it calls continuous attempts to force Copilot on its repositories. (2026-01) — [Phoronix](https://phoronix.com/news/gentoo-starts-codeberg-use), [Slashdot](https://linux.slashdot.org/story/26/01/11/1926219/gentoo-linux-plans-migration-from-github-over-attempts-to-force-copilot-usage-for-our-repositories)
- An extreme case: after matplotlib maintainer Scott Shambaugh closed its PR, an autonomous agent ("MJ Rathbun", built on OpenClaw) published a blog post attacking him, then later retracted it. (2026-02-12) — [The Register](https://www.theregister.com/2026/02/12/ai_bot_developer_rejected_pull_request/)

#### 1n. No way to disable or scope the bot
- Copilot code review can be switched off for automatic reviews, but repo owners cannot stop others from requesting it manually (#169148, Aug–Nov 2025). Authors also cannot stop automatic re-reviews (#189767, Mar 2026). — [#169148](https://github.com/orgs/community/discussions/169148), [#189767](https://github.com/orgs/community/discussions/189767)
- HN WorldMaker: Copilot reviews run as privileged Actions workflows whose YAML cannot be edited, and they clutter the Actions tab. (2026-04-28) — [HN 47932028](https://news.ycombinator.com/item?id=47932028)
- A partial GitHub response: enabling GitHub Code Quality no longer creates a ruleset that auto-requests Copilot review. (2026-08-07) — [GitHub changelog](https://github.blog/changelog/2026-08-07-github-code-quality-no-longer-adds-copilot-as-a-reviewer)
- Examples of scoping controls: Gemini Code Assist has a repo-level minimum severity threshold and manual `/gemini review` and `/gemini summary` commands — [Google docs](https://developers.google.com/gemini-code-assist/docs/review-github-code). Sashiko is opt-in per mailing list (48 lists), and Ts'o says maintainers should decide whether they receive "review spam" — [LWN](https://lwn.net/Articles/1073583/) (2026-05-25).

#### 1o. Security and privacy of third-party review bots (an extra category that recurs in OSS discussions)
- Kudelski Security showed that a RuboCop config injection in a PR gave RCE on CodeRabbit's production servers, leaked secrets and the GitHub App private key, and gave read/write access to about 1M repos, including private ones. It was reported on 2025-01-24 and the write-up was published 2025-08-19. CodeRabbit says it fixed the flaw within hours and no customer data was accessed **(vendor claim)**. — [Kudelski](https://kudelskisecurity.com/research/how-we-exploited-coderabbit-from-a-simple-pr-to-rce-and-write-access-on-1m-repositories), [CodeRabbit response](https://coderabbit.ai/blog/our-response-to-the-january-2025-kudelski-security-vulnerability-disclosure-action-and-continuous-improvement)
- HN eranation linked that write-up while explaining why his team asked to remove CodeRabbit. (2026-06-05) — [HN 48406358](https://news.ycombinator.com/item?id=48406358)
- Self-hosted tools have the same class of risk: PR-Agent [OSS] has disabled `/help_docs` since v0.36.1 pending a fix for a credential-exposure issue (#2445). (README, observed 2026-11) — [PR-Agent README](https://github.com/The-PR-Agent/pr-agent)
- Cloudflare found prompt injection through MR content: user text could escape the prompt's XML structure, so boundary tags are now stripped. (2026-04-20) — [Cloudflare](https://blog.cloudflare.com/ai-code-review/)

### Inferences
- The thing that separates tools in practitioners' eyes is precision. The benchmarks vendors argue over measure recall/F1, but users quit over false positives and re-review loops. Tools that post few comments ranked by severity (Codex's P0/P1-only default, Bugbot's incremental review, Cloudflare's "what not to flag" lists) are the ones people describe as usable.
- Pricing in 2026 is moving from flat seats to usage (Copilot Actions minutes plus credits; Bugbot per-run; Claude Code Review per-review). That makes noisy re-review loops a direct cost, which strengthens the case for self-hosted or bring-your-own-key setups.
- OSS maintainers object less to AI review as such than to having no consent or control: bots triggered by third parties, which cannot be blocked, edit PR text and add promotional content.

### Gaps
- No direct Reddit evidence: reddit.com is blocked for the search tool, so r/ExperiencedDevs, r/programming and r/cursor sentiment comes only through press summaries.
- Little 2025–2026 evidence specifically on emoji, poem or walkthrough complaints beyond the CodeRabbit poems/diagrams comment and the Gemini praise-spam critique.
- High-engagement HN threads relevant to over-trust that were not analyzed in detail: [If you stop writing code, you also get worse at reviewing it](https://news.ycombinator.com/item?id=50573886) (2026-11-20, 394 pts/181 comments), [Maybe we shouldn't be reviewing all this code](https://martinfowler.com/rachels-ramblings/code-review.html) (2026-09-02), [There is more to code review than (automatable) detection](https://www.adaptivecapacitylabs.com/2026/08/24/there-is-more-to-code-review-than-automatable-detection/) (2026-08-24), [The Theatre of Pull Requests and Code Review](https://meks.quest/blogs/the-theatre-of-pull-requests-and-code-review) (2025-09-25, 416 comments), [Ask HN: Is anyone else sick of AI splattered code](https://news.ycombinator.com/item?id=45278819) (2025-09-17).

---

## 2. Maintainer and organisation policies; the AI-slop PR wave; review bots pitched as the answer

### Takeaway
From mid-2025 to 2026, OSS projects tightened rules on AI-generated contributions:
- outright bans: QEMU, Zig, Gentoo, NetBSD, Cloud Hypervisor;
- disclosure or human-in-the-loop rules: Fedora, LLVM, Linux kernel, Django, typescript-eslint;
- structural gates: Ghostty vouching, tldraw auto-closing external PRs, llama.cpp limits;
- shutting things down: curl ended its bug bounty, Jazzband is sunsetting.

Some projects (Zig, Gentoo) also left GitHub partly because of forced Copilot features. I found no formal OSS policy that bans AI *review* bots specifically. Rejection happens at the level of individual teams and maintainers. The Linux kernel is the counter-example: it adopted AI review (Sashiko) on an opt-in basis. Vendors (Anthropic, CodeRabbit, Greptile) and GitHub pitch AI review and triage as the answer to the slop wave. Independent studies say review bots should augment human reviewers, not replace them.

### Cited Findings

#### 2a. Project policies on AI-generated contributions (chronological; historical items labelled)
- *Historical:* the Gentoo Council banned AI-assisted contributions (2024-04-14), and NetBSD presumes LLM code tainted unless core approves it (2024-05). — [codenote.net overview](https://codenote.net/en/posts/oss-ai-slop-contribution-policy-shift/), [NetBSD commit guidelines](https://www.netbsd.org/developers/commit-guidelines.html)
- **QEMU** (2025-06) declines any contribution believed to include or derive from AI-generated content. The stated reason is legal provenance: contributors cannot certify the DCO for such code. — [QEMU code-provenance policy](https://www.qemu.org/docs/master/devel/code-provenance.html)
- **Ghostty** steps:
  - 2025-08-19: required disclosure of AI assistance — [PR #8289](https://github.com/ghostty-org/ghostty/pull/8289)
  - 2026-01-22: banned drive-by AI PRs not tied to an accepted issue — [AI_POLICY.md](https://github.com/ghostty-org/ghostty/blob/main/AI_POLICY.md)
  - 2026-02-15: vouching system; PRs from unvouched first-timers auto-close — [mitchellh/vouch](https://github.com/mitchellh/vouch)
  - 2026-04: left GitHub, citing infrastructure instability rather than AI — [Mitchell Hashimoto](https://mitchellh.com/writing/ghostty-leaving-github)
- **Cloud Hypervisor** (2025-09, v48) restricts AI-generated submissions for license reasons; **Fedora** (2025-10) adopted an AI-assisted contributions policy with accountability and `Assisted-by:` disclosure — [Fedora policy](https://docs.fedoraproject.org/en-US/council/policy/ai-contribution-policy/)
- **Django** (late 2025) requires AI disclosure and verified reproduction for security reports, and closes unverified ones — [Django security docs](https://docs.djangoproject.com/en/dev/internals/security/)
- **Zig** (2025-11-26) has a strict no-LLM/no-AI policy and moved its canonical repo to Codeberg — [ziglang.org](https://ziglang.org/news/migrating-from-github-to-codeberg/)
- **llama.cpp** tightened step by step — [overview](https://codenote.net/en/posts/oss-ai-slop-contribution-policy-shift/):
  - 2025-11-30: AI-generated code guidelines
  - 2026-01-13: banned AI-generated PR descriptions
  - 2026-02-11: banned AI in issues and discussions
  - 2026-03-09: new contributors limited to one open PR
  - 2026-03-21: account bans for violations
- **tldraw** (2026-01-15) auto-closes external PRs by default, citing misdirected AI PRs — [issue #7695](https://github.com/tldraw/tldraw/issues/7695), [blog 2026-01-17](https://tldraw.dev/blog/stay-away-from-my-trash)
- **typescript-eslint** (2026-01-20): no ban, but rules on review, understanding and prose, because low-quality PRs consume review bandwidth — [policy](https://typescript-eslint.io/contributing/ai-policy)
- **curl** (2026-01-26) ended its bug bounty after the share of valid reports fell below ~5% amid AI-fabricated reports — [Daniel Stenberg](https://daniel.haxx.se/blog/2026/01/26/the-end-of-the-curl-bug-bounty/)
- **LLVM** (early 2026) AI Tool Use Policy: no autonomous AI PRs without human approval, no AI on "good first issues", and contributors must review AI output before asking others to — [LLVM docs](https://llvm.org/docs/AIToolPolicy.html)
- **EFF** (2026-02) published a policy on LLM-assisted contributions — [EFF](https://www.eff.org/deeplinks/2026/02/effs-policy-llm-assisted-contributions-our-open-source-projects); **Jazzband** (2026-03-14) is sunsetting because shared push access became untenable amid AI spam — [Jazzband](https://jazzband.co/news/2026/03/14/sunsetting-jazzband)
- **Linux kernel** (2026): AI agents cannot add `Signed-off-by:`, and AI use is declared with `Assisted-by:` — [kernel docs](https://docs.kernel.org/process/coding-assistants.html). Secondary sources conflict on the exact tag format (generic "LLM" vs `AGENT_NAME:MODEL_VERSION`) — [All Things Open](https://allthingsopen.org/articles/open-source-ai-contributions-assisted-by-git-trailer-standard).
- **Counts:**
  - a Medium author who read 120 OSS AI policies counted 37 outright bans (2026-08) — [Medium](https://medium.com/@yadavrakshit60/i-read-the-ai-policies-of-120-open-source-projects-here-is-what-they-actually-say-9a5ea6897893)
  - the CHAOSS catalogue lists 63+ policies, about 14 bans and roughly a third disclosure-based (early 2026) — [chaoss/wg-ai-alignment](https://github.com/chaoss/wg-ai-alignment)
  - curated list — [melissawm/open-source-ai-contribution-policies](https://github.com/melissawm/open-source-ai-contribution-policies)

  The counts differ by method.

#### 2b. Platform-level responses (GitHub)
- GitHub PM Camilla Moraes opened Discussion #185387 on the growing volume of low-quality contributions. Options under consideration: disable PRs entirely, restrict PRs to collaborators, delete PRs, finer-grained permissions, AI-based triage, and AI-use attribution. — [The Register 2026-02-03](https://www.theregister.com/2026/02/03/github_kill_switch_pull_requests_ai/), [Discussion #185387](https://github.com/orgs/community/discussions/185387)
- GitHub blog "Welcome to the Eternal September of open source" (2026-02) laid out its plan for maintainers: PR disabling, collaborator-only PRs, interaction limits, and AI triage via `gh-aw` in progress. — [GitHub blog](https://github.blog/open-source/maintainers/welcome-to-the-eternal-september-of-open-source-heres-what-we-plan-to-do-for-maintainers/)
- GitHub withdrew the Copilot PR "tips" (2026-03-30) and stopped auto-adding Copilot as reviewer through Code Quality (2026-08-07). See 1m and 1n.

#### 2c. Teams and individuals dropping, limiting or refusing AI review bots
- HN eranation's team asked to remove CodeRabbit (2026-06-05) — [HN 48406358](https://news.ycombinator.com/item?id=48406358)
- HN mhitza cancelled Copilot after Actions billing (2026-04-28) — [HN 47932028](https://news.ycombinator.com/item?id=47932028)
- HN causal left Bugbot after per-run pricing (2026-06-05) — [HN 48406358](https://news.ycombinator.com/item?id=48406358)
- HN zmmmmm refuses to run it on every PR; HN furyofantares runs it less often than human review and reads only the top few findings (2026-01-26) — [HN 46766961](https://news.ycombinator.com/item?id=46766961)
- Linux kernel model: lists opt in (48 lists), maintainers may ignore reports, and Mason suggests running the prompts yourself with your own tokens. Anthropic, and probably Google, are willing to donate tokens to maintainers. (2026-05-25) — [LWN](https://lwn.net/Articles/1073583/)

#### 2d. Scale of the AI-slop / review-load wave
- Xavier Portilla Edo (Genkit core team) estimates only about 1 in 10 AI-created PRs is legitimate. Seth Larson (Python security) and Daniel Stenberg object to AI-generated reports. (2026-02-03) — [The Register](https://www.theregister.com/2026/02/03/github_kill_switch_pull_requests_ai/)
- Octoverse 2025: 43.2M PRs merged per month (+23% YoY) and PR creation up 20.4% (47.5M vs 39.5M). (2025-10-28) — [GitHub Octoverse 2025](https://github.blog/news-insights/octoverse/octoverse-a-new-developer-joins-github-every-second-as-ai-leads-typescript-to-1/)
- Octoverse 2026: by September 2026 agents started more than 40% of all PRs, up from 17% in March. (2026-10-28/29) — [Visual Studio Magazine](https://visualstudiomagazine.com/articles/2026/10/29/github-octoverse-agents-started-more-than-40-percent-of-september-pull-requests.aspx)
- HN thread "Harvard researchers find AI coding agents shifted the bottleneck to code review" (2026-11-17; 331 pts, 465 comments). I did not verify the study's details. — [HN 50538303](https://news.ycombinator.com/item?id=50538303), [ComplexDiscovery](https://complexdiscovery.com/harvard-researchers-find-ai-coding-agents-shifted-the-bottleneck-to-code-review/)

#### 2e. Review bots pitched as the answer (vendor claims) vs. evidence
- Anthropic launched Code Review to check the flood of AI-generated code, saying code review has become a bottleneck **(vendor framing)**. (2026-03-09) — [TechCrunch](https://techcrunch.com/2026/03/09/anthropic-launches-code-review-tool-to-check-flood-of-ai-generated-code/), [ITPro](https://www.itpro.com/software/development/anthropic-says-code-review-has-become-a-bottleneck-this-new-claude-code-feature-aims-to-solve-that)
- CodeRabbit offers free review on every public repo and pledged $600k (2025), then $1M, then more than $10M of its direct cost to OSS. It cites AI tools flooding OSS with lower-quality PRs **(vendor claim)**. — [CodeRabbit OSS](https://www.coderabbit.ai/oss), [pledge](https://www.coderabbit.ai/blog/coderabbit-expands-its-commitment-to-open-source)
- Greptile's "There is an AI code review bubble" (Jan 2026) acknowledges a crowded market and argues that independent validation agents and automated feedback loops will be the differentiators **(vendor claim)**. — [Greptile](https://greptile.com/blog/ai-code-review-bubble); HN discussion 2026-01-26, 351 pts/249 comments — [HN 46766961](https://news.ycombinator.com/item?id=46766961)
- **Sashiko** [OSS, Apache-2.0, ownership given to the Linux Foundation] is built by Google's Roman Gushchin. It reviews all LKML patches with Gemini 3.1 Pro and is based on Chris Mason's open review prompts (announced 2026-03) — [LKML announcement](https://lkml.iu.edu/hypermail/linux/kernel/2603.2/03802.html). Google claims a 35% drop in merged commits needing a follow-up fix within 60 days **(vendor claim)** — [Google Cloud blog](https://cloud.google.com/blog/products/application-development/lessons-from-building-sashiko-an-agentic-code-review-system).
- Counter-evidence:
  - The claim that CRAs can handle 80% of OSS PRs without humans is not supported: CRA-only PRs merge less and are abandoned more (2026-04-03) — [arXiv 2604.03196](https://arxiv.org/abs/2604.03196)
  - At FOSDEM, Stenberg warned that AI analyzers can cause issue overload and still need a human filter (2026-02) — [FOSDEM 2026 slides](https://daniel.haxx.se/media/FOSDEM%202026%20OSS%20security%20in%20spite%20of%20AI.pdf)

### Inferences
- Policies target AI-*authored* input (PRs, issues, security reports), not AI *review*. Where AI review is welcome (kernel, curl's analyzer reports), it is opt-in, run or vetted by maintainers, and treated as advisory.
- Vendors frame review bots as the fix for AI slop, which creates a circular dynamic of AI reviewing AI. Independent evidence (MSR 2026, Agarwal et al. 2026) suggests this works only with a human in the loop.

### Gaps
- No formal OSS policy found that bans or restricts AI *review* bots (CodeRabbit, Copilot review, Gemini Code Assist) as such. Rejections show up only as individual team decisions or GitHub complaints.
- No reliable numbers on how many OSS repos uninstalled review bots.
- The details of the Harvard study (Nov 2026) are unverified.
- Some secondary policy reports (QGIS ban, OpenJDK not accepting AI-generated code) were not checked against primary sources: [dev.to on QGIS](https://dev.to/alanwest/qgis-banned-ai-generated-code-heres-an-ai-policy-your-project-can-copy-2a4e), [builtplain on OpenJDK](https://builtplain.com/open-source-ai-contribution-policies/).

---

## 3. Praise categories: what AI review is actually good at

### Takeaway
Practitioners consistently praise AI review for local, mechanical correctness issues that humans skim past: off-by-one, pointer and null mistakes, uninitialized variables, missing arguments, races, redundant calls, missing DB indexes and migration gaps. They also value it as a cheap "second pair of eyes" before human review. At scale it finds real bugs and security problems: curl fixed 100+ AI-found issues, Sashiko reports ~85% true positives, Cloudflare runs 131k reviews a month. Measured acceptance of comments is moderate, about 36–74% depending on tool and metric. AI review is weak on architecture, business intent and cross-system effects.

### Cited Findings

#### 3a. Catching real local bugs humans miss
- HN onedognight: Claude's comments are about 50% useful and catch things human reviewers consistently miss. HN greymalik: Bugbot has very little noise and found issues experienced humans missed. HN shagie: the AI caught a redundant filter and a repeated setter call across a call boundary that the linter missed. HN gherkinnn: Opus 4.5 catches missing DB indexes, migration gaps and edge cases linters don't. HN vimda: Bugbot found a race condition that `go test -race` missed. HN justapassenger: good at mechanical bugs such as off-by-one and pointers. HN The_Fox: CodeRabbit finds subtle problems humans miss. HN cbovis: Copilot uses context beyond the diff, such as existing constants and reusable helpers. (2026-01-26) — [HN 46766961](https://news.ycombinator.com/item?id=46766961)
- Even in the complaint thread #189767, the useful Copilot findings were crash-class bugs: an uninitialized variable and missing arguments. (2026-03-16) — [GitHub #189767](https://github.com/orgs/community/discussions/189767)
- MisinformedDNA: Copilot reviews saved hours by catching simple mistakes. sgryphon: the reviews are often useful. (2025-09-09) — [GitHub #169148](https://github.com/orgs/community/discussions/169148)
- HN lukaslalinsky: CodeRabbit is the only tool that finds real logic bugs. HN atestu: CodeRabbit finds a lot for a flat fee. (2026-06-05) — [HN 48406358](https://news.ycombinator.com/item?id=48406358)
- HN alkonaut: agents now catch issues better than they do themselves. (2026-11-17) — [HN 50538303](https://news.ycombinator.com/item?id=50538303)
- The Bugbot user on the Cursor forum: Bugbot found five genuine defects that would otherwise have shipped, and Codex later found more valid P1s. (2026-08-23) — [Cursor forum](https://forum.cursor.com/t/codex-review-vs-bugbot-review/169245)

#### 3b. Security and correctness findings at scale (maintainer-endorsed)
- **curl.** Daniel Stenberg praised Joshua Rogers' reports from AI-assisted analyzers (ZeroPath, Almanax, Corgea, Gecko, Amplify — all [prop]). About 50 bugfixes were merged, none critical (Oct 2025) — [The Register 2025-10-02](https://www.theregister.com/2025/10/02/curl_project_swamped_with_ai/), [Stenberg, "A new breed of analyzers" 2025-10-10](https://daniel.haxx.se/blog/2025/10/10/). By FOSDEM 2026 curl had fixed 100+ AI-found issues, with the warning about overload and the need for human filtering (2026-02) — [slides](https://daniel.haxx.se/media/FOSDEM%202026%20OSS%20security%20in%20spite%20of%20AI.pdf). ZeroPath claims 170 valid bugs **(vendor claim)** — [ZeroPath](https://zeropath.com/blog/how-zeropath-won-over-curl-with-170-valid-bugs).
- **Linux kernel / Sashiko** [OSS] — [LWN](https://lwn.net/Articles/1073583/) (2026-05-25):
  - In the 1,500-thread analysis, ~85% of findings were true positives and critical/high-severity findings were ~97% accurate **(self-reported by the author)**.
  - Commit messages mentioned Sashiko about 140 times in the ~7 weeks after its mid-March launch.
  - Gushchin was surprised by how many pre-existing bugs it finds.
  - Jonathan Corbet called the review prompts very useful documentation.
  - Lorenzo Stoakes was enthusiastic at launch — [LKML 2026-03](https://lkml.iu.edu/hypermail/linux/kernel/2603.2/05846.html).
- **Cloudflare** (internal system on top of OpenCode [OSS]) — [Cloudflare](https://blog.cloudflare.com/ai-code-review/) (2026-04-20):
  - 131,246 review runs on 48,095 MRs across 5,169 repos between 2026-03-10 and 2026-04-09.
  - About 1.2 findings per review.
  - Humans overrode a block ("break-glass") on only 0.6% of MRs.
  - The security reviewer had the highest critical share (4%, 484 critical findings).
  - The post says it flags real bugs with high accuracy and approves clean code.

#### 3c. Measured usefulness and acceptance (most independent evidence first)
- CodeRabbit in the wild: 36.4% of comments accepted, 7.3% discussed (2026-07-03) — [arXiv 2607.03316](https://arxiv.org/abs/2607.03316)
- Beko industrial case on PR-Agent [OSS]: 238 practitioners, 4,335 PRs, 1,568 auto-reviewed. 73.8% of bot comments were marked resolved, but PR closure time rose. The follow-up paper warns that "resolved" is an imperfect proxy for usefulness. (Dec 2024 / ICSE SEIP 2025; historical) — [arXiv 2412.18531](https://arxiv.org/html/2412.18531v2), [arXiv 2604.24525](https://arxiv.org/html/2604.24525v1)
- Sun et al.: across 16 AI review GitHub Actions, 22,000+ comments and 178 repos, effectiveness varies widely. Comments that are concise, include code snippets, are manually triggered, or come from hunk-level tools are more likely to lead to code changes. (2025-08-26; v2 2026-04-25) — [arXiv 2508.18771](https://arxiv.org/abs/2508.18771)
- OpenAI says authors changed code in response to 52.7% of its reviewer's comments on OpenAI's own PRs, and that the reviewer is tuned to flag fewer issues so more of them are right **(vendor claim)**. (date not captured) — [OpenAI alignment blog](https://alignment.openai.com/scaling-code-verification)
- Augment's knes claims its comments are 2–3× more likely to be fixed than Bugbot's or CodeRabbit's **(vendor claim, unverified)**. (2026-01-26) — [HN 46766961](https://news.ycombinator.com/item?id=46766961)

#### 3d. Usage patterns practitioners say make AI review worthwhile
- Ask for a severity-ranked top-10 list a human can scan in seconds (colechristensen). Run it less often than human review and read only the top items (furyofantares). Run Claude Code first and pass on only the useful findings (thesurlydev). Treat it as an extra second pair of eyes, not a replacement (philipwhiuk). (2026-01-26) — [HN 46766961](https://news.ycombinator.com/item?id=46766961)
- Cloudflare's design lessons (2026-04-20) — [Cloudflare](https://blog.cloudflare.com/ai-code-review/):
  - use narrow specialist reviewers;
  - state explicitly what not to flag;
  - require structured findings with severity;
  - deduplicate in a coordinator;
  - tier by risk: cheap models for trivial diffs, full review for security-sensitive files;
  - bias toward approval: one warning doesn't block, and a break-glass override exists.
- Codex flags only P0/P1 issues by default in GitHub — [Codex docs (third-party mirror)](https://www.codex-docs.com/en/docs/third-party/github). Mason says the kernel review prompts suit interactive development, while Sashiko suits mailing lists — [LWN](https://lwn.net/Articles/1073583/) (2026-05-25).

#### 3e. PR summaries and first pass on large diffs
- The evidence here is thin. Gemini Code Assist offers `/gemini summary` — [Google docs](https://developers.google.com/gemini-code-assist/docs/review-github-code). The Claude Code team says people ask Claude for explainers of the code slice they need **(vendor claim)**, and HN commenters were skeptical that LLM explanations are accurate (daveguy, marcindulak; 2026-10-16) — [HN 50122951](https://news.ycombinator.com/item?id=50122951). ryanchants disabled CodeRabbit's extra summary artefacts (poems, diagrams) (~2025-12-16) — [HN 46295395](https://news.ycombinator.com/item?id=46295395).

### Inferences
- The praise clusters on bounded, local defects a fresh reader can check against the diff. The complaints cluster on things that need system-level knowledge. That fits the use practitioners describe: a pre-human first pass, not an approver.
- Maintainer-endorsed successes (curl, kernel, Cloudflare) share a pattern: humans curate the findings, tools are tuned per domain, and reviews are opt-in or advisory.

### Gaps
- No independent study found that measures whether AI-generated PR summaries actually speed up human reviewers.
- Most praise is anecdotal (HN) or self-reported (Sashiko, OpenAI, Cloudflare). Apart from the CodeRabbit and Beko studies, there is no controlled comparison of AI review against human review.

---

## 4. Comparative sentiment: high-signal vs noisy tools; open source and self-hosted vs proprietary

### Takeaway
Late-2025–2026 practitioner reputation:
- **High-signal, low-volume:** Cursor Bugbot and OpenAI Codex review (precision-first by design).
- **Deep but expensive:** Claude-based reviewers, especially the managed Claude Code Review.
- **Polarized, good once tuned:** CodeRabbit.
- **Noisy or shallow but convenient and most widely deployed:** GitHub Copilot code review. Its 2026 reputation is also hurt by re-review loops, no off switch for OSS owners, PR ad "tips" and Actions-minute billing.
- **High-recall but noisy:** Greptile, according to secondary comparisons.
- **Repetitive and over-praising:** Gemini Code Assist, in one maintainer write-up.

Every vendor claims #1 on some leaderboard metric, so benchmarks do little to settle the question. Open-source options (PR-Agent, now donated by Qodo to the community; Kodus; Alibaba's Open Code Review; OpenCode-based or DIY pipelines; Sashiko/Mason prompts for the kernel) are chosen for cost control, data privacy, model choice and customization. Users give up polish and setup time, keep up with new model APIs themselves, and still pay for tokens.

### Cited Findings

#### 4a. Tool-by-tool reputation (proprietary unless marked)
- **Cursor Bugbot [prop]:**
  - Praised as low-noise: greymalik and vimda (2026-01-26) — [HN 46766961](https://news.ycombinator.com/item?id=46766961)
  - Negatives: output varies per run (vimda); missed concurrency and ordering classes that Codex later caught (2026-08-23) — [Cursor forum](https://forum.cursor.com/t/codex-review-vs-bugbot-review/169245); stale model knowledge (2025-06-26) — [Cursor forum](https://forum.cursor.com/t/false-bug-claude-version/109813); usage-based pricing backlash (2026-05/06) — see 1h
  - Cursor also acquired Graphite [prop] on 2025-12-19 and keeps it as a standalone product — [TechCrunch](https://techcrunch.com/2025/12/19/cursor-continues-acquisition-spree-with-graphite-deal), [Cursor blog](https://cursor.com/blog/graphite)
- **OpenAI Codex review [prop service; the Codex CLI itself is open source]:**
  - Design: flags only P0/P1 and deliberately flags fewer issues **(vendor)** — [OpenAI](https://alignment.openai.com/scaling-code-verification)
  - Recommended by HN CSMastermind, who sees a wide quality gap between tools (2026-01-26) — [HN 46766961](https://news.ycombinator.com/item?id=46766961)
  - Found valid issues after Bugbot came back clean (2026-08-23) — [Cursor forum](https://forum.cursor.com/t/codex-review-vs-bugbot-review/169245)
  - sfortis runs a Codex review skill on subscription quota instead of API tokens (2026-06-05) — [HN 48406358](https://news.ycombinator.com/item?id=48406358)
  - Competitor cubic says the ChatGPT Codex Connector ranks 13th of 15 by F1 (55.6%) on Martian's bench, i.e. it trades recall for precision **(competitor claim)** — [cubic blog](https://www.cubic.dev/blog/codex-code-review)
- **Claude-based reviewers [prop models; Anthropic's `claude-code-action` GitHub Action is open source]:**
  - vimda says the Claude bot is well worth it despite inconsistency; onedognight finds it ~50% useful; shakna reports hallucinated APIs (2026-01-26) — [HN 46766961](https://news.ycombinator.com/item?id=46766961)
  - The managed Claude Code Review (2026-03-09) is praised for depth and its multi-agent design, but criticized for $15–25/review and ~20 min latency — [TechCrunch](https://techcrunch.com/2026/03/09/anthropic-launches-code-review-tool-to-check-flood-of-ai-generated-code/), [InfoQ](https://infoq.com/news/2026/04/claude-code-review)
  - Press notes the open-source Claude Code GitHub Action as the cheaper alternative — [VentureBeat](https://venturebeat.com/ai/anthropic-rolls-out-code-review-for-claude-code-as-it-sues-over-pentagon)
- **CodeRabbit [prop; free for public repos]:** polarized.
  - Positive: ryanchants, after disabling extras (~2025-12-16); The_Fox, cheap and finds subtle problems (2026-01-26); lukaslalinsky, the only tool finding real logic bugs; atestu (2026-06-05).
  - Negative: 56.3% of comments rejected in the 239-repo study (2026-07-03) — [arXiv 2607.03316](https://arxiv.org/abs/2607.03316); eranation's team asked to remove it; lukeasrodgers called CodeRabbit and Qodo trash (2026-06-05) — [HN 48406358](https://news.ycombinator.com/item?id=48406358); security incident write-up (2025-08-19), see 1o.
  - Says it leads Martian's online F1 ranking **(vendor claim; 2026-03)** — [CodeRabbit](https://www.coderabbit.ai/ja/blog/coderabbit-tops-martian-code-review-benchmark)
- **GitHub Copilot code review [prop]:**
  - Most widely adopted: in Jellyfish's customer telemetry 67% of review-agent users use Copilot Review vs 12% CodeRabbit, and overall review-agent adoption grew from 14.8% (Jan 2025) to 51.4% (Oct 2025) **(analytics vendor)** — [Jellyfish "2025 AI Metrics in Review"](https://jellyfish.co/blog/2025-ai-met) (URL as returned by search; may be truncated)
  - Liked for convenience and zero extra cost (bartread) and for context beyond the diff (cbovis); called noisy by greymalik (2026-01-26) — [HN 46766961](https://news.ycombinator.com/item?id=46766961)
  - Negatives: re-review loop (2026-03), no off switch for repo owners (2025-08), PR ad tips (2026-03-30), Actions-minute billing (2026-06-01) — see 1e, 1h, 1m, 1n
  - The New Stack reports Copilot (Balanced) leads a different benchmark, ReviewBench, at 40.1% grounded F1 — [The New Stack](https://thenewstack.io/?p=22839357) (date not captured)
- **Greptile [prop]:**
  - The founder defended the tool on HN with "great catch" counts, and commenters called that metric invalid (2026-01-26) — [HN 46766961](https://news.ycombinator.com/item?id=46766961)
  - Blog-style comparisons describe it as high recall but the noisiest (low-reliability secondary roundups, e.g. [PkgPulse](https://www.pkgpulse.com/guides/coderabbit-vs-greptile-vs-bugbot-ai-code-review-2026))
  - Claims #1 F1 (60.8%; precision 76.2%, recall 50.6%) on Martian's bench **(vendor claim; 2026-07-30)** — [Greptile](https://www.greptile.com/content-library/greptile-martian-code-review-benchmark)
- **Gemini Code Assist [prop GitHub app]:** criticized in a maintainer write-up for praise spam, duplicate flags and non-determinism (date not captured) — [openSUSE Hack Week](https://hackweek.opensuse.org/projects/explore-ways-how-gemini-can-help-with-code-reviews). Google's blog cites positive initial feedback from Delivery Hero **(vendor claim)** — [Google Cloud blog](https://cloud.google.com/blog/products/ai-machine-learning/gemini-code-assist-and-github-ai-code-reviews).
- **Qodo (Qodo Merge, rebranded Qodo 2.0) [prop]:** one HN user lumps it with CodeRabbit as bad (2026-06-05). Qodo claims #1 on Martian's bench **(vendor claim)** — [Qodo](https://www.qodo.ai/blog/qodo-ranked-1-ai-code-review-tool-in-martians-code-review-benchmark)
- **Others** (HN 2026-01-26 unless noted):
  - Atlassian Rovo Dev [prop]: few but relevant comments once configured (brabel)
  - GitLab Duo [prop]: being tested as a supplement (philipwhiuk)
  - TeamScale [prop]: almost never useful (onedognight)
  - DeepSource [prop]: gets less attention than CodeRabbit (The_Fox)
  - SonarQube/CodeQL static analysis: mostly noise (materialpoint)
  - gitar.ai [prop]: recommended for flat-rate pricing (kageiit, 2026-06-05)
  - cubic [prop, formerly mrge.io; launched on HN 2025-04-15] — [HN 43692476](https://news.ycombinator.com/item?id=43692476)
  - Baz and Unblocked [prop]: claim Martian-bench wins (vendor) — [Baz](https://baz.co/resources/baz-1-in-precision-in-independent-code-review-bench), [Unblocked](https://getunblocked.com/blog/unblocked-catches-the-most-bugs-on-code-review-bench/)

#### 4b. Benchmarks: vendor claims vs independent evidence
- Martian's Code Review Bench [OSS benchmark; launched early 2026; an offline set of 50 PRs from 5 OSS projects plus an online leaderboard] became the vendors' scoreboard. Each claims #1 on a different metric or leaderboard: Baz on precision (2026-02), CodeRabbit on online F1 (2026-03), Qodo, Greptile on F1 (2026-07-30), Unblocked on recall (2026-11). — [Byteiota summary](https://byteiota.com/ai-code-review-benchmark-2026-first-real-results/), [Martian (via third-party summary)](https://jacek-mar.github.io/ai-dev-blog/posts/martians-independent-benchmark-tested-13-code-review-tools.html)
- Earlier vendor benchmarks fed HN discussions too: Qodo's GPT-5 PR-benchmark (2025-08-08) — [HN 44833929](https://news.ycombinator.com/item?id=44833929); CodeRabbit's and Entelligence's model-for-review evaluations (2026-09-05, 2026-09-14) — [HN 49572875](https://news.ycombinator.com/item?id=49572875), [HN 49703003](https://news.ycombinator.com/item?id=49703003).
- The most independent evidence is academic: Lin et al. 2026, Chowdhury et al. 2026 and Sun et al. 2025/26 (see 1a, 3c). All report substantial noise and widely varying effectiveness.

#### 4c. Open-source and self-hosted options, and how they are perceived
- **PR-Agent [OSS]:**
  - Its README says Qodo donated it to the open-source community and calls it a community-maintained legacy project of Qodo. Its first external maintainer is @naorpeled, and it is reportedly moving toward a foundation.
  - Supports GitHub, GitLab, Bitbucket, Azure DevOps and Gitea, and any LLM via LiteLLM, including Ollama.
  - Docker images moved to `pragent/pr-agent`.
  - The hosted product evolved into Qodo 2.0 [prop].
  - — [The-PR-Agent/pr-agent](https://github.com/The-PR-Agent/pr-agent) (no donation date stated; observed 2026-11)
  - License not confirmed in this pass; a Kodus comparison page calls it MIT.
  - Industrial evidence: the Beko study (3c).
- **Kodus / Kody [OSS, self-hostable]:** its own material stresses that code, LLM calls and review history stay in your network, BYO LLM with vLLM/Ollama support, and opt-out telemetry **(vendor claims)** — [GitHub](https://github.com/kodustech/kodus-ai), [kodus.io](https://kodus.io/self-hosted-ai-code-review/). No independent practitioner reviews found.
- **Alibaba Open Code Review [OSS CLI]** (HN 2026-06-05, 284 pts, 73 comments) — [HN 48406358](https://news.ycombinator.com/item?id=48406358):
  - Interest centered on a free, token-efficient tool.
  - Problems reported: a hardcoded `max_tokens` broke with gpt-5.x models (sfortis, eranation); rule files originally in Chinese (nutifafa); the advertised divide-and-conquer strategy not implemented (nullbio); one benchmark run reached ~12% precision (eranation).
- **OpenCode [OSS agent]:** Cloudflare's production reviewer is built on it, with 45+ upstream PRs from Cloudflare engineers; the orchestration layer is proprietary (2026-04-20) — [Cloudflare](https://blog.cloudflare.com/ai-code-review/)
- **Sashiko [OSS] and Chris Mason's kernel review prompts [OSS]:** used by the kernel community; see 2e and 3b. HN discussion — [HN 47427647](https://news.ycombinator.com/item?id=47427647) (2026-03-18).
- **DIY wrappers:**
  - lukeasrodgers uses an in-house wrapper around Claude/Codex with per-repo skills; elpakal built a hackathon bot; jayphen built a model-agnostic macOS review app whose full 50-PR benchmark run cost about $7 (2026-06-05) — [HN 48406358](https://news.ycombinator.com/item?id=48406358)
  - storystarling built a LangGraph/Celery pipeline (2026-01-26) — [HN 46766961](https://news.ycombinator.com/item?id=46766961)
- **The open-source review-action ecosystem:** Sun et al. studied 16 popular AI review GitHub Actions and found effectiveness varies widely (2025-08-26) — [arXiv 2508.18771](https://arxiv.org/abs/2508.18771)

#### 4d. Why people choose OSS or self-hosted, and what they give up
- **Cost and SaaS markup:**
  - storystarling, gherkinnn and roncesvalles (2026-01-26) — [HN 46766961](https://news.ycombinator.com/item?id=46766961)
  - lukeasrodgers (2026-06-05) — [HN 48406358](https://news.ycombinator.com/item?id=48406358)
  - Flat-to-usage repricing by Bugbot and Copilot (2026) — see 1h
- **Privacy, security and lock-in:**
  - mawadev self-hosts to avoid vendor lock-in (2026-04-28) — [HN 47932028](https://news.ycombinator.com/item?id=47932028)
  - The CodeRabbit RCE write-up (2025-08-19) — [Kudelski](https://kudelskisecurity.com/research/how-we-exploited-coderabbit-from-a-simple-pr-to-rce-and-write-access-on-1m-repositories)
  - Kodus says it keeps data inside the network **(vendor claim)**
  - Exits from GitHub to Codeberg/Forgejo over forced Copilot (2025–2026) — see 1m
- **Model choice and quality control:**
  - jayphen and cheema33 (different models catch different issues); embedding-shape and tylermarques (2026-06-05) — [HN 48406358](https://news.ycombinator.com/item?id=48406358)
  - Cloudflare's runtime model routing with failback across Claude, GPT-5.x and Kimi K2.5 (2026-04-20)
- **Transparency and customization:** the CLI and rule files can be inspected and tuned (nutifafa, pramodbiligiri; 2026-06-05) — [HN 48406358](https://news.ycombinator.com/item?id=48406358)
- **What they give up:**
  - Setup and maintenance: code patches needed for new models; multi-week deployments **(competitor claim)** — [Augment](https://www.augmentcode.com/tools/open-source-ai-code-review-tools-worth-trying)
  - Missing or unfinished features and docs, and precision problems (Alibaba OCR thread)
  - Token costs remain (krzyk)
  - Running the reliability layer yourself: rate limits, provider outages, circuit breakers, prompt-injection hardening (Cloudflare)
  - Free OSS tiers may gate SSO behind paid plans, per Augment **(competitor claim)**

### Inferences
- The 2026 consensus among HN practitioners: precision-first tools (Bugbot, Codex) earn trust, while recall-maximizing tools need heavy tuning. Copilot wins on distribution, not on reputation.
- Usage-based repricing in 2026 and the security incidents push larger orgs toward a hybrid: an OSS agent or orchestrator (OpenCode, PR-Agent, Sashiko-style) with frontier models via API. Cloudflare is the clearest public example. The trade-off is engineering effort in exchange for control over cost, data and models.
- Vendor leaderboards are contradictory enough that practitioners recommend testing on your own PRs (also the conclusion of several third-party roundups).

### Gaps
- No 2025–2026 practitioner sentiment found for Graphite's AI reviewer (Diamond / "Graphite Agent"), Ellipsis or Sourcery. Search found no confirmation of the product name "Graphite Agent".
- No independent user reviews of Kodus. Little evidence on local-model (Ollama) review quality, because Reddit/r/LocalLLaMA could not be reached.
- PR-Agent's license and the date of the donation were not confirmed.
- No independent head-to-head study of named tools comparable in rigor to the academic papers. The Martian bench results are known here only through vendor and third-party summaries; the live leaderboard (codereview.withmartian.com) was not checked.

---

## 5. Survey data on trust in AI output and on code review

### Takeaway
Surveys show near-universal adoption with low or conditional trust:
- SO 2025: 84% use or plan to use AI, but more developers distrust its accuracy (46%) than trust it (33%), and only 3% trust it highly.
- DORA 2025: 90% adoption, with ~30% reporting little or no trust in AI-generated code.
- Sonar 2026: 96% don't fully trust AI code, yet only 48% always check it.
- SO 2026: trust is conditional on verification and source attribution.

None of the big surveys (SO, JetBrains, DORA) found in this pass asks specifically about satisfaction with AI *review* bots. Review-bot adoption numbers come from vendors (Jellyfish) and GitHub's Octoverse PR statistics.

### Cited Findings
- **Stack Overflow Developer Survey 2025** (2025-07-29):
  - 84% use or plan to use AI tools.
  - 46% distrust the accuracy of AI output vs 33% who trust it; only 3% highly trust it.
  - The SO blog gives a separate trust-in-accuracy series that fell from ~40% to 29%, a different framing from the 33% figure.
  - — [SO press release](https://stackoverflow.co/company/press/archive/stack-overflow-2025-developer-survey/), [SO blog](https://stackoverflow.blog/2025/07/29/developers-remain-willing-but-reluctant-to-use-ai-the-2025-developer-survey-results-are-here/), [TechRepublic](https://www.techrepublic.com/article/news-developer-trust-in-ai-declines/)
- **Stack Overflow Developer Survey 2026** (2026-10-06):
  - 73% of those using AI coding assistants or agents use them daily.
  - Nearly half trust AI when they can verify its work; only 6.6% would trust it with an important decision.
  - The share saying source attribution matters is 93% per the SO blog vs 78.7% per IT Brief, probably different questions.
  - — [SO blog](https://stackoverflow.blog/2026/10/06/the-results-of-the-2026-developer-survey-are-here/), [IT Brief](https://itbrief.com.au/story/stack-overflow-survey-shows-developers-trust-ai-with-caveats)
- **JetBrains State of Developer Ecosystem 2025** (2025-10):
  - 24,534 developers in 194 countries (fieldwork Apr–Jun 2025); 85% regularly use AI.
  - Inconsistent quality of AI-generated code is the top AI concern; The Register reports 23% worry about low-quality generated code.
  - — [JetBrains](https://blog.jetbrains.com/research/2025/10/state-of-developer-ecosystem-2025/), [The Register 2025-10-21](https://www.theregister.com/2025/10/21/massive_jetbrains_dev_survey)
- **DORA 2025 State of AI-assisted Software Development** (2025-09):
  - 90% AI adoption; >80% believe it raised their productivity.
  - ~30% report little or no trust in AI-generated code; 49% trust it "somewhat".
  - 59% see a positive effect on code quality.
  - Higher AI adoption is associated with higher delivery throughput *and* higher instability.
  - Review load shifts to reviewers.
  - — [Google blog](https://blog.google/technology/developers/dora-report-2025/), [Google Cloud](https://cloud.google.com/blog/products/ai-machine-learning/announcing-the-2025-dora-report), [report PDF](https://services.google.com/fh/files/misc/2025_state_of_ai_assisted_software_development.pdf), [DORA insights](https://dora.dev/insights/balancing-ai-tensions/)
- **GitHub Octoverse 2025** (2025-10-28): 43.2M PRs merged/month (+23%); 47.5M PRs created/month (+20.4%); Copilot code review introduced in April 2025 — [GitHub](https://github.blog/news-insights/octoverse/octoverse-a-new-developer-joins-github-every-second-as-ai-leads-typescript-to-1/)
- **GitHub Octoverse 2026** (2026-10-28): agents started more than 40% of PRs by September 2026 (17% in March) — [Visual Studio Magazine](https://visualstudiomagazine.com/articles/2026/10/29/github-octoverse-agents-started-more-than-40-percent-of-september-pull-requests.aspx)
- GitHub added Copilot-review metrics to its usage API: PRs reviewed by Copilot (2025-12-18) and merged PRs reviewed by Copilot (2026-04-08) — [changelog 2025-12-18](https://github.blog/changelog/2025-12-18-enterprise-level-pull-request-activity-metrics-now-in-public-preview), [changelog 2026-04-08](https://github.blog/changelog/2026-04-08-copilot-reviewed-pull-request-merge-metrics-now-in-the-usage-metrics-api)
- **Sonar State of Code Developer Survey 2026** **(vendor survey)** (2026-01-08):
  - more than 1,100 developers;
  - 96% don't fully trust that AI code is functionally correct, and only 48% always check it before committing;
  - 38% vs 27% say AI code takes more vs less effort to review;
  - about 42% of committed code is AI-generated or assisted.
  - The Register flags that the vendor's framing favors its own products.
  - — [Sonar](https://www.sonarsource.com/company/press-releases/sonar-data-reveals-critical-verification-gap-in-ai-coding/), [The Register 2026-01-09](https://www.theregister.com/2026/01/09/devs_ai_code/)
- **Jellyfish** (engineering-analytics vendor): review-agent adoption rose from 14.8% in Jan 2025 to 51.4% in Oct 2025, jumping when Copilot code review became generally available in Mar–Apr 2025. Among users, 67% use Copilot Review and 12% CodeRabbit. — [Jellyfish](https://jellyfish.co/blog/2025-ai-met) (URL may be truncated)
- **Academic synthesis of practitioner discourse:** Agarwal, Miller, Kästner and Vasilescu filtered 38,709 grey-literature documents (engineering blogs, Reddit) and coded 3,100. They frame review as the control point where an agent's effect on software is decided, with the outcome set by team expertise and process, not by AI. (2026-07-08) — [arXiv 2607.07980](https://arxiv.org/abs/2607.07980)

### Inferences
- The "trust but verify" gap (Sonar's 96% vs 48%, SO 2026's conditional trust) is the backdrop for review bots. Teams adopt them as the verification step, but the academic and HN evidence shows that bot-only verification is the weak link (CRA-only PRs merge less; rubber-stamping).
- Reported trust stayed low through 2025–2026 while usage kept rising (SO 2025 → 2026; Octoverse agent PR share 17% → 40%+). The pressure on review capacity is growing, not easing.

### Gaps
- No question specific to AI code-review bots was found in SO 2025/2026, JetBrains 2025 or DORA 2025 coverage. Code-review-specific numbers come from vendors (Sonar, Jellyfish) and academic papers.
- JetBrains 2026 and DORA 2026 reports were not found in this pass and may not exist yet. The full SO 2026 AI section (e.g., a trust-in-accuracy figure comparable to 2025) was not retrieved.
- Some widely repeated SO 2025 figures (e.g., the share frustrated by "almost right" answers) were not re-verified here and are deliberately left out.
