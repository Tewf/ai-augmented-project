# Review: five strands

Step 2 of the review, read on 2026-11-02 and extended on 2026-11-03 by forward citations of Vaccaro 2024 (marked forward). Surveys first in each strand.

**Shape:** [review](https://github.com/Tewf/reader-ergonomics-review/blob/a7f405f26f14cd188291e2a86b630121c4302a94/shapes/review.md)

- Terms are in [frame](frame.md); each key is in the [bibliography](../bibliography.md).
- Grades are the standard's four.
- A number read in an abstract is marked (secondary).

## Strand 0: existing reviews

- Vaccaro 2024 is a meta-analysis of 106 experiments and 370 effect sizes on humans, models and their combination. Berretta 2023 is a scoping review that defines human-AI teaming. Liu 2024b surveys 124 papers on agents for software engineering (secondary). Luo 2026 surveys agent memory. Barr 2015 surveys test oracles.
- No review of the effect of agent context files was found. No study of the audit of an agent's memory was found.

## Strand 1: teaming and complementarity (Q1)

- On average a person with a model scored below the better of the two alone: Hedges g = -0.23, 95% interval -0.39 to -0.07 (Vaccaro 2024, abstract and results, read). Measured.
- The loss came in tasks that decide; tasks that create content gained (Vaccaro 2024). When the person beat the model alone, the team gained; when the model beat the person, the team lost. Measured.
- The team did beat the person alone on average, which Vaccaro 2024 calls augmentation. Measured.
- Forward, the same split holds in a narrower pool. Across 146 experiments in healthcare and public sectors, augmentation raised performance (g = 0.622). Synergy was negative (g = -0.380), with AI alone often ahead of the team. Publication bias favours the augmentation results (Ngo 2025, abstract, secondary). Measured.
- Across 52 clinical studies the team rarely reached complementarity. Reviewing the model's output at the same time gave more than reviewing it after a first judgment, and juniors gained more than seniors (Liu 2025e, abstract, secondary). Measured.
- Across 15 studies of generative AI in organisations, the effect depends on the decision phase. It is positive in intelligence tasks (d = +0.41) and negative in choice tasks (d = -0.28). The authors name outputs that sound equally sure when right or wrong as the cause (Nassiri 2026, abstract, secondary). Measured; a small review.
- Across 42 studies of LLM assistance, physicians' diagnostic accuracy rose a little (g = 0.22, 95% interval 0.18 to 0.27), with the size varying by model and field (Tretow 2025, abstract, secondary). Measured; a preprint, not peer reviewed. Its abstract gives a search window that runs past its own DOI date, so the window is not relied on.
- Complementary performance is possible: in 1,626 users' experiments it appeared on every task when the model was about as accurate as the person (Bansal 2021, introduction, read). Explanations raised acceptance whatever the model's correctness and did not raise team accuracy. Measured.
- In an earlier study that Bansal 2021 tabulates, people alone scored 51.1%, the model alone 87.0% and the team 74.6% (section 2, read). Measured.
- Parasuraman 2000 splits a task into four stages: acquiring information, analysing it, selecting a decision, acting. Each stage gets its own level of automation. Convention, untested.
- Horvitz 1999 and Amershi 2019 give design principles for when a system acts and when it asks; Amershi 2019 validated 18 guidelines with 49 practitioners on 20 products (secondary). Convention, with an evaluation.
- Wu 2023 argues a model should ask clarifying questions before it writes code. A position paper. Convention.
- A vendor's engineering page describes agents that pause for human feedback at checkpoints or at blockers (Anthropic 2024). Practice.
- Among developers, 46% distrust the accuracy of AI tools and 33% trust it; 3% highly trust it (Stack Overflow 2025, read). Measured, descriptive.
- Routing each query to the cheapest model that suffices cut cost by up to 98% at the accuracy of the best single model (Chen 2023b, secondary). Measured.

## Strand 2: instructions and context files (Q2)

- Practice: the convention is shared by many tools. One site counts over 60,000 projects (Agentic AI Foundation 2026, the owners' claim). Two vendors document it (OpenAI 2026b; GitHub 2026j).
- Content: 2,303 files from 1,925 repositories; 75.9% hold test procedures, 14.8% security (Chatlatanagulchai 2026, secondary). Measured, descriptive.
- Content: 401 repositories give five themes: conventions, guidelines, project information, directives to the model, examples (Jiang 2025, secondary). Descriptive.
- Effect: a generated file changed the resolution rate by -0.5% and -2% on two benchmarks, p = 0.87 and 0.37, and raised cost by 20% and 23% (Gloaguen 2026, section 4.2, read). Measured.
- Effect: developer-written files gave +2.4% on average, p = 0.21, with cost up by at most 19% (Gloaguen 2026, section 4.2, read). Measured.
- The same study finds the instructions followed and repository overviews unhelpful; files help to state non-standard practice (Gloaguen 2026, abstract).
- A second ablation found no measurable move in correctness over 288 runs (Khatri 2026, secondary). Measured; the authors say single-agent studies draw tasks from different bands of difficulty.
- A stale file wins over the code: 90.1% of choices followed it. One sentence giving the code precedence raised the share following the code from 4.2% to 91.4% (Xu 2026, secondary). Measured.
- Stale references appear in 23.0% of 356 repositories (Treude 2026, secondary). Supported with caveat.
- A vendor sets a target under 200 lines and says the model treats the file as context, not as enforced configuration (Anthropic 2026b). A default cap of 32 KiB is another vendor's setting (OpenAI 2026b). Practice.
- Context engineering is the choice of what the model holds at each step (Anthropic 2025). The harness around the model also moves quality: 35 releases of one tool, model fixed, changed results (Sghaier 2026, secondary). Measured.
- Interface design for the agent matters: Yang 2024b raised SWE-bench pass@1 to 12.5% with a built interface (secondary). Measured.
- A practitioner blog says models follow about 150 to 200 instructions reliably (HumanLayer 2025). Score 7 of 20: an example only.

## Strand 3: memory (Q3)

- Memory architectures are surveyed as storage, reflection and experience (Luo 2026). A system that moves data between fast and slow tiers is the first design (Packer 2023). Convention.
- Practice: one vendor separates instructions the person writes from notes the model writes, loads both each session, caps the index of the second, and offers an audit of both (Anthropic 2026b). The files are plain text, editable and local. Practice.
- The audit that exists is a consistency check of the file against the code (Treude 2026). It is a roadmap with a sample, not a method with a measure.
- No controlled study of a project memory that a model writes was found.

## Strand 4: productivity and measures (Q4)

- 16 developers, 246 tasks of 2.0 hours on average: AI allowed raised completion time by 19% (Becker 2025, abstract and introduction, read). Developers had forecast 24% faster and believed afterwards 20% faster. Measured.
- A controlled trial with GitHub's tool found tasks 55.8% faster, on one server to write (Peng 2023, secondary). Measured.
- 96 engineers at one company were about 21% faster, with a large interval (Paradis 2024, secondary). Measured.
- A research programme calls AI an amplifier of an organisation's strengths and weaknesses (DORA 2025b, landing page only). Practice.
- Speed and quality can move apart. In a preregistered trial of 758 consultants, AI raised speed (25.1% faster) and quality on tasks inside the model's frontier. On one task outside it, users were 19% less likely to be correct (Dell'Acqua 2026, abstract, secondary). Measured. A time count alone would have missed the second result.
- Round trips, questions asked twice and errors caught before a person saw them are not outcomes in any source found.

## Strand 5: checks as the oracle (Q5)

- A test oracle decides whether an output is right; when none is adequate, a person remains the final source (Barr 2015). Survey.
- Models struggle to correct their reasoning without outside feedback (Huang 2024, secondary). Self-repair gains are modest once cost is counted, limited by the model's own feedback (Olausson 2024, secondary). Measured.
- A vendor says agents need ground truth from the environment at each step (Anthropic 2024). Practice.
- A hook blocks an action whatever the model decides; an instruction does not (Anthropic 2026b). Practice.
- One agent rewrote code to match a stale file in 20 of 80 runs, and the project's own tests failed in 17 of them (Xu 2026, secondary). The check caught what the instruction caused.
- The loop in which a model interprets a checker's verdict is in [the autoformalization review](https://github.com/Tewf/reader-ergonomics-blueprint/blob/f9b2408e7f1ddf4a82d2d480c62d6b5855e14e0b/evidence/autoformalization/README.md).
