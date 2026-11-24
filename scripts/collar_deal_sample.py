# every merger proxy (DEFM14A, 2010 on) whose text mentions a collar and an exchange ratio, from EDGAR full-text search,
# with announcement (8-K item 1.01) and closing (8-K item 2.01 or delisting) dates from each target's filing history
import csv, os, json, math, datetime as dt, statistics as st
import collar
HERE = os.path.dirname(os.path.abspath(__file__))
D = dt.date.fromisoformat
rows = [r for r in csv.DictReader(open(os.path.join(HERE, '..', 'data', 'collar_deal_sample_edgar.csv'))) if r['first_collar_proxy'] < '2025-06-01']
def days(r): return (D(r['close_8k_201_or_delisting']) - D(r['announce_8k_101'])).days
def summary(label, sel):
    d = sorted(days(r) for r in rows if sel(r) and r['close_8k_201_or_delisting'] and r['announce_8k_101'] and days(r) > 20)
    c = [sum(x <= k for x in d) / len(d) for k in (276, 367, 459, 548)]   # Iridium's Mar 31 / Jun 30 / Sep 30 / Dec 28 2027, in days from signing
    print(f'{label:24s} n={len(d):3d} median {st.median(d):.0f} days; closed by Iridium-equivalent Mar 31 {c[0]:.0%}, Jun 30 {c[1]:.0%}, Sep 30 {c[2]:.0%}, Dec 28 {c[3]:.0%}')
    return c
summary('all collar deals', lambda r: True)
c = summary('FCC or CFIUS in proxy', lambda r: r['mentions_fcc'] == '1' or r['mentions_cfius'] == '1')
summary('CFIUS in proxy', lambda r: r['mentions_cfius'] == '1')
print('note: this automated pass dates announcements from the first 8-K item 1.01 before the proxy, which is often a credit agreement,')
print('so it overstates deal length. scripts/late_deals.py uses the hand-checked set instead, and that is what the post quotes.')
print('8-K item 1.02 also covers credit facilities and superseded agreements, so no break rate is taken from this pass')
