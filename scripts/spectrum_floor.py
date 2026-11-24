# is Iridium's spectrum a floor above the $28 break price? price the parts off two spectrum deals
import csv, os
HERE = os.path.dirname(os.path.abspath(__file__))
d = {r['item']: float(r['value']) for r in csv.DictReader(open(os.path.join(HERE, '..', 'data', 'spectrum_comps.csv')))}
mhz_e = d['aws4_mhz'] + d['hblock_mhz']
e_lo = d['spacex_echostar_price'] / mhz_e; e_hi = (d['spacex_echostar_price'] + d['spacex_echostar_interest']) / mhz_e
print(f"SpaceX-EchoStar: ${d['spacex_echostar_price']:,.0f}m (${d['spacex_echostar_price']+d['spacex_echostar_interest']:,.0f}m with interest) for {mhz_e:.0f} MHz -> ${e_lo:,.0f}m to ${e_hi:,.0f}m per MHz (terrestrial-capable spectrum)")
# Globalstar ex-Apple: strip the Apple contract and the non-Apple business, value what is left as spectrum
rev = d['globalstar_9m_revenue'] / 0.75; apple = rev * d['apple_share_of_revenue']; other = rev - apple
g_mhz = d['globalstar_lband_mhz'] + d['globalstar_sband_mhz']
for lab, apple_mult, other_mult in (('Apple contract at 6x revenue, rest at 3x', 6, 3), ('Apple contract at 10x revenue, rest at 3x', 10, 3)):
    resid = d['globalstar_ev'] - apple * apple_mult - other * other_mult
    print(f"Globalstar ex-Apple ({lab}): Apple ${apple:.0f}m/yr, other ${other:.0f}m/yr -> spectrum residual ${resid:,.0f}m / {g_mhz:.3f} MHz = ${resid/g_mhz:,.0f}m per MHz")
g_lo = (d['globalstar_ev'] - apple * 10 - other * 3) / g_mhz; g_hi = (d['globalstar_ev'] - apple * 6 - other * 3) / g_mhz
for lab, ppm in (('EchoStar low', e_lo), ('EchoStar high', e_hi), ('Globalstar ex-Apple low', g_lo), ('Globalstar ex-Apple high', g_hi)):
    spec = ppm * d['iridium_mhz']; parts = spec + d['aireon_fair_value']
    eq = (parts - d['iridium_net_debt']) / d['iridium_diluted_shares']
    print(f"  {lab:26s} ${ppm:,.0f}m/MHz x {d['iridium_mhz']} MHz = ${spec:,.0f}m + Aireon ${d['aireon_fair_value']:.0f}m - net debt ${d['iridium_net_debt']:,.0f}m -> ${eq:.2f} a share")
print("note: both comps carry terrestrial rights (AWS-4, Globalstar n53) that Iridium's L-band lacks, so these per-MHz values flatter Iridium")
