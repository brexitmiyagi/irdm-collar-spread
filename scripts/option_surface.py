# Rocket Lab option surface: put-call parity (implied borrow) and a fitted IV smile per expiry
import csv, os, math, json, datetime as dt
from statistics import NormalDist
from linalg import lstsq
N = NormalDist().cdf
HERE = os.path.dirname(os.path.abspath(__file__)); DATA = os.path.join(HERE, '..', 'data')
A = json.load(open(os.path.join(DATA, 'anchor.json')))
S, t0 = A['rklb'], dt.date.fromisoformat(A['date'])
f = lambda x: float(x) if x not in ('', 'None', None) else None
rows = [dict(e=r['expiry'], K=float(r['strike']), cb=f(r['call_bid']), ca=f(r['call_ask']), pb=f(r['put_bid']), pa=f(r['put_ask'])) for r in csv.DictReader(open(os.path.join(DATA, A['rklb_chain'])))]
curve = [(float(r['tenor_years']), float(r['yield'])) for r in csv.DictReader(open(os.path.join(DATA, 'rates_2026-11-20.csv')))]
def rate(T):
    if T <= curve[0][0]: y = curve[0][1]
    elif T >= curve[-1][0]: y = curve[-1][1]
    else: y = next(ya + (yb - ya) * (T - a) / (b - a) for (a, ya), (b, yb) in zip(curve, curve[1:]) if a <= T <= b)
    return math.log(1 + y)
def bs(K, T, r, q, v):
    d1 = (math.log(S / K) + (r - q + v * v / 2) * T) / (v * math.sqrt(T))
    return S * math.exp(-q * T) * N(d1) - K * math.exp(-r * T) * N(d1 - v * math.sqrt(T)), math.exp(-q * T) * N(d1)
def iv(p, K, T, r, q):
    if p <= max(S * math.exp(-q * T) - K * math.exp(-r * T), 0) + 1e-6: return None
    lo, hi = 0.01, 4.0
    for _ in range(100):
        m = (lo + hi) / 2
        lo, hi = (m, hi) if bs(K, T, r, q, m)[0] < p else (lo, m)
    return m
out = {}
allq = []
for e in sorted(set(r['e'] for r in rows)):
    T = (dt.date.fromisoformat(e) - t0).days / 365; r = rate(T)
    qs = []
    for x in rows:
        if x['e'] != e or None in (x['cb'], x['ca'], x['pb'], x['pa']) or x['cb'] <= 0 or x['pb'] <= 0 or not 35 <= x['K'] <= 70: continue
        val = ((x['cb'] + x['ca']) / 2 - (x['pb'] + x['pa']) / 2 + x['K'] * math.exp(-r * T)) / S
        if val > 0: qs.append(-math.log(val) / T)
    qs.sort(); q = qs[len(qs) // 2] if qs else 0.0
    if T > 0.25: allq.append(q)
    q_par = q
    if 'borrow_override' in A: q = A['borrow_override']   # intraday quotes on a falling stock give nonsense parity borrow; pin it
    pts = []
    for x in rows:
        if x['e'] != e or not x['cb'] or x['ca'] is None: continue
        m = (x['cb'] + x['ca']) / 2
        if (x['ca'] - x['cb']) / m > 0.35 or not 30 <= x['K'] <= 150: continue
        s = iv(m, x['K'], T, r, q)
        if s: pts.append((math.log(x['K'] / S), s, x['K']))
    if len(pts) < 4: continue
    be = lstsq([[1, p[0], p[0] ** 2] for p in pts], [p[1] for p in pts])
    g = lambda K: be[0] + be[1] * math.log(K / S) + be[2] * math.log(K / S) ** 2
    out[e] = dict(T=T, r=r, q=q, n=len(pts), kmax=max(p[2] for p in pts), iv50=g(50), iv675=g(67.5), iv1125=g(112.5))
    print(f"{e}: parity-implied borrow {q_par*100:+.1f}% (used {q*100:+.1f}%), {len(pts)} strikes, IV at 50 {g(50):.0%}, at 67.50 {g(67.5):.0%}, at 112.50 {g(112.5):.0%}")
allq.sort(); qmed = allq[len(allq) // 2]
if 'borrow_override' in A:
    print(f'parity borrow median {qmed*100:.1f}% is not usable intraday; pinned at {A["borrow_override"]*100:.1f}%, the last clean reading (Nov 23 close)')
    qmed = A['borrow_override']
print(f"median parity-implied borrow cost (expiries past 3 months): {qmed*100:.1f}% a year")
json.dump(dict(surface=out, borrow=qmed), open(os.path.join(HERE, '..', 'results', 'option_surface.json'), 'w'), indent=1)
