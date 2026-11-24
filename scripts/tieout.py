# fails loudly if any number quoted in the post stops reproducing
import subprocess, sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
def run(s): return subprocess.run([sys.executable, os.path.join(HERE, s)], capture_output=True, text=True, check=True).stdout
order = ['option_surface.py', 'irr_by_close_date.py', 'article_numbers.py']
for s in order: run(s)
checks = {
 'break_price_model.py': ['$25.90 to $31.74, average $28.63', '$532m', 'Evercore mid  -> $27.44', '6.4x peer median   -> $12.31', 'triangulated standalone break price: $28.04'],
 'sensitivity.py': ['-2.20  falls every quarter', 'Rocket Lab at 10-day VWAP $57.30'],
 'spectrum_floor.py': ['$340m to $380m per MHz', '-> $13.12 a share', '-> $18.71 a share', '= $382m per MHz', '= $410m per MHz'],
 'deal_timing.py': ['median 383.0 days, range 246 to 571', 'Mar 31 2027 17%, Jun 30 2027 33%, Sep 30 2027 33%, Dec 28 2027 17%', '2027-07-16'],
 'arb_universe.py': ['ranks 9 of 15', 'IRDM ranks 6; median excess of the others +2.3%'],
 'drawdown_and_holders.py': ['total 18.26m shares = 17.2%', '27 trading days', '46,410,138', '42.46m', '94.77%'],
 'delay_decomposition.py': ['cash: 0.89', 'stock leg: 0.11', 'received: -0.31'],
 'relative_value.py': ['GSAT  (Amazon): value $85.19 vs $85.96, gross -0.9%', 'TXNM  (Blackstone Infrastructure): value $61.25 vs $58.95, gross +3.9%, +6.6% a year', 'NSC   (Union Pacific): value $377.71 vs $316.65, gross +19.3%, +17.3% a year'],
 'option_adjusted_spread.py': ['spread 3.64 (8.4%)', 'with 3 dividends 44.33', 'net call sold        2.37', 'time value of cash   0.63', 'dividends received  -0.47', 'left for break risk  1.12', '2.59% over the period'],
 'implied_probability.py': ['28.52: implied close odds 93.2%', '35.00: implied close odds 89.0%'],
 'tax_line.py': ['40%: 45.00'],
 'rklb_exposure.py': ['0.261 shares', '$12.97'],
 'fee_comparison.py': ['buyer regulatory fee 5.1%', '$2.25 to $2.48'],
 'organic_trend.py': ['245,733 vs 249,317 (-1.4%)', '371,069 vs 380,018 (-2.4%)'],
 'quote_band.py': ['low 43.91, mid 44.33, high 44.75', 'low 0.70, mid 1.12, high 1.54', '90.9% to 95.6%', '85.4% to 92.8%', '43.9% to 63.3%', 'loss on break 14.69'],
 'break_price_history.py': ['2025 year end 17.38 (-40.1%)', '25.12 -> Sep 10 17.96 (-28.5%)', 'low 15.84', 'high 29.68', '(21.3%)'],
 'tax_threshold_odds.py': ['S = 45.0'],
 'delay_incentive.py': ['($48m) to Rocket Lab'],
 'realized_hedge.py': ['54.59 -> 43.21', '98.01 -> 49.63'],
 'short_interest.py': ['31.5m to 34.2m', '46.4m, 2.8 days to cover', 'rise since Jun 15: 12.2m', 'event-driven funds: 4.7m'],
 'break_price_competition.py': ['$279m', 'worth 0.87 a share', '-> 25.04', '-> 24.35', '-> 22.85', '-> 21.53', '-> 19.15', '-> 16.77', '-1.93 a share'],
 'irdm_options.py': ['60 with a two-sided quote', 'median $5.00', '2028-12-15 $22.50 put: 801', '2028-12-15 $25.00 put: 571', '1945 (45%)', 'after Dec 28 2027: 1474'],
 'collar_deal_sample.py': ['n=604 median 277 days', 'n= 92 median 366 days'],
 'late_deals.py': ['47 closed, median 203 days', 'Mar 31 64%, Jun 30 77%, Sep 30 87%, Dec 28 94%', '5 of 52 = 9.6%', '4 of 8 closed', '1166 days', '600 days'],
 'fcc_team_telecom_timing.py': ['33 granted (30 non-satellite, 3 satellite)', 'median 220 days, middle half 199 to 259, 3 of 30 inside 180, slowest 441', '2022-05-11 -> grant 2023-05-19, 373 days', '2022-11-23 -> grant 2023-08-03, 253 days', '2024-08-29 -> grant 2025-07-11, 316 days', '35% / 45% / 18% / 2%', '60% / 40% / 0% / 0%', 'Apr 22 2027', 'Jul 28 2027', 'median 189', 'Feb 07 2027', 'grant 2026-10-27: 88 days', 'lands on Feb 05 2027'],
 'spectrum_repricing.py': ['25.12 -> Sep 10 2025 17.96 (-28.5%)', '43.21 (+72.0%', '85.96 (+175.2%', '25.67 (-39.5%', '61.02 (+105.8%', '37.94 (+21.5%)'],
 'event_study.py': ['$0.460', '$+0.83 (+1.3 sd)', '$+0.35 (+0.5 sd)'],
 'liquidity.py': ['3.4 days'],
 'break_business_model.py': ['implied fixed costs 139', 'OEBITDA 532 -> 17.70 / 27.47 / 37.24', 'OEBITDA 466 -> 13.14 / 21.69 / 30.24', 'weighted at 9.5x across my case weights: 22.81', 'at 7.5x: 14.02'],
 'arb_crowding.py': ['Q2 1.1m shares (1.0%) -> Q3 4.9m (4.6% of 106m outstanding)', 'Q2 1.2m shares (1.2%) -> Q3 11.4m (10.7% of 106m outstanding)', '2.3m (2.2%) at Jun 30 -> 16.3m (15.4%) at Sep 30'],
}
bad = 0
for s, needles in checks.items():
    out = run(s)
    for n in needles:
        if n not in out:
            print(f'FAIL {s}: {n}'); bad += 1
# every number the article quotes, at the anchor the article was written on (data/anchor.json)
import json
want = json.load(open(os.path.join(HERE, '..', 'data', 'article_numbers_expected.json')))
got = json.load(open(os.path.join(HERE, '..', 'results', 'article_numbers.json')))
for k, val in want.items():
    if got.get(k) != val:
        print(f'FAIL article number {k}: expected {val}, got {got.get(k)}'); bad += 1
print('tieout ok' if not bad else f'{bad} failures'); sys.exit(1 if bad else 0)
