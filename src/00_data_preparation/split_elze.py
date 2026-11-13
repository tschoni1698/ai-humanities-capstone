#!/usr/bin/env python3
"""Cuts the letters to Trubar (second exile) from Elze, Primus Trubers Briefe (1897).

Usage:    python3 split_elze.py <pdf> <target_folder>
Requires: pdftotext (poppler-utils) and elze_pieces.csv in the same folder.

The basis is the OCR text layer of the Google Books scan. The script does not correct misreadings.
It only removes running heads, separates the main text from the notes section (line with "*")
and joins hyphenated words at line ends. Every such change is written to the log.

Elze prints documents by others partly in the main text (appendix), partly in the notes below the
star line. elze_pieces.csv states for every piece on which printed pages and in which part it
stands, and with which words it begins and ends. These details were checked against the text.

Output folder and file names, CSV columns and log messages are kept in German so that the
output is identical to the corpus already in use (an_trubar = to Trubar, anm = notes,
stuecke = pieces, protokoll_schnitt = cutting log).
"""
import csv, os, re, subprocess, sys

VERSATZ = 25   # PDF page = printed page + 25

# nr, printed pages, part ('haupt' = main text or 'anm' = notes), start (regex), end (regex, inclusive)
STUECKE = []   # read from elze_pieces.csv in main()


def lies_seite(pdf, gedruckt):
    out = subprocess.run(['pdftotext', '-layout', '-f', str(gedruckt + VERSATZ), '-l', str(gedruckt + VERSATZ), pdf, '-'],
                         capture_output=True, text=True, check=True).stdout
    zeilen = out.replace('\x0c', '').split('\n')
    # running head: first non-empty line if it is only the page number
    for i, z in enumerate(zeilen):
        if z.strip():
            if z.strip() == str(gedruckt):
                zeilen = zeilen[i + 1:]
            break
    # remove signature marks at the foot of the page ("29 *", "Primus Trubers Briefe. 36")
    zeilen = [z for z in zeilen if not re.fullmatch(r'\s*\d{1,2}\s*\*\s*', z) and not re.fullmatch(r'\s*Primus Trubers Briefe\.\s*\d+\s*', z)]
    stern = [i for i, z in enumerate(zeilen) if re.fullmatch(r'\s*\*\s*', z)]
    if stern:
        return zeilen[:stern[0]], zeilen[stern[0] + 1:]
    return zeilen, []


def einzug(z):
    return len(z) - len(z.lstrip())


def fuege(zeilen, log, name):
    """Joins lines into paragraphs. A new paragraph starts at an empty line, at an indented first
    line (>= 3 characters more than the line before) and at centred lines (heading, date, signature).
    Hyphens at line ends are joined only within a paragraph.
    Page breaks: [S. n]; if a sentence runs over the page, the paragraph stays together."""
    voll = [einzug(z) for z in zeilen if z.strip() and not z.startswith('[S. ') and len(z.strip()) > 45]
    rand = min(voll) if voll else 0
    absaetze, akt, vor, marke = [], '', None, ''
    for z in zeilen:
        if z.startswith('[S. '):
            marke = z.strip()
            continue
        if not z.strip():
            if marke:
                continue                      # empty lines at the top of a page do not end a paragraph
            if akt:
                absaetze.append(akt)
                akt = ''
            vor = None
            continue
        t = re.sub(r'\s+', ' ', z.strip())
        e = einzug(z)
        zentriert = e >= rand + 8
        if marke:
            if akt and re.search(r'[a-zäöüß]-$', akt) and t[:1].islower():
                erstes, _, rest = t.partition(' ')
                log.append(f'{name}: Trennstrich ueber Seitenwechsel zusammengefuehrt: {akt[-14:]}|{erstes}')
                akt = akt[:-1] + erstes + ' ' + marke + (' ' + rest if rest else '')
            elif akt and not re.search(r'[.!?"\]\)]$', akt) and not zentriert:
                akt += ' ' + marke + ' ' + t
            else:
                if akt:
                    absaetze.append(akt)
                akt = marke + ' ' + t
            marke, vor = '', e
            continue
        neu = vor is None or zentriert or (e - vor >= 3) or (vor >= rand + 8 and not zentriert)
        if not akt:
            akt = t
        elif re.search(r'[a-zäöüß]-$', akt) and t[:1].islower():
            log.append(f'{name}: Trennstrich zusammengefuehrt: {akt[-14:]}|{t[:14]}')
            akt = akt[:-1] + t
        elif not neu:
            akt += ' ' + t
        else:
            absaetze.append(akt)
            akt = t
        vor = e
    if akt:
        absaetze.append(akt)
    return absaetze


def main(pdf, ziel):
    hier = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(hier, 'elze_pieces.csv'), encoding='utf8') as f:
        stuecke = list(csv.DictReader(f, delimiter=';'))
    os.makedirs(os.path.join(ziel, 'elze', 'an_trubar'), exist_ok=True)
    log, pruef, zeilen_csv = [], [], []
    for s in stuecke:
        name = f"E{int(s['nr']):02d}"
        seiten = [int(x) for x in s['seiten'].split(',')]
        strom, noten = [], []
        for k, g in enumerate(seiten):
            haupt, anm = lies_seite(pdf, g)
            teil = haupt if s['teil'] == 'haupt' else anm
            if k > 0:
                strom.append(f'[S. {g}]')
            strom += teil
            if s['teil'] == 'haupt' and any(x.strip() for x in anm):
                noten += [f'[S. {g}]'] + anm
        text = '\n'.join(strom)
        a = re.search(s['anfang'], text)
        if not a:
            pruef.append(f'{name}: Anfang nicht gefunden')
            continue
        e = re.search(s['ende'], text[a.start():], re.S)
        if not e:
            pruef.append(f'{name}: Ende nicht gefunden')
            continue
        ausschnitt = text[a.start():a.start() + e.end()]
        absaetze = fuege(ausschnitt.split('\n'), log, name)
        with open(os.path.join(ziel, 'elze', 'an_trubar', name + '.txt'), 'w', encoding='utf8') as f:
            f.write('\n\n'.join(absaetze) + '\n')
        if noten:
            with open(os.path.join(ziel, 'elze', 'an_trubar', name + '_anm.txt'), 'w', encoding='utf8') as f:
                f.write('Anmerkungsteil (unter dem Stern) der Seiten, auf denen das Stueck steht. '
                        'Die Anmerkungen koennen auch zu Nachbarstuecken gehoeren.\n\n')
                f.write('\n\n'.join(fuege(noten, log, name + '_anm')) + '\n')
        zeilen_csv.append([f'elze/an_trubar/{name}.txt', 'Elze 1897', s['nr'], seiten[0], seiten[-1],
                           sum(len(x.split()) for x in absaetze), s['teil'], s['form']])
    with open(os.path.join(ziel, 'elze', 'stuecke.csv'), 'w', encoding='utf8', newline='') as f:
        w = csv.writer(f, delimiter=';')
        w.writerow(['datei', 'edition', 'laufende_nummer', 'seite_von', 'seite_bis', 'woerter', 'steht_im', 'form'])
        w.writerows(zeilen_csv)
    with open(os.path.join(ziel, 'elze', 'protokoll_schnitt.txt'), 'w', encoding='utf8') as f:
        f.write('AUFFAELLIGKEITEN\n' + ('\n'.join(pruef) or 'keine') + '\n\nEINGRIFFE AN ZEILENENDEN\n' + ('\n'.join(log) or 'keine') + '\n')
    print(len(zeilen_csv), 'Stuecke;', len(pruef), 'Auffaelligkeiten;', len(log), 'Trennstriche zusammengefuehrt')


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
