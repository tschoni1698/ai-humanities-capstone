# Data preparation: cutting the editions into letter files

Created on 13 November 2026 with two Python scripts that an AI model (Claude) wrote and ran.
The scripts are in this folder; with the two PDFs they reproduce the corpus exactly.

> **Note:** The text files produced by the scripts are **not** in this public repository, because the 2015 edition is protected by copyright (© Pedagoški inštitut). This file documents how they are made. With the scripts and the two PDFs they can be generated locally.

## Sources

- **Vrečko 2015:** Trubar, Primož. 2015. *Primož Trubar Pisma.* Edited by Edvard Vrečko and Fanika Krajnc-Vrečko. Zbrana dela Primoža Trubarja 10. Ljubljana: Pedagoški inštitut. Born-digital PDF, no OCR.
- **Elze 1897:** Trubar, Primož. 1897. *Primus Trubers Briefe: Mit den dazu gehörigen Schriftstücken gesammelt und erläutert.* Edited by Theodor Elze. Bibliothek des Litterarischen Vereins in Stuttgart 215. Tübingen: Litterarischer Verein in Stuttgart. Google Books scan with OCR text layer.

## Files in this folder

| File | Purpose |
|---|---|
| `split_vrecko.py` | cuts items Nos. 1–85 from the 2015 edition |
| `split_elze.py` | cuts the 19 letters to Trubar (1568–1583) from Elze 1897 |
| `elze_pieces.csv` | for each Elze piece: printed pages, part of the page, first and last words |

## Output

The scripts create the following structure in the target folder. Folder and file names are in German, as in the corpus already in use.

| Folder | Content | Files |
|---|---|---|
| `vrecko/original/` | letter text in the original language (German or Latin), Nos. 1–85 | `V001.txt` … `V085.txt` |
| `vrecko/kopf/` | editors' header (Slovenian): number, addressee, date, archive, earlier prints | `V001_kopf.txt` … |
| `vrecko/fussnoten/` | editors' footnotes (Slovenian) with page and anchor | `V001_fn.txt` … |
| `elze/an_trubar/` | 19 letters to Trubar, 1568–1583 | `E01.txt` … `E19.txt`, plus `E##_anm.txt` |
| `briefe.csv` | technical list for Vrečko: file, number, pages, word count, number of footnotes | |
| `elze/stuecke.csv` | technical list for Elze: file, pages, word count, part of the page, form | |
| `*/protokoll_schnitt.txt` | cutting log: irregularities and every change at line ends | |

The Slovenian translation is not saved. File names and lists deliberately contain neither date nor addressee, because these metadata are recorded by hand in the minimal-AI workflow. The editors' header is kept separately so that the letter text stands on its own.

Size: 85 letter texts with 59,316 words (Nos. 1–51: 39,235; Nos. 52–83: 19,039; Nos. 84–85: 1,042) and 507 footnotes.

## What the scripts do

### Vrečko

The script reads every line with its coordinates and font height and sorts it by fixed rules:

- A letter starts on the page whose first line is the next item number in large type.
- The header runs from the number to the start of the letter text (third larger gap on the first page).
- The original runs up to the line "Prevod" (Slovenian: translation).
- Footnotes are the lines in small type at the foot of the page.
- Superscript footnote numbers appear as `[1]` after the word.
- Page breaks appear as `[S. 233]` in the text (printed page number, equal to the PDF page).
- Lines are joined into paragraphs. A paragraph ends where the print has a larger line gap.

The script does not change any letters. The original texts had no hyphenation; in four footnotes a hyphen was joined (see log).

### Elze

- Running heads (page numbers) and signature marks at the foot of the page are removed.
- Main text and notes are separated at the star line.
- Each piece is cut out by its heading and by the note on its source at the end; the details are in `elze_pieces.csv`.
- Words hyphenated at line ends are joined (115 cases, all in the log).
- OCR misreadings are **not** corrected.
- `E##_anm.txt` contains Elze's notes from the pages concerned. They may also belong to neighbouring pieces.

## Checks

- **Vrečko:** For all 85 items the word sequence of the original was compared with a second, independent text extraction of the PDF. Every word appears in the same order before the line "Prevod". The transition from header to letter text was inspected for all 85 items.
- **Elze:** Beginning and end of all 19 pieces were inspected. All words occur in the OCR layer of the pages concerned.
- There was no character-by-character comparison with the print. During annotation every file should be read against the printed page.

## Known peculiarities

- **Most footnotes belong to the translation.** Of 507 footnotes, 393 are anchored in the Slovenian translation, 89 in the header and 24 in the original; one has no number in the text. The footnote file therefore gives, for each note, the part and the words before the number.
- **V005, footnote 7:** the edition has the footnote text but no number in the text.
- **V006, footnote 6** consists only of a reference.
- **Slovenian editorial lines in the letter text:** a few originals contain short editorial additions, at least V015 (first line), V017 (first line) and V024 ("[Priloga št. 1]", "[Priloga št. 2]").
- **V084** is a letter by Johannes Brenz, not by Trubar. **V009, V026, V043, V075** are not letters (register of books, report, instructions).
- **V084:** the line "Johann Brenz etc. an Herzog Christoph" is in the header; in V085 the corresponding line opens the letter text.
- **E01:** Elze's heading gives 4 August 1568, the letter text 9 August.
- **E02** is not a letter text, only Elze's note that a letter of the same wording went to Trubar.
- **E05:** the heading reads "1563", the text 1568.
- **E19** appears in Elze as No. 14 of appendix 2 to letter 60.
- The column `form` in `elze/stuecke.csv` (full text, summary, mixed) is provisional and should be checked during annotation.

## Running the scripts

```
python3 split_vrecko.py <Vrecko.pdf> <target_folder>
python3 split_elze.py <Elze.pdf> <target_folder>
```

Requires `pdftotext` from poppler-utils.
