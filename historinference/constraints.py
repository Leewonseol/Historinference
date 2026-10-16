"""Step 4 (part 1): partial-order DAG of events and normative-rule table.

Edges are created only from (a) explicit, span-backed sequence statements in
data/curated/event_order.csv or (b) date intervals that are strictly ordered.
Events whose relative order is not established remain incomparable: no order
is invented for them.
"""

from __future__ import annotations

from itertools import combinations

from . import dates
from .io import MODELS, write_csv, write_json


def build_partial_order(tables) -> list[dict]:
    events = tables["events"]
    edges = []
    seen = set()
    for o in tables["event_order"]:
        key = (o["before_id"], o["after_id"])
        seen.add(key)
        edges.append({**o, "case_id": _case(events, o["before_id"])})
    by_case: dict[str, list[dict]] = {}
    for e in events:
        by_case.setdefault(e["case_id"], []).append(e)
    for case, evs in by_case.items():
        for a, b in combinations(evs, 2):
            ia = dates.interval(a["date_start"], a["date_end"])
            ib = dates.interval(b["date_start"], b["date_end"])
            for x, y, ix, iy in ((a, b, ia, ib), (b, a, ib, ia)):
                if dates.strictly_before(ix, iy) and (x["event_id"], y["event_id"]) not in seen:
                    seen.add((x["event_id"], y["event_id"]))
                    edges.append({
                        "before_id": x["event_id"], "after_id": y["event_id"], "basis": "DATE_COMPARISON",
                        "span_ids": "", "note": f"{x['date_start']}~{x['date_end']} < {y['date_start']}~{y['date_end']}",
                        "case_id": case,
                    })
    return edges


def _case(events, eid):
    for e in events:
        if e["event_id"] == eid:
            return e["case_id"]
    return "UNKNOWN"


def transitive_reduction(nodes: list[str], edges: list[tuple[str, str]]) -> list[tuple[str, str]]:
    succ = {n: set() for n in nodes}
    for a, b in edges:
        succ.setdefault(a, set()).add(b)

    def reach(start):
        seen, stack = set(), list(succ.get(start, ()))
        while stack:
            n = stack.pop()
            if n not in seen:
                seen.add(n)
                stack.extend(succ.get(n, ()))
        return seen

    reduced = []
    for a, b in edges:
        others = succ[a] - {b}
        if not any(b in reach(o) or b == o for o in others):
            reduced.append((a, b))
    return reduced


def summarize(tables, edges) -> dict:
    out = {}
    for case in sorted({e["case_id"] for e in tables["events"]}):
        nodes = [e["event_id"] for e in tables["events"] if e["case_id"] == case]
        es = [(e["before_id"], e["after_id"]) for e in edges if e["case_id"] == case]
        closure = _closure(nodes, es)
        comparable = sum(1 for a, b in combinations(nodes, 2) if (a, b) in closure or (b, a) in closure)
        total = len(nodes) * (len(nodes) - 1) // 2
        out[case] = {
            "nodes": nodes,
            "hasse_edges": transitive_reduction(nodes, es),
            "n_edges_total": len(es),
            "n_explicit": sum(1 for e in edges if e["case_id"] == case and e["basis"] == "EXPLICIT_SEQUENCE"),
            "n_pairs": total,
            "n_comparable_pairs": comparable,
            "n_incomparable_pairs": total - comparable,
        }
    return out


def _closure(nodes, edges):
    succ = {n: set() for n in nodes}
    for a, b in edges:
        succ[a].add(b)
    closure = set()
    for n in nodes:
        stack, seen = list(succ[n]), set()
        while stack:
            m = stack.pop()
            if m not in seen:
                seen.add(m)
                closure.add((n, m))
                stack.extend(succ[m])
    return closure


def write_outputs(tables, edges) -> dict:
    write_csv(MODELS / "constraints" / "partial_order_edges.csv", edges,
              ["case_id", "before_id", "after_id", "basis", "span_ids", "note"])
    summary = summarize(tables, edges)
    write_json(MODELS / "constraints" / "partial_order.json", {
        "note": "부분순서 DAG: 명시 근거 또는 확정 날짜 비교로만 간선 생성. 비교 불가 쌍은 순서를 만들지 않음.",
        "cases": {c: {**v, "hasse_edges": [list(e) for e in v["hasse_edges"]]} for c, v in summary.items()},
    })
    write_csv(MODELS / "constraints" / "normative_rules.csv", tables["normative_rules"])
    return summary
