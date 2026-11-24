# can the implied-close-date method be tested on the twin? Amazon-Globalstar: each Globalstar share elects $90 cash or 0.3210 Amazon
# shares (value capped at $90), with cash capped at 40% of shares (Amazon press release, Apr 14 2026). Closing also waits on
# HIBLEO-4 replacement-satellite milestones, so the FCC grant (Oct 27 2026, DA 26-1160) is not the last gate. This looks at the
# spread around the grant, assuming cash is fully elected (40% cash, 60% stock), which is my assumption, not a disclosed fact.
import csv, os
HERE = os.path.dirname(os.path.abspath(__file__))
rows = list(csv.DictReader(open(os.path.join(HERE, '..', 'data', 'globalstar_amazon_closes_nasdaq.csv'))))
def deal(amzn): return 0.4 * 90.0 + 0.6 * min(0.3210 * amzn, 90.0)
out = []
for r in rows:
    if not r['gsat_close'] or not r['amzn_close']: continue
    g, a = float(r['gsat_close']), float(r['amzn_close']); d = deal(a)
    out.append((r['date'], g, a, d, d / g - 1))
for date, g, a, d, sp in out:
    if '2026-10-20' <= date <= '2026-11-03':
        print(f'{date}  Globalstar {g:6.2f}  Amazon {a:7.2f}  deal {d:6.2f}  spread {sp:+.2%}' + ('   <- FCC grant' if date == '2026-10-27' else ''))
pre = next(x for x in out if x[0] == '2026-10-26'); post = next(x for x in out if x[0] == '2026-10-27')
print(f'spread the day before the grant {pre[4]:+.2%}, on grant day {post[4]:+.2%}: a {100*(pre[4]-post[4]):.1f}-point move')
print('the spread swings with Amazon by more than the grant moved it (it even goes negative on Oct 29), so the election-mix assumption is doing')
print('most of the work. Closing also depends on satellite milestones and a $110m adjustment, so the spread does not isolate the FCC.')
print('conclusion: the implied-close-date method cannot be tested cleanly on Globalstar')
