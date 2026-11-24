# who already owns the spread: every 13F holder Nasdaq lists for Iridium, sorted into dedicated merger-arb / event-driven
# managers and multi-strategy pods (both trade spreads), Q2 vs Q3 2026. The classification is mine, by manager name.
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
d = json.load(open(os.path.join(HERE, '..', 'data', 'irdm_13f_all_holders_nasdaq_2026-11-24.json')))['data']
rows = d['holdingsTransactions']['table']['rows']
OUT = float(d['ownershipSummary']['ShareoutstandingTotal']['value']) * 1e6
ARB = ['Pentwater', 'Alpine Associates', 'Magnetar', 'Glazer', 'Aqr Arbitrage', 'Westchester', 'Water Island', 'Kite Lake',
       'Gabelli', 'Gamco', 'Tiaa', 'Davidson Kempner', 'Hudson Bay', 'Weiss Multi', 'Linden', 'Polar Asset', 'Mangrove',
       'Calamos', 'First Trust Capital', 'Tig Advisors', 'Kryger', 'Shaolin', 'Bracebridge', 'Saba', 'Sculptor', 'Arrowmark',
       'Hbk', 'Picton', 'Boothbay', 'Basso', 'Nomura', 'Quarry', 'Spartan', 'Lmr', 'Context Capital', 'Highbridge', 'Taconic', 'Elliott',
       'Kingdon', 'Governors Lane', 'Mason Capital', 'Paulson', 'Cooper Square']
POD = ['Balyasny', 'Millennium', 'Citadel', 'Point72', 'Schonfeld', 'Exoduspoint', 'Verition', 'Tudor', 'Marshall Wace',
       'Squarepoint', 'Walleye', 'Eisler', 'Holocene', 'Bluecrest']  # market makers and quants left out on purpose
def num(s): return float(s.replace(',', '') or 0)
def tag(n):
    n = n.lower()
    if any(k.lower() in n for k in ARB): return 'arb'
    if any(k.lower() in n for k in POD): return 'pod'
    return 'other'
agg = {'arb': [0, 0, []], 'pod': [0, 0, []]}
for r in rows:
    t = tag(r['ownerName'])
    if t == 'other' or r['date'] != '9/30/2026': continue
    q3 = num(r['sharesHeld']); q2 = q3 - num(r['sharesChange'])
    agg[t][0] += q3; agg[t][1] += q2; agg[t][2].append((q3, q2, r['ownerName']))
for t, lab in (('arb', 'merger-arb / event-driven'), ('pod', 'multi-strategy pods')):
    q3, q2, lst = agg[t]
    print(f'{lab}: {len(lst)} filers, Q2 {q2/1e6:.1f}m shares ({q2/OUT:.1%}) -> Q3 {q3/1e6:.1f}m ({q3/OUT:.1%} of {OUT/1e6:.0f}m outstanding)')
    for a, b, n in sorted(lst, reverse=True)[:8]: print(f'   {n[:42]:42s} {b/1e6:5.2f}m -> {a/1e6:5.2f}m')
q3 = agg['arb'][0] + agg['pod'][0]; q2 = agg['arb'][1] + agg['pod'][1]
print(f'spread holders combined: {q2/1e6:.1f}m ({q2/OUT:.1%}) at Jun 30 -> {q3/1e6:.1f}m ({q3/OUT:.1%}) at Sep 30')
print('caveat: 13Fs are long-only snapshots 45 days stale; pods may hold Iridium for reasons other than the spread')
