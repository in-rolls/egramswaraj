"""Shared polite fetcher for eGramSwaraj ER JSON endpoints (survey only)."""
import datetime
import hashlib
import json
import pathlib
import sys
import time

import requests

D = pathlib.Path(sys.argv[0]).resolve().parent.parent
RAW = D / "raw"
S = requests.Session()
S.proxies = {"https": "socks5h://localhost:1080", "http": "socks5h://localhost:1080"}
S.headers.update({"User-Agent": "Mozilla/5.0 (Macintosh) research-survey",
                  "Referer": "https://egramswaraj.gov.in/ElectedRepresentativeReportVp.do"})
BASE = "https://egramswaraj.gov.in/"


def get(path, name):
    out = RAW / name
    if out.exists() and out.stat().st_size > 0:
        return json.loads(out.read_bytes())
    for attempt in range(2):
        time.sleep(2.2)
        try:
            r = S.get(BASE + path, timeout=60)
            break
        except requests.RequestException as e:
            print("retry", attempt, e, file=sys.stderr)
            time.sleep(15)
    else:
        raise RuntimeError("timeout: " + path)
    out.write_bytes(r.content)
    with open(D / "log.tsv", "a") as f:
        f.write("\t".join([datetime.datetime.utcnow().strftime("%FT%TZ"), BASE + path, "",
                           f"{r.status_code} {r.headers.get('content-type','')} {len(r.content)}",
                           hashlib.sha256(r.content).hexdigest(), name]) + "\n")
    return r.json() if r.content else []
