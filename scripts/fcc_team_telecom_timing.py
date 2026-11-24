# how long the FCC takes when Team Telecom is involved: every ECFS docket since the April 2020 executive order with a
# Department of Justice / Team Telecom letter, plus the three big satellite transfers, from public notice to grant
import statistics as st, datetime as dt
import collar
from timing_weights import ROWS, days, NONSAT, SAT, NONREF, NR, BASE, PN, CUT
g_all = days(lambda r: True); g_n = days(lambda r: r['sector'] != 'satellite'); g_s = days(lambda r: r['sector'] == 'satellite')
print(f'{len(ROWS)} dockets; {len(g_all)} granted ({len(g_n)} non-satellite, {len(g_s)} satellite)')
print(f'non-satellite: median {st.median(g_n):.0f} days, middle half {g_n[len(g_n)//4]} to {g_n[3*len(g_n)//4]}, {sum(x<=180 for x in g_n)} of {len(g_n)} inside 180, slowest {g_n[-1]}')
for r in ROWS:
    if r['sector'] == 'satellite': print(f"satellite: docket {r['docket']}: public notice {r['accepted_pn']} -> grant {r['fcc_action']}, {r['days']} days")
lag = sorted(int(r['days_to_first_tt_letter']) for r in ROWS if r['days_to_first_tt_letter'] not in ('', None))
print(f'first Team Telecom letter in the docket: median {st.median(lag):.0f} days after the public notice (n={len(lag)})')
for lab, w in (('non-satellite', NONSAT), ('satellite', SAT), ('not referred', NONREF), ('base blend', BASE)):
    print(f'{lab:14s} weights Mar/Jun/Sep/Dec 2027: ' + ' / '.join(f'{x:.0%}' for x in w))
print(f'non-satellite median applied to Iridium: {PN + dt.timedelta(days=st.median(g_n)):%b %d %Y}; satellite median: {PN + dt.timedelta(days=st.median(g_s)):%b %d %Y}')
# Iridium was not referred: the FCC's notice (DA 26-985, n.20) says "we do not refer the application to the Committee but
# provide a courtesy copy". So the right comparison is large transfers the FCC did not refer either.
print(f'not referred (n={len(NR)}): {NR} days, median {st.median(NR)}; applied to Iridium: '
      + ', '.join((PN + dt.timedelta(days=d)).strftime('%b %d %Y') for d in NR))
