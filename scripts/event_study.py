# did Iridium react to the regulatory news, or just follow Rocket Lab? hedged daily moves and market-implied odds around three docket events
import csv, os, math, statistics as st, datetime as dt
import collar
HERE = os.path.dirname(os.path.abspath(__file__))
d = [(dt.date.fromisoformat(r['date']), float(r['irdm']), float(r['rklb'])) for r in csv.DictReader(open(os.path.join(HERE, '..', 'data', 'daily_closes_nasdaq.csv'))) if r['date'] >= '2026-06-29']
W = [1/6, 2/6, 2/6, 1/6]; B = 0.75 * 28.04 + 0.25 * 43.0
T0 = collar.T0
def model(day, S):
    collar.T0 = day
    pk = [collar.package(c, S=S) for c in collar.CLOSES]
    collar.T0 = T0
    V = sum(a * p['V'] for a, p in zip(W, pk)); delta = sum(a * p['delta'] for a, p in zip(W, pk))
    DFb = math.exp(-math.log(1.0426) * 0.6)
    return V, delta, B * DFb
res, odds = {}, {}
for (d0, i0, r0), (d1, i1, r1) in zip(d, d[1:]):
    V, delta, Bd = model(d0, r0)
    res[d1] = (i1 - i0) - delta * (r1 - r0)
for day, i, r in d:
    V, delta, Bd = model(day, r); odds[day] = (i - Bd) / (V - Bd)
sd = st.pstdev(res.values())
print(f'hedged daily move (Iridium less model delta x Rocket Lab): standard deviation ${sd:.3f}')
for name, day in (('FCC public notice', dt.date(2026, 9, 15)), ('Iridium withdraws 116 petitions', dt.date(2026, 10, 14)), ('reply comments filed', dt.date(2026, 11, 9))):
    ds = [x for x in sorted(res) if day <= x <= day + dt.timedelta(days=3)][:2]
    before = max(x for x in odds if x < day); after = ds[-1]
    move = sum(res[x] for x in ds)
    print(f'{name} ({day}): hedged move over {len(ds)} days ${move:+.2f} ({move/(sd*math.sqrt(len(ds))):+.1f} sd); implied odds {odds[before]:.1%} -> {odds[after]:.1%}')
lo = min(odds, key=odds.get); hi = max(odds, key=odds.get)
print(f'implied odds range since signing: {odds[lo]:.1%} ({lo}) to {odds[hi]:.1%} ({hi}); latest {odds[d[-1][0]]:.1%}')
print('note: uses the Nov 24 option surface for every day, so early-period odds are approximate')
