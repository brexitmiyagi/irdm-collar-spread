# irdm-collar-spread

Data and code behind my Seeking Alpha piece on Iridium (IRDM) and the Rocket Lab deal. I priced Rocket Lab's collar off its whole option surface, weighted the close date by 13 satellite and spectrum deals, and put each regulator on a published base rate. The answer: $43.21 is about fair (expected value $43.13, 0.2% under T-bills), but the payoff is lopsided. Roughly $1 over bills if it closes by June 2027, about $15 down on a break, no fee, and $0.66 to $1.18 a share lost for every quarter of delay. My rating is a Sell on that shape, not on price.

## How to run

Python 3, no packages needed. From any folder:

    python scripts/spread_history.py
    python scripts/option_adjusted_spread.py
    python scripts/tax_line.py
    python scripts/implied_probability.py
    python scripts/rklb_exposure.py
    python scripts/excess_return_grid.py
    python scripts/fee_comparison.py
    python scripts/organic_trend.py
    python scripts/break_price_history.py
    python scripts/quote_band.py
    python scripts/break_price_model.py
    python scripts/option_surface.py
    python scripts/irr_by_close_date.py   (needs option_surface.py first)
    python scripts/regulator_tree.py      (needs irr_by_close_date.py first)
    python scripts/relative_value.py
    python scripts/market_frontier.py     (needs option_surface.py first)
    python scripts/sensitivity.py
    python scripts/delay_decomposition.py
    python scripts/deal_timing.py
    python scripts/spectrum_floor.py
    python scripts/drawdown_and_holders.py
    python scripts/arb_universe.py
    python scripts/tracker.py             (needs internet; weekly refresh, appends to results/tracker_log.csv)
    python scripts/tieout.py              (runs everything in order and checks every quoted number)

## What each script gives you

- spread_history.py: the daily deal value against the Iridium close since June 26, the 8.4% naive spread, the date Rocket Lab first went under the $67.50 floor, and the October Neutron week.
- option_adjusted_spread.py: the package priced with Rocket Lab's June 2027 calls, and where the $3.64 spread goes ($2.37 call sold, $0.63 time value, $0.47 dividends back, $1.12 for break risk). The $44.33 is a present value, so 2.59% / 4.66% a year is return above bills, not total return.
- rklb_exposure.py: how much Rocket Lab sits inside one Iridium share (about 0.26 shares, $12.97).
- excess_return_grid.py: expected return above bills for a grid of close odds and break prices.
- fee_comparison.py: Amazon's $592m regulatory fee to Globalstar (5.1% of equity) against Rocket Lab's zero to Iridium.
- break_price_history.py: Iridium's prices around the SpaceX-EchoStar deal and before the sale went public.
- quote_band.py: the package and implied odds priced anywhere inside the option quotes, so you can see how wide the uncertainty is.
- break_price_model.py: a broken Iridium three ways (peer-adjusted undisturbed price, run-rate OEBITDA, Evercore's peer multiples), triangulated to $28.04.
- option_surface.py: put-call parity on the whole Rocket Lab chain (implied borrow about 0.8% a year) and a fitted volatility smile per expiry.
- irr_by_close_date.py: what an Iridium share is worth today if the deal closes Mar, Jun, Sep or Dec 2027, and the return each way.
- regulator_tree.py: odds by regulator with the base rate each one rests on (94.6% all in), close dates weighted 17/33/33/17 from deal_timing.py, the four-scenario table ($43.13 expected), the odds needed to match bills (95.2%) and the heatmap. Change the odds at the top of the file.
- market_frontier.py: runs the model backwards. For each close month and break price, the close odds $43.21 needs to earn exactly T-bills (95.5% for a June 28 close at a $28 break).
- sensitivity.py: the package by close date with implied vol 10 points either way, Rocket Lab at $40, $60 and its 10-day VWAP, VWAP averaging at closing, and borrow at 0% or 3%. Value falls every quarter in every case.
- delay_decomposition.py: splits the $2.62 lost between a March and a December close into the collar ($1.93), waiting for the cash ($0.89), borrow ($0.11) and extra dividends (-$0.31).
- deal_timing.py: signing-to-close days for 13 satellite and spectrum deals. The six cross-border or FCC-heavy ones have a median of 383 days, which lands on July 16, 2027 for Iridium.
- spectrum_floor.py: Iridium's 8.725 MHz priced at SpaceX-EchoStar and Globalstar-ex-Apple per-MHz values, plus Aireon, less net debt: $13.12 to $18.71 a share.
- drawdown_and_holders.py: mark-to-market hits from an End Date extension, a 30% Rocket Lab move and a break, plus the event-driven 13F holders (18.26m shares, 17.2%) and short interest.
- arb_universe.py: Iridium against 14 other pending US deals on excess return over bills (ninth of 15).
- tracker.py: pulls fresh Iridium, Rocket Lab and 6-month bill prices, reprices the package and expected value, and logs a line. I run it weekly and before each update note.
- relative_value.py: Iridium against Globalstar/Amazon, TXNM/Blackstone and Norfolk Southern/Union Pacific on the same yardstick.
- tieout.py: reruns everything and fails if any number in the post stops reproducing.
- organic_trend.py: Iridium with Aireon taken out of the headline (pro forma revenue, nine month OEBITDA, Q3 by line).
- tax_line.py: the $45.00 Rocket Lab price where the stock leg drops under 40% of the consideration.
- implied_probability.py: the close odds the market is pricing for three guesses at a broken deal price, plus Party A's 5.5% regulatory fee in dollars a share.

Output from my run on Nov 24, 2026 is in results/. Prices are Nov 23 closes; tracker_log.csv has the Nov 24 pre-market refresh.

## Sources

- Iridium DEFM14A, Aug 26 2026 (deal terms, collar, tax condition, background of the merger): https://www.sec.gov/Archives/edgar/data/1418819/000175392626001637/g085903_def14am.htm
- Iridium Q3 2026 press release: https://www.sec.gov/Archives/edgar/data/1418819/000141881926000053/pressreleaseq32026.htm
- Rocket Lab Q3 2026 10-Q: https://www.sec.gov/Archives/edgar/data/1819994/000181999426000074/rklb-20260930.htm
- Rocket Lab 8-K, Oct 14 2026: https://www.sec.gov/Archives/edgar/data/1819994/000181999426000067/rklb-20261014.htm
- 6 month T-bill: https://fred.stlouisfed.org/series/DTB6
- Daily closes (2016 to 2026) and the option chain: Nasdaq.com
- EchoStar spectrum sale release, Sep 8 2025: https://ir.echostar.com/news-releases/news-release-details/echostar-announces-spectrum-sale-and-commercial-agreement-spacex
- FCC Space Bureau order DA 26-398 (Apr 23 2026): https://docs.fcc.gov/public/attachments/DA-26-398A1.pdf
- FCC order DA 26-1078 (Oct 6 2026): https://docs.fcc.gov/public/attachments/DA-26-1078A1.pdf
- Ricks and Lin, How Deals Die: https://corpgov.law.harvard.edu/2024/10/15/how-deals-die/

- Globalstar 8-K, Apr 14 2026: https://www.sec.gov/Archives/edgar/data/1366868/000114036126014528/ef20070409_8k.htm
- Globalstar Q3 2026 10-Q: https://www.sec.gov/Archives/edgar/data/1366868/000136686826000046/gsat-20260930.htm
- Iridium Q3 2026 10-Q: https://www.sec.gov/Archives/edgar/data/1418819/000141881926000052/irdm-20260930.htm
- FCC public notice DA 26-985 (GN Docket 26-257): https://docs.fcc.gov/public/attachments/DA-26-985A1.pdf
- UK NSIA annual report 2025-26 and French Treasury FDI report 2025 (base rates for foreign approvals)
- FCC informal 180-day timeline: https://www.fcc.gov/general/informal-timeline-consideration-applications-transfers-or-assignments-licenses-or
- Deal timing, spectrum comps and arb universe terms: the 8-K and proxy for each deal, listed by row in data/deal_timing_database.csv, data/spectrum_comps.csv and data/arb_universe_2026-11-23.csv

## Things to be careful with

- The real exchange ratio uses a 10 day VWAP before closing. I use daily closes.
- The $112.50 call has a very wide bid/ask. I use midpoints and interpolate between listed strikes.
- Close dates are weighted from 13 precedents, but six heavy deals is a small sample. The End Date runs to June 28 2027 and can be pushed to December 28.
- $0.16 a quarter in dividends until closing is my assumption.
- The break price comes from two methods that agree on about $28, but Evercore's precedent range went as high as $47.77.
- The regulator odds rest on base rates, but turning a base rate into a node number is my judgement. I found no published DCSA or Team Telecom statistics.
- Eutelsat-OneWeb, Indra-Hispasat and Viasat-Inmarsat announcement days are approximate. SpaceX-EchoStar uses its FCC approval date, not closing.
- The Globalstar Apple-contract multiples (6x to 10x revenue) are my assumptions.
- The 13F holder list comes from Nasdaq's aggregation. Only Tudor was cross-checked against the filing itself.
- Arb universe close dates for UNF and BRZE are my estimates. CVRs aren't valued.
- The peer regression fits are loose (R squared 0.10 to 0.18).
- Relative value ignores dividends and Globalstar's Apple adjustment.
- The delta is Black-Scholes at implied vols backed out of wide quotes. It's an estimate.

## Corrections

None so far.
