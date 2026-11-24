# does the market price the collar the way the option model does? regress daily dollar moves in Iridium on Rocket Lab
import csv, os, math, datetime as dt
import collar
HERE = os.path.dirname(os.path.abspath(__file__))
d = [(r['date'], float(r['irdm']), float(r['rklb'])) for r in csv.DictReader(open(os.path.join(HERE, '..', 'data', 'daily_closes_nasdaq.csv'))) if r['date'] >= '2026-06-29']
def ols(x, y):
    mx, my = sum(x) / len(x), sum(y) / len(y)
    b = sum((a - mx) * (c - my) for a, c in zip(x, y)) / sum((a - mx) ** 2 for a in x)
    res = [c - my - b * (a - mx) for a, c in zip(x, y)]
    se = math.sqrt(sum(e * e for e in res) / (len(x) - 2) / sum((a - mx) ** 2 for a in x))
    return b, se, 1 - sum(e * e for e in res) / sum((c - my) ** 2 for c in y)
dI = [b[1] - a[1] for a, b in zip(d, d[1:])]; dR = [b[2] - a[2] for a, b in zip(d, d[1:])]
print(f'{d[0][0]} to {d[-1][0]}: Iridium {d[0][1]} -> {d[-1][1]}, Rocket Lab {d[0][2]} -> {d[-1][2]}')
b, se, r2 = ols(dR, dI); print(f'all days: {b:.3f} Iridium dollars per Rocket Lab dollar (se {se:.3f}, R squared {r2:.2f}, n {len(dI)})')
for a, z in [('2026-06-29', '2026-08-31'), ('2026-09-01', '2026-10-15'), ('2026-10-16', '2026-11-23')]:
    sub = [(x, y) for x, y, dd in zip(dR, dI, d[1:]) if a <= dd[0] <= z]
    lv = [dd[2] for dd in d[1:] if a <= dd[0] <= z]
    b, se, r2 = ols([s[0] for s in sub], [s[1] for s in sub])
    m = collar.package(collar.CLOSES[1], S=sum(lv) / len(lv))['delta']
    print(f'{a} to {z}: realized {b:.3f} (se {se:.3f}, R squared {r2:.2f}); model at average Rocket Lab ${sum(lv)/len(lv):.2f}: {m:.3f}')
