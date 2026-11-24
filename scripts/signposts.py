# what each docket or market event would do to the call. One row per event: grant odds by Apr 30 2027, what Iridium is worth
# on base inputs after it, and the price I'd buy at (a +0.6% edge over T-bills, the same rule as the base case).
# Also the referral-class split of the not-referred deals, and how the buy price moves with Rocket Lab's borrow cost.
import io, contextlib, csv, os, math, datetime as dt
HERE = os.path.dirname(os.path.abspath(__file__))
with contextlib.redirect_stdout(io.StringIO()):
    import collar, implied_timing as IT
    from timing_weights import BASE, NONREF, NONSAT, SAT, BREAK_MODEL, PN, NR, days as _days
P, S = collar.PRICE, collar.SPOT
CUT = [(c - PN).days for c in collar.CLOSES]
DFb = math.exp(-math.log(1.0426) * 0.6)
nonsat = _days(lambda r: r['sector'] != 'satellite'); sat = _days(lambda r: r['sector'] == 'satellite')
def weights(sample, after=0):
    xs = [int(x) for x in sample if int(x) > after]
    if not xs: return None
    c = [sum(x <= k for x in xs) / len(xs) for k in CUT]
    return [c[0], c[1] - c[0], c[2] - c[1], 1 - c[2]]
def blend(parts):
    tot = sum(w for w, W in parts if W); return [sum(w * W[i] for w, W in parts if W) / tot for i in range(4)]
def ev(W, p=0.946, S_=S, q=None):
    V = sum(a * collar.package(c, S=S_, q=q)['V'] for a, c in zip(W, collar.CLOSES))
    return p * V + (1 - p) * (0.75 * BREAK_MODEL + 0.25 * 43.0) * DFb
def by(day, parts):
    tot = sum(w for w, s in parts); return sum(w * sum(int(x) <= day for x in s) / len(s) for w, s in parts) / tot
D_APR = (dt.date(2027, 4, 30) - PN).days
base_parts = [(0.5, NR), (0.25, nonsat), (0.25, sat)]
print(f'Iridium ${P} and Rocket Lab ${S:.2f} at {collar.A["irdm_time"]}; grant odds counted from the Sep 15 2026 notice')
rows = []
def row(lab, g, e, note=''):
    rows.append((lab, g, e)); print(f'  {lab:46s} grant by Apr 30 {g:4.0%}  worth ${e:.2f} ({e/P-1:+.2%})  buy at ${e/1.006:.2f}  {note}')
row('today, base inputs', by(D_APR, base_parts), ev(BASE))
# a Justice Department letter: the deal is in review, so only the referred samples apply
ref_parts = [(0.5, nonsat), (0.5, sat)]
row('Justice Department letter in the docket', by(D_APR, ref_parts), ev(blend([(0.5, weights(nonsat)), (0.5, weights(sat))])), 'my exit')
# foreign clearances disclosed: the 99% foreign-approval leg goes to 100%
row('UK/Australia/NZ clearances disclosed', by(D_APR, base_parts), ev(BASE, p=0.946 / 0.99))
# March 14 (day 180) with no grant: drop every precedent granted by day 180 and re-weight what's left
d180 = 180
left = [(w * sum(int(x) > d180 for x in s) / len(s), [x for x in s if int(x) > d180]) for w, s in base_parts]
left = [(w, s) for w, s in left if s]
W180 = blend([(w, weights(s, d180)) for w, s in left])
row('March 14 2027 passes with no grant', by(D_APR, left), ev(W180), '(repriced on today\'s clock)')
# Rocket Lab under the $45 tax line
row('Rocket Lab at $44', by(D_APR, base_parts), ev(BASE, S_=44.0), f'deal worth ${27 + 0.4 * 44:.2f}')
print('  a Space Bureau or international-office staff meeting: no base rate in my data, so no number; I read it as a sign an order is being drafted')
# the referral-class split
print('not-referred deals by what the FCC order says about referral:')
cls = list(csv.DictReader(open(os.path.join(HERE, '..', 'data', 'fcc_nonreferred_transfers.csv'))))
for k in sorted(set(r['referral_class'] for r in cls)):
    xs = sorted((int(r['days']), r['deal']) for r in cls if r['referral_class'] == k)
    print(f'  {k}: ' + ', '.join(f'{d} {n} ({PN + dt.timedelta(days=d):%b %d %Y})' for d, n in xs))
print('  Mint was pulled into review on day 4; Iridium is past day 70 with nothing from the Justice Department.')
fast_close = PN + dt.timedelta(days=168 + 5)
print(f'  if Iridium matches the two courtesy-copy deals that were not pulled in (145 and 168 days), the grant lands by '
      f'{PN + dt.timedelta(days=168):%b %d %Y}; a close five days later is worth ${IT.worth(fast_close):.2f} ({IT.worth(fast_close)/P-1:+.2%})')
# borrow cost: the model pins Rocket Lab borrow at 0.8%; a higher quoted fee lowers the package and the buy price
print('Rocket Lab borrow cost (used in the collar pricing and the hedge), base timing:')
BORROW = {}
for q in (0.008, 0.02, 0.04, 0.08):
    e = ev(BASE, q=q); BORROW[q] = e; print(f'  borrow {q:.1%}: worth ${e:.2f} ({e/P-1:+.2%}), buy at ${e/1.006:.2f}')
FAST_CLOSE, FAST_WORTH = fast_close, IT.worth(fast_close)
