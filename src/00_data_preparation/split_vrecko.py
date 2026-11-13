#!/usr/bin/env python3
"""Splits items Nos. 1-85 from Vrecko/Krajnc-Vrecko (eds.), Primoz Trubar: Pisma (2015).

Usage:    python3 split_vrecko.py <pdf> <target_folder>
Requires: pdftotext (poppler-utils).

The PDF is born-digital. The script reads every line with its coordinates and font
height and sorts it by fixed rules. It does not change a single character.

Rules
- A letter starts on a page whose first line (after the running head) is only the next item number.
- Editorial header: number, addressee, date and references; the letter text begins after the
  third gap (>= KOPF_LUECKE) on the first page.
- Original: from the end of the header to the line "Prevod".
- Translation: from "Prevod" on (not saved; read only to locate footnote anchors).
- Footnotes: lines in small type (height < FN_HOEHE) at the foot of the page.
- Footnote numbers in the text: superscript digits (word height < HOCH_HOEHE), written as [n].
- Paragraphs: a new printed line after a larger gap (> ABSATZ_LUECKE) starts a new paragraph.
- Page breaks: [S. n] in the text.

Output folder and file names, CSV columns and log messages are kept in German so that the
output is identical to the corpus already in use (kopf = header, fussnoten = footnotes,
protokoll_schnitt = cutting log).
"""
import csv, html, os, re, subprocess, sys
from collections import Counter

ERSTE, LETZTE = 13, 349          # PDF pages of the part "Pisma"
FN_HOEHE = 11.5                  # median word height: footnotes 10.8, letter text 13.5
HOCH_HOEHE = 10.0                # superscript digit 9.4
ABSATZ_LUECKE = 14.5             # line spacing 12.0, paragraph spacing 17.7
KLEB = 0.6                       # pt; normal word spacing about 3 pt
KOPF_LUECKE = 16.0               # gaps in the header: number|addressee|date+references|letter text


def lies_seiten(pdf):
    out = subprocess.run(['pdftotext', '-bbox-layout', '-f', str(ERSTE), '-l', str(LETZTE), pdf, '-'],
                         capture_output=True, text=True, check=True).stdout
    seiten = []
    for nr, block in enumerate(out.split('<page ')[1:], start=ERSTE):
        zeilen = []
        for m in re.finditer(r'<line xMin="([\d.]+)" yMin="([\d.]+)" xMax="([\d.]+)" yMax="([\d.]+)">(.*?)</line>', block, re.S):
            x0, y0, x1, y1 = map(float, m.groups()[:4])
            woerter, wx, wx1 = [], [], []
            for w in re.finditer(r'<word xMin="([\d.]+)" yMin="([\d.]+)" xMax="([\d.]+)" yMax="([\d.]+)">(.*?)</word>', m.group(5)):
                h = float(w.group(4)) - float(w.group(2))
                woerter.append((html.unescape(w.group(5)).replace(chr(173), ''), h))   # chr(173): soft hyphen
                wx.append(float(w.group(1)))
                wx1.append(float(w.group(3)))
            if woerter:
                hoehen = sorted(h for _, h in woerter)
                zeilen.append({'x0': x0, 'y0': y0, 'y1': y1, 'x1': x1, 'h': hoehen[len(hoehen) // 2], 'w': woerter, 'wx': wx, 'wx1': wx1})
        # A superscript digit that pdftotext outputs as a line of its own is put back into the
        # text line it belongs to (same height, within the width of the line).
        for m_ in [z for z in zeilen if len(z['w']) == 1 and z['h'] < HOCH_HOEHE and z['w'][0][0].isdigit()]:
            for z in zeilen:
                if z is not m_ and z['h'] >= FN_HOEHE and abs(z['y0'] - m_['y0']) < 6 and z['x0'] < m_['x0'] <= z['x1'] + 20:
                    i = sum(1 for x in z['wx'] if x < m_['x0'])
                    z['w'].insert(i, m_['w'][0])
                    z['wx'].insert(i, m_['x0'])
                    z['wx1'].insert(i, m_['x1'])
                    zeilen.remove(m_)
                    break
        # Lines with the same baseline (difference < 2 pt) form one row, read from left to right
        zeilen.sort(key=lambda z: z['y1'])
        reihe, letzte = 0, None
        for z in zeilen:
            if letzte is not None and z['y1'] - letzte > 2.0:
                reihe += 1
            z['reihe'] = reihe
            letzte = z['y1']
        zeilen.sort(key=lambda z: (z['reihe'], z['x0']))
        seiten.append((nr, zeilen))
    return seiten


def zeilentext(z, marker=True):
    """Text of one line. Superscript digits are attached as [n] to the preceding word.
    Word parts printed without a space (gap < KLEB) are joined without a space, e.g. XVI + superscript o."""
    teile = []
    for i, (wort, h) in enumerate(z['w']):
        if marker and h < HOCH_HOEHE and z['h'] > FN_HOEHE and wort.isdigit():
            if teile:
                teile[-1] += f'[{wort}]'
            else:
                teile.append(f'[{wort}]')
        elif teile and i > 0 and z['wx'][i] - z['wx1'][i - 1] < KLEB and not (z['w'][i - 1][1] < HOCH_HOEHE):
            teile[-1] += wort
        else:
            teile.append(wort)
    return ' '.join(teile)


def roh(z):
    return ' '.join(w for w, _ in z['w'])


def schneide(seiten):
    briefe, akt, erwartet = [], None, 1
    for nr, zeilen in seiten:
        if not zeilen:
            continue
        z = [x for x in zeilen if not (roh(x).lower() == 'pisma' and x['y1'] < 90)]
        z = [x for x in z if not (x['y1'] > 560 and roh(x).isdigit())]
        if z and roh(z[0]) == str(erwartet) and z[0]['h'] > 15:
            akt = {'nr': erwartet, 'seiten': [], 'kopf': [], 'orig': [], 'ueb': [], 'fn': [], 'zone': 'kopf', 'luecken': 0}
            briefe.append(akt)
            erwartet += 1
        if akt is None:
            continue
        akt['seiten'].append(nr)
        fuss = [x for x in z if HOCH_HOEHE <= x['h'] < FN_HOEHE]
        vor = None
        erste_der_seite = True
        for x in z:
            if x['h'] < HOCH_HOEHE and roh(x).isdigit():
                # superscript digit standing alone at the start of a line: belongs after the last word before it
                if akt[akt['zone']]:
                    akt[akt['zone']][-1]['t'] += f'[{roh(x)}]'
                continue
            if x['h'] < FN_HOEHE:
                continue
            luecke = (x['y1'] - vor['y1']) if vor is not None else 0
            if akt['zone'] == 'kopf' and vor is not None and x['y0'] - vor['y0'] >= KOPF_LUECKE:
                akt['luecken'] += 1
                if akt['luecken'] >= 3:      # 1: number->addressee, 2: addressee->date, 3: references->letter text
                    akt['zone'] = 'orig'
                    luecke = 99
            if roh(x) == 'Prevod' and akt['zone'] != 'ueb':
                akt['zone'] = 'ueb'
                vor = x
                continue
            eintrag = {'t': zeilentext(x), 'neu': luecke > ABSATZ_LUECKE, 'seite': nr, 'seitenanfang': erste_der_seite and len(akt['seiten']) > 1}
            akt[akt['zone']].append(eintrag)
            erste_der_seite = False
            vor = x
        # footnotes of the page
        for x in fuss:
            t = roh(x)
            m = re.match(r'^(\d{1,2})(?:\s+(.*))?$', t) if x['x0'] < 95 else None
            if m:
                akt['fn'].append({'n': int(m.group(1)), 'seite': nr, 'zeilen': [m.group(2)] if m.group(2) else []})
            elif akt['fn']:
                akt['fn'][-1]['zeilen'].append(t)
    return briefe


def fliesstext(eintraege, log, nr):
    """Joins lines into paragraphs. Page breaks as [S. n]."""
    absaetze, akt = [], ''
    for i, e in enumerate(eintraege):
        t = e['t']
        if e['seitenanfang']:
            ende = akt.rstrip()[-1:] if akt else ''
            if akt and ende not in '.!?:':
                akt += f' [S. {e["seite"]}] '
                akt += t
                continue
            if akt:
                absaetze.append(akt)
            akt = f'[S. {e["seite"]}] ' + t
            continue
        if e['neu'] or not akt:
            if akt:
                absaetze.append(akt)
            akt = t
        else:
            if akt.endswith(chr(173)):
                log.append(f'V{nr:03d}: Trennstrich zusammengefuehrt: ...{akt[-20:-1]}|{t[:15]}')
                akt = akt[:-1] + t
            elif akt.endswith('-'):
                log.append(f'V{nr:03d}: Zeile endet mit Bindestrich, unveraendert angeschlossen: ...{akt[-25:]}|{t[:20]}')
                akt += t
            else:
                akt += ' ' + t
    if akt:
        absaetze.append(akt)
    return absaetze


def fn_text(zeilen, log, nr, n):
    s = ''
    for t in zeilen:
        if s.endswith('-') and t[:1].islower():
            log.append(f'V{nr:03d} Fn {n}: Trennstrich zusammengefuehrt: {s[-15:]}|{t[:15]}')
            s = s[:-1] + t
        elif s.endswith(chr(173)):
            s = s[:-1] + t
        else:
            s = (s + ' ' + t) if s else t
    return s


def anker(b, n):
    for zone, name in (('kopf', 'Kopf'), ('orig', 'Original'), ('ueb', 'Uebersetzung')):
        ganz = ' '.join(e['t'] for e in b[zone])
        i = ganz.find(f'[{n}]')
        if i >= 0:
            return name, ganz[max(0, i - 70):i].strip()
    return 'nicht gefunden', ''


def main(pdf, ziel):
    for d in ('original', 'kopf', 'fussnoten'):
        os.makedirs(os.path.join(ziel, 'vrecko', d), exist_ok=True)
    seiten = lies_seiten(pdf)
    briefe = schneide(seiten)
    log, pruef, zeilen_csv = [], [], []
    for b in briefe:
        nr = b['nr']
        name = f'V{nr:03d}'
        absaetze = fliesstext(b['orig'], log, nr)
        with open(os.path.join(ziel, 'vrecko', 'original', name + '.txt'), 'w', encoding='utf8') as f:
            f.write('\n\n'.join(absaetze) + '\n')
        with open(os.path.join(ziel, 'vrecko', 'kopf', name + '_kopf.txt'), 'w', encoding='utf8') as f:
            f.write('\n'.join(e['t'] for e in b['kopf']) + '\n')
        fns = []
        for fn in b['fn']:
            if not fn['zeilen'] and fns:
                continue
            zone, kontext = anker(b, fn['n'])
            fns.append((fn['n'], fn['seite'], zone, kontext, fn_text(fn['zeilen'], log, nr, fn['n'])))
        with open(os.path.join(ziel, 'vrecko', 'fussnoten', name + '_fn.txt'), 'w', encoding='utf8') as f:
            for n, s, zone, kontext, t in fns:
                f.write(f'[{n}] S. {s} | Anker im Teil: {zone} | Stelle: ...{kontext}\n{t}\n\n')
        nummern = [x[0] for x in fns]
        if nummern != list(range(1, len(nummern) + 1)):
            pruef.append(f'{name}: Fussnotennummern nicht lueckenlos: {nummern}')
        for n, s, zone, kontext, t in fns:
            if zone == 'nicht gefunden':
                pruef.append(f'{name}: Fussnote {n} ohne Ziffer im Text')
        if not b['ueb']:
            pruef.append(f'{name}: keine Zeile "Prevod" gefunden')
        if not b['orig']:
            pruef.append(f'{name}: kein Originaltext')
        woerter = sum(len(a.split()) for a in absaetze)
        zeilen_csv.append([f'vrecko/original/{name}.txt', 'Vrecko 2015', nr, b['seiten'][0], b['seiten'][-1], woerter, len(fns)])
    with open(os.path.join(ziel, 'briefe.csv'), 'w', encoding='utf8', newline='') as f:
        w = csv.writer(f, delimiter=';')
        w.writerow(['datei', 'edition', 'nummer_in_edition', 'seite_von', 'seite_bis', 'woerter_original', 'fussnoten'])
        w.writerows(zeilen_csv)
    with open(os.path.join(ziel, 'vrecko', 'protokoll_schnitt.txt'), 'w', encoding='utf8') as f:
        f.write('AUFFAELLIGKEITEN\n' + ('\n'.join(pruef) or 'keine') + '\n\nEINGRIFFE AN ZEILENENDEN\n' + ('\n'.join(log) or 'keine') + '\n')
    print(len(briefe), 'Briefe;', len(pruef), 'Auffaelligkeiten;', len(log), 'Eingriffe an Zeilenenden')
    return briefe


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
