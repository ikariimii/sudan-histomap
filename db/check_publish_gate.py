#!/usr/bin/env python3
"""Publish gate (read-only except its own report). Exit 0 = clean, 1 = flagged, 2 = error.

Flags:
  CONTROL_FATALITY_NO_UN  control/fatality wording in an era starting >= 1956
                          whose sources include no UN or aid-agency cite id
  NUMBER_NO_CITE          a numeric 'value' in a structured record with no cite
  WIKIPEDIA_ONLY          an era (or record) whose only cites are Wikipedia
Usage: python3 db/check_publish_gate.py [--no-report]
Report: db/publish_gate_report.json
"""
import glob, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODERN_FROM = 1956
CTRL = re.compile(r"\b(control(?:s|led|ling)? (?:of|over)|under (?:\w+ ){0,3}control|seiz(?:e|ed|es|ing)|captur(?:e|ed|es|ing)|took over|overr(?:an|un)|fell to|killed|kill(?:s|ing)|deaths?|death toll|dead|fatalit(?:y|ies)|casualt(?:y|ies)|massacre[sd]?)\b", re.I)
UN_AID = re.compile(r"^(UN|OCHA|UNHCR|UNICEF|WFP|FAO|WHO|IOM|IPC|FEWS|ACAPS|RELIEFWEB|RW_|MSF|ICRC|IFRC|OHCHR|UNSC|UNESCO|UNDP|UNMIS|UNAMID|UNISFA|UNITAMS|DTM)", re.I)
UN_AID_PUB = re.compile(r"united nations|\bUN\b|OCHA|UNHCR|UNICEF|World Food Programme|IOM|Integrated Food Security|FEWS NET|ReliefWeb|M[ée]decins Sans Fronti[èe]res|Red Cross|Red Crescent|ACAPS|Human Rights Council|Security Council", re.I)
CITE_KEYS = re.compile(r"(^|_)(cite|cites|source|sources|source_id|source_ids|cite_id|cite_current)$")
SKIP_NUM_KEYS = {"lat", "lon", "start", "end", "year", "zoom", "first_attested", "last_attested"}

def load(p):
    with open(p, encoding="utf-8") as f:
        return json.load(f)

def is_wp(sid, reg):
    s = reg.get(sid) or {}
    return sid.startswith(("WP:", "AR_WIKI")) or "wikipedia.org" in str(s.get("url", "")) or str(s.get("publisher", "")).lower() == "wikipedia"

def is_un(sid, reg):
    s = reg.get(sid) or {}
    return bool(UN_AID.match(sid)) or bool(UN_AID_PUB.search(str(s.get("publisher", "")) + " " + str(s.get("author", ""))))

def ids_in(v):
    out = []
    if isinstance(v, str): out.append(v)
    elif isinstance(v, list):
        for x in v: out += ids_in(x)
    elif isinstance(v, dict):
        for k in ("id", "source_id", "cite"):
            if isinstance(v.get(k), str): out.append(v[k])
    return out

def texts(o, path=""):
    if isinstance(o, dict):
        for k, v in o.items():
            if k in ("flags", "dating_note", "sources") or k.endswith("_ar") or k == "ar" or "null_reason" in k: continue
            yield from texts(v, f"{path}.{k}")
    elif isinstance(o, list):
        for i, v in enumerate(o): yield from texts(v, f"{path}[{i}]")
    elif isinstance(o, str):
        yield path, o

def numbers(o, path, out):
    if isinstance(o, dict):
        cited = any(CITE_KEYS.search(k) and o[k] not in (None, "", []) for k in o)
        for k, v in o.items():
            if isinstance(v, (int, float)) and not isinstance(v, bool) and k in ("value", "share", "amount", "count", "figure") and not cited:
                out.append((f"{path}.{k}", v))
            else:
                numbers(v, f"{path}.{k}", out)
    elif isinstance(o, list):
        for i, v in enumerate(o): numbers(v, f"{path}[{i}]", out)

def main():
    reg = load(os.path.join(ROOT, "data", "periods.json")).get("meta", {}).get("sources", {})
    flags = []
    eras = 0
    for p in sorted(glob.glob(os.path.join(ROOT, "data", "eras", "*.json"))):
        if os.path.basename(p) == "all.json": continue
        e = load(p)
        if not isinstance(e, dict) or "id" not in e: continue
        eras += 1
        eid, srcs = e["id"], [s for s in e.get("sources", []) if isinstance(s, str)]
        try: modern = int(e.get("start")) >= MODERN_FROM
        except (TypeError, ValueError): modern = False
        if srcs and all(is_wp(s, reg) for s in srcs):
            flags.append({"type": "WIKIPEDIA_ONLY", "file": os.path.relpath(p, ROOT), "era": eid, "path": ".sources", "detail": srcs})
        if modern and not any(is_un(s, reg) for s in srcs):
            for tp, t in texts(e):
                m = CTRL.search(t)
                if m:
                    flags.append({"type": "CONTROL_FATALITY_NO_UN", "file": os.path.relpath(p, ROOT), "era": eid, "path": tp, "detail": m.group(0), "text": t[:200]})
        nums = []
        numbers(e, "", nums)
        for np_, v in nums:
            flags.append({"type": "NUMBER_NO_CITE", "file": os.path.relpath(p, ROOT), "era": eid, "path": np_, "detail": v})
    ep = os.path.join(ROOT, "db", "era_economy.json")
    if os.path.exists(ep):
        econ = load(ep)
        for eid, rec in econ.items():
            if eid.startswith("_"): continue
            nums = []
            numbers(rec, "", nums)
            for np_, v in nums:
                flags.append({"type": "NUMBER_NO_CITE", "file": "db/era_economy.json", "era": eid, "path": np_, "detail": v})
            cites = []
            def grab(o):
                if isinstance(o, dict):
                    for k, v in o.items():
                        if k in ("cite", "source_id", "source_ids"): cites.extend(ids_in(v))
                        else: grab(v)
                elif isinstance(o, list):
                    for v in o: grab(v)
            grab(rec)
            if cites and all(is_wp(c, reg) for c in cites):
                flags.append({"type": "WIKIPEDIA_ONLY", "file": "db/era_economy.json", "era": eid, "path": "", "detail": sorted(set(cites))})
    wc = os.path.join(ROOT, "tools", "check_wars_cites.py")
    if os.path.exists(wc):
        import subprocess
        r = subprocess.run([sys.executable, wc], cwd=ROOT, capture_output=True, text=True)
        if r.returncode != 0:
            for ln in (r.stdout + r.stderr).splitlines():
                if ln.startswith("UNREGISTERED"):
                    flags.append({"type": "WARS_CITE_UNREGISTERED", "file": "db/wars_post1956.json", "era": "", "path": "", "detail": ln})
            if not any(f["type"] == "WARS_CITE_UNREGISTERED" for f in flags):
                flags.append({"type": "WARS_CITE_CHECK_FAILED", "file": "tools/check_wars_cites.py", "era": "", "path": "", "detail": (r.stdout + r.stderr)[-300:]})
    counts = {}
    for f in flags: counts[f["type"]] = counts.get(f["type"], 0) + 1
    rep = {"eras_checked": eras, "modern_from": MODERN_FROM, "counts": counts, "total": len(flags), "flags": flags}
    if "--no-report" not in sys.argv:
        with open(os.path.join(ROOT, "db", "publish_gate_report.json"), "w", encoding="utf-8") as f:
            json.dump(rep, f, ensure_ascii=False, indent=1)
            f.write("\n")
    print(f"publish gate: {eras} eras, {len(flags)} flags {counts}")
    return 1 if flags else 0

if __name__ == "__main__":
    try: sys.exit(main())
    except Exception as ex:
        print(f"publish gate ERROR: {ex}", file=sys.stderr); sys.exit(2)
