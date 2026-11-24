# Empirical Evidence on LLM-Based Code Review and the Design Lessons Behind Better AI Reviewers (state as of 2026-11-23)

Labels used below:
- [PEER-REVIEWED] means accepted at a named venue. [PREPRINT] means arXiv only.
- [INDUSTRY SELF-REPORT] means a company is measuring its own internal tool.
- [VENDOR CLAIM / CoI] means a company is measuring a product it sells. Treat these as marketing-grade evidence.
- [BACKGROUND] marks work from before 2025.
- [SECONDARY] marks a number seen only in a search snippet or third-party summary, not confirmed on the primary page.

Measurement warning that applies to every section: "addressed / resolved / accepted" rates are measured with incompatible proxies. Examples: a thread-status label (Beko), an LLM judge of whether the code changed (GitHub Actions study, Cursor, Martian, GitHub), the comment no longer reproducing on re-runs (Uber), flagged lines being modified later (ByteDance "Outdated Rate"), the comment being absent in the next snapshot (Google), and an explicit "accept" button (Mozilla/Ubisoft). Numbers from different sources are not directly comparable.

## Key Question 1 — Academic field studies of deployed AI reviewers: what fraction of comments lead to changes, which comment types are useful, and what happens to cycle time?

### Takeaway
Field evidence (2024–2026) shows a very wide spread. Naive "send the diff to GPT" GitHub Actions get only 0.9–19.2% of their valid comments addressed, against 60% for human comments. Open-source PRs reviewed by CodeRabbit see 36.4% of comments accepted and 56.3% rejected. Engineered industrial systems reach 38.7% (Atlassian, vs 44.45% for humans) and 65% (Uber, vs 51% for humans) on their own proxies. Effects on cycle time are mixed. Beko's PR closure time rose from 5h52m to 8h20m, Google's A/B test found no significant change, and Atlassian reports −30.8% (observational). Developers favour concise, hunk-level, code-bearing comments about correctness. PR-level summaries, verbose prose, and nits are mostly ignored.

### Cited Findings

#### Beko + Qodo PR-Agent — "Automated Code Review In Practice" (Cihan et al., arXiv 2412.18531, v2 28 Dec 2024) [BACKGROUND][PREPRINT; the arXiv page states no venue; industry–academic team, no vendor co-authorship shown]
- Setting: Beko's software division (238 practitioners). The team used Qodo PR-Agent, customized internally as "CodeReviewBot", on GPT-4. The paper is inconsistent about the variant, saying "GPT-4 Turbo" in one place and "GPT-4-32K" elsewhere. 10 projects and 22 repos used it, and 3 projects were analysed. — [arXiv 2412.18531](https://arxiv.org/html/2412.18531v2)
- Data: 4,335 PRs, of which 1,568 came after adoption. The bot wrote 4,408 comments, and 1,408 comments on merged PRs were examined. Data collection ran from Aug 2023 to 20 Sep 2024. — [arXiv 2412.18531](https://arxiv.org/html/2412.18531v2)
- Resolution: 73.8% of bot comments had the thread status "Resolved" and 21.3% had "Won't Fix". By project, the Resolved share was 55% (Project 1) and 90% (Project 3). Caveat: a company resolution policy was announced on 24 May 2024, so "Resolved" is a status developers set, not a verified code change. — [arXiv 2412.18531](https://arxiv.org/html/2412.18531v2)
- PR closure time rose overall from 5h 52m to 8h 20m (p<0.001):

  | Project | Before | After |
  |---|---|---|
  | 1 | 2h48m | 4h38m |
  | 2 | 6h06m | 3h07m (a decrease) |
  | 3 | 20h22m | 30h51m |

  The paper's own Conclusion contradicts this ("50 minutes before and 48 minutes after"). — [arXiv 2412.18531](https://arxiv.org/html/2412.18531v2)
- The bot averaged 3.65 comments per PR. Human comments per PR went from 0.31 to 0.28, which is not significant. — [arXiv 2412.18531](https://arxiv.org/html/2412.18531v2)
- Survey of 22 consenting respondents:
  - Code quality: 14 saw a "minor improvement".
  - Development speed: 8 minor improvement, 4 no effect, 3 minor deterioration, 2 major improvement.
  - Reported problems: out-of-scope or irrelevant suggestions, over-reliance (reviewers assuming the bot catches things), and recursive re-reviews ("With each fix, a new review is generated").
  - Cost: about 3,937 tokens, roughly $0.48, per PR.
  - [arXiv 2412.18531](https://arxiv.org/html/2412.18531v2)

#### "Does AI Code Review Lead to Code Changes? A Case Study of GitHub Actions" (Sun, Kuang, Baltes, Zhou, Zhang, Ma, Rong, Shao, Treude; arXiv 2508.18771, v1 Aug 2025, v2 25 Apr 2026) [PREPRINT; independent academics]
- Scope: 16 AI review GitHub Actions and 178 "mature" repos (at least 50 PRs). 22,326 AI review comments across 3,002 PRs. 13 of the 16 actions use OpenAI models. — [arXiv 2508.18771v2](https://arxiv.org/html/2508.18771v2)
- Adoption:
  - 37.1% of mature repos declared an action but never produced a comment.
  - 82.6% customized parameters. The most common customization was "prompt context augmentation", used by 70.1% of customizing repos.
  - [arXiv 2508.18771v2](https://arxiv.org/html/2508.18771v2)
- Addressed rate for valid comments, judged by an LLM:

  | Reviewer | Level | Addressed | n |
  |---|---|---|---|
  | anc95/ChatGPT-CodeReview | file | 4.2% | 2,831 |
  | mattzcarey/code-review-gpt | file | 0.9% | 773 |
  | coderabbitai/ai-pr-reviewer (early open-source action) | hunk | 19.2% | 713 |
  | aidar-freeed/ai-codereviewer | hunk | 6.5% | 169 |
  | Human reviewers | — | 60.0% | 1,166 |

  [arXiv 2508.18771v2](https://arxiv.org/html/2508.18771v2)
- Comments followed by no change to the file: 65.3% overall, 87.0% for file-level AI comments, 51.9% for hunk-level AI comments, and 8.2% for human comments. Of 30 sampled PR-level AI comments, only 1 was even partially addressed. — [arXiv 2508.18771v2](https://arxiv.org/html/2508.18771v2)
- Factors linked to a comment being addressed:
  - Hunk-level placement.
  - Manual trigger: 14.4% vs 9.0% overall (not significant), but significant for 2 tools (12.8% vs 6.8%, and 22.2% vs 0.5%).
  - Share of code in the comment: 4.2% when there is no code, 23.2% when the code ratio is 0.52–1.00.
  - Shorter text.
  - Less-experienced authors: 16.1% for authors with 30 or fewer prior commits, 3.3% for those with more than 1,013.
  - Model: GPT-4 comments 12.6% vs GPT-3.5 5.4%, but LLM choice ranked low in feature importance.
  - [arXiv 2508.18771v2](https://arxiv.org/html/2508.18771v2)
- In 50 developer replies to unaddressed AI comments, 64% were "defending the change". — [arXiv 2508.18771v2](https://arxiv.org/html/2508.18771v2)
- The authors attribute the best tool's 19.2% to three things: hunk-level comments, a long, detailed prompt (over 400 words), and suppression of "LGTM" comments. — [arXiv 2508.18771v2](https://arxiv.org/html/2508.18771v2)
- Incremental behaviour: 11 of 16 actions re-review the whole base-to-latest diff on every run. Only 3 track which commits were already reviewed. — [arXiv 2508.18771v2](https://arxiv.org/html/2508.18771v2)
- Method validity: the two-stage LLM classifier (gpt-4.1 judging validity, o3-mini judging whether the comment was addressed) reached 91.5% accuracy on "valid & addressed vs other". Human inter-rater κ was 0.674–0.764. — [arXiv 2508.18771v2](https://arxiv.org/html/2508.18771v2)

#### CodeRabbit in open source — "Is Agentic Code Review Helpful? Mining Developers' Feedback to CodeRabbit Reviews in the Wild" (Lin, Liang, Thongtanunam, Tantithamthavorn; arXiv 2607.03316, v1 3 Jul 2026, v2 23 Jul 2026) [PREPRINT; independent of CodeRabbit; one co-author also co-authored Atlassian's RovoDev paper]
- Data: 31,073 review–feedback pairs from 10,191 PRs in 239 GitHub repos. — [arXiv 2607.03316](https://arxiv.org/abs/2607.03316)
- Outcomes: 36.4% of CodeRabbit comments were accepted, 7.3% triggered discussion, and 56.3% were rejected. — [arXiv 2607.03316](https://arxiv.org/abs/2607.03316)
- Rejection reasons: invalid suggestions (false positives, redundant, out of scope) and misalignment with developer intent or coding practices. — [arXiv 2607.03316](https://arxiv.org/abs/2607.03316)
- Agentic reviews focus more on functional concerns than on evolvability, but are more likely to be invalid. Lightweight learned models predict rejection with up to 76% F1. — [arXiv 2607.03316](https://arxiv.org/abs/2607.03316)

#### "Human-AI Synergy in Agentic Code Review" (Zhong, Noei, Zou, Adams; arXiv 2603.15911, v1 16 Mar 2026, v3 30 Oct 2026) [PREPRINT; independent]
- Data: 278,790 review conversations across 300 OSS projects. — [arXiv 2603.15911](https://arxiv.org/abs/2603.15911)
- Findings:
  - AI-agent suggestions were adopted at a significantly lower rate than human suggestions. The abstract gives no exact rate.
  - Over half of unadopted AI suggestions were incorrect or were handled by the developer through an alternative fix.
  - Adopted AI suggestions increased code complexity and size significantly more than human suggestions did.
  - Humans gave more feedback on understanding, testing, and knowledge transfer.
  - Human reviewers exchanged 11.8% more rounds when reviewing AI-generated code.
  - [arXiv 2603.15911](https://arxiv.org/abs/2603.15911)

#### "From Industry Claims to Empirical Reality: An Empirical Study of Code Review Agents in Pull Requests" (Chowdhury et al.; arXiv 2604.03196, 3 Apr 2026; MSR 2026) [PEER-REVIEWED]
- Data: 3,109 PRs, drawn from the 19,450 in AIDev, an agent-authored PR dataset. — [arXiv 2604.03196](https://arxiv.org/abs/2604.03196)
- PRs reviewed only by code review agents merged 45.20% of the time, against 68.37% for human-reviewed PRs (−23.17 pp), and were abandoned more often. — [arXiv 2604.03196](https://arxiv.org/abs/2604.03196)
- 60.2% of closed agent-only PRs fell in the 0–30% "signal" range. 12 of 13 review agents had an average signal ratio below 60%. Caveat: observational and confounded, since PRs that received only bot review may differ systematically. — [arXiv 2604.03196](https://arxiv.org/abs/2604.03196)

#### Mozilla + Ubisoft RevMate — "Impact of LLM-based Review Comment Generation in Practice" (Olewicki, …, Castelluccio, Habchi, Khomh, Adams; arXiv 2411.07091, 11 Nov 2024) [BACKGROUND][PREPRINT]
- Design: an off-the-shelf LLM with RAG for code and review context, plus an LLM-as-judge filter that discards irrelevant comments. The study covered more than 587 patch reviews. — [arXiv 2411.07091](https://arxiv.org/abs/2411.07091)
- Acceptance: 8.1% of generated comments at Mozilla and 7.2% at Ubisoft. A further 14.6% and 20.5% were marked as valuable tips but not accepted. — [arXiv 2411.07091](https://arxiv.org/abs/2411.07091)
- Refactoring comments were accepted far more often (18.2% and 18.6%) than functional ones (4.8% and 5.2%). — [arXiv 2411.07091](https://arxiv.org/abs/2411.07091)
- Cost and effect: reviewers spent a median of 43 seconds extra per patch. Accepted comments led to later revisions about as often as human comments (74% vs 73%, chunk-level). — [arXiv 2411.07091](https://arxiv.org/abs/2411.07091)
- Conflicting figures: Ubisoft's own post (5 Sep 2025) reports a 28.3% "appreciation ratio" and a survey of 22 of 31 participants [SECONDARY]. The arXiv v1 HTML reportedly gives 23% and 28.3% for "appreciated" comments. — [Ubisoft La Forge](https://www.ubisoft.com/en-us/studio/laforge/news/3SsR9KkpyUCBvy1Wyw3lTS/impact-of-an-llm-based-code-review-assistant-in-practice); [Mozilla Foundation summary](https://www.mozillafoundation.org/en/research/library/impact-of-llm-based-review-comment-generation-in-practice-a-mixed-open-closed-source-user-study/)

#### Ericsson — "Automated Code Review Using LLMs at Ericsson: An Experience Report" (Ramesh, Bose, …, Britto; arXiv 2507.19115, v2 31 Jul 2025; ICSME 2025 industry track) [PEER-REVIEWED industry report, very small sample]
- Approach: Code LLaMA / LLaMA 2 (7B and 13B), given the enclosing method extracted by static analysis as context. — [arXiv 2507.19115](https://arxiv.org/html/2507.19115v2); [ICSME 2025 program](https://conf.researchr.org/details/icsme-2025/icsme-2025-industry-track/6/Automated-Code-Review-At-Ericsson-Using-Large-Language-Models-An-Experience-Report)
- Expert ratings (8 experts, 24 comment ratings): 6 positive, 8 neutral, 10 negative. That is about 25%, 33%, and 42%, computed from Table I. — [arXiv 2507.19115](https://arxiv.org/html/2507.19115v2)
- Field trial (9 developers, 15 days): 4 of 9 agreed it saved time. Reported failure modes were that reviews just explained the code (4), focused on irrelevant areas (3), or were factually incorrect (2). — [arXiv 2507.19115](https://arxiv.org/html/2507.19115v2)
- Lesson: simple "review this code" prompts performed poorly. Prompts needed constraints for brevity, a ban on generated code, and focus on the enclosing method. — [arXiv 2507.19115](https://arxiv.org/html/2507.19115v2)

### Inferences
- The biggest determinant of whether AI comments get acted on is engineering around the model, not the model itself:
  - First-generation wrapper actions: 0.9–19.2% addressed.
  - Engineered systems: 36–65% on their own proxies.
  - Within the GitHub Actions study, GPT-4 vs GPT-3.5 mattered less than comment granularity and code content.
- Humans address 44–60% of human review comments on the stricter proxies: 60% in OSS, 44.45% at Atlassian, 51% at Uber. A realistic target for a good AI reviewer is therefore parity with human comments, not 90%+. Rates near 74–80% usually come from lenient proxies (thread status, vendor LLM judges).
- Cycle-time claims are fragile. The one study with project-level breakdown (Beko) found opposite effects across projects. Google's randomized A/B test found no significant change. The large positive effects (Atlassian −30.8%, Microsoft −10–20%) are observational or self-reported.
- In OSS, "AI-only review" correlates with worse PR outcomes (45% vs 68% merge rate). This supports positioning AI review as a complement or first pass, not a replacement.
- Developer resistance mostly targets out-of-scope, redundant, or invalid comments. Precision, scope discipline, and alignment with team practice are the main levers.

### Gaps
- I did not retrieve the WirelessCar study ("Rethinking Code Review Workflows with LLM Assistance", arXiv 2505.16339).
- No retrieved field study isolates the effect of AI review on post-merge defect escape rates, apart from Meta RADAR's revert and incident ratios (Key Question 2).
- The exact adoption-rate gap between AI and human suggestions in arXiv 2603.15911 is not in the abstract.
- The study period of the CodeRabbit study (2607.03316) is not stated in the abstract.
- A study of GPT-assisted PRs (arXiv 2508.11034; 25,473 PRs) reportedly finds merge time correlating with a drop from 23 to 9 hours [SECONDARY]. It concerns ChatGPT-assisted authoring, not review bots, and was not verified.

## Key Question 2 — Industrial deployment reports: key metrics, and what companies had to build to get there (filtering, grading, dedup)

### Takeaway
Every company that publishes numbers reports the same arc. Raw single-shot LLM review was noisy: ByteDance's precision was about 25%, Greptile's comments were about 79% nits, and Uber's single-shot output had hallucinated and duplicate issues. Acceptable quality came only after adding post-generation verification or grading, category suppression, semantic dedup, and feedback loops. Mature systems report useful or addressed rates of roughly 40–80% (proxies vary). Productivity effects range from none (Google A/B) to −30.8% median PR cycle time (Atlassian). Meta's randomized trial showed AI suggestions can slow reviewers by more than 5% unless the UX is changed.

### Cited Findings

#### Uber — uReview (Engineering blog, 12 Aug 2025) [INDUSTRY SELF-REPORT]
- Pipeline:
  1. A prefilter drops config files, generated code, and experimental directories.
  2. Three generator "assistants": Standard (bugs, exception handling, logic), Best Practices (Uber style-rule registry), and AppSec.
  3. A grading prompt assigns a confidence score, with thresholds per assistant, per language, and per category.
  4. Semantic-similarity dedup.
  5. A category classifier suppresses categories "with historically low developer value".
  6. Inline delivery with Useful / Not Useful buttons.
  - [Uber blog](https://www.uber.com/us/en/blog/ureview/)
- Metrics:
  - Usefulness above 75%.
  - On average 65% of comments addressed in the same changeset, vs 51% for human-written comments.
  - Covers over 90% of about 65,000 diffs per week. The post also says 65,000 "per month", which is an internal inconsistency.
  - Median latency 4 minutes in CI.
  - Claimed about 1,500 hours saved per week ("nearly 39 developer years annually").
  - [Uber blog](https://www.uber.com/us/en/blog/ureview/)
- How "addressed" is measured: uReview is re-run 5 times on the final commit. A comment counts as addressed if no re-run reproduces a semantically similar comment. — [Uber blog](https://www.uber.com/us/en/blog/ureview/)
- Model selection: the best configuration was Claude-4-Sonnet as generator with OpenAI o4-mini-high as grader. Using GPT-4.1 as grader instead scored 4.5 points lower. — [Uber blog](https://www.uber.com/us/en/blog/ureview/)
- Why in-house: third-party tools showed "many false positives, low-value true positives" and required GitHub, while Uber uses Phabricator. — [Uber blog](https://www.uber.com/us/en/blog/ureview/)
- Lessons:
  - "Precision over volume".
  - Single-shot prompting produced "hallucinated issues, duplicate suggestions, and inconsistent quality".
  - Readability nits, logging tweaks, low-impact performance changes, and style "consistently received poor ratings".
  - Correctness bugs, missing error handling, and best-practice violations (especially with doc links) were well received.
  - The tool is "much better at catching bugs" than at judging design, because it lacks past PRs, feature flags, schemas, and docs.
  - [Uber blog](https://www.uber.com/us/en/blog/ureview/)

#### Atlassian — RovoDev Code Reviewer (Tantithamthavorn et al., arXiv 2601.01129, Jan 2026; ICSE-SEIP 2026) [PEER-REVIEWED; industry self-evaluation]
- Scale: 12 months of general availability (Jun 2024–Jun 2025), about 54,000 comments (2.1 per PR), and more than 1,900 repos (the paper also says "over 2,000"). Model: Claude 3.5 Sonnet, zero-shot. — [arXiv 2601.01129](https://arxiv.org/html/2601.01129v2); [ICSE-SEIP 2026](https://conf.researchr.org/details/icse-2026/icse-2026-software-engineering-in-practice/2/RovoDev-Code-Reviewer-A-Large-Scale-Online-Evaluation-of-LLM-based-Code-Review-Autom)
- Code resolution rate: 38.70% for RovoDev comments vs 44.45% for human comments (12.9% lower in relative terms), measured over 10–15 Jul 2025. — [arXiv 2601.01129](https://arxiv.org/html/2601.01129v2)
- Workflow:
  - Median PR cycle time 14.35 h with RovoDev comments vs 20.73 h without (−30.8%, p<.001).
  - Human comments per PR 2.87 vs 4.45 (−35.6%).
  - An interrupted time-series analysis supports the cycle-time effect.
  - Atlassian's blog repeats the 30.8% and 35.6% figures.
  - [arXiv 2601.01129](https://arxiv.org/html/2601.01129v2); [Atlassian blog](https://www.atlassian.com/blog/ai-at-work/developer-productivity-improved-with-rovo-dev)
- What they built, and what helped:
  - A ModernBERT "actionability" gate, trained on more than 50,000 comments labelled by whether they led to resolution. It improved human alignment by 20 pp (location only) and 15 pp (location plus semantics).
  - An LLM-as-judge factual-correctness check had "minimal impact".
  - Review guidelines in the prompt added about 5 pp. Persona, chain-of-thought, PR info, and Jira info each added about 1–3 pp.
  - Context enrichment gave minimal improvement.
  - [arXiv 2601.01129](https://arxiv.org/html/2601.01129v2)
- Offline: only 7% of PRs contained at least one human-aligned RovoDev comment. Engineers rarely used thumbs up or down, so explicit feedback was sparse. — [arXiv 2601.01129](https://arxiv.org/html/2601.01129v2)

#### ByteDance — BitsAI-CR (Sun et al., arXiv 2501.15134, 25 Jan 2025; FSE 2025 industry track) [PEER-REVIEWED; industry self-report]
- Architecture:
  - Diff hunks are expanded to function boundaries with tree-sitter.
  - RuleChecker, a fine-tuned LLM, checks against a taxonomy of 219 rules covering Go, JS, TS, Python, and Java.
  - ReviewFilter, a second fine-tuned LLM, makes a yes/no call to remove hallucinated or incorrect comments.
  - Embedding-based dedup.
  - A "data flywheel" of likes and dislikes, daily manual precision sampling, and weekly Outdated Rate.
  - [arXiv 2501.15134](https://arxiv.org/html/2501.15134v1); [FSE 2025](https://conf.researchr.org/details/fse-2025/fse-2025-industry-papers/24/BitsAI-CR-Automated-Code-Review-via-LLM-in-Practice)
- Precision:
  - Overall precision was about 25% before the taxonomy and two-stage design.
  - Online, RuleChecker went from 27.9% to 62.6% and ReviewFilter from 35.6% to a 75% peak. The abstract's 75.0% figure matches this peak.
  - Offline, RuleChecker scored 57.03% alone and 65.59% with ReviewFilter. Without the taxonomy it scored 16.83% and 30.92%.
  - Generic LLMs scored 7.65–10.62% offline.
  - [arXiv 2501.15134](https://arxiv.org/html/2501.15134v1)
- Reasoning format: "Conclusion-First" output reached 77.09% precision at 1.7 s per sample. "Reasoning-First" reached 65.80% at 31.0 s. — [arXiv 2501.15134](https://arxiv.org/html/2501.15134v1)
- Outdated Rate (flagged lines later modified), Go: peaked at 26.7% by week 18, after underperforming rules were removed. The human baseline is 35–46%. — [arXiv 2501.15134](https://arxiv.org/html/2501.15134v1)
- Rules are decommissioned using criteria of about 25%±5% Outdated Rate and about 65%±5% precision over 14 days. — [arXiv 2501.15134](https://arxiv.org/html/2501.15134v1)
- Adoption:
  - More than 12k weekly active users and 210k weekly page views.
  - Retention 61.64% in week 2 and about 48% at week 8.
  - 74.5% (102 of 137) of surveyed users affirmed value.
  - 11 of 12 interviewed experts asked for customizable rules.
  - [arXiv 2501.15134](https://arxiv.org/html/2501.15134v1)

#### Google — AutoCommenter, best-practice comments (Vijayvergiya et al., arXiv 2405.13565, May 2024; AIware 2024) [BACKGROUND][INDUSTRY SELF-REPORT]
- Rollout: about 3k volunteers from Jul 2022, an A/B test with half of all developers in Jul 2023, and general availability from Oct 2023. — [arXiv 2405.13565](https://arxiv.org/html/2405.13565v1)
- Useful ratio:
  - Plateaued at about 54% from developer feedback.
  - Suppressing 17 non-actionable best-practice URLs raised it to 66% (developers) and 74% (raters).
  - Further URL suppression and rewritten summaries reached the 80% target.
  - [arXiv 2405.13565](https://arxiv.org/html/2405.13565v1)
- Filtering:
  - The initial confidence threshold was 0.98, but about 80% of predictions below it were still correct, so it was replaced by per-URL thresholds.
  - 80% of greedy-decoded comments fell on unmodified lines and were filtered out.
  - Outdated rules were suppressed with regex filters instead of retraining.
  - [arXiv 2405.13565](https://arxiv.org/html/2405.13565v1)
- Estimated resolution rate was about 40%: the comment was absent in the next snapshot 50% of the time, and 80% of those were real fixes. — [arXiv 2405.13565](https://arxiv.org/html/2405.13565v1)
- The Jul 2023 A/B test found no statistically significant change in review duration or in iterations. — [arXiv 2405.13565](https://arxiv.org/html/2405.13565v1)
- Coverage: 68% of historical human best-practice-URL comments. 66% (33 of 50) of the top URLs go beyond traditional static analysis. — [arXiv 2405.13565](https://arxiv.org/html/2405.13565v1)

#### Google — ML-suggested edits that resolve reviewer comments (blog 23 May 2023; ICSE-SEIP 2024 paper) [BACKGROUND][INDUSTRY SELF-REPORT]
- Tuned for 50% target precision. Offline, it addresses 52% of comments at that precision. Online, about 50% of relevant comments exceed the confidence threshold. — [Google Research blog](https://research.google/blog/resolving-code-review-comments-with-ml/)
- Usage: reviewer preview rate went from about 20% to about 40% after a "Show ML-edit" button was added, and 40–50% of previewed edits are applied. — [Google Research blog](https://research.google/blog/resolving-code-review-comments-with-ml/)
- Authors address 7.5% of all reviewer comments by applying an ML-suggested edit (paper abstract). An earlier program listing said "almost 5%". [SECONDARY for the 7.5% figure] — [Google paper page](https://research.google/pubs/resolving-code-review-comments-with-machine-learning/); [ICSE 2024 listing](https://conf.researchr.org/details/icse-2024/icse-2024-software-engineering-in-practice/35/Resolving-Code-Review-Comments-with-Machine-Learning)

#### Meta — MetaMateCR, AI fixes for reviewer comments (Maddila et al., arXiv 2507.13499, 17 Jul 2025; FSE 2026 industry track) [INDUSTRY SELF-REPORT]
- Training: 64k pairs of review comment and patch, used to fine-tune Llama. The internal model produced exact-match patches 68% of the time, 9 pp above GPT-4o. — [arXiv 2507.13499](https://arxiv.org/abs/2507.13499); [FSE 2026](https://conf.researchr.org/details/fse-2026/fse-2026-industry-papers/16/AI-Assisted-Fixes-to-Code-Review-Comments-at-Scale)
- Randomized safety trial: showing AI patches to reviewers made reviews take more than 5% longer. After the UX was changed to show patches only to authors, there was no regression. — [arXiv 2507.13499](https://arxiv.org/abs/2507.13499)
- Production: the ActionableToApplied rate was 19.7%, 9.2 pp above GPT-4o. — [arXiv 2507.13499](https://arxiv.org/abs/2507.13499)

#### Meta — RADAR, risk-aware automated review and landing of low/medium-risk diffs (arXiv 2605.30208, v1 28 May 2026, v2 12 Jun 2026) [PREPRINT; industry self-report]
- Context: lines of code per human-landed diff grew 105.9% year over year, and diffs per developer rose 51%. Agentic AI accounts for more than 80% of that growth. — [arXiv 2605.30208](https://arxiv.org/abs/2605.30208)
- Funnel: authorship/source classification, eligibility gates, static heuristics, an ML Diff Risk Score, LLM review, and deterministic validation. — [arXiv 2605.30208](https://arxiv.org/abs/2605.30208)
- Results:
  - 535K+ diffs reviewed and 331K+ landed.
  - Median review wall time −35%.
  - Median time to close reduced by "over 330%", an odd metric to check in the full paper.
  - Revert rate one-third, and production incident rate one-fiftieth, of non-RADAR diffs.
  - Relaxing the risk threshold from the 25th to the 50th percentile raised the approve rate to 60.31%.
  - [arXiv 2605.30208](https://arxiv.org/abs/2605.30208)

#### Microsoft — internal AI reviewer (Engineering@Microsoft blog, 14 Jul 2025) [INDUSTRY SELF-REPORT]
- Coverage: more than 90% of PRs company-wide and more than 600K PRs per month. In early experiments, 5,000 onboarded repos saw "10 – 20% median PR completion time improvements". — [Microsoft blog](https://devblogs.microsoft.com/engineering-at-microsoft/enhancing-code-quality-at-scale-with-ai-powered-code-reviews/)
- Design: categorized comments (e.g., exception handling, null check, sensitive data) and suggested fixes that the author must explicitly apply ("the author remains in control"). Also repo-specific guidelines and custom prompts, and Q&A inside the PR thread. Learning from feedback is listed only as future work. — [Microsoft blog](https://devblogs.microsoft.com/engineering-at-microsoft/enhancing-code-quality-at-scale-with-ai-powered-code-reviews/)

#### OpenAI — Codex code review ("A Practical Approach to Verifying Code at Scale", 1 Dec 2025) [VENDOR CLAIM / CoI]
- Explicit "precision over recall". The team accepted "modestly reduced recall in exchange for high signal quality and developer trust". It frames each comment's value with a utility formula: benefit if correct, minus verification cost, minus false-alarm cost. Stylistic comments may have negative utility. — [OpenAI](https://openai.com/safety-alignment/scaling-code-verification/)
- Giving GPT-5 repository access and code execution produced fewer false alarms and more critical catches than diff-only review. Precision and recall can be steered with AGENTS.md. — [OpenAI](https://openai.com/safety-alignment/scaling-code-verification/)
- Metrics:
  - Comments on 36% of PRs generated entirely by Codex cloud. 46% of those comments led to a code change, vs 53% on human PRs.
  - 52.7% of comments addressed with a code change in deployment.
  - More than 100k external PRs per day (Oct 2025).
  - More than 80% of reactions positive.
  - [OpenAI](https://openai.com/safety-alignment/scaling-code-verification/)

#### Anthropic — Claude Code "Code Review" managed product (blog 9 Mar 2026) [VENDOR CLAIM / CoI]
- Design: agents "look for bugs in parallel, verify bugs to filter out false positives, and rank bugs by severity". Large changes get more agents and trivial ones a light pass. The product never approves PRs. — [Claude blog](https://claude.com/blog/code-review)
- Internal metrics:
  - PRs with substantive review comments rose from 16% to 54%.
  - "Less than 1% of findings are marked incorrect".
  - PRs over 1,000 lines: 84% get findings, averaging 7.5 issues. PRs under 50 lines: 31%, averaging 0.5.
  - About 20 minutes per review, typically $15–25.
  - [Claude blog](https://claude.com/blog/code-review)

#### GitHub — Copilot code review ("60 million Copilot code reviews and counting", 5 Mar 2026) [VENDOR CLAIM / CoI]
- Scale: more than 1 in 5 code reviews on GitHub, and more than 12,000 organizations auto-reviewing every PR. — [GitHub blog](https://github.blog/ai-and-ml/github-copilot/60-million-copilot-code-reviews-and-counting/)
- Quality metrics:
  - 71% of reviews surface actionable feedback. In 29% "the agent says nothing at all" ("Silence is better than noise").
  - About 5.1 comments per review on average.
  - The agentic redesign gave +8.1% positive feedback.
  - A reasoning model gave +6% positive feedback at +16% latency.
  - [GitHub blog](https://github.blog/ai-and-ml/github-copilot/60-million-copilot-code-reviews-and-counting/)
- Online A/B test of a multi-model ensemble (GitHub ReviewBench post, 5 Oct 2026): addressed rate +8.0%, recall +13.6%, comment volume +61%, cost −8.0%. — [GitHub ReviewBench post](https://github.blog/ai-and-ml/github-copilot/reviewbench-an-open-benchmark-for-ai-code-review/)

#### Cursor — Bugbot ("Building a better Bugbot", 15 Jan 2026; "Bugbot learning", 8 Apr 2026) [VENDOR CLAIM / CoI]
- Original pipeline:
  1. 8 parallel passes, each with a randomized diff order.
  2. Bucket similar bugs together.
  3. Majority vote, dropping bugs found in only one pass.
  4. Merge each bucket into one description.
  5. Filter unwanted categories (compiler warnings, documentation errors).
  6. A validator model catches false positives.
  7. Dedupe against bugs posted in previous runs.
  - [Cursor blog](https://cursor.com/blog/building-bugbot)
- Results: 40 experiments. Resolution rate (LLM-judged at merge) went from 52% to over 70%. Bugs per run went from 0.4 to 0.7, and resolved bugs per PR from about 0.2 to about 0.5. The largest gain came from the agentic redesign in fall 2025, which needed more aggressive prompting because the agent was "too cautious". Scale: more than 2M PRs per month. — [Cursor blog](https://cursor.com/blog/building-bugbot)
- Later: "learned rules" built from reactions, replies, and bugs flagged by human reviewers that Bugbot missed. More than 110,000 repos have learning enabled, producing more than 44,000 rules. The resolution rate is "nearing 80%" (78% in the Apr 2026 changelog). — [Cursor blog](https://cursor.com/blog/bugbot-learning); [Cursor changelog](https://cursor.com/changelog/04-08-26)

#### Greptile — "How to Make LLMs Shut Up" (Daksh Gupta, 18 Dec 2024) [BACKGROUND][VENDOR CLAIM / CoI]
- Of the comments analysed, about 19% were good, 2% incorrect, and 79% nits. — [Greptile blog](https://greptile.com/blog/make-llms-shut-up)
- What failed:
  - Prompting could not cut nits without also cutting critical comments.
  - Few-shot examples made output worse.
  - LLM severity self-rating (1–10, dropping scores below 7) was "nearly random" and slow.
  - [Greptile blog](https://greptile.com/blog/make-llms-shut-up)
- What worked: per-team embeddings of past comments labelled addressed, upvoted, or downvoted. A new comment is blocked if it is similar to at least 3 downvoted comments. The address rate went from 19% to "55+%" within two weeks. — [Greptile blog](https://greptile.com/blog/make-llms-shut-up)

### Inferences
- The common "minimum viable architecture" across Uber, ByteDance, Atlassian, Cursor, and Google is:
  1. Prefilter files.
  2. Generate comments, ideally per category or per rule.
  3. Verify, grade, or classify, with per-category thresholds.
  4. Semantic dedup, including against earlier runs.
  5. Suppress low-value categories using feedback history.
  6. Measure addressed rate automatically.
- The verification step pays off most when it is trained or calibrated on real outcome data: ByteDance's fine-tuned ReviewFilter, Atlassian's ModernBERT gate trained on resolution labels, Greptile's feedback embeddings, and Uber's per-category thresholds. Generic LLM self-assessment was reported as weak by Greptile ("nearly random") and Atlassian ("minimal impact").
- Industrial UX matters as much as model quality. Meta's RCT shows AI output shown to the wrong person slowed reviews by more than 5%. Google's preview rate doubled with a single button. Microsoft keeps the author in control of applying fixes.
- At hyperscalers, the frontier is moving from "AI comments" to risk-tiered automation (Meta RADAR) as AI-written code volume grows. Review capacity, not comment quality, is becoming the constraint.

### Gaps
- No independent audit exists of any vendor's internal metrics: Anthropic's <1% incorrect, Cursor's 78–80%, GitHub's 71%, and OpenAI's 52.7%.
- Meta MetaMateCR: the trial sample sizes and the definition of "ActionableToApplied" are only in the full paper, which was not read.
- Microsoft: no acceptance or usefulness rate is published, and the methodology behind the 10–20% figure is unclear.
- Uber: inconsistent weekly vs monthly diff counts.
- Atlassian: inconsistent dogfooding dates (Aug 2024 vs Aug 2025) inside the paper.

## Key Question 3 — Code-review benchmarks: what they show, how open-source tools score, and methodological weaknesses and vendor bias

### Takeaway
Independent academic benchmarks show low absolute performance on real PRs:
- SWR-Bench: best F1 about 19%, or about 22% with aggregation.
- AACR-Bench: F1 about 5–16%.
- "Bigger Isn't Always Better": F1 0.066 on real PRs vs 0.847 on synthetic bugs.

Results are highly sensitive to diff size, context configuration, and ground-truth completeness. Vendor benchmarks are small (50–118 bugs), self-designed and self-run, often ignore false positives, and "every vendor … wins their own". Re-running Greptile's set gave Greptile 45% instead of 82%. The two more neutral leaderboards (Martian's online bench and GitHub's open ReviewBench) disagree with each other and with the vendors. The open-source PR-Agent's review component was the best of five approaches in SWR-Bench, yet still scored F1 of only about 19%.

### Cited Findings

#### Academic benchmarks (2025–2026)
- **SWR-Bench** (Zeng et al., arXiv 2509.01494; v1 1 Sep 2025, v2 5 Jun 2026; listed in the FSE 2026 research track) [PEER-REVIEWED]:
  - 1,000 manually verified PRs (500 with issues, 500 clean) from 12 Python projects aligned with SWE-Bench, reviewed with full repository context.
  - The LLM judge agreed with humans 89.2–94.9% of the time on "hit" decisions.
  - [arXiv 2509.01494](https://arxiv.org/abs/2509.01494); [FSE 2026](https://conf.researchr.org/details/fse-2026/fse-2026-research-papers/78/SWR-Bench-Assessing-LLM-Performance-in-Real-World-Code-Review-Comment-Generation)
- SWR-Bench results, mean across LLMs:

  | Approach | Precision | Recall | F1 |
  |---|---|---|---|
  | PR-Review (PR-Agent's review component) | 15.39 | 24.06 | **18.73** |
  | LLM-Review | 9.22 | 20.39 | 12.49 |
  | SWR-Agent | 9.11 | 20.93 | 12.61 |
  | CR-Agent | 6.23 | 18.10 | 9.22 |
  | Hybrid-Review | 2.79 | 20.04 | 4.87 |

  - Best single configuration: PR-Review with Gemini-2.5-Pro, F1 19.38 (precision 16.65).
  - On functional issues, PR-Review reached recall 43.89 and F1 23.87.
  - [arXiv 2509.01494v1](https://arxiv.org/html/2509.01494v1)
- SWR-Bench, other findings:
  - Functional defects are detected better: Larger Defects F1 27.65, Logic 26.20, vs documentation-type issues at 6–8.
  - Only 27 change-points overlapped across 5 runs of the same LLM.
  - Self-aggregation over 10 runs raised F1 to 21.91% (+43.67%) and recall by +118.83% with Gemini-2.5-Flash.
  - Claude-4-Opus and Claude-4-Sonnet underperformed Claude-3.7-Sonnet.
  - [arXiv 2509.01494v1](https://arxiv.org/html/2509.01494v1)
- **AACR-Bench** (Zhang et al., Nanjing Univ. + Alibaba; arXiv 2601.19494, v3 30 Jan 2026) [PREPRINT]:
  - 200 PRs and 1,505 ground-truth comments, across 50 repos in 10 languages.
  - Context retrieval "is not universally beneficial". For Claude-4.5-Sonnet, F1 fell from 14.46 (no context) to 9.98 (BM25).
  - Agent mode (Claude Code driving retrieval) gave much higher precision (39.90% vs 8.70%) but far lower recall (10.10% vs 42.86%), with 0.08–0.15 comments per patch.
  - GPT-5.2 collapsed in agent mode (precision 9.90%, recall 2.99%).
  - Non-agent methods degrade from diff-level to file-level to repo-level issues, while agents show the inverse.
  - [arXiv 2601.19494](https://arxiv.org/html/2601.19494)
- **ContextCRBench** (Hu et al., arXiv 2511.07017; v1 10 Nov 2025, v2 30 Dec 2025; listed in the FSE 2026 industry track) [PEER-REVIEWED]:
  - 67,910 entries filtered from 153.7K issues and PRs.
  - Three tasks: hunk-level quality assessment, line-level defect localization, and line-level comment generation.
  - 8 LLMs evaluated. Textual context (issue/PR descriptions) yields bigger gains than code context alone. LLMs remain "far from human-level".
  - At ByteDance it served as the reward signal for a self-evolving reviewer, with +61.98% relative improvement (0.2375 to 0.3847).
  - [arXiv 2511.07017](https://arxiv.org/abs/2511.07017); [arXiv HTML](https://arxiv.org/html/2511.07017v1)
- **"Bigger Isn't Always Better"** (Kumar, Bararia, Raj; arXiv 2606.15689, 9 Apr 2026) [PREPRINT; small n=150]:
  - Claude Haiku 4.5 beat Claude Sonnet 4.6 (F1 0.365 vs 0.343) at 3.2x lower cost.
  - The best model scored F1 0.066 on real PRs vs 0.847 on synthetic mutation bugs, a 92% drop.
  - Diff size is the dominant predictor: F1 0.657 for diffs under 10 lines vs 0.043 for diffs over 150 lines.
  - Recall on performance bugs was near zero.
  - The main result was cross-checked on Martian's benchmark.
  - [arXiv 2606.15689](https://arxiv.org/abs/2606.15689)
- **CodeFuse-CR-Bench** (arXiv 2509.14856): 601 instances from 70 Python projects. No single LLM dominates all aspects of code review, and LLMs differ in robustness to redundant context. [SECONDARY, from search snippet] — [arXiv 2509.14856](https://arxiv.org/html/2509.14856v1)
- **CodeReviewQA** (Lin et al., arXiv 2503.16167; ACL 2025 Findings) [PEER-REVIEWED]:
  - 900 manually verified examples in 9 languages, used to evaluate 72 LLMs.
  - Splits review comprehension into three probes: change-type recognition, localisation, and solution identification.
  - Designed to resist data contamination. It exposes weaknesses hidden by generative refinement scores.
  - [ACL Anthology](https://aclanthology.org/2025.findings-acl.476); [arXiv 2503.16167](https://arxiv.org/html/2503.16167v2)
- **CRScore** (Naik, Alenius, Fried, Rose; NAACL 2025) [PEER-REVIEWED]:
  - A reference-free review-quality metric grounded in LLM "claims" and static-analysis "smells". 82.6% of its pseudo-references are correct.
  - Spearman correlation about 0.54 with human judgments, the best of the metrics compared, vs BLEU-style metrics.
  - Released with 2.9k human annotations.
  - [ACL Anthology](https://aclanthology.org/2025.naacl-long.457)
- **Microsoft CodeReviewer dataset** (Li et al., 2022) [BACKGROUND]:
  - The standard training and evaluation set for comment generation. Prior work found about 32% of its test-set comments are noise (vague or non-actionable).
  - LLM-based cleaning identified valid comments with 66–85% precision. Training on the cleaned set (25–66% smaller) did not hurt, and produced more informative comments ("Too Noisy To Learn", Liu, Lin, Thongtanunam, arXiv 2502.02757, Feb 2025).
  - This undermines BLEU-on-CodeReviewer results as evidence of real-world review quality.
  - [arXiv 2502.02757](https://arxiv.org/html/2502.02757v2); [CodeReviewer, arXiv 2203.09095](https://arxiv.org/abs/2203.09095)

#### Neutral-ish public leaderboards (2026)
- **Martian Code Review Bench** (launched Feb 2026; data, judge prompts, and pipeline open-sourced under MIT) [SECONDARY for most details]. Martian claims independence ("does not train models or sell coding tools").
  - Online track: measures what developers changed after bot comments on fresh public PRs. Precision is the share of suggestions matched by later changes; recall is the share of post-review fixes the bot had flagged.
  - Offline track: 50 PRs from the same 5 repos as Greptile's benchmark, with 136 (another source says 173) golden comments.
  - Martian reportedly said offline results diverged from real-world use and made online the headline metric.
  - [Greptile post on Martian](https://www.greptile.com/content-library/greptile-martian-code-review-benchmark); [The New Stack](https://thenewstack.io/github-reviewbench-code-review/)
- Martian online snapshot of 30 Jul 2026, as published by Greptile, a vendor [VENDOR-REPORTED snapshot]:

  | Tool | F1 | Precision | Recall |
  |---|---|---|---|
  | Greptile | 60.8% | 76.2% | 50.6% |
  | ChatGPT Codex Connector | 59.4% | 73.3% | 50.0% |
  | Cubic | 58.7% | 72.6% | 49.3% |
  | Devin | 58.6% | 73.6% | 48.6% |
  | CodeRabbit | 57.5% | 64.9% | 51.6% |

  [Greptile post](https://www.greptile.com/content-library/greptile-martian-code-review-benchmark)
- Other Martian snapshots:
  - CodeRabbit claimed first place with 51.2% F1 in Mar 2026. [VENDOR]
  - Qodo claimed 64.3% F1 at one point. [VENDOR]
  - In Oct 2026, The New Stack reported Cubic first with 64.9% F1 and Copilot fourth at 60.9%. [SECONDARY, page not fetched: HTTP 403]
  - Being listed reportedly requires several hundred public reviews.
  - [CodeRabbit JP blog](https://www.coderabbit.ai/ja/blog/coderabbit-tops-martian-code-review-benchmark); [Qodo blog](https://www.qodo.ai/blog/qodo-ranked-1-ai-code-review-tool-in-martians-code-review-benchmark); [The New Stack](https://thenewstack.io/github-reviewbench-code-review/)
- **GitHub ReviewBench** (5 Oct 2026; built by GitHub/Microsoft but open) [VENDOR-BUILT, CoI]:
  - 219 PRs from 187 repos in 19 languages.
  - Golden findings were assembled from human reviews, follow-up commits, deterministic tools, and multiple frontier LLMs, then deduplicated. A finding counts only if "true, relevant, and non-trivial".
  - Independent senior engineers agreed with the labels 96.6% of the time. The judge is Claude Sonnet 5.
  - "Grounded" metrics use only gold labels. "Augmented" metrics also credit valid novel findings.
  - [GitHub blog](https://github.blog/ai-and-ml/github-copilot/reviewbench-an-open-benchmark-for-ai-code-review/)
- ReviewBench leaderboard: Copilot code review ("Balanced") is first at 40.1% grounded F1. GitHub ran the competitors' initial tests itself. [SECONDARY] — [The New Stack](https://thenewstack.io/github-reviewbench-code-review/); [DevX](https://www.devx.com/coding/what-is-reviewbench-ai-code-review-benchmark/)

#### Vendor benchmarks [all VENDOR CLAIM / CoI]
- **Greptile** (Jul 2025): 50 real bugs reintroduced into PRs on forks of Sentry, Cal.com, Grafana, Keycloak, and Discourse.
  - "Caught" means a line-level comment that identifies the bug and explains its impact.
  - Catch rates: Greptile 82%, Bugbot 58%, Copilot 54%, CodeRabbit 44%, Graphite 6%.
  - False positives explicitly "did not affect the catch rate", and no noise data were published.
  - Severity tables do not reconcile with the case tables.
  - [Greptile benchmarks](https://www.greptile.com/benchmarks)
- **Augment** (post references GPT-5.2): the same 50 PRs, with golden comments "expanded and corrected". Judge method undisclosed. Note that Codex has higher precision than Augment, despite Augment's "highest precision" claim.

  | Tool | Precision | Recall | F-score |
  |---|---|---|---|
  | Augment | 65 | 55 | 59 |
  | Cursor Bugbot | 60 | 41 | 49 |
  | Greptile | 45 | 45 | 45 |
  | Codex | 68 | 29 | 41 |
  | CodeRabbit | 36 | 43 | 39 |
  | Claude Code | 23 | 51 | 31 |
  | GitHub Copilot | 20 | 34 | 25 |

  [Augment blog](https://www.augmentcode.com/blog/we-benchmarked-7-ai-code-review-tools-on-real-world-prs-here-are-the-results)
- **Qodo** (2026): 100 merged PRs with 580 injected issues, across 8 repos and 7 languages. LLM judge.
  - Qodo F1 60.1%; later production figures of 79% precision and 60% recall.
  - "Most tools cluster toward high precision and low recall."
  - Ground truth is synthetic (LLM-injected).
  - [Qodo benchmark page](https://qodo.ai/ai-code-review-benchmark/); [DeepSource analysis](https://deepsource.com/blog/ai-code-review-benchmarks)
- **Cursor's cross-product table** (8 Apr 2026): resolution rate on public repos, judged by an LLM, for PRs analysed per tool. Judge accuracy and the time window are not disclosed.

  | Tool | Resolution rate | PRs analysed |
  |---|---|---|
  | Bugbot | 78.13% | 50,310 |
  | Greptile | 63.49% | 11,419 |
  | CodeRabbit | 48.96% | 33,487 |
  | Copilot | 46.69% | 24,336 |
  | Codex | 45.07% | 19,384 |
  | Gemini Code Assist | 30.93% | 21,031 |

  [Cursor blog](https://cursor.com/blog/bugbot-learning)
- **DeepSource meta-critique** (26 Feb 2026; DeepSource discloses "We have skin in this game"):
  - "Every vendor that has published one wins their own."
  - Datasets are small (50–118 bugs), with a single-bug framing, synthetic or LLM-generated ground truth, unpublished ground truth (Qodo), and metrics that are not comparable (recall vs F1 vs detection rate).
  - Augment's rerun of Greptile's repos scored Greptile "45%, not 82%".
  - Also lists Macroscope (118 bugs, 45 repos, 8 languages, 48% detection), Entelligence (67 bugs, 47.2% F1), and Propel (64% F1 on Augment's dataset).
  - [DeepSource](https://deepsource.com/blog/ai-code-review-benchmarks)

#### Where open-source tools have been measured
- **PR-Agent** (Qodo's open-source tool):
  - SWR-Bench: best of 5 approaches, with mean F1 18.73 and functional recall 43.89. [arXiv 2509.01494v1](https://arxiv.org/html/2509.01494v1)
  - Beko field study: 73.8% of comments had the "Resolved" status (lenient proxy). [arXiv 2412.18531](https://arxiv.org/html/2412.18531v2)
- **Open-source GitHub Actions**: addressed rates of 0.9–19.2%. The best was the early open-source coderabbitai/ai-pr-reviewer at 19.2%. [arXiv 2508.18771v2](https://arxiv.org/html/2508.18771v2)
- **Claude Code used as a general agent reviewer**:
  - Augment's vendor run: precision 23 / recall 51 / F 31. [Augment](https://www.augmentcode.com/blog/we-benchmarked-7-ai-code-review-tools-on-real-world-prs-here-are-the-results)
  - AACR-Bench agent mode: precision 39.90 / recall 10.10 / F1 16.12. [arXiv 2601.19494](https://arxiv.org/html/2601.19494)

### Inferences
- Benchmark numbers vary roughly 10x depending on design:
  - Real PRs with complete golden sets: F1 about 5–25%.
  - Curated single-bug sets: catch rates of 40–82%.
  - Online "developer acted on it" leaderboards: F1 about 50–65%.
  - Synthetic injected bugs: up to about 85% F1.
  - Absolute numbers should never be compared across benchmarks. Within-benchmark rankings are also unstable: Greptile is 82% on its own set and 45% on Augment's version of the same set.
- Fixed golden sets punish valid novel findings, which artificially lowers precision. This is why ReviewBench added "augmented" metrics and AACR-Bench warns about incomplete ground truth. Online acted-upon metrics reward tools that comment on easy, acceptable things. Both biases should be stated when citing numbers.
- Recurring signals across independent benchmarks:
  - Functional and logic defects are found better than documentation, performance, and design issues.
  - Run-to-run variance is high, so sampling multiple times and aggregating helps.
  - Large diffs are dramatically harder.
  - Agentic and retrieval setups trade recall for precision in model-dependent ways.
  - Bigger or newer models are not reliably better (Haiku 4.5 > Sonnet 4.6; Claude 3.7 > Claude 4 in SWR-Bench).
- For an open-source agent, the most defensible evaluation is an internal resolution or addressed-rate metric with a human-comment baseline, plus a small held-out bug set. Vendor leaderboards should not be relied on.

### Gaps
- I could not access Martian's live leaderboard page (codereview.withmartian.com returned only a title). No Martian results for PR-Agent or other open-source/self-hosted reviewers were found.
- ReviewBench's per-tool table was not in the GitHub blog text. The 40.1% figure is from secondary sources.
- Augment's post date was not captured, and its judge method is undisclosed.
- Qodo's exact per-competitor table is in images only.
- No benchmark measures the noise cost per PR (false positives per review) consistently across tools.

## Key Question 4 — Design lessons: what architecture and practices the evidence supports

### Takeaway
The evidence converges on these practices:
1. Precision-first behaviour, including staying silent.
2. A generate → verify/grade → dedupe → suppress-by-category pipeline, or an agentic reviewer that verifies its own hypotheses.
3. Multiple samples with voting or aggregation to beat run-to-run variance.
4. Filters learned from real developer outcomes (addressed, reactions, replies) rather than generic LLM self-scoring.
5. Explicit rules, taxonomies, or convention files.
6. Targeted context (task/issue text, enclosing code, agent-fetched repo context) rather than blanket retrieval.
7. Concise, hunk-level comments that carry code.
8. Dedup across pushes.

Bugs, correctness, error handling, and security are where LLM reviewers earn acceptance. Style, nits, docs, low-impact performance, PR-level summaries, and architecture/design are where they fail.

### Cited Findings

#### A. Precision-first, comment budgets, and silence
- OpenAI chose "modestly reduced recall in exchange for high signal quality and developer trust", using a utility formula in which false alarms carry an explicit cost. Stylistic comments may have negative utility. — [OpenAI](https://openai.com/safety-alignment/scaling-code-verification/)
- GitHub: "Silence is better than noise". 29% of Copilot reviews post nothing, and "Our goal isn't to maximize comment volume". — [GitHub blog](https://github.blog/ai-and-ml/github-copilot/60-million-copilot-code-reviews-and-counting/)
- Uber: "precision over volume", delivering "fewer but more useful comments". — [Uber](https://www.uber.com/us/en/blog/ureview/)
- ByteDance: "Prioritizing precision over recall helps build early user trust". — [arXiv 2501.15134](https://arxiv.org/html/2501.15134v1)
- Counter-evidence that over-restriction hurts:
  - Cursor's agent became "too cautious" and had to be prompted to "err on the side of flagging". Bugs per run rose from 0.4 to 0.7 without a comparable rise in false positives. — [Cursor](https://cursor.com/blog/building-bugbot)
  - Qodo notes most tools "cluster toward high precision and low recall". — [Qodo](https://qodo.ai/ai-code-review-benchmark/)
- Budget scaling with PR size: Anthropic adds agents for large PRs (84% of PRs over 1,000 lines get findings, averaging 7.5 issues; 31% of PRs under 50 lines, averaging 0.5). — [Claude blog](https://claude.com/blog/code-review)
- Typical comment volumes: Atlassian 2.1 per PR, Beko 3.65 per PR, GitHub about 5.1 per review. — [arXiv 2601.01129](https://arxiv.org/html/2601.01129v2); [arXiv 2412.18531](https://arxiv.org/html/2412.18531v2); [GitHub](https://github.blog/ai-and-ml/github-copilot/60-million-copilot-code-reviews-and-counting/)

#### B. Generate → verify/grade → dedupe → suppress pipelines
- Uber: generator, then a grader with per-assistant, per-language, per-category thresholds, then semantic dedup, then a category classifier that suppresses low-value categories. — [Uber](https://www.uber.com/us/en/blog/ureview/)
- ByteDance: RuleChecker, then ReviewFilter, then embedding dedup.
  - ReviewFilter raised precision in every configuration (offline 57.03% → 65.59%).
  - Online overall precision went from about 25% to 75%.
  - Outputting the decision before the rationale ("Conclusion-First", 77.09%) beat "Reasoning-First" (65.80%) and was 18x faster.
  - [arXiv 2501.15134](https://arxiv.org/html/2501.15134v1)
- Cursor (pre-agentic): 8 passes, majority vote, merge, category filter, validator model, dedupe against previous runs. — [Cursor](https://cursor.com/blog/building-bugbot)
- Atlassian: a learned actionability gate (ModernBERT) gave +15–20 pp human alignment, while an LLM-judge factual check had "minimal impact". — [arXiv 2601.01129](https://arxiv.org/html/2601.01129v2)
- Greptile: LLM self-rated severity filtering was "nearly random", while feedback-embedding filtering lifted the address rate from 19% to 55%+. — [Greptile](https://greptile.com/blog/make-llms-shut-up)
- Uber: grader model choice matters. An o4-mini-high grader beat GPT-4.1 by 4.5 points. — [Uber](https://www.uber.com/us/en/blog/ureview/)
- Google AutoCommenter: filter comments on unmodified lines (80% of raw comments) and suppress non-actionable rule URLs. The useful ratio went from 54% to 66–74%, then to 80%. — [arXiv 2405.13565](https://arxiv.org/html/2405.13565v1)

#### C. Multi-pass sampling, voting, and aggregation
- Cursor: 8 parallel passes with randomized diff order plus majority voting were "among the most effective early quality gains". — [Cursor](https://cursor.com/blog/building-bugbot)
- SWR-Bench: only 27 change-points overlapped across 5 runs of the same LLM. Self-aggregation over 10 runs raised F1 by up to 43.67% and recall by 118.83%. — [arXiv 2509.01494v1](https://arxiv.org/html/2509.01494v1)
- Uber uses 5 re-runs to decide whether a comment was addressed, because single runs are nondeterministic. — [Uber](https://www.uber.com/us/en/blog/ureview/)
- GitHub's lite-tier multi-model ensemble: addressed rate +8.0%, recall +13.6%, cost −8.0% in an online A/B test. — [GitHub ReviewBench post](https://github.blog/ai-and-ml/github-copilot/reviewbench-an-open-benchmark-for-ai-code-review/)

#### D. Multi-agent and agentic review, with confidence thresholds
- Anthropic's open-source Claude Code code-review plugin (official page):
  - Multiple specialized agents in parallel: CLAUDE.md compliance, bug detection, git-history context, previous PR comments, and code-comment verification.
  - Each finding gets a 0–100 confidence score, and only findings at or above 80 (the default, configurable) are posted.
  - It skips closed, draft, automated, or already-reviewed PRs, and links to code with full SHA and line ranges.
  - Third-party analyses describe 4 agents instead (2 for CLAUDE.md compliance, 1 bug detector, 1 history analyzer), so the agent count differs by version. [partly SECONDARY]
  - [Claude plugin page](https://claude.com/plugins/code-review); [instagit analysis](https://instagit.com/anthropics/claude-code/code-review-confidence-scoring-claude-code)
- Anthropic's managed Code Review: parallel bug-finding agents, a verification step "to filter out false positives", and severity ranking. Under 1% of findings are marked incorrect (vendor claim). — [Claude blog](https://claude.com/blog/code-review)
- Cursor: the largest gains came from switching to a fully agentic design, where the agent decides where to dig deeper. "Tool design had an outsized impact". More context moved from static to dynamic, pulled in at runtime. — [Cursor](https://cursor.com/blog/building-bugbot)
- GitHub: the agentic architecture (tool calls to gather repo context, memory across reviews, planning for long PRs, reading linked issues and PRs) gave +8.1% positive feedback. — [GitHub](https://github.blog/ai-and-ml/github-copilot/60-million-copilot-code-reviews-and-counting/); [GitHub changelog](https://github.blog/changelog/2026-03-05-copilot-code-review-now-runs-on-an-agentic-architecture/)
- AACR-Bench caution: agent mode gave much higher precision but much lower recall, and was strongly model-dependent (GPT-5.2 collapsed). — [arXiv 2601.19494](https://arxiv.org/html/2601.19494)

#### E. Context strategies (diff-only vs RAG vs code graph/AST vs agentic exploration)
- Diff-only is weakest for deep issues. OpenAI found repo access plus code execution gave fewer false alarms and more critical catches than diff-only. — [OpenAI](https://openai.com/safety-alignment/scaling-code-verification/)
- Uber attributes weak design and architecture review to missing context: past PRs, feature flags, schemas, docs. — [Uber](https://www.uber.com/us/en/blog/ureview/)
- Textual intent beats more code: in ContextCRBench, issue and PR descriptions gave larger gains than code context. — [arXiv 2511.07017](https://arxiv.org/abs/2511.07017)
- Blanket retrieval can hurt:
  - AACR-Bench: BM25 retrieval cut Claude-4.5-Sonnet's F1 from 14.46 to 9.98, and the best retrieval method differs by model and language. — [arXiv 2601.19494](https://arxiv.org/html/2601.19494)
  - Atlassian: context enrichment gave minimal improvement, and Jira and PR info added only about 1–3 pp. — [arXiv 2601.01129](https://arxiv.org/html/2601.01129v2)
- AST/structural expansion of hunks:
  - ByteDance expands hunks to function boundaries with tree-sitter. — [arXiv 2501.15134](https://arxiv.org/html/2501.15134v1)
  - Ericsson extracts the enclosing method by static analysis. — [arXiv 2507.19115](https://arxiv.org/html/2507.19115v2)
  - Uber adds nearby functions, class definitions, and imports. — [Uber](https://www.uber.com/us/en/blog/ureview/)
- Code graph: CodeRabbit builds a dependency graph on each review and assembles a multi-source context (graph, linked tickets, CI, learnings). It claims fewer false positives, but there is no public ablation. [VENDOR CLAIM; partly SECONDARY] — [CodeRabbit blog](https://coderabbit.ai/blog/context-engineering-ai-code-reviews); [CodeRabbit docs](https://docs.coderabbit.ai/integrations/code-graph-analysis)
- Augment credits its "Context Engine" for benchmark wins, without retrieval-specific metrics. [VENDOR CLAIM] — [Augment](https://www.augmentcode.com/blog/we-benchmarked-7-ai-code-review-tools-on-real-world-prs-here-are-the-results)
- Diff size dominates: F1 0.657 for diffs under 10 lines vs 0.043 for diffs over 150 lines. This argues for chunking or decomposing large PRs and scaling effort with PR size. — [arXiv 2606.15689](https://arxiv.org/abs/2606.15689)

#### F. Learning from reviewer feedback
- Cursor's learned rules: reactions (downvotes), replies explaining errors, and human-reviewer comments on bugs Bugbot missed become candidate rules. Rules are promoted to active, or disabled after consistent negative signal. More than 110k repos and 44k rules; resolution rate about 78–80%. — [Cursor](https://cursor.com/blog/bugbot-learning)
- Greptile: per-team vector memory of addressed, upvoted, and downvoted comments. A new comment is blocked when similar to at least 3 downvoted ones. Address rate went from 19% to 55%+. — [Greptile](https://greptile.com/blog/make-llms-shut-up)
- Atlassian: a classifier trained on whether past comments led to resolution, because explicit thumbs feedback was too sparse. — [arXiv 2601.01129](https://arxiv.org/html/2601.01129v2)
- Google: only about 10% of review comments and about 2% of IDE diagnostics got explicit feedback, so outcome-based signals (the comment disappearing in the next snapshot) are needed. — [arXiv 2405.13565](https://arxiv.org/html/2405.13565v1)
- ByteDance runs a data flywheel (likes and dislikes, daily precision sampling, weekly Outdated Rate) and decommissions rules that underperform for 14 days. — [arXiv 2501.15134](https://arxiv.org/html/2501.15134v1)
- Uber suppresses categories with historically low developer value, using Useful/Not Useful ratings streamed to Hive. — [Uber](https://www.uber.com/us/en/blog/ureview/)
- Rejection is predictable from comment features (up to 76% F1 for CodeRabbit comments), which supports a pre-posting rejection classifier. — [arXiv 2607.03316](https://arxiv.org/abs/2607.03316)

#### G. Rules, conventions, and taxonomies
- ByteDance: removing the 219-rule taxonomy dropped RuleChecker precision from 57.03% to 16.83%. 11 of 12 experts wanted customizable rules. — [arXiv 2501.15134](https://arxiv.org/html/2501.15134v1)
- Atlassian: review guidelines were the single most useful prompt component, at about 5 pp. — [arXiv 2601.01129](https://arxiv.org/html/2601.01129v2)
- Convention files are used for scope and invariants:
  - Anthropic's plugin dedicates agents to CLAUDE.md compliance. — [Claude plugin page](https://claude.com/plugins/code-review)
  - OpenAI steers precision and recall through AGENTS.md. — [OpenAI](https://openai.com/safety-alignment/scaling-code-verification/)
  - Cursor uses "Bugbot rules" for codebase-specific invariants. — [Cursor](https://cursor.com/blog/building-bugbot)
  - Microsoft supports repo-specific guidelines and custom prompts. — [Microsoft](https://devblogs.microsoft.com/engineering-at-microsoft/enhancing-code-quality-at-scale-with-ai-powered-code-reviews/)
  - Uber has a Best Practices assistant backed by a style-rule registry. — [Uber](https://www.uber.com/us/en/blog/ureview/)
- In open source, 70.1% of repos that customized an AI review action added prompt context, and the best-performing action used a prompt of over 400 words. — [arXiv 2508.18771v2](https://arxiv.org/html/2508.18771v2)
- Rule hygiene: Google had to suppress outdated rules (e.g., a Python imports guideline changed in 2022) and non-actionable rule links. — [arXiv 2405.13565](https://arxiv.org/html/2405.13565v1)
- Uber recommends leaving simple syntactic checks to linters and using LLMs for semantic rules. — [Uber](https://www.uber.com/us/en/blog/ureview/)

#### H. Incremental review across pushes
- 11 of 16 open-source review actions re-review the entire diff on each push. Only 3 track already-reviewed commits. — [arXiv 2508.18771v2](https://arxiv.org/html/2508.18771v2)
- Beko developers complained "With each fix, a new review is generated". — [arXiv 2412.18531](https://arxiv.org/html/2412.18531v2)
- Mitigations:
  - Cursor dedupes against bugs posted in previous runs. — [Cursor](https://cursor.com/blog/building-bugbot)
  - Anthropic's plugin skips already-reviewed PRs. — [Claude plugin page](https://claude.com/plugins/code-review)
  - GitHub keeps memory across reviews and clusters repeated patterns into one unit. — [GitHub](https://github.blog/ai-and-ml/github-copilot/60-million-copilot-code-reviews-and-counting/)
  - Uber reviews every commit in CI (median 4 minutes) and re-runs on the final commit to decide which comments were addressed. — [Uber](https://www.uber.com/us/en/blog/ureview/)

#### I. Which comment categories work vs fail
- **Work (accepted, detected):**
  - Correctness bugs, missing error handling, and best-practice violations with doc links. — [Uber](https://www.uber.com/us/en/blog/ureview/)
  - Functional defects: logic and larger defects have the highest F1 in SWR-Bench. — [arXiv 2509.01494v1](https://arxiv.org/html/2509.01494v1)
  - Null checks, exception handling, sensitive data, and API-ordering bugs. — [Microsoft](https://devblogs.microsoft.com/engineering-at-microsoft/enhancing-code-quality-at-scale-with-ai-powered-code-reviews/)
  - Semantic best practices that linters cannot catch (66% of AutoCommenter's top rules). — [arXiv 2405.13565](https://arxiv.org/html/2405.13565v1)
  - Concise, code-bearing, hunk-level comments. — [arXiv 2508.18771v2](https://arxiv.org/html/2508.18771v2)
- **Fail (ignored, poorly rated, or poorly detected):**
  - Readability nits, logging tweaks, low-impact performance, and style. — [Uber](https://www.uber.com/us/en/blog/ureview/)
  - Nits made up 79% of an unfiltered bot's output. — [Greptile](https://greptile.com/blog/make-llms-shut-up)
  - Documentation-type issues (F1 6–8). — [arXiv 2509.01494v1](https://arxiv.org/html/2509.01494v1)
  - Performance bugs (recall near zero). — [arXiv 2606.15689](https://arxiv.org/abs/2606.15689)
  - PR-level summary comments (1 of 30 addressed). — [arXiv 2508.18771v2](https://arxiv.org/html/2508.18771v2)
  - Design and architecture, for lack of context. — [Uber](https://www.uber.com/us/en/blog/ureview/)
  - Code explanations instead of critique (Ericsson). — [arXiv 2507.19115](https://arxiv.org/html/2507.19115v2)
- **Nuance and conflicts:**
  - At Mozilla and Ubisoft, refactoring comments were accepted more often (about 18%) than functional ones (about 5%), likely because functional claims were more often wrong. — [arXiv 2411.07091](https://arxiv.org/abs/2411.07091)
  - CodeRabbit's agentic comments focus on functional concerns but are more often invalid. — [arXiv 2607.03316](https://arxiv.org/abs/2607.03316)
  - Lesson: functional and bug comments carry the most value only when precision is high.
  - Humans give more feedback than AI on understanding, testing, and knowledge transfer. — [arXiv 2603.15911](https://arxiv.org/abs/2603.15911)

#### J. Workflow and UX
- Show AI fixes to authors, not reviewers: in Meta's RCT, showing them to reviewers made reviews more than 5% slower, and showing them to authors only caused no regression. — [arXiv 2507.13499](https://arxiv.org/abs/2507.13499)
- Discoverability: Google's preview rate doubled from 20% to 40% with a "Show ML-edit" button. — [Google Research blog](https://research.google/blog/resolving-code-review-comments-with-ml/)
- Manual triggers saw higher addressed rates for some tools (22.2% vs 0.5% for one action). — [arXiv 2508.18771v2](https://arxiv.org/html/2508.18771v2)
- Never auto-approve:
  - Anthropic: "It won't approve PRs". — [Claude blog](https://claude.com/blog/code-review)
  - Over-reliance risk was flagged by both OpenAI and Beko. — [OpenAI](https://openai.com/safety-alignment/scaling-code-verification/); [arXiv 2412.18531](https://arxiv.org/html/2412.18531v2)
  - Meta's RADAR auto-lands only low-risk, risk-scored diffs behind deterministic validation. — [arXiv 2605.30208](https://arxiv.org/abs/2605.30208)
- Cost and latency trade-offs:
  - GitHub accepted +16% latency for +6% positive feedback. — [GitHub](https://github.blog/ai-and-ml/github-copilot/60-million-copilot-code-reviews-and-counting/)
  - A cheaper model (Haiku 4.5) beat a larger one at 3.2x lower cost. — [arXiv 2606.15689](https://arxiv.org/abs/2606.15689)
  - Beko: about $0.48 per PR (GPT-4 era). Anthropic managed review: $15–25 per review. — [arXiv 2412.18531](https://arxiv.org/html/2412.18531v2); [Claude blog](https://claude.com/blog/code-review)

#### K. Measuring success
- Recommended primary metric: the resolution or addressed rate, computed automatically. Each source uses a different detector:
  - Cursor: an LLM judge at merge time, spot-checked with authors. — [Cursor](https://cursor.com/blog/building-bugbot)
  - Uber: 5 re-runs. — [Uber](https://www.uber.com/us/en/blog/ureview/)
  - ByteDance: Outdated Rate. — [arXiv 2501.15134](https://arxiv.org/html/2501.15134v1)
  - Greptile: the comment is addressed between the first and last commit. — [Greptile](https://greptile.com/blog/make-llms-shut-up)
- Always compare against a human-comment baseline on the same proxy. Measured baselines: 51% (Uber), 44.45% (Atlassian), 60% (OSS), and 35–46% Outdated Rate (ByteDance). — [Uber](https://www.uber.com/us/en/blog/ureview/); [arXiv 2601.01129](https://arxiv.org/html/2601.01129v2); [arXiv 2508.18771v2](https://arxiv.org/html/2508.18771v2); [arXiv 2501.15134](https://arxiv.org/html/2501.15134v1)
- Use an offline set of known bugs for regression testing (Cursor's BugBench, Uber's curated benchmark), and roll out gradually per team or assistant with dashboards. — [Cursor](https://cursor.com/blog/building-bugbot); [Uber](https://www.uber.com/us/en/blog/ureview/)

### Inferences
- Design implications for an open-source review agent, ranked by strength of evidence:
  1. Add a post-generation verification or filtering stage, tuned to real outcomes, and suppress categories with low acceptance. Evidence: ByteDance 25% → 75% precision; Google 54% → 80% useful; Greptile 19% → 55% addressed; Atlassian +15–20 pp.
  2. Restrict output to changed lines and hunks, keep it concise, include code, never post PR-level filler or "LGTM", and allow silence.
  3. Sample multiple times, vote or aggregate, or use an agent that verifies its own hypotheses.
  4. Support convention or rule files and a category taxonomy.
  5. Track the addressed rate automatically, use it as the north-star metric against a human baseline, and feed it back into suppression or learned rules.
  6. Dedupe across pushes.
  7. Treat context as targeted and agent-pulled (PR/issue intent text plus enclosing code, with repo exploration on demand) rather than bulk RAG, which can lower F1.
- Generic "LLM-as-judge" filtering is not a reliable fix on its own. Its value depends on calibration or fine-tuning: it helped at ByteDance and Uber and failed at Greptile and Atlassian. Learned filters based on real developer outcomes have the most consistent evidence.
- Agentic exploration improves precision but can collapse recall. Cursor and AACR-Bench both show that prompting toward thoroughness and choosing the right model are necessary.
- LLM reviewers should be positioned as bug, correctness, and security screeners that complement humans on design, testing, and knowledge transfer. Style should be offloaded to linters and formatters.

### Gaps
- No controlled, independent ablation compares code-graph context, embedding RAG, and agentic exploration on the same review benchmark. Evidence is split between AACR-Bench (no code-graph arm) and vendor claims.
- The exact contents and agent count of Anthropic's open-source plugin are inconsistent between the official page (five review angles) and third-party analyses (four agents). The raw command file could not be fetched: GitHub returned 404 and API rate limits blocked access.
- Few sources quantify comment budgets (max comments per PR) as a lever. Most report only averages.
- Long-term effects (reviewer skill atrophy, over-reliance, effects on knowledge sharing) are only qualitative. The Beko survey says 9 respondents saw no effect on knowledge sharing and 8 a positive one.
- No source gives security-specific acceptance rates for LLM review comments. DeepSource's CVE benchmark is vendor-run, and its scores are not in its article text.
