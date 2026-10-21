import csv
import json

from egs import BASE, D, get

HEAD = {"sarpanch", "mukhiya", "president gp", "village panchayat president", "pradhan"}
blocks = [(21, 3639, "Odisha"), (23, 4263, "Madhya Pradesh"), (3, 797, "Punjab")]
heads, everyone = [], []
for sc, bp, sname in blocks:
    name = f"egs_ER_{sc}_gp_{bp}.json" if sc != 21 else "egs_ER_od_gp_3639.json"
    gps = json.loads((D / "raw" / name).read_bytes())
    for g in gps[:20]:
        path = f"ElectedMemberRepresent.do?code={g['gpCode']}&stateCode={sc}&level=V"
        m = get(path, f"egs_ER_{sc}_mem_{g['gpCode']}.json")
        for r in m:
            row = {
                "state_code": sc,
                "state": sname,
                "block_lb_code": bp,
                "gp_lgd_code": g["gpCode"],
                "gp_name": g["gpName"],
                "name": r["electedname"],
                "designation": r["designationname"],
                "ward": r["wardName"],
                "gender": r["gender"],
                "request": BASE + path,
            }
            everyone.append(row)
            if (r["designationname"] or "").strip().lower() in HEAD:
                heads.append(row)
for fn, rows in (
    ("sample_heads_OD_MP_PB.csv", heads),
    ("sample_all_members_OD_MP_PB.csv", everyone),
):
    with open(D / "samples" / fn, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
print(len(heads), len(everyone))
