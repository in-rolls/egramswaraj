"""Parse a collect_er.py output directory into typed, validated tables.

    uv run python bin/build_er.py --src er_partial --out er_build

Builds only the states run.out reports as finished ("state S: n/n GPs saved").
Writes gps.parquet, members.parquet, checks.json and sample.json to --out, and
validates both parquet files, as read back from disk, against the Frictionless
Table Schemas in schema/.

Checks compare what was parsed with the site's own published counts (states.json,
zp.json, bp_*.json, gp_*.json) and report agreement rates. Only structural
problems stop the build: unreadable files, unexpected keys, duplicate keys,
orphan files, gender outside the site's vocabulary, or a designation with no
class in DESIGNATION_CLASS.
"""

import argparse
import collections
import json
import pathlib
import random
import re
import sys

import pandas as pd
from pandera.io.pandas_io import from_frictionless_schema

ROOT = pathlib.Path(__file__).resolve().parent.parent
SCHEMA_DIR = ROOT / "schema"
TWO_TIER = {30, 38, 12, 11, 34, 31}  # same set as collect_er.py
# The site's own codes; it prints N/A for one member.
GENDERS = ["Male", "Female", "Transgender", "N/A"]
CLASSES = ["head", "ward_member", "other"]
MEMBER_KEYS = {"electedname", "designationname", "wardName", "gender"}
FINISHED = re.compile(r"^state (\d+): (\d+)/(\d+) GPs saved$")

# (state code, designationname exactly as printed) -> class. A designation not
# listed here stops the build, so each new state gets an explicit decision.
# Deputies (Up Mukhiya, Up Sarpanch, Vice President, ...) are ward_member: every
# deputy row carries a ward name and almost none shares its ward with another
# member row, so they hold a ward seat (Bihar's Up Mukhiya is the exception:
# about a third repeat a Ward Member row of the same ward).
DESIGNATION_CLASS = {
    # Himachal Pradesh: Pradhan is printed "President GP".
    (2, "President GP"): "head",
    (2, "Vice President"): "ward_member",
    (2, "Ward Members"): "ward_member",
    # Haryana
    (6, "Sarpanch"): "head",
    (6, "Panch"): "ward_member",
    # Bihar: Sarpanch, Up Sarpanch and Panch belong to the Gram Kachahari, the
    # village court, elected separately from the GP; its Panch sits beside a
    # Ward Member of the same ward in 90% of rows. Mukhiya heads the GP.
    (10, "Mukhiya"): "head",
    (10, "Up Mukhiya"): "ward_member",
    (10, "Ward Member"): "ward_member",
    (10, "Sarpanch"): "other",
    (10, "Up Sarpanch"): "other",
    (10, "Panch"): "other",
    (10, "Data Entry Operator"): "other",
    # Arunachal Pradesh
    (12, "Gram Panchayat Chairperson"): "head",
    (12, "Gram Panchayat Member"): "ward_member",
    # Assam
    (18, "President"): "head",
    (18, "Vice President"): "ward_member",
    (18, "Ward Member"): "ward_member",
    # Jharkhand
    (20, "Mukhiya"): "head",
    (20, "UP MUKHIYA"): "ward_member",
    (20, "WARD MEMBER"): "ward_member",
    # Chhattisgarh: the PESA Gram Sabha Adhyaksh chairs the gram sabha, not a ward.
    (22, "Sarpanch"): "head",
    (22, "Up Sarpanch"): "ward_member",
    (22, "Panch"): "ward_member",
    (22, "PESA Gram Sabha Adhyaksh"): "other",
    # Gujarat: VAHIVATDAR (administrator) and TALATI (village secretary) are
    # officials' titles, but the rows are ward seats: one per ward (mode 8 per
    # GP, the statutory minimum), each with a ward name, and a GP uses one title
    # or the other for all its seats. Read as ward members entered under the
    # data-entry officer's title. Many names are placeholders ('abcd', 'sabhya').
    (24, "SARPANCH"): "head",
    (24, "VAHIVATDAR"): "ward_member",
    (24, "TALATI"): "ward_member",
    # Goa
    (30, "Sarpanch"): "head",
    (30, "Deputy Sarpanch"): "ward_member",
    (30, "Panch Member"): "ward_member",
    (30, "Coopted member"): "other",
    # Kerala: standing committee chairs are elected ward members.
    (32, "President"): "head",
    (32, "Vice President "): "ward_member",
    (32, "Standing Committee Chairman"): "ward_member",
    (32, "Member"): "ward_member",
    (32, "Deputy Director"): "other",
    # Andaman and Nicobar: Pradhan heads the GP. Sarpanch / UP Sarpanch appear
    # beside a Pradhan in 61 of 70 GPs, each with a ward no Ward Member row
    # covers; what office they are is unresolved, so they are not counted as GP
    # ward members.
    (35, "Pradhan"): "head",
    (35, "UP Pradhan"): "ward_member",
    (35, "Ward Member"): "ward_member",
    (35, "Sarpanch"): "other",
    (35, "UP Sarpanch"): "other",
    # Sikkim: the Secretary is the panchayat's official, not an elected seat.
    (11, "President"): "head",
    (11, "Vice President"): "ward_member",
    (11, "Member"): "ward_member",
    (11, "Secretary"): "other",
    # Tripura
    (16, "Pradhan"): "head",
    (16, "Upa-Pradhan"): "ward_member",
    (16, "Member"): "ward_member",
    # West Bengal: one CHAIRMAN per GP (2,936 in 2,935 GPs) heads it. The
    # upa-samiti posts (Artha O Parikalpana, Nari O Sishu Unnayan, ...) are
    # held by elected members, as Kerala's standing committee chairs are.
    (19, "CHAIRMAN"): "head",
    (19, "VICE CHAIRMAN"): "ward_member",
    (19, "MEMBER"): "ward_member",
    (19, "CHARMAN STANDING COMMITTEE"): "ward_member",
    (19, "Artha O Parikalpana"): "ward_member",
    (19, "Krishi O Pranisampad"): "ward_member",
    (19, "Nari O Sishu Unnayan"): "ward_member",
    (19, "Shilpa O Parikathamo"): "ward_member",
    (19, "Sikha O Jana Swastha"): "ward_member",
    # Odisha
    (21, "Sarpanch"): "head",
    (21, "Naib Sarpanch"): "ward_member",
    (21, "Member"): "ward_member",
    # Madhya Pradesh: the Sachiv is the panchayat secretary, an official.
    (23, "Sarpanch"): "head",
    (23, "Upsarpanch"): "ward_member",
    (23, "Panch"): "ward_member",
    (23, "Sachiv"): "other",
    # Maharashtra
    (27, "SARPANCH"): "head",
    (27, "DEPUTY SARPANCH"): "ward_member",
    (27, "GRAMPANCHAYAT SADASYA"): "ward_member",
    # Punjab
    (3, "Sarpanch"): "head",
    (3, "Panch"): "ward_member",
    # Telangana: co-opted members are appointed, not elected to a ward.
    (36, "Sarpanch"): "head",
    (36, "Upa Sarpanch"): "ward_member",
    (36, "Ward Member"): "ward_member",
    (36, "Co-Opted Member"): "other",
    # Dadra and Nagar Haveli and Daman and Diu
    (38, "Sarpanch"): "head",
    (38, "Upa - Sarpanch"): "ward_member",
    (38, "Ward Member"): "ward_member",
    # Uttarakhand
    (5, "Pradhan Gram Panchayat "): "head",  # printed with a trailing space
    (5, "Uppradhan Gram Panchayat"): "ward_member",
    (5, "Member Gram Panchayat"): "ward_member",
}

NUMBER_WORDS = {
    w: i
    for i, w in enumerate(
        "zero one two three four five six seven eight nine ten eleven twelve thirteen "
        "fourteen fifteen sixteen seventeen eighteen nineteen twenty twenty-one twenty-two "
        "twenty-three twenty-four twenty-five twenty-six twenty-seven twenty-eight "
        "twenty-nine thirty".split()
    )
}
# Explicit ward numbers only: "Ward No. - 5", "Word No 5", "WardNumber5",
# "Naudiha-Ward No. 5" (place prefix), bare "5", "5 No. Ward" (Assam) and
# "Wimc no.5" (Bihar's Ward Implementation and Management Committee, one per
# ward). Place-numbered segments such as "Bambooflat-2" stay null.
WARD_PATTERNS = [
    re.compile(
        r"(?:^|[\s\-,(/])(?:w[aor]{1,2}d|wimc)\s*(?:no|number|num|name|o)?"
        r"\s*[.:\-]*\s*(\d{1,3})\s*\.?\s*$",
        re.I,
    ),
    re.compile(r"^\s*(\d{1,3})\s*$"),
    re.compile(r"^\s*(\d{1,3})\s*no\.?\s*ward\s*$", re.I),
]

PLACEHOLDER_NAMES = {
    "sarpanch", "talati", "vahivatdar", "sabhya", "member", "membar", "ward", "word",
    "wordno", "wored no", "word one", "shabhy one", "name", "nameeee", "abc", "abcd",
    "xyz", "xyx", "na", "n/a", "nil", "test", "-", ".",
}  # fmt: skip

GPS_DTYPES = {
    "state_code": "int16",
    "state_name": "string",
    "zp_code": "int64",
    "zp_name": "string",
    "bp_code": "Int64",
    "bp_name": "string",
    "gp_code": "int64",
    "gp_name": "string",
    "site_er_count": "int32",
    "site_male_count": "int32",
    "site_female_count": "int32",
    "site_other_count": "int32",
    "members_parsed": "Int32",
    "members_repeated": "Int32",
    "heads_listed": "Int16",
    "members_file": "string",
    "members_sha256": "string",
    "fetched_at": "datetime64[us, UTC]",
}
MEMBERS_DTYPES = {
    "state_code": "int16",
    "gp_code": "int64",
    "member_index": "int32",
    "elected_name": "string",
    "designation": "string",
    "designation_class": pd.CategoricalDtype(CLASSES),
    "ward_name": "string",
    "ward_no": "Int16",
    "gender": pd.CategoricalDtype(GENDERS),
}


class StructuralError(Exception):
    pass


def ward_no(name):
    if pd.isna(name):
        return None
    s = name.strip()
    if s.lower() in NUMBER_WORDS:
        return NUMBER_WORDS[s.lower()]
    for pat in WARD_PATTERNS:
        m = pat.search(s)
        if m:
            return int(m.group(1))
    return None


def is_placeholder(name):
    s = "" if pd.isna(name) else re.sub(r"\s+", " ", name.strip().lower())
    return (
        s in PLACEHOLDER_NAMES
        or re.fullmatch(r"(.)\1{2,}", s.replace(" ", "")) is not None
        or not re.search(r"[^\W\d_]", s)
    )


def read_json(path, problems):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        problems.append(f"unreadable {path}: {exc}")
        return None


def finished_states(src):
    done = {}
    for line in (src / "run.out").read_text(encoding="utf-8").splitlines():
        m = FINISHED.match(line.strip())
        if m and m.group(2) == m.group(3):
            done[int(m.group(1))] = int(m.group(3))
    return done


def read_log(src):
    """file -> (sha256, time) of its last successful fetch."""
    ok = {}
    with open(src / "log.jsonl", encoding="utf-8") as fh:
        for line in fh:
            e = json.loads(line)
            if "sha256" in e:
                ok[e["file"]] = (e["sha256"], e["time"])
    return ok


def site_er(row):
    # bp_alt rows (findElectedStateBpByZpCode) report ERs in bperCount, not gperCount
    return row["gperCount"] if row.get("gperCount") is not None else row.get("bperCount")


def walk_state(src, sc, sname, problems):
    """GP listing rows with their hierarchy, plus block/zp site counts."""
    d = src / str(sc)
    zps = read_json(d / "zp.json", problems) or []
    gps, units, used = [], [], {d / "zp.json"}
    for z in zps:
        zp = z["zpCode"]
        zunit = {"level": "zp", "zp_code": zp, "name": z["zpName"], "site_gp_count": z["gpCount"]}
        zunit |= {
            "site_er": site_er(z),
            "site_male": z["maleCount"],
            "site_female": z["femaleCount"],
        }
        units.append(zunit)
        if not z.get("gperCount"):
            zunit["listed"] = "skipped: zp gperCount 0"
            continue
        if sc in TWO_TIER:
            blocks = [(None, None, zp, None)]
        else:
            f = d / f"bp_{zp}.json"
            if not f.exists():
                f = d / f"bp_alt_{zp}.json"
            if not f.exists():
                zunit["listed"] = "missing block list"
                continue
            used.add(f)
            blocks = []
            for b in read_json(f, problems) or []:
                bunit = {"level": "bp", "zp_code": zp, "bp_code": b["bpCode"], "name": b["bpName"]}
                bunit |= {"site_gp_count": b["gpCount"], "site_er": site_er(b)}
                bunit |= {"site_male": b["maleCount"], "site_female": b["femaleCount"]}
                bunit["source"] = f.name.rsplit("_", 1)[0]
                units.append(bunit)
                blocks.append((b["bpCode"], b["bpName"], b["bpCode"], bunit))
        zunit["listed"] = "yes"
        for bp, bpname, key, bunit in blocks:
            f = d / f"gp_{key}.json"
            if not f.exists():
                if bunit is not None:
                    why = "skipped: bp gperCount 0" if bunit["site_er"] == 0 else "MISSING"
                    if bunit["site_er"] and bunit.get("source") == "bp_alt":
                        why = "MISSING: collector drops bp_alt blocks (gperCount is null)"
                    bunit["listed"] = why
                continue
            if bunit is not None:
                bunit["listed"] = "yes"
            used.add(f)
            for g in read_json(f, problems) or []:
                gps.append(
                    {
                        "state_code": sc,
                        "state_name": sname,
                        "zp_code": zp,
                        "zp_name": z["zpName"],
                        "bp_code": bp,
                        "bp_name": bpname,
                        "gp_code": g["gpCode"],
                        "gp_name": g["gpName"],
                        "site_er_count": g["gperCount"] or 0,
                        "site_male_count": g["maleCount"] or 0,
                        "site_female_count": g["femaleCount"] or 0,
                        "site_other_count": g["otherCount"] or 0,
                    }
                )
    listing_files = set(d.glob("*.json"))
    # A block list fetched by the fallback endpoint after the main one timed out,
    # where a later retry of the main one succeeded: superseded, not orphaned.
    for f in list(listing_files - used):
        if f.name.startswith("bp_alt_") and (d / f.name.replace("bp_alt_", "bp_")) in used:
            used.add(f)
    for f in sorted(listing_files - used):
        problems.append(f"orphan listing file {f}")
    return gps, units


def parse_members(src, sc, gps, log, problems):
    rows = []
    listed = {g["gp_code"] for g in gps}
    for f in sorted((src / str(sc) / "members").glob("*.json")):
        if not f.stem.isdigit() or int(f.stem) not in listed:
            problems.append(f"orphan member file {f}")
    for g in gps:
        rel = f"{sc}/members/{g['gp_code']}.json"
        path = src / rel
        g["members_parsed"] = g["members_file"] = g["members_sha256"] = g["fetched_at"] = None
        g["members_repeated"] = None
        if not path.exists():
            if g["site_er_count"]:
                problems.append(f"missing member file {rel} (site_er_count {g['site_er_count']})")
            continue
        data = read_json(path, problems)
        if not isinstance(data, list):
            problems.append(f"{rel}: not a list")
            continue
        if rel not in log:
            problems.append(f"{rel}: no successful fetch in log.jsonl")
            continue
        g["members_file"] = rel
        g["members_sha256"], g["fetched_at"] = log[rel]
        g["members_parsed"] = len(data)
        # The site stores some people twice: 923 GPs' responses repeat a row
        # exactly (all four fields), and in 871 of them the site's own ER count
        # includes the repeat. A repeat is dropped; member_index keeps the
        # position in the response, and members_repeated says how many went.
        seen, g["members_repeated"] = set(), 0
        for i, r in enumerate(data):
            key = json.dumps(r, sort_keys=True)
            if key in seen:
                g["members_repeated"] += 1
                continue
            seen.add(key)
            if not isinstance(r, dict) or set(r) != MEMBER_KEYS:
                problems.append(
                    f"{rel}[{i}]: unexpected keys {sorted(r) if isinstance(r, dict) else r}"
                )
                continue
            rows.append(
                {
                    "state_code": sc,
                    "gp_code": g["gp_code"],
                    "member_index": i,
                    "elected_name": r["electedname"],
                    "designation": r["designationname"],
                    "ward_name": r["wardName"],
                    "gender": r["gender"],
                }
            )
    return rows


def to_frames(gps, members, problems):
    g = pd.DataFrame(gps, columns=list(GPS_DTYPES))
    g["fetched_at"] = pd.to_datetime(g["fetched_at"], utc=True, format="%Y-%m-%dT%H:%M:%SZ")
    g = g.astype(GPS_DTYPES).sort_values(["state_code", "gp_code"], ignore_index=True)
    m = pd.DataFrame(members)
    bad_gender = m.loc[~m["gender"].isin(GENDERS), ["gp_code", "member_index", "gender"]]
    for row in bad_gender.head(20).itertuples():
        problems.append(f"gender outside {GENDERS}: {row}")
    keys = list(zip(m["state_code"], m["designation"]))
    unmapped = sorted({k for k in keys if k not in DESIGNATION_CLASS}, key=str)
    for k in unmapped:
        problems.append(f"designation with no class in DESIGNATION_CLASS: {k}")
    m["designation_class"] = [DESIGNATION_CLASS.get(k) for k in keys]
    m["ward_no"] = [ward_no(w) for w in m["ward_name"]]
    m = m[list(MEMBERS_DTYPES)].astype(MEMBERS_DTYPES)
    m = m.sort_values(["state_code", "gp_code", "member_index"], ignore_index=True)
    # More than one head after repeats are dropped: the same person entered
    # twice with a spelling, ward or gender change, or two different people
    # (a successor kept beside the predecessor, undated). Counted, not chosen.
    heads = m[m.designation_class == "head"].groupby("gp_code").size()
    g["heads_listed"] = g.gp_code.map(heads).fillna(0).astype("Int16")
    g.loc[g.members_file.isna(), "heads_listed"] = pd.NA
    return g, m


def validate(path, schema_path, dtypes):
    """Frictionless constraints via pandera, with exact dtypes and no coercion."""
    schema = from_frictionless_schema(schema_path)
    schema = schema.update_columns({c: {"dtype": t, "coerce": False} for c, t in dtypes.items()})
    schema.coerce = False
    df = pd.read_parquet(path)
    schema.validate(df, lazy=True)
    return df


def jsonable(x):
    return None if x is pd.NA else int(x)


def rate(num, den):
    return None if not den else round(num / den, 6)


def examples(df, cols, n=5):
    return json.loads(df[cols].head(n).to_json(orient="records", force_ascii=False))


def state_checks(sc, st, gps_df, mem_df, units, sample_gp_codes):
    g = gps_df[gps_df.state_code == sc]
    m = mem_df[mem_df.state_code == sc]
    fetched = g[g.members_file.notna()]
    c = {"state_name": st["stateName"]}

    # GP coverage against the state row and the zp/bp rows
    zps = [u for u in units if u["level"] == "zp"]
    bps = [u for u in units if u["level"] == "bp"]
    c["site_state_gp_count"] = st["gpCount"]
    c["site_zp_gp_count_sum"] = sum(u["site_gp_count"] or 0 for u in zps)
    c["gp_listing_rows"] = len(g)
    c["gp_listing_rows_with_er"] = int((g.site_er_count > 0).sum())
    c["gp_listing_share_of_state_gp_count"] = rate(len(g), st["gpCount"])
    c["members_files"] = len(fetched)
    unlisted = collections.Counter()
    unlisted_gps = collections.Counter()
    unlisted_ers = collections.Counter()
    for u in zps + bps:
        if u.get("listed") not in (None, "yes"):
            unlisted[u["listed"]] += 1
            unlisted_gps[u["listed"]] += u["site_gp_count"] or 0
            unlisted_ers[u["listed"]] += u["site_er"] or 0
    c["units_not_listed"] = {
        k: {"units": v, "site_gp_count": unlisted_gps[k], "site_er_count": unlisted_ers[k]}
        for k, v in unlisted.items()
    }
    c["units_not_listed_examples"] = [
        {k: u.get(k) for k in ("level", "zp_code", "bp_code", "name", "site_gp_count", "site_er")}
        | {"why": u["listed"]}
        for u in zps + bps
        if u.get("listed") not in (None, "yes") and u["listed"].startswith("MISSING")
    ][:5]

    # per-unit agreement: GPs listed and members by gender vs the unit's published counts
    sex = m.groupby(["gp_code", "gender"], observed=True).size().unstack(fill_value=0)
    sex = sex.reindex(columns=GENDERS, fill_value=0)
    gx = g.set_index("gp_code").join(sex).fillna({k: 0 for k in GENDERS})
    for level, key in (("zp", "zp_code"), ("bp", "bp_code")):
        us = [u for u in (zps if level == "zp" else bps) if u.get("listed") == "yes"]
        if not us:
            continue
        agg = gx.groupby(key).agg(
            gps=("gp_name", "size"),
            ers=("members_parsed", "sum"),
            male=("Male", "sum"),
            female=("Female", "sum"),
        )
        gp_eq = er_eq = sex_eq = 0
        bad = []
        for u in us:
            a = agg.loc[u[key]] if u[key] in agg.index else None
            got = (0, 0, 0, 0) if a is None else (a.gps, a.ers, a.male, a.female)
            want = (u["site_gp_count"], u["site_er"], u["site_male"], u["site_female"])
            gp_eq += got[0] == want[0]
            er_eq += got[1] == want[1]
            sex_eq += got[2:] == want[2:]
            if got != want and len(bad) < 5:
                bad.append({key: u[key], "name": u["name"], "parsed": list(map(int, got))})
                bad[-1]["site"] = want
        c[f"{level}_units_compared"] = len(us)
        c[f"{level}_gp_count_agreement"] = rate(gp_eq, len(us))
        c[f"{level}_er_count_agreement"] = rate(er_eq, len(us))
        c[f"{level}_male_female_agreement"] = rate(sex_eq, len(us))
        c[f"{level}_mismatch_examples (gps, ers, male, female)"] = bad

    # per-GP agreement
    f = gx[gx.members_file.notna()]
    diff = f.members_parsed.astype(int) - f.site_er_count
    c["gp_er_count_agreement"] = rate(int((diff == 0).sum()), len(f))
    c["gp_er_count_more_than_site"] = int((diff > 0).sum())
    c["gp_er_count_fewer_than_site"] = int((diff < 0).sum())
    sex_ok = (
        (f.Male == f.site_male_count)
        & (f.Female == f.site_female_count)
        & (f.Transgender == f.site_other_count)
    )
    c["gp_gender_count_agreement"] = rate(int(sex_ok.sum()), len(f))
    bad = f[(diff != 0) | ~sex_ok].reset_index()
    c["gp_mismatch_examples"] = examples(
        bad,
        ["gp_code", "gp_name", "site_er_count", "members_parsed", "site_male_count", "Male"]
        + ["site_female_count", "Female", "site_other_count", "Transgender"],
    )
    c["gp_zero_member_rows"] = int((f.members_parsed == 0).sum())

    # state totals
    gender = m.gender.value_counts().reindex(GENDERS, fill_value=0)
    c["members"] = len(m)
    c["members_by_gender"] = {k: int(v) for k, v in gender.items()}
    c["site_state_er_count"] = st["gperCount"]
    c["site_state_by_gender"] = {
        "Male": st["maleCount"],
        "Female": st["femaleCount"],
        "Transgender": st["otherCount"],
    }
    c["state_er_count_share"] = rate(len(m), st["gperCount"])
    # The state row's gperCount can exceed the sum of the site's own zp rows, so the
    # chain shows where a shortfall arises: state -> zp rows -> GP listing -> parsed.
    c["site_zp_er_sum"] = sum(u["site_er"] or 0 for u in zps)
    c["site_gp_listing_er_sum"] = int(g.site_er_count.sum())

    # designations and heads
    c["designations"] = {
        f"{d} -> {DESIGNATION_CLASS[(sc, d)]}": int(n)
        for d, n in m.designation.value_counts().items()
    }
    heads = m[m.designation_class == "head"].groupby("gp_code").size()
    nh = heads.reindex(f.index, fill_value=0)
    c["gps_with_members"] = len(f)
    c["heads"] = int(heads.sum())
    c["share_gps_0_heads"] = rate(int((nh == 0).sum()), len(f))
    c["share_gps_1_head"] = rate(int((nh == 1).sum()), len(f))
    c["share_gps_2plus_heads"] = rate(int((nh > 1).sum()), len(f))
    c["gps_0_heads_examples"] = [int(x) for x in nh[nh == 0].index[:5]]
    c["gps_2plus_heads_examples"] = [int(x) for x in nh[nh > 1].index[:5]]
    for cls in ("head", "ward_member"):
        x = m[m.designation_class == cls]
        c[f"share_female_{cls}"] = rate(int((x.gender == "Female").sum()), len(x))
    c["share_female_all"] = rate(int((m.gender == "Female").sum()), len(m))

    # names
    name = m.elected_name.fillna("").str.strip().str.lower().str.replace(r"\s+", " ", regex=True)
    # Where the head is chosen from among ward members, the site lists them twice.
    keyed = m.assign(n=name)
    wm = keyed[keyed.designation_class == "ward_member"][["gp_code", "n"]].drop_duplicates()
    hd = keyed[(keyed.designation_class == "head") & (name != "")][["gp_code", "n"]]
    both = hd.merge(wm, on=["gp_code", "n"], how="inner")
    c["share_heads_also_listed_as_ward_member"] = rate(len(both), len(hd))
    empty = name == ""
    c["empty_names"] = int(empty.sum())
    c["empty_name_examples"] = examples(m[empty], ["gp_code", "member_index", "designation"])
    ph = m.elected_name.map(is_placeholder).astype(bool) & ~empty
    c["placeholder_names"] = int(ph.sum())
    c["placeholder_name_share"] = rate(int(ph.sum()), len(m))
    c["placeholder_name_top"] = dict(collections.Counter(name[ph]).most_common(10))
    dup = m.assign(n=name)[~empty].duplicated(["gp_code", "n"], keep=False)
    dup = dup.reindex(m.index, fill_value=False)
    c["rows_with_duplicate_name_in_gp"] = int(dup.sum())
    c["gps_with_duplicate_name"] = int(m[dup].gp_code.nunique())
    c["share_gps_with_duplicate_name"] = rate(c["gps_with_duplicate_name"], len(f))
    c["duplicate_name_examples"] = examples(
        m[dup], ["gp_code", "member_index", "elected_name", "designation", "ward_name"]
    )

    # wards
    w = m[m.ward_name.notna()]
    c["ward_name_present"] = len(w)
    c["ward_no_parsed_share"] = rate(int(w.ward_no.notna().sum()), len(w))
    c["ward_name_unparsed_top"] = {
        k: int(v)
        for k, v in w[w.ward_no.isna()]
        .ward_name.str.replace(r"\d+", "N", regex=True)
        .value_counts()
        .head(8)
        .items()
    }
    c["sample_blocks"] = sample_gp_codes
    return c


def build_sample(gps_df, mem_df, states, seed):
    rng = random.Random(seed)
    out = {}
    for sc in states:
        g = gps_df[gps_df.state_code == sc]
        unit = "zp_code" if sc in TWO_TIER else "bp_code"
        units = sorted(g[unit].dropna().unique().tolist())
        blocks = []
        for u in rng.sample(units, min(3, len(units))):
            gb = g[g[unit] == u]
            pick = sorted(rng.sample(gb.gp_code.tolist(), min(8, len(gb))))
            gp_rows = []
            for code in pick:
                r = gb[gb.gp_code == code].iloc[0]
                mm = mem_df[mem_df.gp_code == code]
                gp_rows.append(
                    {
                        "gp_code": int(code),
                        "gp_name": r.gp_name,
                        "site_er_count": int(r.site_er_count),
                        "members_parsed": (
                            None if pd.isna(r.members_parsed) else int(r.members_parsed)
                        ),
                        "members": [
                            {
                                "name": x.elected_name,
                                "designation": x.designation,
                                "class": x.designation_class,
                                "ward": x.ward_name,
                                "ward_no": None if pd.isna(x.ward_no) else int(x.ward_no),
                                "gender": x.gender,
                            }
                            for x in mm.itertuples()
                        ],
                    }
                )
            first = gb.iloc[0]
            blocks.append(
                {
                    "zp_code": int(first.zp_code),
                    "zp_name": first.zp_name,
                    "bp_code": None if pd.isna(first.bp_code) else int(first.bp_code),
                    "bp_name": None if pd.isna(first.bp_name) else first.bp_name,
                    "gps_in_unit": len(gb),
                    "gps": gp_rows,
                }
            )
        out[sc] = blocks
    return out


SUMMARY_KEYS = [
    "state_name", "site_state_gp_count", "gp_listing_rows", "members_files", "members",
    "site_state_er_count", "heads", "share_gps_0_heads", "share_gps_1_head",
    "share_gps_2plus_heads", "share_female_head", "share_female_ward_member",
    "share_heads_also_listed_as_ward_member", "gp_listing_share_of_state_gp_count",
    "gp_er_count_agreement", "gp_gender_count_agreement", "bp_gp_count_agreement",
    "bp_male_female_agreement", "zp_gp_count_agreement", "zp_male_female_agreement",
    "site_zp_er_sum", "site_gp_listing_er_sum", "state_er_count_share", "ward_no_parsed_share",
    "placeholder_name_share", "share_gps_with_duplicate_name",
]  # fmt: skip


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", type=pathlib.Path, required=True, help="collect_er.py --out dir")
    ap.add_argument("--out", type=pathlib.Path, required=True)
    ap.add_argument("--seed", type=int, default=20261019)
    args = ap.parse_args()
    src, out = args.src, args.out
    out.mkdir(parents=True, exist_ok=True)

    problems = []
    states = {s["stateCode"]: s for s in json.loads((src / "states.json").read_text("utf-8"))}
    done = finished_states(src)
    log = read_log(src)
    all_gps, all_members, units = [], [], {}
    for sc in sorted(done):
        gps, units[sc] = walk_state(src, sc, states[sc]["stateName"], problems)
        all_members += parse_members(src, sc, gps, log, problems)
        all_gps += gps
        fetched = sum(g["members_file"] is not None for g in gps)
        if fetched != done[sc]:
            problems.append(f"state {sc}: run.out says {done[sc]} GPs saved, parsed {fetched}")
        print(f"state {sc}: {len(gps)} GPs listed, {fetched} with members", flush=True)
    gps_df, mem_df = to_frames(all_gps, all_members, problems)
    if gps_df.gp_code.duplicated().any():
        problems.append(
            f"duplicate gp_code: {gps_df.gp_code[gps_df.gp_code.duplicated()].tolist()[:10]}"
        )
    if problems:
        raise StructuralError("\n".join(problems[:50]) + f"\n({len(problems)} problems)")

    gps_df.to_parquet(out / "gps.parquet", index=False)
    mem_df.to_parquet(out / "members.parquet", index=False)
    gps_df = validate(out / "gps.parquet", SCHEMA_DIR / "gps.schema.json", GPS_DTYPES)
    mem_df = validate(out / "members.parquet", SCHEMA_DIR / "members.schema.json", MEMBERS_DTYPES)
    if not mem_df.gp_code.isin(gps_df.gp_code).all():
        raise StructuralError("members.gp_code not in gps.gp_code")

    sample = build_sample(gps_df, mem_df, sorted(done), args.seed)
    checks = {"src": str(src), "finished_states": sorted(done), "states": {}}
    for sc in sorted(done):
        picked = [b["bp_code"] or b["zp_code"] for b in sample[sc]]
        checks["states"][sc] = state_checks(sc, states[sc], gps_df, mem_df, units[sc], picked)
    tot = {
        "gp_listing_rows": len(gps_df),
        "gps_with_members": int(gps_df.members_file.notna().sum()),
        "members": len(mem_df),
        "gender_values": mem_df.gender.value_counts().astype(int).to_dict(),
        "designation_class_values": mem_df.designation_class.value_counts().astype(int).to_dict(),
    }
    checks["overall"] = tot
    (out / "checks.json").write_text(
        json.dumps(checks, indent=1, ensure_ascii=False, default=jsonable)
    )

    summary = [
        {"state_code": sc} | {k: checks["states"][sc].get(k) for k in SUMMARY_KEYS} for sc in done
    ]
    viewer = {
        "note": "Random blocks (zp in two-tier states) and GPs per state, seed "
        f"{args.seed}; names as published by eGramSwaraj. Counts from checks.json.",
        "summary": sorted(summary, key=lambda r: r["state_code"]),
        "states": {str(sc): sample[sc] for sc in sorted(done)},
    }
    (out / "sample.json").write_text(json.dumps(viewer, ensure_ascii=False, default=jsonable))
    print(f"wrote {out}: {tot}")


if __name__ == "__main__":
    try:
        main()
    except StructuralError as exc:
        sys.exit(f"STRUCTURAL FAILURE\n{exc}")
