# which input moves the answer: expected value vs T-bills at $43.21 as each input moves across a plausible range, others at base
import math
import collar
from timing_weights import NONSAT, SAT, NONREF, BASE, BREAK_MODEL
DFb = math.exp(-math.log(1.0426) * 0.6)
def ev(p=0.946, B0=BREAK_MODEL, q=0.25, W=BASE, ivs=0.0):
    pk = [collar.package(c, iv_shift=ivs)['V'] for c in collar.CLOSES]
    V = sum(a * b for a, b in zip(W, pk)); B = (1 - q) * B0 + q * 43.0
    return (p * V + (1 - p) * B * DFb) / collar.PRICE - 1
print(f'base: {ev():+.2%} vs T-bills')
cases = [('close odds 92% / 98%', ev(p=0.92), ev(p=0.98)),
         ('break price $15 / $28', ev(B0=15), ev(B0=28.04)),
         ('Party A returns 0% / 50%', ev(q=0.0), ev(q=0.5)),
         ('timing: referred satellite / not referred', ev(W=SAT), ev(W=NONREF)),
         ('Rocket Lab implied vol +10 / -10 pts', ev(ivs=0.10), ev(ivs=-0.10))]
for name, lo, hi in sorted(cases, key=lambda c: -abs(c[2] - c[1])):
    print(f'{name:38s} {lo:+.2%} to {hi:+.2%}  (range {abs(hi-lo)*100:.2f} pts)')
