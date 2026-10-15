"""Step 5: compare (A) anchor + transplant designs with (B) synthetic designs.

Morphological analysis: every story design picks one value per dimension of
``models/synthesis/morphological_box.csv`` (B) or keeps the documented values
of one historical case and fills only its empty dimensions with transplants
from other cases (A). ``compatibility_rules.csv`` is the CSP that removes
mutually inconsistent combinations.

Nothing here is a probability. Goal levels come from ``config/objectives.toml``
(a human-editable design specification), and candidates are compared by
Pareto dominance over explicit, countable criteria:

  maximise  Y1..Y6 goal levels (NONE=0, PARTIAL=1, FULL=2)
  minimise  assumption severity (Occam), untraced fiction-only elements,
            cross-case causal links (hypothesised), secondary-only elements,
            contested mechanisms used as plot fact, period risks,
            historical overlays, real-person attribution risks.
"""

from __future__ import annotations

import tomllib
from itertools import product

from .io import CONFIG, MODELS, read_csv, split, write_csv, write_json
from .normalize import GRADE_ORDER, span_grade

DIMS = [
    "M1_TRIGGER", "M2_FIRST_ERROR", "M3_TESTIMONY", "M4_OPINION", "M5_OFFICIAL_FAULT", "M6_TARGET_FATE",
    "M7_APPEAL", "M8_REVERIFICATION", "M9_SECOND_ORDER", "M10A_PERPETRATOR_ACCOUNTABILITY",
    "M10B_OFFICIAL_ACCOUNTABILITY", "M11_RESOLUTION",
]
# causal chain used to count links between consecutive story elements
CHAIN = [
    "M1_TRIGGER", "M4_OPINION", "M3_TESTIMONY", "M2_FIRST_ERROR", "M5_OFFICIAL_FAULT", "M6_TARGET_FATE",
    "M7_APPEAL", "M8_REVERIFICATION", "M9_SECOND_ORDER", "M11_RESOLUTION",
    "M10A_PERPETRATOR_ACCOUNTABILITY", "M10B_OFFICIAL_ACCOUNTABILITY",
]
NONE_VALUE = {
    "M2_FIRST_ERROR": "D_NONE", "M3_TESTIMONY": "W_NONE", "M4_OPINION": "O_NONE", "M5_OFFICIAL_FAULT": "F_NONE",
    "M6_TARGET_FATE": "X_NONE", "M7_APPEAL": "P_NONE", "M8_REVERIFICATION": "V_NONE", "M9_SECOND_ORDER": "S_NONE",
    "M10A_PERPETRATOR_ACCOUNTABILITY": "K_NONE", "M10B_OFFICIAL_ACCOUNTABILITY": "KB_NONE",
}
GOALS = ["Y1", "Y2", "Y3", "Y4", "Y5", "Y6"]
CASES = ["CHOI", "CHO", "YE", "GUSUN"]
ANCHOR_YEAR = {"CHOI": 1787, "CHO": 1782, "YE": 1795, "GUSUN": 1793}
SETTING_YEARS = [1785, 1789, 1794]
COST_KEYS = ["severity", "untraced", "cross_links", "secondary_only", "contested_as_fact",
             "period_risk", "overlays", "real_person_risk"]


# ------------------------------------------------------------------ loading
def load_config() -> dict:
    with open(CONFIG / "objectives.toml", "rb") as fh:
        return tomllib.load(fh)


def load_box(spans: dict[str, dict], grade_cutoff: str = "D") -> list[dict]:
    rows = []
    for r in read_csv(MODELS / "synthesis" / "morphological_box.csv"):
        r = dict(r)
        if r["fiction_only"] == "1":
            r["grade"] = "F"
        else:
            r["grade"] = span_grade(split(r["span_ids"]), spans)
            if GRADE_ORDER.get(r["grade"], 9) > GRADE_ORDER[grade_cutoff]:
                continue
        r["year"] = int(r["source_year"])
        rows.append(r)
    return rows


def load_rules() -> list[dict]:
    rules = []
    for r in read_csv(MODELS / "synthesis" / "compatibility_rules.csv"):
        rules.append({
            "rule_id": r["rule_id"],
            "if_dim": r["if_dim"],
            "if_values": set(split(r["if_values"])),
            "then_dims": split(r["then_dim"]),
            "then_values": set(split(r["then_values"])),
            "dims": {r["if_dim"], *split(r["then_dim"])},
            "basis": r["basis"],
        })
    return rules


# ------------------------------------------------------------------ evaluation
def _present(values: set[str], allowed: list[str], dim: str) -> bool:
    if allowed == ["*"]:
        return any(v != NONE_VALUE.get(dim) for v in values)
    return bool(values & set(allowed))


def goal_levels(assign: dict[str, set[str]], cfg: dict) -> dict[str, int]:
    levels = cfg["levels"]
    out = {}
    for g in GOALS:
        out[g] = levels["NONE"]
        for level in ("FULL", "PARTIAL"):
            alts = cfg["goal_rules"][g].get(level, [])
            if any(all(_present(assign.get(d, set()), allowed, d) for d, allowed in alt.items()) for alt in alts):
                out[g] = levels[level]
                break
    return out


def rule_violations(assign: dict[str, set[str]], rules: list[dict]) -> list[str]:
    bad = []
    for r in rules:
        if assign.get(r["if_dim"], set()) & r["if_values"]:
            got = set().union(*(assign.get(d, set()) for d in r["then_dims"]))
            if not got & r["then_values"]:
                bad.append(r["rule_id"])
    return bad


def gate_pass(levels: dict[str, int], gates: dict[str, str], cfg: dict) -> bool:
    return all(levels[g] >= cfg["levels"][lvl] for g, lvl in gates.items())


def gate_variants(cfg: dict) -> dict[str, dict[str, str]]:
    base = dict(cfg["hard_gates"])
    out = {"default": base}
    names = cfg["sensitivity"]["gate_variants"]
    if "Y3_FULL" in names:
        out["Y3_FULL"] = {**base, "Y3": "FULL"}
    if "Y6_FULL" in names:
        out["Y6_FULL"] = {**base, "Y6": "FULL"}
    if "no_Y6_gate" in names:
        out["no_Y6_gate"] = {k: v for k, v in base.items() if k != "Y6"}
    return out


def period_risk(rows: list[dict], year: int, cfg: dict) -> int:
    risk = 0
    for r in rows:
        b = cfg["period_breakpoints"].get(r["procedural_domain"])
        if b is None or r["fiction_only"] == "1":
            continue
        if r["year"] < b <= year or year < b <= r["year"]:
            risk += 1
    return risk


def chain_cross_links(case_sets: dict[str, set[str]]) -> int:
    present = [case_sets[d] for d in CHAIN if case_sets.get(d)]
    return sum(1 for a, b in zip(present, present[1:]) if not (a & b))


# ------------------------------------------------------------------ B: synthetic designs
def _choose_sources(values: dict[str, str], options: dict[str, list[dict]]) -> list[dict]:
    """DP along the chain: minimise (cross-case links, secondary-only rows)."""
    seq = [(d, options[values[d]]) for d in CHAIN if values[d] in options]
    if not seq:
        return []
    # state: chosen row index at step i -> (cost, back-pointer)
    prev = [((1 if r["grade"] == "D" else 0), None) for r in seq[0][1]]
    table = [prev]
    for i in range(1, len(seq)):
        cur = []
        for r in seq[i][1]:
            best = None
            for j, pr in enumerate(seq[i - 1][1]):
                cost = table[i - 1][j][0] + (100 if pr["source_case"] != r["source_case"] else 0)
                if best is None or cost < best[0]:
                    best = (cost, j)
            cur.append((best[0] + (1 if r["grade"] == "D" else 0), best[1]))
        table.append(cur)
    k = min(range(len(table[-1])), key=lambda j: table[-1][j][0])
    chosen = []
    for i in range(len(seq) - 1, -1, -1):
        chosen.append(seq[i][1][k])
        k = table[i][k][1] if table[i][k][1] is not None else 0
    return list(reversed(chosen))


def metrics_for(rows: list[dict], assign: dict[str, set[str]], cfg: dict, strategy: str,
                anchor: str | None = None, transplants: list[dict] | None = None,
                anchor_roles: set[str] | None = None) -> dict:
    sev = cfg["assumption_severity"]
    case_sets: dict[str, set[str]] = {}
    for r in rows:
        case_sets.setdefault(r["dim"], set()).add(r["source_case"])
    cross = chain_cross_links(case_sets)
    transplants = transplants or []
    if strategy == "A":
        year = ANCHOR_YEAR[anchor]
        prisk = period_risk(transplants, year, cfg)
        best_year = year
        untraced = 0
        contested = sum(1 for r in transplants if r["source_status"] == "CONTESTED")
        overlays = len(transplants)
        rp_risk = sum(1 for r in transplants if r["actor_role"] in (anchor_roles or set()))
        severity = overlays * sev["historical_overlay"] + cross * sev["cross_case_link"]
    else:
        risks = {y: period_risk(rows, y, cfg) for y in SETTING_YEARS}
        best_year = min(SETTING_YEARS, key=lambda y: (risks[y], y))
        prisk = risks[best_year]
        untraced = sum(1 for r in rows if r["fiction_only"] == "1")
        traced = len(rows) - untraced
        contested = sum(1 for r in rows if r["source_status"] == "CONTESTED")
        overlays = 0
        rp_risk = 0
        if strategy == "C":
            severity = len(rows) * sev["fiction_only_element"]
        else:
            severity = traced * sev["traced_fictionalized"] + untraced * sev["fiction_only_element"] + cross * sev["cross_case_link"]
    levels = goal_levels(assign, cfg)
    return {
        **levels,
        "severity": severity,
        "untraced": untraced,
        "cross_links": cross,
        "secondary_only": sum(1 for r in rows if r["grade"] == "D"),
        "contested_as_fact": contested,
        "period_risk": prisk,
        "overlays": overlays,
        "real_person_risk": rp_risk,
        "n_elements": len(rows),
        "setting_year": best_year,
        "source_cases": "|".join(sorted({r["source_case"] for r in rows})),
    }


def _compile_goals(cfg: dict):
    """Pre-compile goal rules for single-valued assignments (dim -> value)."""
    comp = {}
    for g in GOALS:
        levels = []
        for level in ("FULL", "PARTIAL"):
            alts = []
            for alt in cfg["goal_rules"][g].get(level, []):
                alts.append([(d, None if allowed == ["*"] else frozenset(allowed)) for d, allowed in alt.items()])
            levels.append((cfg["levels"][level], alts))
        comp[g] = levels
    return comp


def _fast_level(comp_g, a: dict[str, str]) -> int:
    for value, alts in comp_g:
        for alt in alts:
            if all((a[d] != NONE_VALUE.get(d) if allowed is None else a[d] in allowed) for d, allowed in alt):
                return value
    return 0


def _rule_ok(r, a: dict[str, str]) -> bool:
    if a[r["if_dim"]] not in r["if_values"]:
        return True
    return any(a[d] in r["then_values"] for d in r["then_dims"])


def enumerate_B(box: list[dict], rules: list[dict], cfg: dict, weakest_gates: dict[str, str]) -> list[dict]:
    options: dict[str, list[dict]] = {}
    values_by_dim: dict[str, list[str]] = {d: [] for d in DIMS}
    for r in box:
        options.setdefault(r["value_id"], []).append(r)
        if r["value_id"] not in values_by_dim[r["dim"]]:
            values_by_dim[r["dim"]].append(r["value_id"])
    for d, none in NONE_VALUE.items():
        values_by_dim[d].append(none)
    order = ["M11_RESOLUTION", "M10A_PERPETRATOR_ACCOUNTABILITY", "M1_TRIGGER", "M6_TARGET_FATE", "M9_SECOND_ORDER",
             "M8_REVERIFICATION", "M7_APPEAL", "M2_FIRST_ERROR", "M5_OFFICIAL_FAULT", "M3_TESTIMONY", "M4_OPINION",
             "M10B_OFFICIAL_ACCOUNTABILITY"]
    comp = _compile_goals(cfg)
    goal_dims = {g: {d for _, alts in comp[g] for alt in alts for d, _ in alt} for g in GOALS}
    rules_at: dict[int, list[dict]] = {}
    for r in rules:
        rules_at.setdefault(max(order.index(d) for d in r["dims"]), []).append(r)
    gates_at: dict[int, list[tuple[str, int]]] = {}
    for g, lvl in weakest_gates.items():
        gates_at.setdefault(max(order.index(d) for d in goal_dims[g]), []).append((g, cfg["levels"][lvl]))
    rules_touching = {d: [r for r in rules if d in r["dims"]] for d in DIMS}

    designs: list[dict[str, str]] = []
    feasible = 0
    a: dict[str, str] = {}

    def is_minimal(values: dict[str, str]) -> bool:
        """Occam filter: drop designs with an element removable without changing goals or feasibility.

        Removing an element never increases any cost and strictly lowers severity, so a
        non-minimal design is always Pareto-dominated by its reduction."""
        for d, none in NONE_VALUE.items():
            v = values[d]
            if v == none:
                continue
            values[d] = none
            removable = all(_rule_ok(r, values) for r in rules_touching[d])
            if removable:
                for g in GOALS:
                    if d in goal_dims[g]:
                        new = _fast_level(comp[g], values)
                        values[d] = v
                        old = _fast_level(comp[g], values)
                        values[d] = none
                        if new != old:
                            removable = False
                            break
            values[d] = v
            if removable:
                return False
        return True

    def rec(i: int):
        nonlocal feasible
        if i == len(order):
            feasible += 1
            if is_minimal(a):
                designs.append(dict(a))
            return
        d = order[i]
        checks = rules_at.get(i, [])
        gates = gates_at.get(i, [])
        for v in values_by_dim[d]:
            a[d] = v
            if all(_rule_ok(r, a) for r in checks) and all(_fast_level(comp[g], a) >= lvl for g, lvl in gates):
                rec(i + 1)
        del a[d]

    rec(0)
    enumerate_B.last_feasible = feasible
    out = []
    for n, values in enumerate(designs, 1):
        rows = _choose_sources(values, options)
        m = metrics_for(rows, {d: {values[d]} for d in DIMS}, cfg, "B")
        out.append({"design_id": f"B-{n:06d}", "strategy": "B", "anchor": "NONE", **values, **m,
                    "trace_rows": "|".join(r["row_id"] for r in rows)})
    return out


# ------------------------------------------------------------------ A: anchor + transplant
def anchor_designs(box: list[dict], rules: list[dict], cfg: dict, max_transplants: int = 4) -> tuple[list[dict], dict]:
    out = []
    native = {}
    for k in CASES:
        own = [r for r in box if r["source_case"] == k]
        base: dict[str, set[str]] = {d: set() for d in DIMS}
        for r in own:
            base[r["dim"]].add(r["value_id"])
        for d in DIMS:
            if not base[d]:
                base[d] = {NONE_VALUE.get(d, "NONE")}
        native_bad = set(rule_violations(base, rules))
        native[k] = sorted(native_bad)
        roles = {r["actor_role"] for r in own}
        empty = [d for d in DIMS if not any(r["dim"] == d for r in own)]
        choices = []
        for d in empty:
            cands = [r for r in box if r["dim"] == d and r["source_case"] != k and r["fiction_only"] != "1"]
            choices.append([None] + cands)
        n = 0
        for combo in product(*choices) if choices else [()]:
            trans = [r for r in combo if r is not None]
            if len(trans) > max_transplants:
                continue
            assign = {d: set(v) for d, v in base.items()}
            for r in trans:
                assign[r["dim"]] = {r["value_id"]}
            bad = set(rule_violations(assign, rules)) - native_bad
            if bad:
                continue
            n += 1
            rows = own + trans
            m = metrics_for(rows, assign, cfg, "A", anchor=k, transplants=trans, anchor_roles=roles)
            out.append({
                "design_id": f"A-{k}-{n:03d}", "strategy": "A", "anchor": k,
                **{d: "|".join(sorted(assign[d])) for d in DIMS}, **m,
                "trace_rows": "|".join(r["row_id"] for r in rows),
                "transplant_rows": "|".join(r["row_id"] for r in trans),
            })
    return out, native


# ------------------------------------------------------------------ C: pure invention baseline
def baseline_C(cfg: dict) -> dict:
    values = {
        "M1_TRIGGER": "C_INVENTED", "M2_FIRST_ERROR": "C_INVENTED", "M3_TESTIMONY": "C_INVENTED",
        "M4_OPINION": "O_NONE", "M5_OFFICIAL_FAULT": "C_INVENTED", "M6_TARGET_FATE": "X_DETAINED_RELEASED",
        "M7_APPEAL": "P_VICTIM_FAMILY_PETITION", "M8_REVERIFICATION": "V_SPECIAL_INSPECTOR",
        "M9_SECOND_ORDER": "C_INVENTED", "M10A_PERPETRATOR_ACCOUNTABILITY": "K_PERPETRATOR_EXILED",
        "M10B_OFFICIAL_ACCOUNTABILITY": "K_OFFICIAL_SANCTIONED", "M11_RESOLUTION": "U_FICTIONAL_PROVEN_CULPRIT",
    }
    rows = [{"dim": d, "source_case": "FICTION", "grade": "F", "fiction_only": "1", "source_status": "FICTION_ONLY",
             "procedural_domain": "NONE", "year": 0, "row_id": f"C-{d}"} for d in DIMS if not values[d].endswith("_NONE")]
    assign = {d: {v} for d, v in values.items()}
    m = metrics_for(rows, assign, cfg, "C")
    m["cross_links"] = 0  # a single invented story has no cross-case juxtaposition
    return {"design_id": "C-000001", "strategy": "C", "anchor": "NONE", **values, **m,
            "trace_rows": "", "note": "완전 창작 baseline: 기획의도 수준은 작가 선언으로만 충족(출처 추적 0)"}


# ------------------------------------------------------------------ Pareto
def vector(d: dict) -> tuple:
    return tuple(d[g] for g in GOALS) + tuple(-d[c] for c in COST_KEYS)


def pareto_front(designs: list[dict]) -> list[dict]:
    groups: dict[tuple, list[dict]] = {}
    for d in designs:
        groups.setdefault(vector(d), []).append(d)
    vecs = list(groups)
    front = []
    for v in vecs:
        dominated = False
        for w in vecs:
            if w is v:
                continue
            if all(x >= y for x, y in zip(w, v)) and any(x > y for x, y in zip(w, v)):
                dominated = True
                break
        if not dominated:
            front.append(v)
    out = []
    for v in sorted(front, reverse=True):
        members = groups[v]
        rep = dict(members[0])
        rep["n_equivalent_designs"] = len(members)
        rep["equivalent_design_ids_sample"] = "|".join(m["design_id"] for m in members[:5])
        out.append(rep)
    return out


PROFILES = {
    "fidelity_first": lambda d: (d["untraced"], d["contested_as_fact"], d["real_person_risk"], d["overlays"],
                                 d["secondary_only"], d["severity"], -sum(d[g] for g in GOALS)),
    "goal_first": lambda d: tuple(-d[g] for g in ["Y3", "Y4", "Y5", "Y6", "Y1", "Y2"]) + (d["severity"], d["untraced"]),
    "parsimony_first": lambda d: (d["severity"], d["cross_links"], d["untraced"], -sum(d[g] for g in GOALS)),
}


def weighted_view(front: list[dict], cfg: dict) -> list[dict]:
    """Configuration-dependent auxiliary view: winner frequency over a weight grid."""
    if not front:
        return []
    mx = {c: max(1, max(d[c] for d in front)) for c in COST_KEYS}

    def group_scores(d):
        return {
            "goals": sum(d[g] for g in GOALS) / 12.0,
            "fidelity": -(d["untraced"] / mx["untraced"] + d["contested_as_fact"] / mx["contested_as_fact"]
                          + d["secondary_only"] / mx["secondary_only"]) / 3.0,
            "coherence": -d["cross_links"] / mx["cross_links"],
            "plausibility": -d["period_risk"] / mx["period_risk"],
            "parsimony": -(d["severity"] / mx["severity"] + d["overlays"] / mx["overlays"]
                           + d["real_person_risk"] / mx["real_person_risk"]) / 3.0,
        }

    groups = cfg["sensitivity"]["weight_groups"]
    levels = cfg["sensitivity"]["weight_levels"]
    wins: dict[str, int] = {d["design_id"]: 0 for d in front}
    n = 0
    scored = [(d, group_scores(d)) for d in front]
    for ws in product(levels, repeat=len(groups)):
        if not any(ws):
            continue
        n += 1
        best = max(scored, key=lambda x: (sum(w * x[1][g] for w, g in zip(ws, groups)), x[0]["design_id"]))
        wins[best[0]["design_id"]] += 1
    return [{"design_id": k, "weight_grid_wins": v, "weight_grid_size": n,
             "share": round(v / n, 4)} for k, v in sorted(wins.items(), key=lambda kv: -kv[1])]


# ------------------------------------------------------------------ driver
def run(tables) -> dict:
    cfg = load_config()
    spans = {s["span_id"]: s for s in tables["source_spans"]}
    rules = load_rules()
    variants = gate_variants(cfg)
    weakest = {}
    for g in GOALS:
        lv = [cfg["levels"][v[g]] for v in variants.values() if g in v]
        if lv and len(lv) == len(variants):
            weakest[g] = [k for k, val in cfg["levels"].items() if val == min(lv)][0]
    results = {"by_cutoff": {}}
    for cutoff in cfg["sensitivity"]["evidence_grade_cutoffs"]:
        box = load_box(spans, cutoff)
        A, native = anchor_designs(box, rules, cfg)
        B = enumerate_B(box, rules, cfg, weakest)
        B_feasible_total = enumerate_B.last_feasible
        C = [baseline_C(cfg)]
        per_variant = {}
        for vname, gates in variants.items():
            passing = [d for d in A + B + C if gate_pass(d, gates, cfg)]
            front = pareto_front(passing)
            per_variant[vname] = {
                "n_passing": {s: sum(1 for d in passing if d["strategy"] == s) for s in "ABC"},
                "front": front,
                "profiles": {p: (min(front, key=f)["design_id"] if front else None) for p, f in PROFILES.items()},
                "weighted": weighted_view(front, cfg),
                "anchors_passing": sorted({d["anchor"] for d in passing if d["strategy"] == "A"}),
                "anchors_passing_without_transplant": sorted({d["anchor"] for d in passing
                                                              if d["strategy"] == "A" and d["overlays"] == 0}),
            }
        results["by_cutoff"][cutoff] = {
            "box_rows": len(box), "A": A, "B_count": len(B), "B_feasible_total": B_feasible_total, "B_front_all": pareto_front(B), "C": C,
            "native_rule_conflicts": native, "variants": per_variant, "B": B,
        }
    write_outputs(results, cfg)
    return results


def write_outputs(results: dict, cfg: dict) -> None:
    out = MODELS / "synthesis"
    main = results["by_cutoff"]["D"]
    cols = ["design_id", "strategy", "anchor", *DIMS, *GOALS, *COST_KEYS, "n_elements", "setting_year",
            "source_cases", "trace_rows"]
    write_csv(out / "candidates_A.csv", main["A"], cols + ["transplant_rows"])
    write_csv(out / "candidates_B_pareto_all.csv", main["B_front_all"], cols + ["n_equivalent_designs", "equivalent_design_ids_sample"])
    write_csv(out / "candidates_C.csv", main["C"], cols + ["note"])
    sens_rows, front_rows, weight_rows = [], [], []
    for cutoff, res in results["by_cutoff"].items():
        for vname, v in res["variants"].items():
            sens_rows.append({
                "evidence_grade_cutoff": cutoff, "gate_variant": vname,
                "box_rows": res["box_rows"], "B_designs_feasible_total": res["B_feasible_total"],
                "B_designs_minimal": res["B_count"],
                "A_passing": v["n_passing"]["A"], "B_passing": v["n_passing"]["B"], "C_passing": v["n_passing"]["C"],
                "pareto_size": len(v["front"]),
                "pareto_A": sum(1 for d in v["front"] if d["strategy"] == "A"),
                "pareto_B": sum(1 for d in v["front"] if d["strategy"] == "B"),
                "pareto_C": sum(1 for d in v["front"] if d["strategy"] == "C"),
                "anchors_passing": "|".join(v["anchors_passing"]) or "NONE",
                "anchors_passing_without_transplant": "|".join(v["anchors_passing_without_transplant"]) or "NONE",
                **{f"profile_{p}": did for p, did in v["profiles"].items()},
            })
            for d in v["front"]:
                front_rows.append({"evidence_grade_cutoff": cutoff, "gate_variant": vname,
                                   **{k: d.get(k, "") for k in cols + ["transplant_rows", "n_equivalent_designs"]}})
            for w in v["weighted"]:
                weight_rows.append({"evidence_grade_cutoff": cutoff, "gate_variant": vname, **w})
    write_csv(out / "sensitivity.csv", sens_rows)
    write_csv(out / "pareto_front.csv", front_rows, ["evidence_grade_cutoff", "gate_variant", *cols,
                                                    "transplant_rows", "n_equivalent_designs"])
    write_csv(out / "weighted_view_sensitivity.csv", weight_rows)
    # inspiration trace for every design on the default Pareto front (cutoff D)
    box = {r["row_id"]: r for r in read_csv(MODELS / "synthesis" / "morphological_box.csv")}
    trace = []
    for d in main["variants"]["default"]["front"]:
        for rid in split(d["trace_rows"]):
            r = box.get(rid)
            if not r:
                continue
            trace.append({
                "design_id": d["design_id"], "strategy": d["strategy"], "dim": r["dim"], "value_id": r["value_id"],
                "source_case": r["source_case"], "code_row_ids": r["code_row_ids"], "span_ids": r["span_ids"],
                "source_status": r["source_status"],
                "role_in_design": ("TRANSPLANT" if rid in split(d.get("transplant_rows", "")) else
                                   ("IN_SITU_DOCUMENTED" if d["strategy"] == "A" else "INSPIRATION_FICTIONALIZED")),
            })
    write_csv(out / "inspiration_trace.csv", trace)
    write_json(out / "synthesis_summary.json", {
        "note": "가중합·프로필은 설정 의존 보조 화면이며 연구 결과가 아니다. 확률 없음.",
        "native_rule_conflicts": main["native_rule_conflicts"],
        "sensitivity": sens_rows,
    })
