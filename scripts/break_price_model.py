# what a broken Iridium is worth, three ways
import csv, os, math, datetime as dt
from linalg import lstsq
HERE = os.path.dirname(os.path.abspath(__file__)); DATA = os.path.join(HERE, '..', 'data')
rows = list(csv.DictReader(open(os.path.join(DATA, 'peer_closes_2025_2026_nasdaq.csv'))))
P = {k: {dt.date.fromisoformat(r['date']): float(r[k]) for r in rows} for k in rows[0] if k != 'date'}
ds = sorted(P['IRDM'])
a, b = dt.date(2026, 4, 1), dt.date(2026, 11, 23)
undisturbed = P['IRDM'][a]

# 1) peer-adjusted undisturbed price: regress weekly IRDM returns on factors, Jan 2025 to Mar 2026,
#    then roll the Apr 1 price forward by what the factors did since
est = [d for d in ds if dt.date(2025, 1, 2) <= d <= dt.date(2026, 3, 31)][::5]
ret = lambda t: [math.log(P[t][est[i]] / P[t][est[i - 1]]) for i in range(1, len(est))]
move = lambda t: math.log(P[t][b] / P[t][a])
y = ret('IRDM'); preds = []
print(f"undisturbed Apr 1 2026: {undisturbed}")
for names in (['SPY'], ['SPY', 'VSAT'], ['SPY', 'ASTS'], ['SPY', 'VSAT', 'ASTS'], ['XLC', 'VSAT']):
    X = [[1.0] + [ret(n)[i] for n in names] for i in range(len(y))]
    be = lstsq(X, y)
    yh = [sum(c * x for c, x in zip(be, r)) for r in X]; my = sum(y) / len(y)
    r2 = 1 - sum((u - v) ** 2 for u, v in zip(y, yh)) / sum((u - my) ** 2 for u in y)
    p = undisturbed * math.exp(sum(be[i + 1] * move(n) for i, n in enumerate(names)))
    preds.append(p)
    print(f"  factors {'+'.join(names):14s} betas {', '.join(f'{v:.2f}' for v in be[1:])}  R2 {r2:.2f}  -> ${p:.2f}")
for t in ('SPY', 'VSAT', 'ASTS', 'XLC'):
    print(f"  {t} Apr 1 -> Nov 23: {P[t][b]/P[t][a]-1:+.1%}")
peer_mid = sum(preds) / len(preds)
print(f"peer-adjusted: ${min(preds):.2f} to ${max(preds):.2f}, average ${peer_mid:.2f}")

# 2) and 3) run-rate OEBITDA times peer multiples
bal = {r['item']: float(r['value']) for r in csv.DictReader(open(os.path.join(DATA, 'iridium_balance_q3_2026.csv')))}
run = bal['q3_oebitda_m'] * 4 * 0.98   # Q3 annualised, less the ~2% the core is shrinking
comps = [r for r in csv.DictReader(open(os.path.join(DATA, 'evercore_trading_comps.csv'))) if 'Iridium' not in r['company']]
m27 = sorted(float(r['tev_2027e_ebitda']) for r in comps)
med = m27[len(m27) // 2]
eq = lambda m: (m * run - bal['net_debt_m']) / bal['diluted_shares_m']
print(f"run-rate OEBITDA ${run:.0f}m (Q3 x4 less 2%)")
print(f"peer 2027E multiples {m27}, median {med}x")
for m, lab in ((med, 'peer median'), (7.5, 'Evercore low'), (9.5, 'Evercore mid'), (11.5, 'Evercore high')):
    print(f"  {m:.1f}x {lab:13s} -> ${eq(m):.2f}")
mult_mid = eq(9.5)
central = (peer_mid + mult_mid) / 2
print(f"triangulated standalone break price: ${central:.2f} (range ${eq(7.5):.2f} to ${max(preds):.2f})")
