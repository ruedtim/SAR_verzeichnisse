"""Suchlauf «Tippfehler in Dezimalsignaturen» (NP13): Kandidaten, bei denen ein Tippfehler in der Signatur eine Einheit unter
fremde Eltern stellt oder zum Teil einer fremden Einheit macht (Muster 10 der NP12). Die PDF-Folge kommt aus dem Zeilen-Cache:
jede Einheit wird an der ersten freien Zeile ihrer PDF-Seite verankert, die mit «Nr. im PDF» beginnt (danach keine weitere
Stelle: «29.2» greift nicht auf «29.2.9.»).
  AEHNLICH     Die PDF-Nachbarn (vorige und nächste Einheit) lassen eine Signatur erwarten (gleiches Präfix: eine Nummer
               dazwischen; gleiche Signatur: ein weiterer Teil). Die Einheit trägt eine andere Signatur, die sich davon nur in
               1–2 Zeichen unterscheidet, und hängt dadurch unter anderen Eltern als die Nachbarn. Die erwartete Signatur fehlt
               als Einheit (D149628 20.1.2.19., 29.2.9., D4054 10.8.2.10., D150296 3.3.7., D2857 1.224.3., D32837 1.1.2.1.1.).
  AEHNLICH_DA  wie AEHNLICH, die erwartete Signatur gibt es aber schon (D149628 28.1.1.3. vor den Teilen von 27.1.1.3.,
               D4054 10.8.4. zwischen den Teilen von 10.3.4.).
  EINZELN      Einheit ohne Geschwister (einzige ihres Präfixes) mit Hinweis «Übergeordnete Signatur … fehlt», deren PDF-Nachbarn
               unter anderen Eltern stehen und nicht AEHNLICH sind: zur Sichtung.
  LUECKE_ZEILE Die Nummer q.m+1 fehlt, und zwischen den Signaturzeilen von q.m und q.m+2 steht in der Signaturspalte eine Zeile
               mit einer Nummer, die keine Einheit ist (Signatur nicht erkannt, Einheit im Darin?).
  TEIL         Teil >= 2 einer Signatur q.N, deren Nachbarnummer in der Folge fehlt (N-1 fehlt, N-2 da; oder N+1 fehlt, N+2 da),
               oder ein Teil mit anderem Titel in einer Folge mit genau einer Lücke: wohl Tippfehler statt Teil
               (D1473 :113, D1479 :15, D176060 7.4.1.26., D3472 1952.8). Nur Signaturen, die genau zweimal vorkommen, mit
               verschiedenem Titel; Läufe ab drei Nennungen sind Konvention (Planlisten: eine Nummer, mehrere Objekte).
               Spalte «planliste» = ja, wenn die Datei mindestens 10 Teile mit anderem Titel als Teil 1 hat.
Aufruf: python -I suchlauf_tippfehler.py <cache> <excel_ordner> <aus.csv> [D ...]   (ohne D: alle Excel im Ordner)"""
import collections, csv, glob, json, os, re, sys
import openpyxl

cache, o, aus, *dd = sys.argv[1:]
if not dd:
    dd = sorted(os.path.basename(p).split("_")[0] for p in glob.glob(f"{o}/D*_scope_import.xlsx"))


def lokal(sig, bestand):
    s = str(sig or "")
    if ":" in s:
        return s.split(":", 1)[1]
    b = str(bestand or "")
    return s[len(b):] if b and s.startswith(b) else s


def teile(l):
    return tuple(x for x in re.split(r"[.\s]+", str(l).strip().strip(".")) if x)


def num(x):
    return int(x) if re.fullmatch(r"\d+", x) else None


def nrn(s):
    return re.sub(r"\s+", "", str(s or "")).rstrip(".")


def lev(a, b):
    if abs(len(a) - len(b)) > 2:
        return 9
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1]


def worte(t):
    return {w for w in re.findall(r"[a-zäöü]{4,}", str(t or "").lower())}


felder = ["datei", "art", "id", "signatur", "teil", "seite", "vorher", "nachher", "erwartet", "planliste", "titel", "hinweis"]
out = []
stat = collections.Counter()
for d in dd:
    p = f"{o}/{d}_scope_import.xlsx"
    if not os.path.exists(p) or not os.path.exists(f"{cache}/{d}.zeilen.json"):
        stat["ohne Excel/Cache"] += 1
        continue
    zz = json.load(open(f"{cache}/{d}.zeilen.json", encoding="utf-8"))["zeilen"]
    wb = openpyxl.load_workbook(p, read_only=True)
    info = {}
    for x in wb["Info"].iter_rows(values_only=True):
        if x and x[0]:
            info.setdefault(str(x[0]), x[1])
    best = str(info.get("Bestand") or "")
    rows = list(wb["scope-Import"].iter_rows(values_only=True))
    h = rows[0]
    ee = [dict(zip(h, r)) for r in rows[1:] if r and r[0] is not None]
    idx = {e["ID"]: e for e in ee}
    seiten = collections.defaultdict(list)
    for i, z in enumerate(zz):
        if z["worte"]:
            seiten[z["seite"]].append(i)
    belegt, pos = set(), {}

    def passt(i, nr, streng):
        if streng:   # ganze Wörter vom Zeilenanfang, danach nur Satzzeichen («1+2 (…)» passt nicht zu «1»)
            kette = ""
            for w in zz[i]["worte"][:6]:
                kette += re.sub(r"\s+", "", w[0])
                if len(kette) >= len(nr):
                    break
            return kette.startswith(nr) and re.fullmatch(r"[.):,;\]]*", kette[len(nr):]) is not None
        t = re.sub(r"\s+", "", " ".join(w[0] for w in zz[i]["worte"][:6]))
        return t.startswith(nr) and not re.match(r"\.?\d", t[len(nr):])

    for streng in (True, False):
        for e in ee:
            nr = nrn(e.get("Nr. im PDF"))
            if not nr or e["ID"] in pos:
                continue
            for i in seiten.get(e.get("PDF-Seite"), []):
                if i not in belegt and passt(i, nr, streng):
                    pos[e["ID"]] = i
                    belegt.add(i)
                    break
    stat["Einheiten"] += len(ee)
    stat["verankert"] += len(pos)
    loc = {e["ID"]: ".".join(str(int(x)) if x.isdigit() else x for x in teile(lokal(e["Signatur"], best))) for e in ee}
    vorn = {e["ID"]: (str(e["Signatur"]).split(":", 1)[0] if ":" in str(e["Signatur"] or "") else best) for e in ee}
    tt = {k: teile(v) for k, v in loc.items()}
    dez = {k: v for k, v in tt.items() if v and all(re.fullmatch(r"\d+[a-z]?", x) for x in v)}
    vorhanden = {loc[e["ID"]] for e in ee if not e.get("Teil")}
    gruppe = collections.defaultdict(lambda: collections.defaultdict(list))
    for e in ee:
        v = dez.get(e["ID"])
        if v and not e.get("Teil") and num(v[-1]) is not None:
            gruppe[v[:-1]][num(v[-1])].append(e)
    abgedeckt = collections.defaultdict(set)   # Präfix -> Nummern, auch aus «3:1-3», «12a»
    for e in ee:
        mm = re.match(r"(\d+(?:\.\d+)*)", loc[e["ID"]])
        if mm:
            cc = mm.group(1).split(".")
            abgedeckt[tuple(cc[:-1])].add(int(cc[-1]))
    teil1 = {}
    for e in ee:
        if not e.get("Teil"):
            teil1.setdefault(e["Signatur"], e)
    verschieden = sum(1 for e in ee if e.get("Teil") and e["Signatur"] in teil1
                      and not (worte(e.get("Titel")) & worte(teil1[e["Signatur"]].get("Titel"))))
    planliste = "ja" if verschieden >= 10 else ""
    reihe = [e for _, e in sorted((pos[e["ID"]], e) for e in ee if e["ID"] in pos and e["ID"] in dez)]

    def zeile(e, art, vor, nach, erw):
        out.append({"datei": d, "art": art, "id": e["ID"], "signatur": e["Signatur"], "teil": e.get("Teil") or "",
                    "seite": e.get("PDF-Seite"), "vorher": f"{vor['ID']} {vor['Signatur']}" if vor else "",
                    "nachher": f"{nach['ID']} {nach['Signatur']}" if nach else "", "erwartet": erw, "planliste": planliste,
                    "titel": str(e.get("Titel") or "")[:80], "hinweis": str(e.get("Prüfhinweise") or "")[:160].replace("\n", " / ")})
        stat[art] += 1

    def eltern(e):
        """Eltern ohne Teil-Kette: ein Teil hängt an Teil 1, massgebend sind dessen Eltern."""
        while e and e.get("Teil") and e.get("Parent-ID") in idx:
            e = idx[e["Parent-ID"]]
        return e.get("Parent-ID") if e else None

    gemeldet = set()
    for k, e in enumerate(reihe):
        if k == 0 or k == len(reihe) - 1:
            continue
        vor, nach = reihe[k - 1], reihe[k + 1]
        if not (vorn[vor["ID"]] == vorn[e["ID"]] == vorn[nach["ID"]]):
            continue   # mehrere Bestände in einer Datei: nur innerhalb desselben Bestandsteils vergleichen
        u, tv, tn = loc[e["ID"]], dez[vor["ID"]], dez[nach["ID"]]
        erw = set()
        if tv[:-1] == tn[:-1] and num(tv[-1]) is not None and num(tn[-1]) is not None and 0 <= num(tn[-1]) - num(tv[-1]) <= 4:
            erw |= {".".join(tv[:-1] + (str(j),)) for j in range(num(tv[-1]), num(tn[-1]) + 1)}
        if loc[vor["ID"]] == loc[nach["ID"]]:
            erw.add(loc[vor["ID"]])
        if not erw or u in erw:
            continue
        if any(u.startswith(x + ".") or x.startswith(u + ".") or re.fullmatch(re.escape(x) + r"[a-z]", u) for x in erw):
            continue   # Kind, Eltern oder Buchstabenzusatz («3a» nach «3») der erwarteten Signatur
        if any(loc[x["ID"]] != u and loc[x["ID"]].startswith(u) for x in (vor, nach)):
            continue   # Ziffern angehängt: «2.4.» ist Kopf von «2.41.», «2.42.» (D3774)
        best_x = min(erw, key=lambda x: (lev(u, x), x))
        if lev(u, best_x) > 2:
            continue
        # nur melden, wenn die Einheit dadurch andere Eltern hat als die Nachbarn
        ev = eltern(vor) if dez[vor["ID"]][:-1] == teile(best_x)[:-1] or loc[vor["ID"]] == best_x else eltern(nach)
        if eltern(e) == ev:
            continue
        zeile(e, "AEHNLICH_DA" if best_x in vorhanden else "AEHNLICH", vor, nach, best_x)
        gemeldet.add(e["ID"])
    # EINZELN
    stelle = {e["ID"]: k for k, e in enumerate(reihe)}
    for e in ee:
        v = dez.get(e["ID"])
        hw = str(e.get("Prüfhinweise") or "")
        if not v or e["ID"] in gemeldet or e.get("Teil") or not re.search(r"Übergeordnete Signatur", hw):
            continue
        if len(gruppe[v[:-1]]) != 1:
            continue
        k = stelle.get(e["ID"])
        vor = reihe[k - 1] if k else None
        nach = reihe[k + 1] if k is not None and k + 1 < len(reihe) else None
        if any(x and eltern(x) == eltern(e) for x in (vor, nach)):
            continue
        zeile(e, "EINZELN", vor, nach, "")
        gemeldet.add(e["ID"])
    # LUECKE_ZEILE: Nummer q.m+1 fehlt; zwischen den Signaturzeilen von q.m und q.m+2 steht eine Zeile ohne Einheit, die in
    # der Signaturspalte mit einer Nummer beginnt (Signatur mit Tippfehler nicht erkannt, Einheit im Darin?)
    NUMWORT = re.compile(r"^[0-9IVX][0-9IVX.,:;/]*[0-9IVX.]$|^[0-9]$")
    for q, g in gruppe.items():
        for m in sorted(g):
            if m + 1 in g or m + 2 not in g or m + 1 in abgedeckt[q]:
                continue
            a = [x for x in g[m] if x["ID"] in pos]
            b = [x for x in g[m + 2] if x["ID"] in pos]
            if not a or not b:
                continue
            p1, p2 = pos[a[0]["ID"]], pos[b[0]["ID"]]
            if not p1 < p2 or p2 - p1 > 400:
                continue
            gr = min(zz[p1]["worte"][0][4], zz[p2]["worte"][0][4])
            xs = [zz[p1]["worte"][0][1], zz[p2]["worte"][0][1]]
            for i in range(p1 + 1, p2):
                if i in belegt or not zz[i]["worte"]:
                    continue
                w0 = zz[i]["worte"][0]
                t0 = w0[0].strip()
                if not NUMWORT.match(t0) or not any(abs(w0[1] - x) <= 4 for x in xs):
                    continue
                if re.fullmatch(r"(1[2-9]|20)\d\d\.?", t0) or re.fullmatch(r"\d{1,2}\.\d{1,2}\.(\d{2}|\d{4})", t0):
                    continue   # Jahreszahl oder Datum
                text = " ".join(w[0] for w in zz[i]["worte"])
                if w0[4] < gr - 1 or zz[i]["top"] < 60 or zz[i]["top"] > 800:
                    continue   # Fussnote (kleinere Schrift) oder Kopf-/Fusszeile
                if best and re.sub(r"\s+", "", text).startswith(re.sub(r"\s+", "", best)):
                    continue   # Kopfzeile mit der Bestandssignatur
                out.append({"datei": d, "art": "LUECKE_ZEILE", "id": "", "signatur": ".".join(q + (str(m + 1),)) + " fehlt",
                            "teil": "", "seite": zz[i]["seite"], "vorher": f"{a[0]['ID']} {a[0]['Signatur']}",
                            "nachher": f"{b[0]['ID']} {b[0]['Signatur']}", "erwartet": text[:90], "planliste": planliste,
                            "titel": "", "hinweis": ""})
                stat["LUECKE_ZEILE"] += 1
    # TEIL
    lauf = collections.Counter(e["Signatur"] for e in ee)
    for e in ee:
        v = dez.get(e["ID"])
        if not v or not e.get("Teil") or num(v[-1]) is None or e["ID"] in gemeldet:
            continue
        m, g = num(v[-1]), gruppe[v[:-1]]
        luecken = [j for j in range(min(g), max(g)) if j not in g] if g else []
        t1 = teil1.get(e["Signatur"])
        anders = t1 is not None and not (worte(e.get("Titel")) & worte(t1.get("Titel")))
        if lauf[e["Signatur"]] != 2 or not anders:
            continue   # Läufe ab 3 Nennungen (eine Nummer, mehrere Objekte: Planlisten) und gleiche Titel sind Konvention
        if (m - 1 not in g and m - 2 in g) or (m + 1 not in g and m + 2 in g):
            fehlt = m - 1 if (m - 1 not in g and m - 2 in g) else m + 1
            zeile(e, "TEIL", None, None, f"eigene Einheit? {'.'.join(v[:-1] + (str(fehlt),))} fehlt in der Folge")
        elif anders and len(luecken) == 1 and e.get("Teil") == 2:
            zeile(e, "TEIL", None, None, f"eigene Einheit? Titel anders als Teil 1, Folge hat genau eine Lücke "
                                         f"({'.'.join(v[:-1] + (str(luecken[0]),))})")

with open(aus, "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=felder, delimiter=";")
    w.writeheader()
    w.writerows(out)
print(dict(stat))
