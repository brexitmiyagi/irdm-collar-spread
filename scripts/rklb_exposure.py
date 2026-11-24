# how much Rocket Lab is inside one Iridium share
# Black-Scholes delta at each strike's implied vol (backed out of the midpoints)
import csv, os, math
from statistics import NormalDist
from common import DATA, terms
N = NormalDist().cdf
t = terms()
q = {float(r['strike']): (float(r['bid']) + float(r['ask'])) / 2 for r in csv.DictReader(open(os.path.join(DATA, 'rklb_calls_2027-06-17_quoted_2026-11-24.csv')))}
S, T = t['rklb_close'], t['days_to_close'] / 365
r = math.log(1 + t['tbill_6m'])

def bs(K, v):
    d1 = (math.log(S / K) + (r + v * v / 2) * T) / (v * math.sqrt(T))
    return S * N(d1) - K * math.exp(-r * T) * N(d1 - v * math.sqrt(T)), N(d1)

def iv(K, price):
    lo, hi = 0.05, 3.0
    for _ in range(80):
        m = (lo + hi) / 2
        lo, hi = (m, hi) if bs(K, m)[0] < price else (lo, m)
    return m

v1, v2 = iv(67.5, (q[65] + q[70]) / 2), iv(112.5, (q[110] + q[115]) / 2)
d1, d2 = bs(67.5, v1)[1], bs(112.5, v2)[1]
delta = 0.4 - 0.4 * d1 + 0.24 * d2
print(f"implied vol 67.50: {v1*100:.0f}%, 112.50: {v2*100:.0f}%")
print(f"Iridium delta to Rocket Lab: {delta:.3f} shares, about ${delta*S:.2f} of RKLB per IRDM share ({delta*S/t['irdm_close']*100:.0f}% of the price)")
print(f"Oct 9 to Oct 16 actual: {(47.47-43.76)/(68.21-50.84):.2f}")
