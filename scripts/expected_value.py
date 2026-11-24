# base case and ranges: timing from the FCC datasets (base = half not-referred, a quarter each referred set), break price from the line-by-line model or the old $28, close odds 94.6% / 97%, Party A 0/25/50%
import math
import collar
from timing_weights import NONSAT, SAT, REFERRED, NONREF, BASE, BREAK_MODEL
pk = [collar.package(c)['V'] for c in collar.CLOSES]
DFb = math.exp(-math.log(1.0426) * 0.6)
def ev(W, p=0.946, q=0.25, B0=BREAK_MODEL):
    V = sum(a * b for a, b in zip(W, pk)); return V, p * V + (1 - p) * ((1 - q) * B0 + q * 43.0) * DFb
for lab, W in (('non-satellite', NONSAT), ('satellite', SAT), ('referred 50/50', REFERRED), ('not referred', NONREF), ('base blend', BASE)):
    print(f'{lab:14s} package {ev(W)[0]:.2f}')
print('expected value vs T-bills at $43.21 (timing / break / odds / Party A):')
for lab, W in (('non-satellite', NONSAT), ('satellite', SAT), ('referred 50/50', REFERRED), ('not referred', NONREF), ('base blend', BASE)):
    for B0 in (BREAK_MODEL, 28.04):
        for p in (0.946, 0.97):
            e = ev(W, p, 0.25, B0)[1]
            print(f'  {lab:14s} break {B0:5.2f} odds {p:.1%} Party A 25%: {e:.2f} ({e/collar.PRICE-1:+.2%})')
for q in (0.0, 0.5):
    e = ev(BASE, 0.946, q)[1]; print(f'  base, Party A {q:.0%}: {e:.2f} ({e/collar.PRICE-1:+.2%})')
V, e = ev(BASE); T = sum(a * (c - collar.T0).days / 365 for a, c in zip(BASE, collar.CLOSES))
print(f'base case: {e:.2f}, {e/collar.PRICE-1:+.2%} vs T-bills over about {T:.2f} years')
e97 = ev(BASE, 0.97)[1]
print(f'fair value range (base timing and break, odds 94.6% to 97%): {e:.2f} to {e97:.2f}')
entry = e / 1.006
print(f'entry price for a +0.6% expected edge over T-bills (about 1% a year) on base inputs: {entry:.2f}')

def implied_odds(px, W=BASE):
    lo, hi = 0.5, 1.0
    for _ in range(60):
        m = (lo + hi) / 2
        lo, hi = (m, hi) if ev(W, m)[1] < px else (lo, m)
    return (lo + hi) / 2
print(f'close odds implied by the entry price on base timing: {implied_odds(entry):.1%}; by $43.21: {implied_odds(collar.PRICE):.1%}')
