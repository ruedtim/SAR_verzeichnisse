"""Suchlauf «Gruppenende, enger Filter» (NP15): wie `suchlauf_gruppenende.py` mit Faktor 1,0, also auch Zeilen mit dem Abstand
eines neuen Eintrags, aber nur die Lagen, die zu Regel 3 der Runde 12 passen. Die breite Liste besteht fast nur aus
Listeneinträgen der letzten Unternummer; die fallen hier weg.

Für die erste Zeile nach der letzten Untereinheit c einer Gruppe g, deren Abstand grösser ist als der übliche Abstand vor einem
neuen Eintrag und deren Text im Darin von c steht, wird die Lage bestimmt:
  x_sig = Einzug der Signatur von c, x_text = Einzug des Titels von c (erstes Wort nach der Signatur),
  x_zeile = Einzug der Kandidatenzeile, davor = Zahl der Zeilen von c zwischen Signaturzeile und Kandidat,
  x_davor = häufigster Einzug dieser Zeilen.
Lage:
  A «links vom Text»     x_zeile < x_text − 3 (Regel 3a: Vermerk auf der Höhe der Unternummern)
  B «Textspalte, gleich nach c»  |x_zeile − x_text| ≤ 3 und davor = 0 (Regel 3b: Eintrag ohne Nummer in der Textspalte)
  C «wie die Zeilen davor»  davor > 0 und |x_zeile − x_davor| ≤ 3 – Fortsetzung des Inhalts von c, fällt weg
  D «eingerückt, gleich nach c»  x_zeile > x_text + 3 und davor = 0 – eigene Beschreibung von c, fällt weg
  B2 «wie die Zeilen davor, aber neuer Absatz»: Einzug wie die Zeilen von c, Abstand > 1,3 × der Abstände in c (K208)
  G «wie der Inhalt der Geschwister»: Einzug wie mindestens 30 % der Inhaltszeilen der Geschwister und Abstand wie dort
     (Listen in der Signaturspalte, VII.200.) – fällt weg
  E sonst (zur Sichtung)
Gemeldet werden A, B und E, dazu je Gruppe, ob alle direkten Untereinheiten Einzelabsätze ohne eigene Untereinheiten sind
(Bedingung von Regel 3b).
Aufruf: python -I suchlauf_gruppenende_eng.py <cache> <excel_ordner> <aus.csv> [faktor]"""
import collections, csv, glob, json, os, re, statistics, sys
import openpyxl

cache, o, aus = sys.argv[1:4]
FAKTOR = float(sys.argv[4]) if len(sys.argv) > 4 else 1.0


def nrn(s):
    return re.sub(r"\s+", "", str(s or "")).rstrip(".")


def norm(s):
    return re.sub(r"[^0-9a-zäöüß]", "", str(s or "").lower())


out = []
zaehler = collections.Counter()
for p in sorted(glob.glob(f"{o}/D*_scope_import.xlsx")):
    d = os.path.basename(p).split("_")[0]
    if not os.path.exists(f"{cache}/{d}.zeilen.json"):
        continue
    ws = openpyxl.load_workbook(p, read_only=True)["scope-Import"]
    rows = list(ws.iter_rows(values_only=True)); h = rows[0]
    ee = [dict(zip(h, r)) for r in rows[1:] if r and r[0] is not None]
    if len(ee) < 3:
        continue
    zz = json.load(open(f"{cache}/{d}.zeilen.json", encoding="utf-8"))["zeilen"]
    seiten = collections.defaultdict(list)
    for i, z in enumerate(zz):
        if z["worte"]:
            seiten[z["seite"]].append(i)
    belegt, pos, wortzahl = set(), {}, {}
    for e in ee:
        nr = nrn(e.get("Nr. im PDF"))
        if not nr or e.get("Teil"):
            continue
        for i in seiten.get(e.get("PDF-Seite"), []):
            if i in belegt:
                continue
            kette = ""
            for j, w in enumerate(zz[i]["worte"][:6]):
                kette += re.sub(r"\s+", "", w[0])
                if len(kette) >= len(nr):
                    break
            if kette.startswith(nr) and re.fullmatch(r"[.):,;\]]*", kette[len(nr):]):
                pos[e["ID"]] = i; belegt.add(i); wortzahl[e["ID"]] = j + 1; break
    if len(pos) < 3:
        continue
    idx = {e["ID"]: e for e in ee}
    kinder = collections.defaultdict(list)
    for e in ee:
        if e.get("Parent-ID") in idx and not e.get("Teil"):
            kinder[e["Parent-ID"]].append(e)
    abst = []
    for i in pos.values():
        j = i - 1
        while j >= 0 and not zz[j]["worte"]:
            j -= 1
        if j >= 0 and zz[j]["seite"] == zz[i]["seite"]:
            abst.append(zz[i]["top"] - zz[j]["top"])
    if not abst:
        continue
    ueblich = statistics.median(abst)
    reihe = sorted((i, eid) for eid, i in pos.items())
    stelle = {eid: k for k, (i, eid) in enumerate(reihe)}

    def nachfahre(x, g):
        while x and x.get("Parent-ID") in idx:
            if x["Parent-ID"] == g:
                return True
            x = idx[x["Parent-ID"]]
        return False

    for g in ee:
        if g["ID"] not in pos or not kinder.get(g["ID"]):
            continue
        k = stelle[g["ID"]]
        ende = len(zz)
        letzte = None
        for (i, eid) in reihe[k + 1:]:
            x = idx[eid]
            if nachfahre(x, g["ID"]):
                letzte = (i, x)
                continue
            ende = i
            break
        if not letzte:
            continue
        i_c, c = letzte
        darin = norm(c.get("Darin"))
        if not darin:
            continue
        vor = i_c
        davor = []
        for i in range(i_c + 1, ende):
            z = zz[i]
            if not z["worte"] or z["top"] < 60 or z["top"] > 800:
                continue
            if zz[vor]["seite"] == z["seite"]:
                gap = z["top"] - zz[vor]["top"]
                text = " ".join(w[0] for w in z["worte"])
                if gap > FAKTOR * ueblich and len(norm(text)) >= 8 and norm(text) in darin:
                    wc = zz[i_c]["worte"]
                    x_sig = wc[0][1]
                    nw = wortzahl.get(c["ID"], 1)
                    if len(wc) > nw:
                        x_text = wc[nw][1]
                    else:   # Titel erst auf der nächsten Zeile
                        nxt = next((zz[j] for j in range(i_c + 1, i) if zz[j]["worte"]), None)
                        x_text = nxt["worte"][0][1] if nxt else z["worte"][0][1]
                    x_z = z["worte"][0][1]
                    x_davor = collections.Counter(round(zz[j]["worte"][0][1]) for j in davor).most_common(1)[0][0] if davor else None
                    # Abstände innerhalb von c (Signaturzeile -> Zeilen davor), auf derselben Seite
                    kette_c = [i_c] + davor
                    innen = [zz[b]["top"] - zz[a]["top"] for a, b in zip(kette_c, kette_c[1:]) if zz[a]["seite"] == zz[b]["seite"]]
                    neuer_absatz = not innen or gap > 1.3 * max(innen)
                    # Inhaltszeilen der Geschwister von c: Einzug und Abstand
                    gx, gg = collections.Counter(), []
                    for s in kinder[g["ID"]]:
                        if s["ID"] == c["ID"] or s["ID"] not in pos:
                            continue
                        a0 = pos[s["ID"]]
                        nach = [i2 for (i2, _) in reihe if i2 > a0]
                        b0 = nach[0] if nach else len(zz)
                        vorig = a0
                        for i2 in range(a0 + 1, min(b0, a0 + 40)):
                            if zz[i2]["worte"] and 60 <= zz[i2]["top"] <= 800:
                                gx[round(zz[i2]["worte"][0][1])] += 1
                                if zz[i2]["seite"] == zz[vorig]["seite"] and vorig != a0:
                                    gg.append(zz[i2]["top"] - zz[vorig]["top"])
                                vorig = i2
                    gsum = sum(gx.values())
                    wie_geschw = gsum >= 3 and sum(v for xx, v in gx.items() if abs(xx - x_z) <= 3) >= 0.3 * gsum \
                        and gg and gap <= 1.3 * statistics.median(gg)
                    if wie_geschw:
                        lage = "G wie der Inhalt der Geschwister"
                    elif x_z < x_text - 3:
                        lage = "A links vom Text"
                    elif abs(x_z - x_text) <= 3 and not davor:
                        lage = "B Textspalte, gleich nach c"
                    elif davor and abs(x_z - x_davor) <= 3 and not neuer_absatz:
                        lage = "C wie die Zeilen davor"
                    elif davor and abs(x_z - x_davor) <= 3:
                        lage = "B2 wie die Zeilen davor, aber neuer Absatz"
                    elif x_z > x_text + 3 and not davor:
                        lage = "D eingerückt, gleich nach c"
                    else:
                        lage = "E sonst"
                    zaehler[lage[0]] += 1
                    kk = kinder[g["ID"]]
                    einzel = all(not kinder.get(x["ID"]) and len([t for t in str(x.get("Darin") or "").split("\n") if t.strip()]) <= 1
                                 for x in kk if x["ID"] != c["ID"])
                    if lage[0] in "ABE":   # B2 beginnt mit B
                        out.append({"datei": d, "gruppe": f"{g['ID']} {g['Signatur']}", "letzte_untereinheit": f"{c['ID']} {c['Signatur']}",
                                    "seite": z["seite"], "y": round(z["top"]), "abstand": round(gap, 1), "ueblich": round(ueblich, 1),
                                    "x_sig": round(x_sig), "x_text": round(x_text), "x_zeile": round(x_z),
                                    "zeilen_davor": len(davor), "x_davor": x_davor if x_davor is not None else "",
                                    "lage": lage, "geschwister_einzelabsatz": "ja" if einzel else "nein", "zeile": text[:100]})
                    break
            davor.append(i)
            vor = i
with open(aus, "w", encoding="utf-8", newline="") as f:
    felder = ["datei", "gruppe", "letzte_untereinheit", "seite", "y", "abstand", "ueblich", "x_sig", "x_text", "x_zeile",
              "zeilen_davor", "x_davor", "lage", "geschwister_einzelabsatz", "zeile"]
    w = csv.DictWriter(f, fieldnames=felder, delimiter=";")
    w.writeheader(); w.writerows(out)
print(len(out), "Kandidaten (A/B/E) in", len({x["datei"] for x in out}), "Dateien; Lagen gesamt:", dict(sorted(zaehler.items())))
