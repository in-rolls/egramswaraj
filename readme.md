# eGramSwaraj

We scrape the [expenditure reports](https://egramswaraj.gov.in/RecExpReportNew.do?finYear=2024-2025&scheme_uid=3287) for various years.

## Elected representatives (surveyed 2026-10-18)

A survey of eGramSwaraj's elected-representative (ER) data, made for a quota study
that needs, per gram panchayat (GP) and per election, the head seat's reservation
and the winner. Nothing here is a bulk collection.

### What it has and does not have

For each GP, the people elected in the **current term**, six fields each:
`electedname, designationname, wardName, gender, mobno, emailid` (phone and email
masked by the site; both are removed from the files committed here).

- **No seat reservation and no caste category**, for the seat or the person.
- **No election year and no history.** The `year` parameter changes only the GP
  count; ER counts are identical for 2018, 2022 and 2026.
- **GP code is the LGD code**: 7 of 7 sampled codes matched the India Data Portal's
  LGD mirror (March 2023) by name, block and state.
- Coverage (state-level response, `raw/egs_ER_stateGp.json`): 24 states, about
  168,000 GPs and 1.59 million GP-level ERs. None for Andhra Pradesh, Karnataka,
  Rajasthan, Uttar Pradesh, Jammu & Kashmir, Ladakh, Meghalaya, Nagaland,
  Puducherry, Lakshadweep. Maharashtra lists 1-10 ERs per GP (incomplete); Tamil
  Nadu covers 9 of 37 districts.
- Rows seen that need care: a male-named sarpanch coded female (Mandla, MP);
  administrators ("VAHIVATDAR", "TALATI") listed beside sarpanches (Gujarat).

Use: current-term head name, sex and LGD code, joinable to a state election
commission's reservation list. Reservation must come from the state commission.

### Endpoints

Plain GETs returning JSON, no captcha or cookie; a Referer header was sent. The site
refuses non-Indian connections. `raw/er_service.js` is the site's Angular source.

| Step | Endpoint |
|---|---|
| States | `ElectedStateReportGp.do?year=2026` |
| Districts (zp) | `ElectedStatePanReportGp.do?stateCode=S&year=2026` |
| Blocks (bp) | `findBpNameAndGPCountByZpCode.do?stateCode=S&year=2026&zpCode=Z` (Maharashtra and Punjab time out; `findElectedStateBpByZpCode.do` works) |
| GPs | `findGpNameAndERCountByBpCode.do?stateCode=S&year=2026&bpCode=B` (two-tier states 30, 38, 12, 11, 34, 31: pass zpCode as bpCode) |
| People | `ElectedMemberRepresent.do?code=GPCODE&stateCode=S&level=V` |

zp and bp codes are LGD local-body codes, a different series from LGD district and
block codes.

A full sweep is about 175,000 requests; at the measured 7.5 s each, about 15 days
sequentially and 350 MB. The site's terms of use restrict copying and
redistribution; check them before any bulk run.

### Files

- `samples/sample_heads_OD_MP_PB.csv`: 60 heads, 20 GPs each in Odisha (Anugul),
  Madhya Pradesh (Bichhiya, Mandla) and Punjab (Ajnala); `request` is the URL.
- `samples/sample_all_members_OD_MP_PB.csv`: all 780 members of those GPs.
- `raw/`: the responses looked at, with `mobno` and `emailid` removed.
- `log.tsv`: every request (URL, UTC time, status, sha256 of the response **as
  received**, before the contact fields were removed).
- `bin/`: the survey scripts. They route through a SOCKS proxy at localhost:1080
  (an SSH tunnel to a VM in India) and cache each response under `raw/`.
