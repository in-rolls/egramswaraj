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
sequentially and 350 MB.

### Full collection (2026-10-20)

`bin/collect_er.py` ran from a VM in Mumbai, 18-20 October 2026, and finished
with no failed requests. `raw/er_2026-10-20.tgz` (37 MB, SHA-256 in the
`.sha256` beside it) holds every response, contact fields removed, and the
request log (`er/log.jsonl`: URL, time, status, bytes, SHA-256).

    tar xzf raw/er_2026-10-20.tgz -C /tmp
    uv run python bin/build_er.py --src /tmp/er --out er_build

The built tables are in `data/`: `gps.parquet`, `members.parquet` and
`checks.json`, as below. `build_er.py` writes `gps.parquet` (150,019 GPs listed, 148,495 with members)
and `members.parquet` (1,541,551 members), validated against `schema/`, and
`checks.json` comparing them with the site's own published counts. It stops on
any designation not classified in `DESIGNATION_CLASS` (head, ward_member,
other).

The site stores some people twice: 923 GPs' responses repeat a row exactly
(2,963 rows; the site's own counts include them). Repeats are dropped and
counted in `gps.members_repeated`. Ten GPs list one head twice with a change
(ward, case, a stray letter, gender); the first entry is kept, or the one with a
recorded gender, and the pairs are in `checks.json` (`merged_head_reentries`).
Six GPs list two different people as head (`heads_listed = 2`), with no date to
say which is current; neither is chosen.

Care: Maharashtra lists about 4 members per GP against at least 7 seats, and
the site's own counts agree, so the site is incomplete there; Bihar's district
member counts match the site's in 5% of districts.

### Files

- `samples/sample_heads_OD_MP_PB.csv`: 60 heads, 20 GPs each in Odisha (Anugul),
  Madhya Pradesh (Bichhiya, Mandla) and Punjab (Ajnala); `request` is the URL.
- `samples/sample_all_members_OD_MP_PB.csv`: all 780 members of those GPs.
- `raw/`: the responses looked at, with `mobno` and `emailid` removed.
- `log.tsv`: every request (URL, UTC time, status, sha256 of the response **as
  received**, before the contact fields were removed).
- `bin/collect_er.py`: the full collector (every GP's elected representatives, state by state; resumable; drops the masked contact fields as it saves). Run on a VM in India: `python3 bin/collect_er.py --out er --workers 3`.
- `bin/`: the survey scripts. They route through a SOCKS proxy at localhost:1080
  (an SSH tunnel to a VM in India) and cache each response under `raw/`.

## Tables

```python
import pandas as pd
gps = pd.read_parquet("data/gps.parquet")
heads = pd.read_parquet("data/members.parquet").query("designation_class == 'head'")
heads.merge(gps.query("heads_listed == 1"), on=["state_code", "gp_code"])  # one head per GP
```

Types are as stored; `bin/describe.py` writes this section from the files and
`schema/*.schema.json`, and `--check` fails when it is stale.

<!-- tables:start -->

### `data/gps.parquet`

150,019 rows; one row per `gp_code`.

| Column | Type | Required | Allowed | Description |
|---|---|---|---|---|
| `state_code` | int16 | yes | 1–99 | eGramSwaraj / LGD state code. |
| `state_name` | string | yes |  | State name as in states.json. |
| `zp_code` | int64 | yes | 1– | District panchayat (zila parishad) code: an LGD local-body code, not an LGD district code. |
| `zp_name` | string | yes |  | District panchayat name as printed. |
| `bp_code` | int64 |  | 1– | Block panchayat code (LGD local-body code). Null in two-tier states, where GPs hang off the district panchayat. |
| `bp_name` | string |  |  | Block panchayat name as printed. Null in two-tier states. |
| `gp_code` | int64 | yes | 1– | Gram panchayat LGD local-body code. |
| `gp_name` | string | yes |  | Gram panchayat name as printed. |
| `site_er_count` | int32 | yes | 0– | Elected representatives the GP listing reports for this GP (gperCount). The collector fetches members only when this is above zero. |
| `site_male_count` | int32 | yes | 0– | Male ERs the GP listing reports (maleCount). |
| `site_female_count` | int32 | yes | 0– | Female ERs the GP listing reports (femaleCount). |
| `site_other_count` | int32 | yes | 0– | Other-gender ERs the GP listing reports (otherCount); corresponds to gender 'Transgender' in member responses. |
| `members_parsed` | int32 |  | 0– | Rows in the GP's member response as received, repeats included (the site's own ER count includes them). Null when the member response was not fetched (site_er_count is 0). |
| `members_repeated` | int32 |  | 0– | Rows that exactly repeat an earlier row of the same response (all four fields) and are left out of members.parquet. Null when not fetched. |
| `heads_merged` | int16 |  | 0– | Head rows dropped as a second entry of the same person (names equal ignoring case and spacing, or one stray character apart); the pairs are listed in checks.json. Null when not fetched. |
| `heads_listed` | int16 |  | 0– | Members classed head after repeats and re-entries are dropped. 2 means two different people (a successor beside a predecessor, or a proxy beside the head; undated); none is chosen. Null when not fetched. |
| `members_file` | string |  |  | Member response path relative to the collection directory, e.g. '10/members/93638.json'. Null when not fetched. |
| `members_sha256` | string |  |  | sha256 of the member response as received (before mobno/emailid were dropped), from log.jsonl. |
| `fetched_at` | timestamp (UTC) |  |  | UTC time the member response was saved, from log.jsonl. |

### `data/members.parquet`

1,541,551 rows; one row per `gp_code`, `member_index`.

| Column | Type | Required | Allowed | Description |
|---|---|---|---|---|
| `state_code` | int16 | yes | 1–99 | eGramSwaraj / LGD state code. |
| `gp_code` | int64 | yes | 1– | Gram panchayat LGD local-body code; joins to gps.gp_code. |
| `member_index` | int32 | yes | 0– | 0-based position of the person in the GP's member response. |
| `elected_name` | string |  |  | electedname exactly as printed, including stray whitespace and placeholder entries. |
| `designation` | string | yes |  | designationname exactly as printed. |
| `designation_class` | category | yes | `head`, `ward_member`, `other` | head: the GP's elected chief (Sarpanch, Mukhiya, Pradhan, President...). ward_member: a ward-elected GP member, including deputies who hold a ward. other: offices of other bodies (e.g. Bihar's Gram Kachahari), staff, co-opted members. Mapping per state is DESIGNATION_CLASS in bin/build_er.py. |
| `ward_name` | string |  |  | wardName exactly as printed; null for most heads. |
| `ward_no` | int16 |  | 0–999 | Ward number parsed from ward_name when it is an explicit ward number ('Ward No. 5', 'Ward-5', '5', 'Five', 'Wimc no.5', '5 No. Ward'); null otherwise (place names, village segments). |
| `gender` | category | yes | `Male`, `Female`, `Transgender`, `N/A` | gender exactly as the site codes it (N/A on one member). |

<!-- tables:end -->
