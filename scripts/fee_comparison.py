# regulatory reverse fee as a share of target equity, the two 2026 Big LEO deals
import csv, os
HERE = os.path.dirname(os.path.abspath(__file__))
for r in csv.DictReader(open(os.path.join(HERE, '..', 'data', 'fee_comparison.csv'))):
    eq = float(r['price_per_share']) * float(r['shares_m'])
    print(f"{r['deal']}: equity ~${eq:,.0f}m, buyer regulatory fee {float(r['buyer_regulatory_fee_m'])/eq*100:.1f}%, target fee {float(r['target_fee_m'])/eq*100:.1f}%")
print(f"Party A proposal: 5.5% of equity = ${0.055*41:.2f} to ${0.055*45:.2f} a share on a $41 to $45 bid")
