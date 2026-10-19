"""Collect every gram panchayat's elected representatives from eGramSwaraj.

    python3 bin/collect_er.py --out er --workers 3

Walks state -> district panchayat (zp) -> block panchayat (bp) -> GP -> members
through the JSON endpoints documented in readme.md, and saves each response to
its own file under --out, so a rerun skips what is already saved. Needs an
Indian connection; it is meant to run on a VM in India.

Each member response is saved without the masked `mobno` and `emailid` fields;
log.jsonl records the sha256 and size of every response as received, before
anything is removed. Failures are logged and retried on the next run; a
request that keeps failing never stops the walk.

Only the standard library and requests, so it runs on a bare Debian VM
(apt install python3-requests).
"""

import argparse
import concurrent.futures as cf
import datetime
import hashlib
import json
import pathlib
import threading
import time

import requests

BASE = "https://egramswaraj.gov.in/"
YEAR = "2026"
# States whose GP lists hang off the district panchayat directly.
TWO_TIER = {"30", "38", "12", "11", "34", "31"}
HEADERS = {
    "User-Agent": "Mozilla/5.0 (research data collection; in-rolls)",
    "Referer": BASE + "ElectedRepresentativeReportVp.do",
}
DROP = ("mobno", "emailid")

lock = threading.Lock()
local = threading.local()


def session():
    if not hasattr(local, "s"):
        local.s = requests.Session()
        local.s.headers.update(HEADERS)
    return local.s


def log(out, **entry):
    entry["time"] = datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%dT%H:%M:%SZ")
    with lock, open(out / "log.jsonl", "a", encoding="utf-8") as fh:
        fh.write(json.dumps(entry, ensure_ascii=False) + "\n")


def scrub(x):
    if isinstance(x, dict):
        return {k: scrub(v) for k, v in x.items() if k not in DROP}
    if isinstance(x, list):
        return [scrub(v) for v in x]
    return x


def get(out, path, rel, delay, attempts=4):
    """Return the saved JSON for path, fetching it if not yet saved; None on failure."""
    # rel is built from server-supplied codes; never write outside --out
    target = (out / rel).resolve()
    if not target.is_relative_to(out.resolve()):
        raise ValueError(f"refusing to write outside {out}: {rel!r}")
    if target.exists():
        return json.loads(target.read_text(encoding="utf-8"))
    for attempt in range(1, attempts + 1):
        time.sleep(delay)
        try:
            r = session().get(BASE + path, timeout=90)
            r.raise_for_status()
            data = r.json() if r.content else []
        except (requests.RequestException, ValueError) as exc:
            log(out, url=BASE + path, file=rel, error=str(exc)[:200], attempt=attempt)
            time.sleep(15 * attempt)
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(scrub(data), ensure_ascii=False), encoding="utf-8")
        log(
            out,
            url=BASE + path,
            file=rel,
            status=r.status_code,
            bytes=len(r.content),
            sha256=hashlib.sha256(r.content).hexdigest(),
        )
        return data
    return None


def gp_lists(out, sc, delay):
    """Every (bp code, GP list) pair for one state."""
    zps = get(out, f"ElectedStatePanReportGp.do?stateCode={sc}&year={YEAR}", f"{sc}/zp.json", delay)
    for z in zps or []:
        if not z.get("gperCount"):
            continue
        zp = str(z["zpCode"])
        if not zp.isdigit():
            continue
        if sc in TWO_TIER:
            bps = [zp]
        else:
            q = f"findBpNameAndGPCountByZpCode.do?stateCode={sc}&year={YEAR}&zpCode={zp}"
            rows = get(out, q, f"{sc}/bp_{zp}.json", delay)
            if rows is None:  # times out for Maharashtra and Punjab
                q = f"findElectedStateBpByZpCode.do?stateCode={sc}&year={YEAR}&zpCode={zp}"
                rows = get(out, q, f"{sc}/bp_alt_{zp}.json", delay)
            # The fallback endpoint's rows carry gperCount null, not 0: skip a
            # block only when the site says it has no GP members.
            bps = [b["bpCode"] for b in rows or [] if b.get("gperCount") != 0]
            bps = [b for b in bps if str(b).isdigit()]
        for bp in bps:
            q = f"findGpNameAndERCountByBpCode.do?stateCode={sc}&year={YEAR}&bpCode={bp}"
            yield bp, get(out, q, f"{sc}/gp_{bp}.json", delay) or []


def members(out, sc, gp, delay):
    q = f"ElectedMemberRepresent.do?code={gp}&stateCode={sc}&level=V"
    return get(out, q, f"{sc}/members/{gp}.json", delay) is not None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="er")
    ap.add_argument("--workers", type=int, default=3)
    ap.add_argument("--delay", type=float, default=2.0, help="seconds before each request, per worker")
    ap.add_argument("--states", default="", help="comma-separated state codes; default all")
    args = ap.parse_args()
    out = pathlib.Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    states = get(out, f"ElectedStateReportGp.do?year={YEAR}", "states.json", args.delay) or []
    codes = [str(s["stateCode"]) for s in states if s.get("gperCount")]
    codes = [c for c in codes if c.isdigit()]
    if args.states:
        codes = [c for c in codes if c in args.states.split(",")]
    log(out, event="start", states=codes, workers=args.workers)

    for sc in codes:
        gps = []
        for _bp, rows in gp_lists(out, sc, args.delay):
            gps += [str(g["gpCode"]) for g in rows if g.get("gperCount")]
        gps = [g for g in gps if g.isdigit()]
        with cf.ThreadPoolExecutor(args.workers) as pool:
            ok = sum(pool.map(lambda g: members(out, sc, g, args.delay), gps))
        log(out, event="state_done", state=sc, gps=len(gps), saved=ok, failed=len(gps) - ok)
        print(f"state {sc}: {ok}/{len(gps)} GPs saved", flush=True)
    log(out, event="finish")


if __name__ == "__main__":
    main()
