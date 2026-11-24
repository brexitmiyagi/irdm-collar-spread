# shared pricing for the Iridium package: $27 cash + 0.4 RKLB - 0.4 C(67.50) + 0.24 C(112.50) + dividends
import os, math, json, datetime as dt
from statistics import NormalDist
N = NormalDist().cdf
HERE = os.path.dirname(os.path.abspath(__file__))
A = json.load(open(os.path.join(HERE, '..', 'data', 'anchor.json')))   # one timestamp for every price (pull_snapshot.py)
T0 = dt.date.fromisoformat(A['date']); PRICE = A['irdm']; SPOT = A['rklb']
_sv = None
def surface():
    global _sv
    if _sv is None:
        _sv = json.load(open(os.path.join(HERE, '..', 'results', 'option_surface.json')))
    return _sv
USE = ['2027-03-19', '2027-06-17', '2027-09-17', '2028-01-21']   # expiries with enough clean strikes
DIVS = [dt.date(2026, 12, 31), dt.date(2027, 3, 31), dt.date(2027, 6, 30), dt.date(2027, 9, 30)]
def rate(T):
    pts = [(0.25, 0.0413), (0.5, 0.0426), (1.0, 0.0451)]
    y = pts[0][1] if T <= 0.25 else pts[-1][1] if T >= 1 else next(ya + (yb - ya) * (T - a) / (b - a) for (a, ya), (b, yb) in zip(pts, pts[1:]) if a <= T <= b)
    return math.log(1 + y)
def vol(key, T):
    s = surface()['surface']; xs = [(s[e]['T'], s[e][key]) for e in USE]
    if T <= xs[0][0]: return xs[0][1]
    for (a, va), (b, vb) in zip(xs, xs[1:]):
        if a <= T <= b: return math.sqrt((va * va * a + (vb * vb * b - va * va * a) * (T - a) / (b - a)) / T)
    return xs[-1][1]
def call(S, K, T, v, r, q):
    d1 = (math.log(S / K) + (r - q + v * v / 2) * T) / (v * math.sqrt(T))
    return S * math.exp(-q * T) * N(d1) - K * math.exp(-r * T) * N(d1 - v * math.sqrt(T)), math.exp(-q * T) * N(d1)
def package(close, S=SPOT, iv_shift=0.0, q=None, avg_days=0):
    """PV today of the deal if it closes on `close` for sure. avg_days>0 shortens variance for VWAP averaging."""
    q = surface()['borrow'] if q is None else q
    T = (close - T0).days / 365; r = rate(T); DF = math.exp(-r * T)
    Teff = T - (2 / 3) * avg_days / 252 if avg_days else T   # averaging over the last n days cuts variance by ~2/3 of that window
    v1 = max(vol('iv675', T) + iv_shift, 0.05); v2 = max(vol('iv1125', T) + iv_shift, 0.05)
    c1, d1 = call(S, 67.5, Teff, v1, r, q); c2, d2 = call(S, 112.5, Teff, v2, r, q)
    dv = sum(0.16 * math.exp(-rate((d - T0).days / 365) * (d - T0).days / 365) for d in DIVS if d <= close)
    V = 27 * DF + 0.4 * S * math.exp(-q * T) - 0.4 * c1 + 0.24 * c2 + dv
    delta = 0.4 * math.exp(-q * T) - 0.4 * d1 + 0.24 * d2
    return dict(V=V, T=T, DF=DF, r=r, delta=delta, c1=c1, c2=c2)
CLOSES = [dt.date(2027, 3, 31), dt.date(2027, 6, 30), dt.date(2027, 9, 30), dt.date(2027, 12, 28)]
