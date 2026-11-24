# who gains when the deal is slow: Rocket Lab holds the other side of the collar
import collar
SH = 106.158479   # Iridium shares outstanding, Oct 13 2026 (10-Q cover)
pk = [collar.package(c) for c in collar.CLOSES]
held = [0.4 * p['c1'] - 0.24 * p['c2'] for p in pk]
for c, h, p in zip(collar.CLOSES, held, pk):
    print(f'{c}: collar value on Rocket Lab side {h:.2f} a share (${h*SH:.0f}m); Iridium package {p["V"]:.2f}')
for i in range(3):
    dc = held[i + 1] - held[i]; dv = pk[i]['V'] - pk[i + 1]['V']
    print(f'{collar.CLOSES[i]} -> {collar.CLOSES[i+1]}: collar moves {dc:.2f} a share (${dc*SH:.0f}m) to Rocket Lab; Iridium holders lose {dv:.2f} (${dv*SH:.0f}m) in all')
print(f'Mar -> Dec 2027: collar {held[3]-held[0]:.2f} a share (${(held[3]-held[0])*SH:.0f}m); package {pk[0]["V"]-pk[3]["V"]:.2f} (${(pk[0]["V"]-pk[3]["V"])*SH:.0f}m)')
