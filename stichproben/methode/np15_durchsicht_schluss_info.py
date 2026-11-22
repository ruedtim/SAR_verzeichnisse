"""Durchsicht «Schlussteil und Info» (NP15): je Datei ein Block mit allem, was am Ende des Verzeichnisses oder neben den
Einheiten steht. Gedacht zum vollständigen Durchsehen aller 715 Dateien, nicht als Suchlauf mit Muster.

Je Datei:
  [Schluss]   die Zeilen der Prüfmappe ab der Zeile der letzten Einheit (PDF-Folge) bis zum Ende, mit ihrem Ort in der Excel.
              Lange Schlussteile (> MAX Zeilen): die ersten 15 und die letzten MAX-15 Zeilen.
  [Letzte]    die letzte Einheit ganz: Signatur, Stufe, Eltern, Titel, Zeitraum, Schachtel, Umfang, Darin (Ende), Prüfhinweise.
  [Bestand]   die Bestandszeile, falls vorhanden (Titel, Darin).
  [Info]      die Zeilen von «Schlussvermerke im Findmittel», die im [Schluss]-Block nicht vorkommen (sonst nur ein Verweis).
  [Nicht übernommen]  die Liste im Blatt Vollständigkeit (Art, Seite, Zeile), ohne Tabellenköpfe der Form «Signatur Titel Zeit».
  [Vorspann]  «Signaturen nur im Vorspann», falls nicht «–».

Aufruf: python -I durchsicht_schluss_info.py <excel_ordner> <mappen_ordner> <aus_ordner> <teile> [MAX]
Schreibt <aus_ordner>/teil_<k>.txt (Dateien nach Name verteilt, Teile etwa gleich gross) und uebersicht.csv."""
import csv, glob, os, re, sys
import openpyxl

o, mappen, aus, teile = sys.argv[1:5]
teile = int(teile)
MAX = int(sys.argv[5]) if len(sys.argv) > 5 else 40
os.makedirs(aus, exist_ok=True)
KOPF = re.compile(r"^(Signatur|Sign\.?|Nr\.?|Nummer|Archivsignatur)\b.{0,40}\b(Titel|Inhalt|Bezeichnung|Gegenstand|Zeit|Jahr|Datum)\b"
                  r"[\w\s,./()-]{0,60}$", re.I)


def n(s):
    return re.sub(r"[^0-9a-zäöüß]", "", str(s or "").lower())


# Fusszeilen («© Stadtarchiv Zürich», «Seite 3 von 9», Seitenzahl allein) zeigen nichts über die Zuordnung
FUSS = re.compile(r"©\s*Stadtarchiv|Seite \d+ von \d+|\|\s*-?\s*\d{1,3}\s*-?\s*→ \?$")


def kurz(z):
    """Prüfmappenzeile kürzer: Lage kompakt, bei EINHEIT ohne den wiederholten Titel."""
    z = re.sub(r"^S(\d+)\s+(\d+) \| x\s*(\d+) (\S*)\s*\| ", r"S\1 y\2 x\3 \4 | ", z)
    z = re.sub(r" \| T: [^|]*", "", z)
    return z


bloecke = []
for p in sorted(glob.glob(f"{o}/D*_scope_import.xlsx")):
    d = os.path.basename(p).split("_")[0]
    mp = f"{mappen}/{d}.txt"
    if not os.path.exists(mp):
        bloecke.append((d, f"### {d} – keine Prüfmappe\n", {"datei": d, "fehler": "keine Prüfmappe"}))
        continue
    wb = openpyxl.load_workbook(p, read_only=True)
    rows = list(wb["scope-Import"].iter_rows(values_only=True))
    h = rows[0]
    ee = [dict(zip(h, r)) for r in rows[1:] if r and r[0] is not None]
    idx = {e["ID"]: e for e in ee}
    info = {}
    for x in wb["Info"].iter_rows(values_only=True):
        if x and x[0]:
            info.setdefault(str(x[0]), x[1])
    vliste, vkopf = [], {}
    kopf = None
    for x in wb["Vollständigkeit"].iter_rows(values_only=True):
        if x and x[0] == "PDF-Seite":
            kopf = x
            continue
        if kopf and x and x[0] is not None:
            r = dict(zip(kopf, x))
            vliste.append(r)
        elif x and x[0] and not kopf:
            vkopf[str(x[0])] = x[1]
    zeilen = open(mp, encoding="utf-8").read().split("\n")
    try:
        a = next(i for i, z in enumerate(zeilen) if z.startswith("== PDF:"))
        b = next(i for i, z in enumerate(zeilen) if z.startswith("== Excel:"))
    except StopIteration:
        bloecke.append((d, f"### {d} – Prüfmappe ohne PDF-Teil\n", {"datei": d, "fehler": "Prüfmappe ohne PDF-Teil"}))
        continue
    pdf = zeilen[a + 1:b]
    letzte_i = max((i for i, z in enumerate(pdf) if "→ EINHEIT ID " in z), default=None)
    out = []
    bestand = [e for e in ee if e.get("Stufe") == "Bestand"]
    letzte = None
    if letzte_i is not None:
        m = re.search(r"→ EINHEIT ID (\d+)", pdf[letzte_i])
        letzte = idx.get(int(m.group(1))) if m else None
    out.append(f"### {d} – Bestand {info.get('Bestand')} – {len(ee)} Einheiten – Bestandszeile: {'ja' if bestand else 'nein'}"
               f" – letzte Einheit (PDF-Folge): {('ID ' + str(letzte['ID']) + ' ' + str(letzte['Signatur'])) if letzte else '–'}")
    schluss = pdf[letzte_i:] if letzte_i is not None else pdf[-MAX:]
    schluss = [z for z in schluss if z.strip() and not FUSS.search(z)]
    schluss = [kurz(z) for z in schluss]
    # Abstandsmarke «⇣»: Zeile mit mehr als doppeltem üblichem Zeilenabstand zur vorigen Zeile derselben Seite
    lage = [re.match(r"^S(\d+) y(\d+) ", z) for z in schluss]
    alle = [re.match(r"^S(\d+)\s+(\d+) \|", z) for z in pdf]   # üblicher Zeilenabstand aus der ganzen Datei
    abst = [int(b.group(2)) - int(a.group(2)) for a, b in zip(alle, alle[1:]) if a and b and a.group(1) == b.group(1)
            and int(b.group(2)) > int(a.group(2))]
    ueblich = sorted(abst)[len(abst) // 2] if abst else None
    if ueblich:
        for k in range(1, len(schluss)):
            a, b = lage[k - 1], lage[k]
            if a and b and a.group(1) == b.group(1) and int(b.group(2)) - int(a.group(2)) > 2 * ueblich:
                schluss[k] = "⇣ " + schluss[k]
    verdichtet = any("weitere unauffällige Zeilen" in z for z in schluss) or len(schluss) > MAX
    out.append(f"[Schluss] {len(schluss)} PDF-Zeilen ab der letzten Einheit (S y x Schrift | Text → Ort; ⇣ = grosser Abstand)")
    if len(schluss) > MAX:
        out.extend(schluss[:10])
        out.append(f"      … {len(schluss) - MAX} Zeilen ausgelassen …")
        out.extend(schluss[-(MAX - 10):])
    else:
        out.extend(schluss)
    if letzte:
        darin = [x for x in str(letzte.get("Darin") or "").split("\n") if x.strip()]
        dz = " / ".join(darin)
        if len(dz) > 350:
            dz = "… " + dz[-350:]
        eltern = idx.get(letzte.get("Parent-ID"))
        out.append(f"[Letzte] ID {letzte['ID']} {letzte['Signatur']}{' T' + str(letzte['Teil']) if letzte.get('Teil') else ''}"
                   f" ({letzte['Stufe']}, E{letzte['Ebene']}, Eltern {('ID ' + str(eltern['ID']) + ' ' + str(eltern['Signatur'])) if eltern else '-'})"
                   f" | Sch.{letzte['Schachtel-Nr.'] or '-'} | {letzte['von'] or ''}–{letzte['bis'] or ''}"
                   f"{' | U: ' + str(letzte['Umfang']) if letzte.get('Umfang') else ''}")
        out.append(f"   Titel: {str(letzte['Titel'])[:250]}")
        if darin and verdichtet:   # sonst stehen die Darin-Zeilen oben im Schluss
            out.append(f"   Darin ({len(darin)} Z., Ende): {dz}")
        elif darin:
            out.append(f"   Darin: {len(darin)} Z. (oben im Schluss)")
        if letzte.get("Prüfhinweise"):
            out.append(f"   Hinweise: {str(letzte['Prüfhinweise'])[:300].replace(chr(10), ' / ')}")
    for e in bestand:
        darin = [x for x in str(e.get("Darin") or "").split("\n") if x.strip()]
        out.append(f"[Bestand] ID {e['ID']} {e['Signatur']} | T: {str(e['Titel'])[:200]}"
                   f"{' | Darin: ' + ' / '.join(darin)[:600] if darin else ''}")
    sv = [x.strip() for x in str(info.get("Schlussvermerke im Findmittel") or "").split("\n") if x.strip() and x.strip() != "–"]
    schluss_n = n(" ".join(schluss))
    sv_rest = [x for x in sv if n(x)[:40] not in schluss_n]
    if sv:
        out.append(f"[Info] Schlussvermerke: {len(sv)} Zeilen" + (f", davon {len(sv) - len(sv_rest)} oben im Schluss" if len(sv) != len(sv_rest) else ""))
        for x in sv_rest:
            out.append(f"   {x[:300]}")
    nu = [r for r in vliste if r.get("Art") and not (r.get("Art") == "Text vor der ersten Signatur" and KOPF.match(str(r.get("Zeile im PDF") or "")))]
    if nu:
        out.append(f"[Nicht übernommen] {len(nu)} Zeilen")
        for r in nu:
            extra = f" | fehlt: {r.get('Fehlt im Import')}" if r.get("Fehlt im Import") else ""
            ort = f" | bei ID {r.get('ID')} {r.get('Signatur')}" if r.get("ID") else ""
            out.append(f"   S{r.get('PDF-Seite')} {r.get('Art')}: {str(r.get('Zeile im PDF') or '')[:200]}{extra}{ort}")
    sv_vor = str(vkopf.get("Signaturen nur im Vorspann") or info.get("Signaturen nur im Vorspann") or "–")
    if sv_vor not in ("–", "None"):
        out.append(f"[Vorspann] Signaturen nur im Vorspann: {sv_vor[:300]}")
    text = "\n".join(out) + "\n"
    bloecke.append((d, text, {"datei": d, "einheiten": len(ee), "schluss_zeilen": len(schluss), "info_zeilen": len(sv),
                              "info_rest": len(sv_rest), "nicht_uebernommen": len(nu), "zeichen": len(text)}))

# auf Teile verteilen (Reihenfolge nach Name, Teile etwa gleich viele Zeichen)
gesamt = sum(len(t) for _, t, _ in bloecke)
ziel = gesamt / teile
k, summe, teil_von = 1, 0, {}
for d, t, _ in bloecke:
    if summe >= ziel * k and k < teile:
        k += 1
    teil_von[d] = k
    summe += len(t)
for k in range(1, teile + 1):
    with open(f"{aus}/teil_{k}.txt", "w", encoding="utf-8") as f:
        for d, t, _ in bloecke:
            if teil_von[d] == k:
                f.write(t + "\n")
with open(f"{aus}/uebersicht.csv", "w", encoding="utf-8", newline="") as f:
    felder = ["datei", "teil", "einheiten", "schluss_zeilen", "info_zeilen", "info_rest", "nicht_uebernommen", "zeichen", "fehler"]
    w = csv.DictWriter(f, fieldnames=felder, delimiter=";")
    w.writeheader()
    for d, t, r in bloecke:
        w.writerow({**r, "teil": teil_von[d]})
print(len(bloecke), "Dateien,", gesamt, "Zeichen,", teile, "Teile à etwa", round(ziel), "Zeichen")
