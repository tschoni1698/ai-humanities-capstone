# Milestone 1 — Pitch
**Due: 30.10.2026**

Nico Tschojer · 28 October 2026
*Transferred unchanged from the submitted PDF pitch.*

---

## Working title
<!-- A short name for your project -->
**Reading Trubar Twice:** A minimal-AI and an AI-intensive workflow for Primož Trubar's exile network (1565–1586)

## The theme and question
<!-- What are you exploring, and why does it matter to you? -->
The reformer Primož Trubar (1508–1586), who printed the first Slovenian books, tried to steer the Carniolan church from his exile in Württemberg through his letters. I will reconstruct this network in parallel, in two seminars, once in a traditional DH workflow with little AI and once in an AI-intensive workflow, and focus on the method: how the experiences differ, where each reaches its limits, and whether AI helps me push mine. My interest in religious identity in the Alps-Adriatic region, especially the history of persecuted Protestants, comes from my own background; I also want to see how AI can serve such questions for someone with little programming experience.

**Questions**

1. **Method (main question):** How does the research experience differ between the two workflows? Where did I fail, where did AI move me forward, and did it help me push my limits?
2. **Results:** Which persons, ties and functions does each workflow find, miss or invent?
3. **History (shared):** Who belonged to Trubar's exile network, which functions did they fulfil, and how did he use it to influence the church in Carniola?

## The material
<!-- What will your system draw on? Who created it, and whose voices might be missing? -->
Letters, almost all in German, from two digitized editions: Elze 1897 (public domain; also about 20 letters to Trubar and further documents from his circle) and Vrečko and Krajnc-Vrečko 2015 (Trubar's own letters, more complete; © Pedagoški inštitut). The about 30–35 letters of the second exile, annotated by hand, form the gold standard and test set; the roughly 45 earlier letters serve for prompt development. Letters from and to Trubar form the network; the further documents serve only as context for retrieval.

**Missing voices:** only part of the correspondence survives, mostly in Trubar's own view. Opponents, printers and the Carniolan congregations appear mainly through his words.

## Why AI?
<!-- What could an AI system help you see or do here, and where might it mislead? -->
### Two workflows

- **Minimal AI** (traditional DH, also a parallel course project): letters, persons, places and functions recorded by hand in linked tables with a controlled vocabulary; network analysis in Python; AI only for single, checked suggestions. Its annotations of the exile letters become the gold standard.
- **AI-intensive** (this capstone): LLMs separate the letters, extract persons, places, dates and functions with the same vocabulary and suggest GND matches, which I check; RAG answers the research questions with citations; code is written with much stronger AI support.
- **Interference and documentation:** both workflows run in parallel and shape each other, so this is no controlled experiment. It relies on a research diary (steps, problems, failures, hours) for both workflows and on prompts versioned on GitHub. A prototype with first results in December is the starting point for further comparison.

### What AI may do, and where it may mislead

AI may take over separating the irregular 1897 edition, reading 16th-century German at speed, reconciling name variants and writing code beyond my Python skills. It may mislead by misreading Early New High German, merging persons, inventing ties and turning ambiguous roles into confident labels.

### Evaluation

The minimal workflow is the reference: the gold standard and my own answers to 5–10 fixed questions. Following the capstone stages, I compare a plain instruction, my designed prompt and RAG. Extraction is scored against the gold standard (found, missed, invented); for the questions, stages 1–2 show what the model knows or invents without the letters, stage 3 what retrieval adds. Each stage runs with a cloud and a local model; divergences feed the failure analysis.

## Who is it for?
<!-- Who might use what you build? -->
DH researchers and historians deciding how much AI to build into edition-based network research.

## Your team
<!-- Who is involved, and what does each person bring? -->
Individual. I bring theology and religious studies and close knowledge of the letters; my Python is very basic.

## Concerns
<!-- The biggest technical or ethical uncertainty you can foresee -->
- Linking the project with a second course needs approval from both lecturers.
- It still needs to be clarified whether the German transcriptions of the 2015 edition may be published as text files on GitHub.
- Functions are interpretive, and this is one corpus and one researcher: a documented case study, not a general verdict.
