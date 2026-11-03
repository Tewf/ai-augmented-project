# Position

Step 4 of the review. What is known, what was not found, and what this repository would ask. Each "not found" is a statement about these searches, not about the world. Terms are in [frame](frame.md).

**Shape:** [position](https://github.com/Tewf/reader-ergonomics-review/blob/a7f405f26f14cd188291e2a86b630121c4302a94/shapes/position.md)

## Known

- A person with a model does not beat the better of the two on average, and does best on tasks that create (Vaccaro 2024).
- A context file does not raise success on average and costs more; it states non-standard practice (Gloaguen 2026).
- A model obeys a stale file over the code (Xu 2026, secondary).
- A model repairs its own output poorly without outside feedback (Huang 2024; Olausson 2024).
- Experienced developers' own speed estimates were wrong in sign (Becker 2025).

## Not found in these searches

- A study of a whole setup (instructions, memory, checks, delegation and questions) measured together.
- A controlled study of a memory the model writes, or of its audit.
- A measure of questions asked twice, round trips or errors caught before a person saw them.
- A study of delegation by cost inside a person's own workflow, rather than in a service.
- Practice and research are apart: practice recommends length limits and overviews; the one evaluation finds overviews unhelpful.

## The four questions

| Question | Answer from the evidence | Grade |
|---|---|---|
| Decisions: whose are they? | Programs decide what a program can check. The person decides what is to be built and which checks count. The model drafts and proposes. For decision tasks the evidence is against handing the model the call. The blueprint's answer of none holds for decisions; the model may take drafting. | supported with caveat |
| The start of a session | Hand the model only what it cannot infer and a program can verify: commands, non-standard conventions, what to do on a conflict. Keep it short; test it for staleness. | supported with caveat |
| Memory | Not settled. Practice keeps notes as plain files an index points to, written by the model and read by the person. The audit found is a consistency check against the code. | convention, untested |
| The measure | Do not trust self-report. Count time per task against a control, and errors a check caught before a person saw them. Round trips are not measured anywhere found. | supported with caveat |

## What this repository would ask

- Which of the five practices of [the baseline](baseline.md) each have a measurable effect on a single person's project?
- Whether a short, tested instruction file with a conflict rule beats none, on the maintainer's own tasks.
- Whether a counted question, asked once, falls when a memory exists.

## What the design document would have to decide

- The unit of measure: tasks, sessions or questions.
- The control: how to run a task with and without a practice, for one person.
- Where the person's decisions are logged so they can be counted.
- Which checks are programs and which are judgments.
- How stale instructions and memory are found by a program.
