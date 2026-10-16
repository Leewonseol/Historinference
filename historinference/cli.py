"""Single CLI for the reproducible pipeline.

    python -m historinference inventory   # step 0: register + local files -> data/raw_index, sources
    python -m historinference build       # step 1-2: normalized tables (CSV + Parquet)
    python -m historinference validate    # step 6: audits -> data/audit/validation_findings.csv
    python -m historinference worlds      # step 4: partial order + possible-world candidates
    python -m historinference synthesize  # step 5: A/B/C designs, CSP, Pareto, sensitivity
    python -m historinference test        # run pytest, store results in data/audit
    python -m historinference report      # docs/ and outputs/ markdown + dashboard data
    python -m historinference all         # everything above in order

No command touches the network. External source URLs are provenance pointers only.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
import xml.etree.ElementTree as ET

from . import constraints, normalize, synthesis, validate, worlds
from .io import AUDIT, RAW_INDEX, ROOT, read_csv, sha256_file, write_csv, write_json


def cmd_build(_args=None):
    tables = normalize.build_all()
    print(f"[build] {len(tables)} normalized tables -> data/normalized/")
    return tables


def cmd_validate(_args=None, tables=None):
    tables = tables or normalize.load_normalized()
    edges = constraints.build_partial_order(tables)
    expected = read_csv(RAW_INDEX / "imported_checksums.csv")
    actual = {row["path"]: sha256_file(ROOT / row["path"]) for row in expected if (ROOT / row["path"]).exists()}
    findings = validate.run_all(tables, edges, expected, actual)
    rows = validate.findings_rows(findings)
    write_csv(AUDIT / "validation_findings.csv", rows, ["check", "severity", "table", "row", "message"])
    summary = {
        "errors": sum(1 for f in findings if f.severity == "ERROR"),
        "warnings": sum(1 for f in findings if f.severity == "WARN"),
        "by_check": {},
    }
    for f in findings:
        summary["by_check"].setdefault(f.check, {"ERROR": 0, "WARN": 0})[f.severity] += 1
    write_json(AUDIT / "validation_summary.json", summary)
    print(f"[validate] errors={summary['errors']} warnings={summary['warnings']}")
    return summary


def cmd_worlds(_args=None, tables=None):
    tables = tables or normalize.load_normalized()
    edges = constraints.build_partial_order(tables)
    po = constraints.write_outputs(tables, edges)
    ws = worlds.build(tables)
    for case, s in ws.items():
        print(f"[worlds] {case}: {s['n_consistent_worlds']} / {s['n_combinations']} consistent (UNSCORED); "
              f"partial order incomparable pairs={po[case]['n_incomparable_pairs']}")
    return po, ws


def cmd_synthesize(_args=None, tables=None):
    tables = tables or normalize.load_normalized()
    t0 = time.time()
    res = synthesis.run(tables)
    main = res["by_cutoff"]["D"]
    v = main["variants"]["default"]
    print(f"[synthesize] A designs={len(main['A'])} B feasible={main['B_count']} "
          f"default-gate Pareto={len(v['front'])} ({time.time() - t0:.1f}s)")
    return res


def cmd_test(_args=None):
    AUDIT.mkdir(parents=True, exist_ok=True)
    xml_path = AUDIT / "pytest_junit.xml"
    proc = subprocess.run([sys.executable, "-m", "pytest", "-q", "tests", f"--junitxml={xml_path}"],
                          cwd=ROOT, capture_output=True, text=True)
    (AUDIT / "pytest_output.txt").write_text(proc.stdout + proc.stderr, encoding="utf-8")
    summary = {"exit_code": proc.returncode, "runner": "pytest (Python 로컬 실행; Oracle 실행 아님)"}
    if xml_path.exists():
        root = ET.parse(xml_path).getroot()
        suite = root if root.tag == "testsuite" else root.find("testsuite")
        for k in ("tests", "failures", "errors", "skipped"):
            summary[k] = int(suite.get(k, 0))
        summary["passed"] = summary["tests"] - summary["failures"] - summary["errors"] - summary["skipped"]
        summary["cases"] = [
            {"name": f"{tc.get('classname')}::{tc.get('name')}",
             "status": ("failed" if tc.find("failure") is not None or tc.find("error") is not None
                        else "skipped" if tc.find("skipped") is not None else "passed")}
            for tc in suite.iter("testcase")
        ]
    write_json(AUDIT / "test_results.json", summary)
    print(f"[test] exit={proc.returncode} passed={summary.get('passed')} failed={summary.get('failures')} "
          f"errors={summary.get('errors')} skipped={summary.get('skipped')}")
    return summary


def cmd_report(_args=None, tables=None):
    from . import reports
    tables = tables or normalize.load_normalized()
    reports.write_all(tables)
    print("[report] docs/, outputs/, REQUEST_FOR_RESEARCHER.md, outputs/dashboard_data.js")


def cmd_all(args=None):
    tables = cmd_build()
    cmd_validate(tables=tables)
    cmd_worlds(tables=tables)
    cmd_synthesize(tables=tables)
    test_summary = cmd_test()
    cmd_report(tables=tables)
    return 0 if test_summary.get("exit_code") == 0 else 1


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(prog="historinference", description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("command", choices=["inventory", "build", "validate", "worlds", "synthesize", "test", "report", "all"])
    args = parser.parse_args(argv)
    if args.command in ("inventory", "build"):
        cmd_build(args)
        return 0
    if args.command == "validate":
        s = cmd_validate(args)
        return 1 if s["errors"] else 0
    if args.command == "worlds":
        cmd_worlds(args)
        return 0
    if args.command == "synthesize":
        cmd_synthesize(args)
        return 0
    if args.command == "test":
        return cmd_test(args)["exit_code"]
    if args.command == "report":
        cmd_report(args)
        return 0
    return cmd_all(args)


if __name__ == "__main__":
    raise SystemExit(main())
