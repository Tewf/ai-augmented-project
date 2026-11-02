# Frame: the problem and its names

Step 1 of the review, read on 2026-11-02. It states the problem, gives the field's names beside the practitioners' names, and says whether the repository's name matches.

## The problem in one sentence

How one person, one language model and one machine are set up so that the project gets done, with the person's time spent only on what is theirs to decide.

## What the field calls it

The field has no single name. Four literatures meet, each with its own word.

| Level | The field's name | First met in |
|---|---|---|
| the whole setting | **human-AI teaming**, **human-AI collaboration** | Berretta 2023; Vaccaro 2024 |
| the aim | **hybrid intelligence**: human and machine intelligence combined to reach goals neither reaches alone | Akata 2020; Dellermann 2019 |
| the test of the aim | **complementary performance**: the team scores above the better of the person alone and the model alone | Bansal 2021 |
| the same test, other words | **synergy** (above the best of the two); **augmentation** (above the person alone) | Vaccaro 2024 |
| the software setting | **AI-assisted software engineering**; **agentic coding** | Liu 2024b; Chatlatanagulchai 2025 |
| the software around the model | **agent harness**: the layer that wraps a model and lets it act on a repository | Macedo 2026; Sghaier 2026 |
| what the model is handed | **context engineering**; **agent context file**, **agent manifest** | Anthropic 2025; Chatlatanagulchai 2026 |
| who decides what | **levels of automation** across four stages of a task | Parasuraman 2000 |
| how a question reaches the person | **mixed-initiative interaction**; **clarifying questions** | Horvitz 1999; Wu 2023 |

## What practice calls it

- The practitioners' words are file names and product features: AGENTS.md, CLAUDE.md, cursor rules, custom instructions, auto memory (Agentic AI Foundation 2026; Anthropic 2026b; GitHub 2026j).
- A **standing instruction** is a file read at the start of each session. The field's word is context file.
- A **project memory** is notes a model writes and reads across sessions. The field's word is agent memory (Luo 2026).
- A **check as the oracle** is a program that decides whether output is right. The field's word is test oracle (Barr 2015).
- **Delegation by cost** sends a task to the cheapest worker that can do it. The field's word is LLM cascade (Chen 2023b).

## Does the repository's name match?

- "AI-augmented project" echoes **augmentation** and **hybrid intelligence**, which are the field's words for the aim.
- It does not echo the software words: human-AI teaming, agentic coding, agent harness.
- The finding of this step: the name is close, not wrong. It is not renamed; the maintainer decides.
- The topic folder takes the field's word, human-ai-teaming.

## Sub-questions

The front page's four questions, with the strand that answers each.

| Question | Strand in review.md |
|---|---|
| Decisions: whose are they? | 1 teaming and complementarity; 5 checks |
| The start of a session | 2 instructions and context files |
| Memory | 3 memory |
| The measure | 4 productivity and measures |

## Held elsewhere

- A model that interprets a checker's verdict and decides nothing, on reasoning: [the autoformalization review](https://github.com/Tewf/reader-ergonomics-blueprint/blob/f9b2408e7f1ddf4a82d2d480c62d6b5855e14e0b/evidence/autoformalization/README.md). It is linked, not repeated.
- Several agents, the tool itself and the steps of the project are out of scope (front page).
