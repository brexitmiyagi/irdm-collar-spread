# Living datasets

Two datasets here are built to be reused and extended with every merger I cover. Each new piece adds its rows and keeps the old ones.

## fcc_team_telecom_transfers_ecfs.csv
Every FCC docket since the April 2020 Team Telecom executive order where the Justice Department or Team Telecom put a letter in ECFS, plus the three large satellite transfers (Viasat/Inmarsat, Eutelsat/OneWeb, SES/Intelsat).
Columns: docket, sector, accepted_pn (date of the FCC's accepted-for-filing notice), fcc_action (grant or withdrawal date), days, outcome, first_team_telecom_letter, days_to_first_tt_letter, tt_extension_or_secondary, action_doc (the FCC document I read).
How rows are added: find the docket, read the accepted-for-filing notice and the grant document, record both dates and the document number. Never infer a grant from a filename.
Known gaps: filings that sit only in the FCC's international filing system (ICFS) aren't covered unless the grant document is public on docs.fcc.gov.

## collar_deal_sample_edgar.csv, regulated_collar_deals_handchecked.csv, late_regulated_deals_handchecked.csv
Merger proxies since 2010 that mention a collar and an exchange ratio (EDGAR full-text search), the regulated subset dated from merger 8-Ks to Form 25 or 15, and the deals that ran long, each with the 8-Ks I read.
How rows are added: date from the 8-K whose Item 1.01 says the company "entered into" a merger agreement, to the target's Form 25 or 15. Terminations are read from the 8-K text, never from item numbers alone.

## foreign_approvals_tracker.csv
Approval-by-approval status for the deal in hand, with statutory clocks and sources. Rebuilt per deal.

## fcc_nonreferred_transfers.csv

Large FCC transfers the FCC did not refer to Team Telecom. Each row is dated from the accepted-for-filing notice to the grant order, and the referral note says how I know it wasn't referred: the order says so (Amazon-Globalstar), or it has no national security section (the others). To extend it, read the grant order's national security section and look for "courtesy copy" or "not referred". Iridium's own notice (DA 26-985, n.20) says it wasn't referred.

## irdm_13f_all_holders_nasdaq_2026-11-24.json

Nasdaq's full 13F holder list for Iridium as of Sep 30 2026, with each holder's change from the prior quarter. scripts/arb_crowding.py sorts holders by name; the name lists are mine and easy to edit.
