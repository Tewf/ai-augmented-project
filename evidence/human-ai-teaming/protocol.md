# Protocol: how the pool was built

A first pass of a multivocal literature review to Garousi 2019, run on 2026-11-02 by one reviewer. Terms are in [frame](frame.md).

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

- One reviewer, no second rater; the grey scores are one person's.
- Most numbers come from abstracts. Only the sources marked read in the text were checked in the paper.
- Preprints of 2026 are not peer reviewed.
- Search engines change; counts are those of 2026-11-02.
