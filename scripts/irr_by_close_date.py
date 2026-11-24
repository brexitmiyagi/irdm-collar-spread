# value of the Iridium package and the return, by when the deal closes
import os, math, json, datetime as dt
from statistics import NormalDist
N = NormalDist().cdf
HERE = os.path.dirname(os.path.abspath(__file__))
sv = json.load(open(os.path.join(HERE, '..', 'results', 'option_surface.json'))); surf, q = sv['surface'], sv['borrow']
A = json.load(open(os.path.join(HERE, '..', 'data', 'anchor.json')))
S, P, t0 = A['rklb'], A['irdm'], dt.date.fromisoformat(A['date'])
use = ['2027-03-19', '2027-06-17', '2027-09-17', '2028-01-21']   # expiries with enough clean strikes
def rate(T):
    pts = [(0.25, 0.0413), (0.5, 0.0426), (1.0, 0.0451)]
    y = pts[0][1] if T <= 0.25 else pts[-1][1] if T >= 1 else next(ya + (yb - ya) * (T - a) / (b - a) for (a, ya), (b, yb) in zip(pts, pts[1:]) if a <= T <= b)
    return math.log(1 + y)
def vol(key, T):
    xs = [(surf[e]['T'], surf[e][key]) for e in use]
    if T <= xs[0][0]: return xs[0][1]
    for (a, va), (b, vb) in zip(xs, xs[1:]):
        if a <= T <= b: return math.sqrt((va * va * a + (vb * vb * b - va * va * a) * (T - a) / (b - a)) / T)
    return xs[-1][1]
def call(K, T, v, r):
    d1 = (math.log(S / K) + (r - q + v * v / 2) * T) / (v * math.sqrt(T))
    return S * math.exp(-q * T) * N(d1) - K * math.exp(-r * T) * N(d1 - v * math.sqrt(T)), math.exp(-q * T) * N(d1)
divs = [dt.date(2026, 12, 31), dt.date(2027, 3, 31), dt.date(2027, 6, 30), dt.date(2027, 9, 30)]
res = []
print("close date  days  bill   C67.5  C112.5  package  excess/yr  total/yr if closes  odds needed @ $28.04")
for c in (dt.date(2027, 3, 31), dt.date(2027, 6, 30), dt.date(2027, 9, 30), dt.date(2027, 12, 28)):
    T = (c - t0).days / 365; r = rate(T); DF = math.exp(-r * T)
    c1, d1 = call(67.5, T, vol('iv675', T), r); c2, d2 = call(112.5, T, vol('iv1125', T), r)
    dv = sum(0.16 * math.exp(-rate((d - t0).days / 365) * (d - t0).days / 365) for d in divs if d <= c)
    V = 27 * DF + 0.4 * S * math.exp(-q * T) - 0.4 * c1 + 0.24 * c2 + dv
    delta = 0.4 * math.exp(-q * T) - 0.4 * d1 + 0.24 * d2
    exc = (V / P) ** (1 / T) - 1; tot = ((V / DF) / P) ** (1 / T) - 1
    need = (P - 28.04 * DF) / (V - 28.04 * DF)
    res.append(dict(close=str(c), T=T, r=r, DF=DF, V=V, delta=delta, borrow_cost=q * delta * S * T, excess=exc, total=tot, need=need))
    print(f"{c}  {(c-t0).days:4d}  {math.exp(r)-1:.2%}  {c1:5.2f}  {c2:5.2f}   {V:6.2f}   {exc:+7.2%}    {tot:+7.2%}          {need:.1%}")
json.dump(res, open(os.path.join(HERE, '..', 'results', 'irr_by_close_date.json'), 'w'), indent=1)
d = [r['V'] for r in res]
print(f"value lost per quarter of delay: {d[0]-d[1]:.2f}, {d[1]-d[2]:.2f}, {d[2]-d[3]:.2f}")
print(f"hedge: about {res[1]['delta']:.2f} RKLB per IRDM; borrow cost to a Jun close ~${res[1]['borrow_cost']:.2f} a share")
j = res[1]; hx = ((j['V'] - j['borrow_cost']) / P) ** (1 / j['T']) - 1
print(f"hedged (long IRDM, short {j['delta']:.2f} RKLB), Jun close, after borrow: {hx:+.1%} a year over bills")
