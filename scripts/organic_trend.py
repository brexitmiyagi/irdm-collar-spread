# what Iridium looks like with Aireon taken out of the headline
import csv, os
HERE = os.path.dirname(os.path.abspath(__file__))
d = {r['item']: (float(r['2026']), float(r['2025'])) for r in csv.DictReader(open(os.path.join(HERE, '..', 'data', 'iridium_quarterly.csv')))}
for k, (a, b) in d.items():
    print(f"{k}: {a:,.0f} vs {b:,.0f} ({(a/b-1)*100:+.1f}%)")
c26 = sum(d[k][0] for k in ('q3_voice_data_k', 'q3_iot_k', 'q3_broadband_k'))
c25 = sum(d[k][1] for k in ('q3_voice_data_k', 'q3_iot_k', 'q3_broadband_k'))
print(f"Q3 voice + IoT + broadband: {c26:,.0f} vs {c25:,.0f} ({(c26/c25-1)*100:+.1f}%)")
