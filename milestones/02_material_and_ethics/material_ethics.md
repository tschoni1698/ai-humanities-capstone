# Milestone 2 — Material and Ethics Note
**Due: 13.11.2026**

Nico Tschojer · *Reading Trubar Twice*

---

## Your collection

**What is it?**
<!-- Describe the body of material your system will draw on -->
The correspondence of the Slovenian reformer Primož Trubar (1508–1586), taken from two printed editions:

- **Vrečko and Krajnc-Vrečko 2015** — Trubar's own letters with German or Latin transcriptions, Slovenian translations and Slovenian editorial notes. This is the main source.
- **Elze 1897** — the older German edition. From it I use only the 19 letters written *to* Trubar during his second exile (1568–1583). Elze's further documents (letters among third parties, minutes of the Carniolan estates) are used only as background for identifying persons, not as network data.

The focus is Trubar's second exile in Württemberg (1565–1586). The 31 letters of this period are annotated by hand in the parallel minimal-AI workflow and serve as gold standard and test set.

**Where does it come from?**
<!-- Source(s), institution(s), creator(s), date range -->

| Source | Creator | Date range of the letters | Form |
|---|---|---|---|
| Trubar, Primož. 2015. *Primož Trubar Pisma.* Edited by Edvard Vrečko and Fanika Krajnc-Vrečko. Zbrana dela Primoža Trubarja 10. Ljubljana: Pedagoški inštitut. https://www.pei.si/ISBN/978-961-270-231-1/mobile/index.html#p=5 | Edvard Vrečko, Fanika Krajnc-Vrečko (eds.); transcriptions based on Jože Rajhman's edition of 1986 | 1533–1585 | born-digital PDF, freely available from the publisher |
| Trubar, Primož. 1897. *Primus Trubers Briefe: Mit den dazu gehörigen Schriftstücken gesammelt und erläutert.* Edited by Theodor Elze. Bibliothek des Litterarischen Vereins in Stuttgart 215. Tübingen: Litterarischer Verein in Stuttgart. https://www.google.at/books/edition/Primus_Trubers_Briefe/bgU3AAAAMAAJ?hl=de&gbpv=1&dq=Primus+Trubers+Briefe&printsec=frontcover | Theodor Elze (ed.) | 1543–1584 | Google Books scan with OCR text layer |

The manuscripts themselves are kept mainly in the Archives of the Republic of Slovenia (Carniolan estates), the Hauptstaatsarchiv Stuttgart, the Haus-, Hof- und Staatsarchiv Vienna and the Staatsarchiv Zürich. I work only with the printed editions, not with the manuscripts.

**How will you prepare it?**
<!-- Cleaning, chunking, OCR, transcription, format — describe your pipeline -->
1. **Separation.** A rule-based Python script (written with AI support, fully documented and repeatable) cuts the 2015 edition into one file per letter: original text, editorial header and footnotes are stored separately; the Slovenian translation is not kept. A second script cuts the 19 letters to Trubar from Elze. OCR errors in Elze are **not** corrected; only line-end hyphenation is joined, and every such change is logged.
2. **Check.** The original text of all 85 numbers was compared word for word, in sequence, with an independent text extraction of the PDF. Beginning and end of every Elze piece were checked by eye. During annotation every file is read against the printed page.
3. **Annotation (minimal-AI workflow) for the gold standard letetrs.** Letters, mentioned persons, places and their functions (e.g. funding, printing, carrying letters, recommending, obstructing) are recorded by hand in linked CSV tables with a controlled vocabulary.
4. **AI workflow.** LLMs extract the same information with the same vocabulary; RAG answers the research questions on the letter files, one letter per retrieval unit, with citations to letter number and page.
5. **Data split.** About 9 letters before 1565 for prompt development; the 31 letters of the second exile (1565–1586) as gold standard (10 for validation, 21 as test, used once); the 7 letters to the Carniolan estates from the first exile (1548–1562) and Elze's letters to Trubar are held back as reserve test material (because most letters from the second exile are directed to the to the Carniolan estates).

**Size and scope**
<!-- Approximate number of documents / images / recordings, word count, etc. -->
- 2015 edition: 85 numbered items, of which about 80 are letters by Trubar (the others are a book register, a report, two instructions, and one letter by Johannes Brenz); about 59,300 words of original text and 507 editorial footnotes.
- Second exile: 31 letters, about 19,000 words; almost all in German.
- Elze: 19 letters to Trubar, about 5,500 words; about half are printed only as summaries (regests) in indirect speech, not in full.

---

## Ethical considerations

**Copyright and licensing**
<!-- Is the material in the public domain? Under a Creative Commons licence? Used with permission? -->
- The 16th-century letters themselves are in the public domain.
- **Elze 1897** is in the public domain.
- **Vrečko and Krajnc-Vrečko 2015** is © Pedagoški inštitut. The publisher offers the PDF freely online, but I have not found an open licence. The transcriptions, notes and translations are editorial work.
- Consequences: the text files of the 2015 edition are **not** stored in this public repository (`data/raw/` is excluded by `.gitignore`). They are kept locally and in a private repository for my own research. Here I publish only scripts, metadata, my annotations, and short quotations with references. Before any wider publication I will ask the publisher.
- The letters are sent to a cloud model (Claude) for the AI workflow; I compare it with a local model, which keeps the texts on my machine.

**Consent**
<!-- If the material involves living people or community archives: how was consent obtained? -->
The material concerns persons who died more than 400 years ago and contains no data on living people. Consent is therefore not required. Modern contributors are the editors, whose work I credit and cite.

**Whose voices are present?**
<!-- Who created this material, and whose perspectives does it centre? -->
- Above all **Trubar himself**: the network is reconstructed from his letters and through his eyes.
- The **Protestant elite**: the Carniolan estates, the dukes of Württemberg, Tübingen and Stuttgart theologians (Andreae, Bidembach, Osiander, Schnepf, Schmidlin), and in Elze's letters a few Württemberg pastors.
- The **editors**: Elze writes from a 19th-century German Protestant perspective; the 2015 edition and its predecessors frame Trubar as the founder of Slovenian literature. Their notes shape who can be identified and how.

**Whose voices are absent or marginalised?**
<!-- Who is missing, and does that matter for your question? -->
- **Opponents**: the Catholic bishop, Archduke Charles and the Habsburg court appear in the exile letters only through Trubar's words.
- **Printers, messengers, students and congregations** are mentioned, but rarely speak.
- **Women**: Trubar's wives and other women barely appear.
- **Lost letters**: much of the correspondence did not survive. The surviving letters come mainly from the archive of the Carniolan estates, so the network is skewed towards them. Some letters are known only because another letter mentions them.
- This matters directly for the question: a missing tie in the network may mean a lost letter, not a missing relationship.

**Limits you will communicate to users**
<!-- What should users know before trusting the system's outputs? -->
- The network shows **Trubar's surviving correspondence**, not his whole network.
- **Functions are interpretations**, coded by one researcher with a controlled vocabulary; they can be contested.
- The models may **misread Early New High German**, merge or invent persons, and turn ambiguous roles into confident labels. Every answer cites letter number and page so that it can be checked; persons identified only through an editorial footnote are marked as such.
- The project is **one case study** with one corpus and one researcher, not a general verdict on AI in historical research.
- **Human in the loop**: no AI output enters the gold standard or the final network tables without my check.
