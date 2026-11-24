# hand-checked: what happened to regulated collar deals that ran long or reached their outside date,
# and how fast the clean, hand-checked regulated sample closed
import csv, os, math, json, statistics as st, datetime as dt
import collar
HERE = os.path.dirname(os.path.abspath(__file__)); DATA = os.path.join(HERE, '..', 'data')
D = dt.date.fromisoformat
rows = list(csv.DictReader(open(os.path.join(DATA, 'regulated_collar_deals_handchecked.csv'))))
closed = [int(r['days']) for r in rows if r['outcome'].startswith('closed')]
broke = [r for r in rows if not r['outcome'].startswith('closed') and 'restructured' not in r['outcome']]
d = sorted(closed)
print(f'hand-checked regulated collar deals: {len(closed)} closed, median {st.median(d):.0f} days from the signing 8-K to delisting')
print('closed by Iridium-equivalent dates: ' + ', '.join(f'{lab} {sum(x <= k for x in d)/len(d):.0%}' for k, lab in ((276, 'Mar 31'), (367, 'Jun 30'), (459, 'Sep 30'), (548, 'Dec 28'))))
print(f'regulatory terminations: {len(broke)} of {len(closed) + len(broke)} = {len(broke)/(len(closed)+len(broke)):.1%}')
late = list(csv.DictReader(open(os.path.join(DATA, 'late_regulated_deals_handchecked.csv'))))
print('deals that ran past ~18 months or reached their outside date:')
for r in late:
    print(f"  {r['deal']:28s} {(D(r['ended'])-D(r['signed'])).days:5d} days  {r['outcome']:18s} {r['what_happened']}")
c = sum(r['outcome'].startswith('closed') for r in late)
print(f'{c} of {len(late)} closed; the {len(late)-c} terminations came from state utility commissions (2), a DOJ court injunction (1) and CFIUS with a foreign buyer (1)')
# expected value with the satellite-deal timing (17/33/33/17) at three close-odds levels
pk = [collar.package(x)['V'] for x in collar.CLOSES]; V = sum(a * b for a, b in zip([1/6, 2/6, 2/6, 1/6], pk))
DFb = math.exp(-math.log(1.0426) * 0.6); B = 0.75 * 28.04 + 0.25 * 43.0
for p in (0.946, 0.97, 0.98):
    ev = p * V + (1 - p) * B * DFb
    print(f'close odds {p:.1%}: expected {ev:.2f}, {ev/collar.PRICE-1:+.2%} vs T-bills')
