# fails loudly if any number quoted in the post stops reproducing
import subprocess, sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
def run(s): return subprocess.run([sys.executable, os.path.join(HERE, s)], capture_output=True, text=True, check=True).stdout
order = ['option_surface.py', 'irr_by_close_date.py']
for s in order: run(s)
checks = {
 'break_price_model.py': ['$25.90 to $31.74, average $28.63', '$532m', 'Evercore mid  -> $27.44', '6.4x peer median   -> $12.31', 'triangulated standalone break price: $28.04'],
 'option_surface.py': ['median parity-implied borrow cost (expiries past 3 months): 0.8% a year'],
 'irr_by_close_date.py': ['45.27', '44.09', '43.43', '42.64', '+14.17%', '+3.40%', '+0.59%', '-1.19%', '88.3%', '94.8%', '98.7%', 'value lost per quarter of delay: 1.18, 0.66, 0.78', 'after borrow: +3.2% a year over bills'],
 'regulator_tree.py': ['close odds: 94.6%', 'package 43.82', 'expected value today $43.13 vs price $43.21: -0.18% vs T-bills (-0.25% a year)', 'odds needed to match T-bills (with the Party A mix): 95.2%', '10/35/35/20: expected -0.48%', '25/50/20/5: expected +0.59%'],
 'market_frontier.py': ['2027-03-28       90.9%    88.9%', '2027-06-28       96.4%    95.5%', '2027-07-28       97.0%    96.3%', '2027-09-28       99.6%    99.5%'],
 'sensitivity.py': ['-2.20  falls every quarter', '-2.82  falls every quarter', 'Rocket Lab at 10-day VWAP $57.30'],
 'spectrum_floor.py': ['$340m to $380m per MHz', '-> $13.12 a share', '-> $18.71 a share', '= $382m per MHz', '= $410m per MHz'],
 'deal_timing.py': ['median 383.0 days, range 246 to 571', 'Mar 31 2027 17%, Jun 30 2027 33%, Sep 30 2027 33%, Dec 28 2027 17%', '2027-07-16'],
 'arb_universe.py': ['ranks 9 of 15', 'IRDM ranks 6; median excess of the others +2.3%', '+2.0% a year over bills'],
 'drawdown_and_holders.py': ['(-0.66); to Dec -> 42.64 (-1.44)', 'about -0.32 more', 'about -0.80 more', '39.82 (-4.26)', '= -3.85', '(+3.55)', 'total 18.26m shares = 17.2%', '27 trading days', '46,410,138', '42.46m', '94.77%'],
 'delay_decomposition.py': ['loss 2.62', 'collar (short $67.50 call, long $112.50 call): 1.93', 'cash: 0.89', 'stock leg: 0.11', 'received: -0.31'],
 'relative_value.py': ['GSAT  (Amazon): value $85.19 vs $85.96, gross -0.9%', 'TXNM  (Blackstone Infrastructure): value $61.25 vs $58.95, gross +3.9%, +6.6% a year', 'NSC   (Union Pacific): value $377.71 vs $316.65, gross +19.3%, +17.3% a year', '+7.9% a year if it closes, +3.4% over bills'],
 'option_adjusted_spread.py': ['spread 3.64 (8.4%)', 'with 3 dividends 44.33', 'net call sold        2.37', 'time value of cash   0.63', 'dividends received  -0.47', 'left for break risk  1.12', '2.59% over the period'],
 'implied_probability.py': ['28.52: implied close odds 93.2%', '35.00: implied close odds 89.0%'],
 'tax_line.py': ['40%: 45.00'],
 'rklb_exposure.py': ['0.261 shares', '$12.97'],
 'fee_comparison.py': ['buyer regulatory fee 5.1%', '$2.25 to $2.48'],
 'organic_trend.py': ['245,733 vs 249,317 (-1.4%)', '371,069 vs 380,018 (-2.4%)'],
 'quote_band.py': ['low 43.91, mid 44.33, high 44.75', 'low 0.70, mid 1.12, high 1.54', '90.9% to 95.6%', '85.4% to 92.8%', '43.9% to 63.3%', 'loss on break 14.69'],
 'break_price_history.py': ['2025 year end 17.38 (-40.1%)', '25.12 -> Sep 10 17.96 (-28.5%)', 'low 15.84', 'high 29.68', '(21.3%)'],
}
bad = 0
for s, needles in checks.items():
    out = run(s)
    for n in needles:
        if n not in out:
            print(f'FAIL {s}: {n}'); bad += 1
print('tieout ok' if not bad else f'{bad} failures'); sys.exit(1 if bad else 0)
