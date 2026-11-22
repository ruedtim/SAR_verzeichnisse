"""Prüfmappe je Findmittel: jede PDF-Zeile (Seite, y, x, Schrift) mit dem Ort, an dem ihr Text in der Excel steht
(ID + Feld, Blatt Vollständigkeit/Info oder «?»), dazu Warnzeichen, und danach alle Einheiten kompakt.
Warnzeichen:
  [SIG?]   Zeile beginnt in der Signaturspalte mit einer Signaturform der Datei, ist aber keine Einheit
  [VOR]    Text steht bei einer Einheit, deren Zeile im PDF erst später kommt (Verschiebung?)
  [NACH]   Text steht bei einer Einheit, nach deren Ende im PDF schon eine andere Einheit begann
  [NICHT]  Text in keinem importierten Feld (Blatt Vollständigkeit/Info) – Verzeichnistext oder Vorspann?
  [?]      Text nicht wiedergefunden (oft nur Datum/Schachtel in eigenen Feldern, Umbruch)
Aufruf: python -I pruefmappe.py <cache> <excel_ordner> <aus_ordner> D [D ...]"""
import collections, json, os, re, sys
import openpyxl

cache, o, aus, *dd = sys.argv[1:]
os.makedirs(aus, exist_ok=True)


def n(s):
    return re.sub(r"[^0-9a-zäöüß]", "", str(s or "").lower())


def form(t):
    t = re.sub(r"\d+", "9", re.sub(r"\s+", "", str(t or "")).rstrip("."))
    return re.sub(r"[a-z]+", "a", t)


DATUM = re.compile(r"^\d{1,2}\.\d{1,2}\.\d{2,4}$|^\d{1,2}\.\d{4}$|^(1[2-9]|20)\d\d$")

for d in dd:
    zz = json.load(open(f"{cache}/{d}.zeilen.json", encoding="utf-8"))["zeilen"]
    wb = openpyxl.load_workbook(f"{o}/{d}_scope_import.xlsx", read_only=True)
    rows = list(wb["scope-Import"].iter_rows(values_only=True))
    h = rows[0]
    ee = [dict(zip(h, r)) for r in rows[1:] if r and r[0] is not None]
    info = {}
    for x in wb["Info"].iter_rows(values_only=True):
        if x and x[0]:
            info.setdefault(str(x[0]), x[1])
    voll_rows = list(wb["Vollständigkeit"].iter_rows(values_only=True))
    vkopf = {}
    vliste = []
    for x in voll_rows:
        if not x or x[0] is None:
            continue
        if isinstance(x[0], (int, float)) and len(x) > 2:
            vliste.append((int(x[0]), str(x[1] or ""), str(x[2] or "")))
        elif str(x[0]) not in vkopf:
            vkopf[str(x[0])] = x[1] if x[1] is not None else (x[2] if len(x) > 2 else None)
    vmap = collections.defaultdict(list)
    for s, art, t in vliste:
        vmap[n(t)[:30]].append((s, art))
    schluss = n(info.get("Schlussvermerke im Findmittel"))
    # Felder je Einheit
    felder = []
    for e in ee:
        for k in ("Signatur", "Titel", "Umfang", "Entstehungszeitraum, Anm.", "Verwandte Verzeichnungseinheiten", "Schachtel-Nr."):
            if k in e and e[k]:
                felder.append((e, k, n(e[k])))
        for i, dz in enumerate(str(e.get("Darin") or "").split("\n")):
            if dz.strip():
                felder.append((e, f"Darin {i + 1}", n(dz)))
    # Zeile jeder Einheit (Signatur am Zeilenanfang)
    seiten = collections.defaultdict(list)
    for i, z in enumerate(zz):
        if z["worte"]:
            seiten[z["seite"]].append(i)
    start = {}
    xs = collections.Counter()
    formen = set()
    belegt = set()
    for e in ee:
        nr = re.sub(r"\s+", "", str(e["Nr. im PDF"] or "")).rstrip(".")
        if not nr or e.get("Teil"):
            continue
        for i in seiten.get(e["PDF-Seite"], []):
            if i in belegt:
                continue
            t = re.sub(r"\s+", "", " ".join(w[0] for w in zz[i]["worte"][:4])).rstrip(".")
            if t.startswith(nr) and not t[len(nr):len(nr) + 1].isdigit():
                start[e["ID"]] = i
                belegt.add(i)
                xs[round(zz[i]["worte"][0][1])] += 1
                formen.add(form(zz[i]["worte"][0][0]))
                break
    spalten = [x for x, c in xs.items() if c >= 2] or list(xs)
    formen |= {f + "a" for f in formen}
    reihe = sorted((i, eid) for eid, i in start.items())
    naechste = {}
    for (i, eid), nachf in zip(reihe, reihe[1:] + [(10 ** 9, None)]):
        naechste[eid] = nachf[0]
    idx = {e["ID"]: e for e in ee}
    if start:
        erste = min(start.values())
    else:
        s1 = min([e["PDF-Seite"] or 1 for e in ee] or [1])
        erste = min(seiten.get(s1, [0]) or [0])
    MONAT = re.compile(r"^(Jan|Feb|Mär|Apr|Mai|Jun|Jul|Aug|Sep|Okt|Nov|Dez)", re.I)
    out = []
    g = info.get("Gliederung")
    out.append(f"### {d} – Gliederung: {g} – {len(ee)} Einheiten – PDF bis S. {max([z['seite'] for z in zz] or [0])}")
    out.append(f"Bestand: {info.get('Bestand')} | Schlussvermerke: {str(info.get('Schlussvermerke im Findmittel') or '–')[:300]!r}")
    out.append("Vollständigkeit: " + "; ".join(f"{k}: {str(v)[:90]}" for k, v in vkopf.items()
                                                if k in ("davon im Import gefunden", "Nicht übernommen", "Schlussvermerke",
                                                         "Übersichtszeilen", "Vorspann (nicht importiert)", "Signaturen nur im Vorspann")))
    out.append("== PDF: Seite y | x Schriftgrösse (B = fett, K = kursiv) | Text → Ort in der Excel  [Warnzeichen]  (Kopf-/Fusszeilen, die auf 3+ Seiten wiederkehren, nur einmal; lange Läufe unauffälliger Darin-Zeilen verdichtet – nie Zeilen mit Warnzeichen, in der Signaturspalte, fett oder mit Signaturform am Anfang)")
    warn = collections.Counter()
    pdfz = []
    SIGART = re.compile(r"^\s*(?:[A-Z]{1,3}\s?\d|[IVXL]+[.)]|\d+[a-z]?[.:)]|\d+\s*[:.]\s*\d|[a-z][.)]\s|[A-Z][.)]\s|\(?[A-Z]\.[A-Z]|[IVX]+\.[A-Z])")
    kf = collections.defaultdict(set)
    for z in zz:
        if z["worte"]:
            kf[re.sub(r"\d+", "#", " ".join(x[0] for x in z["worte"]))].add(z["seite"])
    wiederholt = {k for k, v in kf.items() if len(v) >= 3}
    gezeigt = set()
    for i, z in enumerate(zz):
        w = z["worte"]
        if not w:
            continue
        kk = re.sub(r"\d+", "#", " ".join(x[0] for x in w))
        if kk in wiederholt and i not in belegt:
            if kk in gezeigt:
                continue
            gezeigt.add(kk)
        text = " ".join(x[0] for x in w)
        font = w[0][3] if len(w[0]) > 3 else ""
        gr = w[0][4] if len(w[0]) > 4 else ""
        stil = ("B" if "bold" in str(font).lower() else "") + ("K" if "italic" in str(font).lower() or "oblique" in str(font).lower() else "")
        ziel, marke = "?", ""
        if i in belegt:
            eid = [k for k, v in start.items() if v == i][0]
            e = idx[eid]
            hw = str(e.get("Prüfhinweise") or "").replace("\n", " / ")
            hw = " | H: " + hw[:90] if re.search(r"Signatur|übergeordnet|Nummerierung|erneut|Teil|Überschrift|Liste|Darin", hw) else ""
            ziel = (f"EINHEIT ID {eid} {e['Signatur']}{' T' + str(e['Teil']) if e.get('Teil') else ''} ({e['Stufe']}, E{e['Ebene']}, Eltern {e['Parent-ID'] or '-'})"
                    f" | Sch.{e['Schachtel-Nr.'] or '-'} | {e['von'] or ''}–{e['bis'] or ''} | T: {str(e['Titel'])[:80]}"
                    f"{' | U: ' + str(e['Umfang'])[:30] if e.get('Umfang') else ''}"
                    f"{' | Darin ' + str(len([x for x in str(e.get('Darin') or '').split(chr(10)) if x.strip()])) + ' Z.' if e.get('Darin') else ''}{hw}")
        else:
            # Text ohne führende Nummer und ohne Datum/Schachtel am Ende
            ww = [x[0] for x in w]
            while ww and re.fullmatch(r"[\d–\-/.,;:()]+", ww[-1]):
                ww.pop()
            probe = n(" ".join(ww))
            if len(probe) < 4:
                probe = n(text)
            probe = probe[:24]
            kand = [(e, k) for e, k, t in felder if probe and probe in t] if len(probe) >= 4 else []
            if kand and i < erste:
                e, k = kand[0]
                ziel = f"Vorspann-Bereich (Text auch in ID {e['ID']} {k})"
            elif kand:
                # nächste Einheit nach PDF-Reihenfolge bevorzugen
                def abst(ek):
                    s0 = start.get(ek[0]["ID"])
                    return abs((s0 if s0 is not None else 10 ** 6) - i)
                e, k = min(kand, key=abst)
                ziel = f"ID {e['ID']} {k}"
                s0 = start.get(e["ID"])
                if s0 is not None and k != "Signatur":
                    if i < s0:
                        marke = "[VOR]"
                    elif i >= naechste.get(e["ID"], 10 ** 9) and not e.get("Teil"):
                        marke = "[NACH]"
            else:
                key = n(text)[:30]
                if key in vmap:
                    ziel = "Vollst.: " + vmap[key][0][1]
                    marke = "[NICHT]"
                elif len(n(text)) >= 6 and n(text)[:24] in schluss:
                    ziel = "Info: Schlussvermerk"
                    marke = "[NICHT]"
                elif i < erste:
                    ziel = "Vorspann-Bereich"
        if (i not in belegt and i >= erste and not (len(w) > 1 and MONAT.match(w[1][0])) and any(abs(w[0][1] - x) <= 3 for x in spalten) and form(w[0][0]) in formen
                and re.search(r"\d", w[0][0]) and not DATUM.match(re.sub(r"\s+", "", w[0][0]).rstrip("."))):
            marke = (marke + " [SIG?]").strip()
        if marke:
            for m in marke.split():
                warn[m] += 1
        tl = 70 if ziel.startswith("Vorspann") else 95
        zeile = f"S{z['seite']:<3} {round(z['top']):>4} | x{round(w[0][1]):>3} {gr}{stil:<2} | {text[:tl]}  → {ziel} {marke}".rstrip()
        m_d = re.match(r"ID (\d+) Darin", ziel)
        unauff = bool(m_d) and not marke and not stil and not any(abs(w[0][1] - x) <= 3 for x in spalten) \
            and not SIGART.match(text)
        pdfz.append((zeile, m_d.group(1) if (m_d and unauff) else None))
    j = 0
    while j < len(pdfz):
        zeile, eid = pdfz[j]
        if eid is None:
            out.append(zeile); j += 1; continue
        k = j
        while k < len(pdfz) and pdfz[k][1] == eid:
            k += 1
        lauf = pdfz[j:k]
        if len(lauf) >= 6:
            out.extend(x[0] for x in lauf[:2])
            out.append(f"      … {len(lauf) - 3} weitere unauffällige Zeilen → ID {eid} Darin …")
            out.append(lauf[-1][0])
        else:
            out.extend(x[0] for x in lauf)
        j = k
    ohne = [e for e in ee if e["ID"] not in start]
    out.append(f"== Excel: {len(ee)} Einheiten; {len(ee) - len(ohne)} oben mit ihrer PDF-Zeile (→ EINHEIT). Hier nur die {len(ohne)} ohne eigene Zeile (Teile, Schachtel-/Mappen-Einheiten, Nr. nicht gefunden):")
    for e in ohne:
        out.append(f"ID {e['ID']} P{e['Parent-ID'] or '-'} E{e['Ebene']} {e['Stufe']} {e['Signatur']}{' T' + str(e['Teil']) if e.get('Teil') else ''}"
                   f" S.{e['PDF-Seite']} Sch.{e['Schachtel-Nr.'] or '-'} | {e['von'] or ''}–{e['bis'] or ''} | {str(e['Titel'])[:150]}"
                   f"{' | U: ' + str(e['Umfang']) if e.get('Umfang') else ''}")
        dz = [x for x in str(e.get("Darin") or "").split("\n") if x.strip()]
        if dz:
            out.append(f"      Darin: {len(dz)} Zeilen, erste: {dz[0][:90]}")
        if e.get("Prüfhinweise"):
            out.append(f"      H: {str(e['Prüfhinweise'])[:200].replace(chr(10), ' / ')}")
    out.insert(3, "Warnzeichen: " + (", ".join(f"{k} {v}" for k, v in sorted(warn.items())) or "keine"))
    open(f"{aus}/{d}.txt", "w", encoding="utf-8").write("\n".join(out) + "\n")
    print(d, len(ee), dict(warn))
