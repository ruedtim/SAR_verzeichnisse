import json, sys
d = json.load(open(sys.argv[1]))
pages = [int(x) for x in sys.argv[2].split(",")]
lim = int(sys.argv[3]) if len(sys.argv) > 3 else 60
print("META:", {k: v for k, v in d["meta"].items() if k in ("Title", "Author", "Creator", "Producer", "Seiten")})
for p in pages:
    print(f"--- Seite {p}")
    n = 0
    for z in d["zeilen"]:
        if z["seite"] == p:
            t = " ".join(w[0] for w in z["worte"])
            f = z["worte"][0][3].split("+")[-1][-14:]
            print(f"{z['top']:6.1f} x0={z['worte'][0][1]:6.1f} x1={z['worte'][-1][2]:6.1f} {f:14s} {z['worte'][0][4]:4.1f} | {t[:105]}")
            n += 1
            if n >= lim: break
