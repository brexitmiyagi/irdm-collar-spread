# what direct-to-device competition does to a broken Iridium: shrink voice/data and broadband, hold the rest
import csv, os
HERE = os.path.dirname(os.path.abspath(__file__))
q = {r['line']: int(r['q3_2026_k']) / 1000 for r in csv.DictReader(open(os.path.join(HERE, '..', 'data', 'irdm_revenue_q3_2026.csv')))}
exposed = 4 * (q['voice_and_data'] + q['broadband'])
NET_DEBT, SHARES, MULT, BASE = 2061.605, 108.926, 9.5, 532.0
base = (BASE * MULT - NET_DEBT) / SHARES
print(f'annualized voice/data + broadband: ${exposed:.0f}m; base break value {base:.2f} on ${BASE:.0f}m OEBITDA at {MULT}x')
print('each $10m of OEBITDA is worth', round(10 * MULT / SHARES, 2), 'a share')
for g in (0.05, 0.10, 0.20):
    lost = exposed * (1 - (1 - g) ** 3)
    for flow in (0.7, 0.9):
        e = BASE - lost * flow
        print(f'  exposed lines fall {g:.0%} a year for 3 years, {flow:.0%} drops to OEBITDA: OEBITDA ${e:.0f}m -> {(e*MULT-NET_DEBT)/SHARES:.2f} a share')
print('EMSS (fixed $110.5m a year) repriced 20% lower:', round(-0.2 * 110.5 * MULT / SHARES, 2), 'a share')
