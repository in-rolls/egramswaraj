import sys

from egs import get

TWO_TIER = {30, 38, 12, 11, 34, 31}
states = [int(x) for x in sys.argv[1].split(",")]
nmem = int(sys.argv[2]) if len(sys.argv) > 2 else 3


def one(sc):
    zps = get(f"ElectedStatePanReportGp.do?stateCode={sc}&year=2026", f"egs_ER_{sc}_zp.json")
    zps = [z for z in zps if z.get("gperCount")]
    print(sc, "districts with ER>0:", len(zps))
    if not zps:
        return
    z = zps[0]
    if sc in TWO_TIER:
        bp = z["zpCode"]
    else:
        bps = get(
            f"findBpNameAndGPCountByZpCode.do?stateCode={sc}&year=2026&zpCode={z['zpCode']}",
            f"egs_ER_{sc}_bp_{z['zpCode']}.json",
        )
        bps = [b for b in bps if b.get("gperCount")]
        bp = bps[0]["bpCode"]
        print(
            "  zp", z["zpCode"], z["zpName"], "blocks w/ER", len(bps), "-> bp", bp, bps[0]["bpName"]
        )
    gps = get(
        f"findGpNameAndERCountByBpCode.do?stateCode={sc}&year=2026&bpCode={bp}",
        f"egs_ER_{sc}_gp_{bp}.json",
    )
    withER = [g for g in gps if g.get("gperCount")]
    print("  GPs in block", len(gps), "with ER", len(withER))
    for g in withER[:nmem]:
        m = get(
            f"ElectedMemberRepresent.do?code={g['gpCode']}&stateCode={sc}&level=V",
            f"egs_ER_{sc}_mem_{g['gpCode']}.json",
        )
        des = {}
        for r in m:
            des[r["designationname"]] = des.get(r["designationname"], 0) + 1
        print(
            "   gp",
            g["gpCode"],
            g["gpName"],
            "n=",
            len(m),
            des,
            "keys",
            sorted(m[0]) if m else None,
        )


for sc in states:
    try:
        one(sc)
    except RuntimeError as e:
        print(sc, "FAILED", e)
