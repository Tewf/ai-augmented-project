# Protocol: how the pool was built

A first pass of a multivocal literature review to Garousi 2019, run on 2026-11-02 by one reviewer. Terms are in [frame](frame.md).

**Shape:** [protocol](https://github.com/Tewf/reader-ergonomics-review/blob/a7f405f26f14cd188291e2a86b630121c4302a94/shapes/protocol.md)

## 1. Why grey literature

Garousi's seven questions, answered for this topic.

| Question | Answer |
|---|---|
| Is the context broader than academic? | yes: the practice is set by vendors and projects |
| Is the practice ahead of the research? | yes: instruction files existed before any study of them |
| Do practitioners hold the data? | yes: surveys and vendor documentation |
| Are the formal sources thin? | yes: the studies on context files date from 2025 and 2026 |
| Is the topic contested? | yes: speed results disagree |
| Does practice need a baseline? | yes: this review ends on one |
| Do formal sources miss the form? | yes: the file formats are specified in documentation |

## 2. Questions

- Q1 decisions: which are the person's, which the machine's?
- Q2 session start: what must a model be handed, and how short?
- Q3 memory: how is it kept, who writes it, how is it audited?
- Q4 measure: what is counted to say a setup works?
- Q5 checks: what does a program decide before a person reads?

## 3. Existing reviews (Garousi guideline 2)

- Found: a meta-analysis of 106 experiments (Vaccaro 2024) and a scoping review of human-AI teaming (Berretta 2023).
- Also found: a survey of 124 papers on agents for software engineering (Liu 2024b), a survey of agent memory (Luo 2026) and a survey of test oracles (Barr 2015).
- Not found: a review of the effect of agent context files, or of the audit of an agent's memory.

## 4. Formal search

Databases without a key or an account: OpenAlex (counts, `title_and_abstract.search`) and the arXiv API. No email or identity was sent.

| Id | String as run | OpenAlex | arXiv |
|---|---|---|---|
| F1 | "human-AI teaming" | 1,261 | not run |
| F2 | "human-AI teaming" AND (survey OR review) | 273 | not run |
| F3 | "complementary performance" | 560 | not run |
| F4 | "complementary performance" AND (human OR AI) | 71 | not run |
| F5 | "hybrid intelligence" | 2,099 | not run |
| F6 | "hybrid intelligence" AND (human OR AI) | 1,303 | not run |
| F7 | "human-AI collaboration" AND "systematic review" | 386 | not run |
| F8 | "AI-assisted software engineering" OR "AI for software engineering" AND survey | 9 | not run |
| F9 | "AGENTS.md" | 151 | 32 with CLAUDE.md and cursor rules |
| F10 | "context files" AND "coding agents" | not run | 6 |
| F11 | "coding agent" AND harness | 439 | 489 (harness, scaffolding) |
| F12 | "context engineering" | 681 | not run |
| F13 | randomized trial of developers using AI tools | not run | 4 |
| F14 | SWE-agent | not run | 26 |
| F15 | memory of LLM agents, survey | not run | 10 |
| F16 | memory of agents with audit | not run | 9 |
| F17 | clarifying questions in code generation | not run | 1 |
| F18 | LLM-based agents for software engineering, survey | not run | 5 |
| F19 | human-AI interaction guidelines, mixed-initiative | not run | 89 |
| F20 | self-repair with test feedback | not run | 1 |

- Backward snowball from Vaccaro 2024, Bansal 2021 and Gloaguen 2026: Amershi 2019, Parasuraman 2000, Horvitz 1999, Barr 2015 and Olausson 2024 were added by name and checked in OpenAlex.
- Forward snowball: not run, for the first pass.

## 5. Grey search

- Producers visited: the agent-file convention's site, three vendors' documentation, one vendor's engineering pages, one research programme, one developer survey, one practitioner blog.
- Web searches: two (instruction-file practice; developer survey on trust). Results seen: about 24. Included from them: 2.
- Not searched: forums, Q/A sites, talks, videos, patents, social media, books.

## 6. Stopping rule

- Effort bounded: top 5 results per string for formal strings, the producers named above for grey.
- Saturation: a string stopped after 5 consecutive results that added no concept. F9 and F10 returned the same context-file studies, so no further string was run on them.

## 7. Selection

- Include: studies or documents about setting a model to work with a person on software, or the field's concept for it.
- Exclude: security attacks on agents, several-agent systems, benchmarks of models alone, tutorials without data.
- Quality: formal sources carry an evidence grade; grey sources are scored in section 8.

## 8. Quality of grey sources

Garousi's 20 criteria, scored 1, 0.5 or 0 and summed in eight groups: authority 4, methodology 6, objectivity 4, date 1, position 1, novelty 2, impact 1, outlet 1. The threshold is 10 of 20. Scores are in [sources](sources.md).

## 9. Extraction and synthesis

Each source was read at the level [sources](sources.md) states. Numbers were taken from the paper where read in full or in part, and marked (secondary) where read from an abstract or a summary. Synthesis is narrative by question.

## 10. Limits

- One reviewer and one model rater on the grey scores. The rater agreed poorly with the review before the reread (section 12); the review's grey scores are still one person's judgment, now checked against the source text.
- Most numbers come from abstracts. Only the sources marked read in the text were checked in the paper.
- Preprints of 2026 are not peer reviewed.
- Search engines change; counts are those of 2026-11-02 (first pass) and 2026-11-03 (forward pass).

## 11. Forward pass, 2026-11-03

The three sources the review cites most, counted in [review](review.md): Vaccaro 2024 (4 mentions), Gloaguen 2026 (3) and Anthropic 2026b (3). OpenAlex was queried with requests paced at one per second.

| Source | Index and string | Counted | Screened | Added |
|---|---|---|---|---|
| Vaccaro 2024 | OpenAlex W4403839497, doi 10.1038/s41562-024-02024-1; `filter=cites:W4403839497` | 597 citing works | 200 by title (the top 200 by citation count), all titles read; then `title.search` on teaming, complementar, synerg, meta-analys, systematic review, team: 54 titles read; abstracts read for about 20 candidates | 5 |
| Gloaguen 2026 | OpenAlex W7128774696, arXiv 2602.11988; `filter=cites:W7128774696` | 2 citing works | both titles and abstracts read | 0 |
| Anthropic 2026b | none | not indexed | not searched | 0 |

- Gloaguen's two citers are a routing-policy paper for coding agents and a single-agent memory system. Neither changes a finding in the review.
- Anthropic 2026b is a vendor documentation page. It has no DOI and no citation index. An OpenAlex full-text query for "CLAUDE.md agent memory" returned 183 works; they mention the term and were not screened as citers of the page. The page was not forward-searched.
- The Vaccaro citers are many and mostly applied (health, marketing, education). The five added are those whose abstracts change or sharpen a finding in review.md:

| Added | Work | Screened number (abstract, so secondary) | Finding it sharpens |
|---|---|---|---|
| Ngo 2025 | meta-analysis of 146 experiments, healthcare and public sectors | augmentation g = 0.622; synergy g = -0.380; publication bias favours augmentation | Q1, the synergy result |
| Liu 2025e | 52 clinical studies | teaming mode: simultaneous beats sequential; juniors gain more | Q1, the team against the person |
| Nassiri 2026 | 15 studies, N = 15,752 | intelligence tasks d = +0.41; choice tasks d = -0.28 | Q1, tasks that decide |
| Dell'Acqua 2026 | 758 workers, 18 tasks, preregistered | inside the frontier: 12.2% more tasks, 25.1% faster; one task outside: 19% less likely to be correct | Q4, speed against quality |
| Tretow 2025 | 42 studies, 101 effect sizes, preprint | g = 0.22 (95% CI 0.18 to 0.27) | Q1, the size of the gain in a clinical setting |

- Dropped at screening: surveys and viewpoints with no number, for example "Better off alone?" (a viewpoint with no data, so a convention at most).
- Tretow 2025's abstract gives a search window that runs past its own DOI date. The window is not checked; its numbers are used with that caveat.
- The pool is now 44 against the first-pass target of 40 in the rules: the brief asked for up to five forward works, and five were added. This is noted, not resolved.

## 12. Second rater on the grey sources, 2026-11-03

### Rater and material

A second model, prompted blind, one source per call: nine calls, all answered on the first try. The prompt pasted Garousi 2019's twenty criteria in their eight groups and the scoring rules of the review. It gave only the source text, the first 16,000 characters, and asked for the eight subtotals. The rater did not see the review's scores.

The text was taken from each page's body. Date metadata in the page head was not in that text, so the rater had no date for Anthropic 2025 and Anthropic 2026b. Three pages refused the first automated request and were fetched again.

### Agreement before reread

- Nine sources.
- Mean absolute difference of the total is 6.17 of 20, and of the eight group subtotals 0.92 on average over 72 cells.
- Threshold agreement (10 of 20) is 3 of 9; kappa on the threshold decision is 0.07.
- The rater scored more sources below threshold.
- Its largest gaps, summed over the nine sources, were on authority (22 points), then objectivity (12), methodology (9) and impact (8.5).

### Disagreements of more than 3 points

Five: Agentic AI Foundation (review 11, rater 0.5), Anthropic 2025 (12.5, 6.5), Anthropic 2026b (12, 0.5), OpenAI 2026b (11.5, 1.5), GitHub 2026j (10.5, 0.5). Each page was reread against the criteria. Rules applied, the same in every source:

- D1 needs a date in the page's text or head. Dates in the head count (Anthropic 2025 has one, 2025-09-29, in its page metadata).
- I1 needs a count or a named adopter in the text. Unnamed customers and a nav item "Adoption" do not count.
- O3 is 0 for a vendor's page about its own tool, as the rules say of company pages.
- Criteria the rater zeroed for lack of visible text are kept where the text shows them, e.g. the stated aim (M1) and the stewardship line (A1).

| Source | Review, first | Rater | Reread | Change and reason |
|---|---|---|---|---|
| Agentic AI Foundation 2026 | 11 | 0.5 | 9 | O 2 to 1: owner's own format page, no data, not balanced. D 1 to 0: no date in the page. A 3 kept: the stewardship line (Linux Foundation) is an institution. M 2 kept: the page states its aim ("Why AGENTS.md?"); the rater gave M 0 and missed it |
| Anthropic 2025 | 12.5 | 6.5 | 11 | O 2 to 1.5: the post gives trade-offs and no data. I 1 to 0: "working alongside our customers" names no one and counts nothing. D 1 kept: dated 2025-09-29 in the page head, which the rater's text lacked. A 4 kept: an institution's post; the rater's A1 0 treated it as a personal blog |
| Anthropic 2026b | 12 | 0.5 | 10 | O 2 to 1: vendor's page about its own tool. I 1 to 0: no count or named adopter in the text. M 2 kept, A 4 kept |
| OpenAI 2026b | 11.5 | 1.5 | 8.5 | O 2 to 1 (vendor's own tool). I 1 to 0 (no count). D 1 to 0: no date found in the page or its head. Its 32 KiB default is in the text, so the review's claim stands as a vendor setting |
| GitHub 2026j | 10.5 | 0.5 | 8.5 | O 2 to 1 (vendor's own tool). I 1 to 0 (no count; "Adoption" is a navigation item). D kept: dated in the page head |

### After the reread

Three sources move below 10 of 20 (Agentic AI Foundation 9, OpenAI 8.5, GitHub 8.5), so with HumanLayer 2025 four grey sources are examples of practice only. Anthropic 2026b stays at threshold (10). The review uses all four below threshold only for practice statements, labelled as such, so no claim moves to support. The rater still differs from the reread by more than 3 on all five; the reread did not move to the rater's values, because its zeros came from criteria the visible text does meet.

- Agreement after the reread: mean absolute difference between the rater and the reread totals: 5.0 of 20. Threshold agreement 6 of 9; kappa 0.37. These are not an independent check, since the reread's decisions are the review's.

### Not changed, flagged

- Anthropic 2024 scores I 1 on an appendix about customers' domains, with no count or named adopter. The rule would give 0. Its disagreement is under 3, so it was not reread; the maintainer should decide. - DORA 2025b and Stack Overflow 2025 were under 3 and not reread. The DORA landing page shows no date in its text; the same D check should be run on it.

