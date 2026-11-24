# the professional version of the trade: long Iridium, short 0.4 Rocket Lab, long 0.4 of the $67.50 call,
# short 0.24 of the $112.50 call (January 2028 options, the first listed expiry past the final End Date).
# No $67.50 or $112.50 strikes are listed, so each is built from the two strikes either side.
import csv, os, math, random, datetime as dt
import collar
from timing_weights import BASE, BREAK_MODEL
HERE = os.path.dirname(os.path.abspath(__file__))
rows = list(csv.DictReader(open(os.path.join(HERE, '..', 'data', collar.A['rklb_chain']))))
EXP = '2028-01-21'
def q(K, side):
    r = next(x for x in rows if x['expiry'] == EXP and float(x['strike']) == K)
    return float(r['call_' + side])
mid = lambda K: (q(K, 'bid') + q(K, 'ask')) / 2
c675 = {'mid': (mid(65) + mid(70)) / 2, 'pay': (q(65, 'ask') + q(70, 'ask')) / 2}
c1125 = {'mid': (mid(110) + mid(115)) / 2, 'get': (q(110, 'bid') + q(115, 'bid')) / 2}
S0, P0 = collar.SPOT, collar.PRICE
legs_mid = -0.4 * S0 + 0.4 * c675['mid'] - 0.24 * c1125['mid']
legs_ba = -0.4 * S0 + 0.4 * c675['pay'] - 0.24 * c1125['get']
print(f'Jan 2028 calls: synthetic $67.50 {c675["mid"]:.2f} mid ({c675["pay"]:.2f} at the ask), synthetic $112.50 {c1125["mid"]:.2f} mid ({c1125["get"]:.2f} at the bid)')
print(f'outlay per Iridium share: {P0 + legs_mid:.2f} at mids, {P0 + legs_ba:.2f} paying the spread (bid/ask cost {legs_ba - legs_mid:.2f})')
Texp = (dt.date.fromisoformat(EXP) - collar.T0).days / 365
qb = collar.surface()['borrow']
def bs(S, K, T, v, r):
    if T <= 0: return max(S - K, 0)
    d1 = (math.log(S / K) + (r - qb + v * v / 2) * T) / (v * math.sqrt(T))
    N = lambda x: 0.5 * (1 + math.erf(x / math.sqrt(2)))
    return S * math.exp(-qb * T) * N(d1) - K * math.exp(-r * T) * N(d1 - v * math.sqrt(T))
random.seed(7); Z = [random.gauss(0, 1) for _ in range(20000)]
def close_value(c, ivs=0.0):
    # PV today of what the structure is worth at closing on date c: $27 cash + leftover time value in the options, + dividends - borrow
    T = (c - collar.T0).days / 365; r = collar.rate(T); DF = math.exp(-r * T)
    v1 = collar.vol('iv675', Texp) + ivs; v2 = collar.vol('iv1125', Texp) + ivs; vs = collar.vol('iv675', T)
    tau = Texp - T; tv = 0.0
    for z in Z:
        S = S0 * math.exp((r - qb - vs * vs / 2) * T + vs * math.sqrt(T) * z)
        tv += 0.4 * (bs(S, 67.5, tau, v1, r) - max(S - 67.5, 0)) - 0.24 * (bs(S, 112.5, tau, v2, r) - max(S - 112.5, 0))
    tv /= len(Z)
    dv = sum(0.16 * math.exp(-collar.rate((d - collar.T0).days / 365) * (d - collar.T0).days / 365) for d in collar.DIVS if d <= c)
    return DF * (27 + tv) + dv - qb * 0.4 * S0 * T, tv
W = BASE   # same timing and break inputs as expected_value.py
DFb = math.exp(-math.log(1.0426) * 0.6); B = 0.75 * BREAK_MODEL + 0.25 * 43.0
for lab, legs in (('mids', legs_mid), ('paying bid/ask', legs_ba)):
    out = P0 + legs
    print(f'-- {lab}: outlay {out:.2f}')
    for c in collar.CLOSES:
        pv, tv = close_value(c)
        print(f'   close {c}: leftover option time value {tv:.2f}, PV of payoff {pv:.2f}, {pv/out-1:+.2%} vs T-bills if it closes then')
    for ivs in (-0.10, 0.0, 0.10):
        pvc = sum(w * close_value(c, ivs)[0] for w, c in zip(W, collar.CLOSES))
        ev = 0.946 * pvc + 0.054 * (B * DFb + legs)
        print(f'   blend timing, 94.6% odds, implied vol {ivs*100:+.0f} pts at closing: expected {ev/out-1:+.2%} vs T-bills on the {out:.2f} outlay')
print(f'a break costs the same as the plain hedge: Iridium to about ${BREAK_MODEL} (or $43 if Party A re-bids) while the Rocket Lab legs are unwound near their current value')
