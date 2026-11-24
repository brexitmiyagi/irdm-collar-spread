# Rocket Lab short interest before and after the deal, against the most an arb book could need
import csv, os
HERE = os.path.dirname(os.path.abspath(__file__))
rows = sorted(csv.DictReader(open(os.path.join(HERE, '..', 'data', 'rklb_short_interest_nasdaq_2026-11-24.csv'))), key=lambda r: r['settlement_date'])
pre = [int(r['short_interest']) for r in rows if '2026-04-01' <= r['settlement_date'] <= '2026-06-15']
last = rows[-1]
print(f'before the deal (Apr 15 to Jun 15 2026): {min(pre)/1e6:.1f}m to {max(pre)/1e6:.1f}m shares short')
print(f'latest ({last["settlement_date"]}): {int(last["short_interest"])/1e6:.1f}m, {float(last["days_to_cover"]):.1f} days to cover')
rise = int(last['short_interest']) - int([r for r in rows if r['settlement_date'] == '2026-06-15'][0]['short_interest'])
print(f'rise since Jun 15: {rise/1e6:.1f}m shares')
print(f'arb hedge on 106.16m Iridium shares at the model ratio of 0.26: {0.26*106.16:.1f}m; on the 18.26m held by event-driven funds: {0.26*18.26:.1f}m')
