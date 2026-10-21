"""Write the readme's table reference from schema/*.schema.json and data/*.parquet.

    uv run python bin/describe.py           # rewrite the section in readme.md
    uv run python bin/describe.py --check   # fail if the readme is out of date

Types are read from the parquet files themselves, so the readme shows what a
reader gets, and the declared constraints come from the schemas the build
validates against.
"""

import json
import pathlib
import sys

import pyarrow as pa
import pyarrow.parquet as pq

ROOT = pathlib.Path(__file__).resolve().parents[1]
README = ROOT / "readme.md"
START, END = "<!-- tables:start -->", "<!-- tables:end -->"
TABLES = ["gps", "members"]


def arrow_type(t):
    if pa.types.is_dictionary(t):
        return "category"
    if pa.types.is_large_string(t) or pa.types.is_string(t):
        return "string"
    if pa.types.is_timestamp(t):
        return f"timestamp ({t.tz})"
    return str(t)


def allowed(spec):
    c = spec.get("constraints", {})
    bits = []
    if c.get("enum"):
        bits.append(", ".join(f"`{v}`" for v in c["enum"]))
    if "minimum" in c or "maximum" in c:
        bits.append(f"{c.get('minimum', '')}–{c.get('maximum', '')}")
    return "; ".join(bits)


def section():
    out = [START, ""]
    for name in TABLES:
        path = ROOT / "data" / f"{name}.parquet"
        schema = json.loads((ROOT / "schema" / f"{name}.schema.json").read_text())
        spec = {f["name"]: f for f in schema["fields"]}
        arrow = pq.read_schema(path)
        rows = pq.read_metadata(path).num_rows
        key = ", ".join(f"`{k}`" for k in schema.get("primaryKey", []))
        out += [
            f"### `data/{name}.parquet`",
            "",
            f"{rows:,} rows; one row per {key}.",
            "",
            "| Column | Type | Required | Allowed | Description |",
            "|---|---|---|---|---|",
        ]
        for field in arrow:
            s = spec.get(field.name, {})
            req = "yes" if s.get("constraints", {}).get("required") else ""
            desc = (s.get("description") or "").replace("|", "\\|")
            out.append(
                f"| `{field.name}` | {arrow_type(field.type)} | {req} | {allowed(s)} | {desc} |"
            )
        out.append("")
    out.append(END)
    return "\n".join(out)


def main():
    text = README.read_text()
    if START in text:
        head, rest = text.split(START, 1)
        new = head + section() + rest.split(END, 1)[1]
    else:
        new = text.rstrip("\n") + "\n\n## Tables\n\n" + section() + "\n"
    if "--check" in sys.argv:
        if new != text:
            sys.exit("readme.md table reference is out of date: run bin/describe.py")
        print("readme.md table reference is current")
        return
    README.write_text(new)


if __name__ == "__main__":
    main()
