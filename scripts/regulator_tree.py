# close odds by regulator (anchored on base rates), timing from the deal database, scenarios, heatmap
import os, math, json, datetime as dt
from collar import package, CLOSES, PRICE, HERE
nodes = [
    ('FCC consent', 0.98, '6 of 6 FCC-heavy satellite/spectrum precedents in data/deal_timing_database.csv obtained FCC consent; docket closed Nov 9 2026 with no petition to deny'),
    ('Team Telecom', 0.99, 'existing Iridium NSA; applicants accept an NSA compliance condition; enforcement precedent (Marlink 2026) is a fine, not a block'),
    ('DCSA FOCI', 0.99, 'condition only if DCSA asks; mitigation instruments exist; no public record of DCSA blocking a deal (timing risk: adjudications "generally exceed a year" per White & Case 2023)'),
    ('Foreign approvals', 0.99, 'UK NSIA 2025-26: 1 of 1,220 reviewed acquisitions blocked, 8 of 9 final orders allowed with conditions; France: 7 formal refusals in four years, 49% of 167 2025 authorisations conditional'),
    ('Everything else', 0.995, 'cash pre-funded ($2,362.5m Q3 ATM), bridge terminated unused; litigation/MAE'),
]
p = 1.0
for n, x, why in nodes:
    p *= x; print(f"{x:6.1%}  {n:18s} {why}")
print(f"close odds: {p:.1%}")
w = {dt.date(2027, 3, 31): 1/6, dt.date(2027, 6, 30): 2/6, dt.date(2027, 9, 30): 2/6, dt.date(2027, 12, 28): 1/6}   # from deal_timing.py
pk = {c: package(c) for c in CLOSES}
V = sum(w[c] * pk[c]['V'] for c in CLOSES); Tw = sum(w[c] * pk[c]['T'] for c in CLOSES)
DFb = math.exp(-0.0422 * 0.6)
print(f"data-derived timing 17/33/33/17 -> package {V:.2f}, average time {Tw:.2f} years")
B = 28.04; Bparty = 43.0; pa = 0.25
scen = [
    ('Closes by Jun 30 2027', p * (w[CLOSES[0]] + w[CLOSES[1]]), (w[CLOSES[0]] * pk[CLOSES[0]]['V'] + w[CLOSES[1]] * pk[CLOSES[1]]['V']) / (w[CLOSES[0]] + w[CLOSES[1]]), 'Mar-Jun 2027'),
    ('Closes after an extension', p * (w[CLOSES[2]] + w[CLOSES[3]]), (w[CLOSES[2]] * pk[CLOSES[2]]['V'] + w[CLOSES[3]] * pk[CLOSES[3]]['V']) / (w[CLOSES[2]] + w[CLOSES[3]]), 'Sep-Dec 2027'),
    ('Breaks, Party A returns', (1 - p) * pa, Bparty * DFb, 'mid-2027'),
    ('Breaks, standalone', (1 - p) * (1 - pa), B * DFb, 'mid-2027'),
]
ev = sum(pr * v for _, pr, v, _ in scen)
for lab, pr, v, t in scen: print(f"  {lab:28s} prob {pr:6.1%}  value today ${v:6.2f}  timing {t}")
print(f"expected value today ${ev:.2f} vs price ${PRICE}: {ev/PRICE-1:+.2%} vs T-bills ({(ev/PRICE)**(1/Tw)-1:+.2%} a year)")
need = (PRICE - (pa * Bparty + (1 - pa) * B) * DFb) / (V - (pa * Bparty + (1 - pa) * B) * DFb)
print(f"odds needed to match T-bills (with the Party A mix): {need:.1%}")
for lab, wt in (('my old judgement weights 10/35/35/20', {CLOSES[0]: .10, CLOSES[1]: .35, CLOSES[2]: .35, CLOSES[3]: .20}), ('generous 25/50/20/5', {CLOSES[0]: .25, CLOSES[1]: .50, CLOSES[2]: .20, CLOSES[3]: .05})):
    Vx = sum(wt[c] * pk[c]['V'] for c in CLOSES); evx = p * Vx + (1 - p) * (pa * Bparty + (1 - pa) * B) * DFb
    print(f"  with {lab}: expected {evx/PRICE-1:+.2%} vs T-bills")
grid_B = (20, 24, 28, 32, 36, 40, 43); grid = []
print('heatmap, expected return over T-bills a year:')
print('odds  ' + ''.join(f'{b:>7}' for b in grid_B))
for pp in (0.86, 0.88, 0.90, 0.92, 0.94, 0.96, 0.98):
    row = [((pp * V + (1 - pp) * b * DFb) / PRICE) ** (1 / Tw) - 1 for b in grid_B]; grid.append(row)
    print(f'{pp:.2f}  ' + ''.join(f'{x*100:+7.1f}' for x in row))
json.dump(dict(p=p, V=V, Tw=Tw, ev=ev, scen=[dict(label=a, prob=b, value=c, timing=d) for a, b, c, d in scen], grid_B=grid_B, grid=grid, date_label='mid-2027 (17/33/33/17)'), open(os.path.join(HERE, '..', 'results', 'regulator_tree.json'), 'w'), indent=1)
