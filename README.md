# irdm-collar-spread

Data and code behind my Seeking Alpha piece on Iridium (IRDM) and the Rocket Lab deal. It's a carry trade worth roughly T-bills plus a little, so the piece sells a rule rather than a price view: own it hedged when the price implies about 93% close odds or less, and exit on a Justice Department or Team Telecom filing, an FCC clock stop or an End Date extension. The FCC never referred this deal to Team Telecom (it sent a courtesy copy), so the timing leans on large transfers that weren't referred either. Everything behind that rule is here: the collar priced off Rocket Lab's options, FCC timing from the FCC's own grant records (referred and not referred), a line-by-line break model, a vol-neutral version of the trade priced with real bid/ask, capacity and P&L in dollars, the decision tree, and a tracker that flags the entry and exit signals. See data/DATASETS.md for the datasets I keep extending.

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
    python scripts/realized_hedge.py
    python scripts/delay_incentive.py
    python scripts/collar_deal_sample.py
    python scripts/late_deals.py
    python scripts/tax_threshold_odds.py
    python scripts/short_interest.py
    python scripts/break_price_competition.py
    python scripts/irdm_options.py        (pass a chain CSV to run it on a newer pull)
    python scripts/fcc_team_telecom_timing.py
    python scripts/arb_crowding.py
    python scripts/implied_timing.py
    python scripts/holder_view.py
    python scripts/expected_value.py
    python scripts/tornado.py
    python scripts/spectrum_repricing.py
    python scripts/event_study.py
    python scripts/decision_tree.py
    python scripts/break_business_model.py
    python scripts/vol_neutral_structure.py
    python scripts/liquidity.py
    python scripts/tracker.py             (needs internet; weekly refresh, appends to results/tracker_log.csv)
    python scripts/tieout.py              (runs everything in order and checks every quoted number)

## What each script gives you

One thing first. Every valuation script reads data/anchor.json, which holds one snapshot of Iridium, Rocket Lab and Rocket Lab's option chain. The piece uses Nov 24 2026 at 10:36 a.m. ET (Iridium $42.18, Rocket Lab $45.45), with borrow pinned at 0.8% because intraday put-call parity gave a negative number. Some descriptions below still quote what a script printed on the Nov 23 close when I first wrote it, so today's output will differ. The numbers the piece actually quotes are in results/article_numbers.json, and tieout.py checks every one of them.

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
- realized_hedge.py: Iridium's daily dollar moves against Rocket Lab's since the signing, next to the option model's hedge ratio. They match (0.255 realized against 0.243 modeled over the last five weeks).
- delay_incentive.py: what the collar is worth on Rocket Lab's side at each close date. $205m moves to Rocket Lab between a March and a December close.
- collar_deal_sample.py: the first automated pass over 733 collar merger proxies from EDGAR full-text search. Kept for transparency. Its announcement dates are biased early, because the first 8-K item 1.01 is often a credit agreement, so the post doesn't use it.
- late_deals.py: the hand-checked set. 47 regulated collar deals closed (median 203 days) and 5 of 52 were terminated. It also lists the 8 that ran past about 18 months or hit their outside date: 4 closed and 4 terminated, and all 4 terminations came from regulators Iridium doesn't face. Expected value at 94.6%, 97% and 98% close odds.
- tax_threshold_odds.py: the odds Rocket Lab is under $45 at closing, which makes the deal taxable. It's about even, and it isn't a closing condition.
- short_interest.py: Rocket Lab short interest before and after the deal. It rose 12.2m shares and days to cover is 2.8, so it isn't crowded.
- break_price_competition.py: a broken Iridium if direct-to-device competition shrinks voice/data and broadband. $17 to $25 depending on how fast.
- irdm_options.py: Iridium's own option chain is too thin to price a break, and this shows how thin. Plus where the put open interest sits.
- fcc_team_telecom_timing.py: two FCC samples. Referred: every ECFS docket since the April 2020 Team Telecom executive order with a Team Telecom letter, 30 non-satellite grants (median 220 days) and three satellite ones (253, 316, 373). Not referred: 12 transfers and assignments where the grant order says the FCC didn't refer it or has no national security section at all (145 to 407 days, median 224). I started with five, all under 224 days, and the seven I added took it from a March grant to a late-April one. T-Mobile-Mint is in there even though the Justice Department pulled it back in four days after the notice, because it wasn't referred at the notice and that's the state Iridium is in. Iridium's notice says it wasn't referred, so the not-referred dates (Feb 7 to Oct 27 2027) carry half the weight. It also prints the twin's pace after its comment cycle: Globalstar's grant came 88 days after its reply deadline, which put on Iridium's Nov 9 deadline is Feb 5 2027.
- pull_snapshot.py: pulls Iridium, Rocket Lab and Rocket Lab's whole option chain from Nasdaq at one moment and writes data/anchor.json. Run it with a label, then tieout.py, to re-price everything at a new moment.
- article_numbers.py: computes every number the piece quotes from the anchor and writes results/article_numbers.json. (render_article.py is the small helper I use to fill my draft from that file.)
- implied_timing.py: holds my close odds fixed and solves for the closing date the price pays for. At the anchor it's Jun 7 2027, against a Mar 23 2027 median grant for the deals the FCC didn't refer.
- holder_view.py: the trade at $10,000: P&L for each outcome hedged, what Rocket Lab does to an unhedged holder, and the odds of an FCC grant by Mar 31 and Apr 30 2027 on each timing sample.
- arb_crowding.py: every 13F holder of Iridium, sorted by name into merger-arb and multi-strategy funds. They went from 2.2% of the shares at Jun 30 to 15.4% at Sep 30.
- expected_value.py: the base case. Close-date weights blended from the FCC sample and the six satellite deals, with close odds at 94.6% and 97% and a Party A re-bid at 0%, 25% and 50%.
- tornado.py: expected value as each input moves across its range. Close odds and Rocket Lab volatility matter most.
- spectrum_repricing.py: Iridium, Globalstar, Viasat and AST around SpaceX's EchoStar spectrum deal and now.
- event_study.py: Iridium's hedged daily moves around the FCC public notice, the petition withdrawal and the reply comments.
- data/foreign_approvals_tracker.csv: every approval the agreement requires, its clock and its public status.
- timing_weights.py: shared close-date weights: half the not-referred set, a quarter each referred set (35/45/18/2 for Mar/Jun/Sep/Dec 2027), and the model break price.
- decision_tree.py: each branch with its probability, date, Iridium's price then and the P&L on a $20m hedged position.
- break_business_model.py: a broken Iridium line by line, with direct-to-device erosion and EMSS repricing cases at 7.5x, 9.5x and 11.5x. Probability-weighted $22.81 at 9.5x.
- vol_neutral_structure.py: long Iridium, short 0.4 Rocket Lab, long 0.4 $67.50 call, short 0.24 $112.50 call, priced from the January 2028 chain with bid/ask. The spread costs $0.31 a share, more than the edge, and the structure flips the volatility exposure rather than removing it.
- liquidity.py: days to trade at 20% of volume for $5m, $20m and $50m, the hedge's footprint, and the dollar loss on a break.
- tracker.py: the monitor. It pulls prices, the bill rate and FCC docket 26-257, re-prices on base inputs, and flags the buy zone (implied odds below 93%), exit triggers (any DOJ or Team Telecom filing, which would mean a referral), new filings, and Rocket Lab under $45. Pulls fresh Iridium, Rocket Lab and 6-month bill prices, reprices the package and expected value, and logs a line. I run it weekly and before each update note.
- relative_value.py: Iridium against Globalstar/Amazon, TXNM/Blackstone and Norfolk Southern/Union Pacific on the same yardstick.
- tieout.py: reruns everything and fails if any number in the post stops reproducing.
- organic_trend.py: Iridium with Aireon taken out of the headline (pro forma revenue, nine month OEBITDA, Q3 by line).
- tax_line.py: the $45.00 Rocket Lab price where the stock leg drops under 40% of the consideration.
- implied_probability.py: the close odds the market is pricing for three guesses at a broken deal price, plus Party A's 5.5% regulatory fee in dollars a share.

Output from my run on Nov 24, 2026 is in results/, priced at the 10:36 a.m. ET anchor. The tracker logs have each refresh.

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
- FCC ECFS, GN Docket 26-257 filings list: data/fcc_docket_26-257_filings.csv
- EDGAR full-text search (DEFM14A, 2010 to 2026, "collar" "exchange ratio" "merger agreement") and data.sec.gov submissions histories: data/collar_deal_sample_edgar.csv
- Nasdaq short interest and option chains: data/rklb_short_interest_nasdaq_2026-11-24.csv, data/irdm_short_interest_nasdaq_2026-11-24.csv, data/irdm_option_chain_premarket_2026-11-24.csv
- FCC informal 180-day timeline: https://www.fcc.gov/general/informal-timeline-consideration-applications-transfers-or-assignments-licenses-or
- Deal timing, spectrum comps and arb universe terms: the 8-K and proxy for each deal, listed by row in data/deal_timing_database.csv, data/spectrum_comps.csv and data/arb_universe_2026-11-23.csv

## Things to be careful with

- results/tracker_log_v2.csv: the 9:33 a.m. row on Nov 24 was run on the older timing weights (referred deals only). Rows from 9:49 a.m. on use the current blend, which is why implied odds drop between them.
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
- The FCC sample is ECFS dockets with a Team Telecom letter: mostly wireline and media transfers, not satellite. Satellite filings that sit only in the FCC's international filing system aren't in it.
- No live borrow fee was available. Borrow is parity-implied (about 0.8%) and stressed from 0% to 3%.
- The hand-checked regulated set is small (52 deals) and mixed: utilities, cable, airlines, steel. It shows how regulated deals end, not how this one will. The automated pass in collar_deal_sample.py is noisier.
- The EDGAR collar sample is broad. "Mentions the FCC or CFIUS" pulls in utilities, cable and defense deals. Dates come from filing histories (8-K items 1.01 and 2.01, Forms 25 and 15), not press releases. Some joint proxies list the acquirer first. I don't report a break rate from it, because 8-K item 1.02 also covers credit facilities and old agreements and would need checking by hand.
- The competition scenarios (decline rates, flow-through to OEBITDA) are my assumptions.
- The Iridium option chain in data/ is a pre-market snapshot.
- The peer regression fits are loose (R squared 0.10 to 0.18).
- Relative value ignores dividends and Globalstar's Apple adjustment.
- The delta is Black-Scholes at implied vols backed out of wide quotes. It's an estimate.

## Corrections

Nov 24 2026, before publication: I grew the not-referred FCC sample from five deals to 12 by reading seven more grant orders. On the same 10:36 a.m. prices, the odds of a grant by Apr 30 2027 went from 63% to 43%, by Mar 31 from 35% to 26%, the base case from $42.26 to $42.03, and my rating from a buy to a hold. The first five are still in the file. The new rows say where each one came from.
