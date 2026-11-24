# can a real book get in and out? days to trade at 20% of average volume, and the hedge's footprint in Rocket Lab
import csv, os
import collar
HERE = os.path.dirname(os.path.abspath(__file__))
def last(t):
    rows = sorted(csv.DictReader(open(os.path.join(HERE, '..', 'data', f'{t}_short_interest_nasdaq_2026-11-24.csv'))), key=lambda r: r['settlement_date'])
    return int(rows[-1]['avg_daily_volume']), rows[-1]['settlement_date']
adv_i, d = last('irdm'); adv_r, _ = last('rklb')
print(f'average daily volume (Nasdaq, period to {d}): Iridium {adv_i:,} shares (${adv_i*collar.PRICE/1e6:.1f}m), Rocket Lab {adv_r:,} shares (${adv_r*collar.SPOT/1e6:.0f}m)')
for size in (5e6, 20e6, 50e6):
    sh = size / collar.PRICE; hedge = 0.26 * sh
    print(f'${size/1e6:.0f}m: {sh:,.0f} Iridium shares = {sh/(0.2*adv_i):.1f} days at 20% of volume; hedge {hedge:,.0f} Rocket Lab shares = {hedge/adv_r:.1%} of one day; a break costs ${sh*(collar.PRICE-22.81)/1e6:.1f}m at the model break price')
print('borrow: no live fee source available; the options imply about 0.8% a year. 1 pt more borrow on the hedge costs about $0.13 an Iridium share a year')
