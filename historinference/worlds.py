"""Step 4 (part 2): possible-world candidates per case (CSP over latent axes).

Observed administrative acts are fixed (listed once per world); only latent
axes (actual deed, origin of the false accusation, evidence reliability,
collusion) branch. No posterior/likelihood is computed: the four cases do not
identify one, so every world is ``UNSCORED``. Worlds are analysis candidates,
not the final creative story.
"""

from __future__ import annotations

from itertools import product

from .io import MODELS, read_csv, split, write_csv, write_json

UNSUPPORTED = "UNSUPPORTED_HYPOTHESIS"


def load_axes():
    axes: dict[str, dict[str, list[dict]]] = {}
    for r in read_csv(MODELS / "worlds" / "world_axes.csv"):
        axes.setdefault(r["case_id"], {}).setdefault(r["axis_id"], []).append(r)
    rules: dict[str, list[dict]] = {}
    for r in read_csv(MODELS / "worlds" / "world_constraints.csv"):
        rules.setdefault(r["case_id"], []).append(r)
    return axes, rules


def satisfies(assign: dict[str, str], rules: list[dict]) -> list[str]:
    """Return ids of violated rules."""
    bad = []
    for r in rules:
        if assign.get(r["if_axis"]) in split(r["if_values"]):
            if assign.get(r["then_axis"]) not in split(r["then_values"]):
                bad.append(r["rule_id"])
    return bad


def enumerate_case(case: str, axes: dict[str, list[dict]], rules: list[dict], fixed: list[str]) -> tuple[list[dict], int]:
    names = list(axes)
    rows = []
    total = 0
    for combo in product(*(axes[a] for a in names)):
        total += 1
        assign = {a: v["value_id"] for a, v in zip(names, combo)}
        if satisfies(assign, rules):
            continue
        departures = [a for a, v in zip(names, combo) if v["is_last_affirmative_official"] != "1"
                      and any(x["is_last_affirmative_official"] == "1" for x in axes[a])]
        row = {
            "world_id": "",
            "case_id": case,
            **{a: assign[a] for a in names},
            "n_axes": len(names),
            "n_departures_from_last_affirmative_official": len(departures),
            "departure_axes": "|".join(departures),
            "n_unsupported_hypotheses": sum(1 for v in combo if v["basis_status"] == UNSUPPORTED),
            "n_hypotheses_raised_in_source": sum(1 for v in combo if v["basis_status"] == "HYPOTHESIS_RAISED_IN_SOURCE"),
            "requires_unnamed_identity": int(any("UNNAMED" in v["value_id"] for v in combo)),
            "basis_span_ids": "|".join(sorted({s for v in combo for s in split(v["basis_span_ids"])})),
            "fixed_observed_ids": "|".join(fixed),
            "posterior": "UNSCORED",
            "likelihood": "UNSCORED",
            "layer": "WORLD_CANDIDATE_NOT_STORY",
        }
        rows.append(row)
    rows.sort(key=lambda r: (r["n_unsupported_hypotheses"], r["n_departures_from_last_affirmative_official"],
                             tuple(r[a] for a in names)))
    for i, r in enumerate(rows, 1):
        r["world_id"] = f"W-{case}-{i:03d}"
    return rows, total


def build(tables) -> dict:
    axes, rules = load_axes()
    summary = {}
    for case in ("CHOI", "CHO", "YE", "GUSUN"):
        fixed = [e["event_id"] for e in tables["events"] if e["case_id"] == case and e["layer"] == "OBSERVED_ACT"]
        fixed += [d["decision_id"] for d in tables["decisions"] if d["case_id"] == case]
        rows, total = enumerate_case(case, axes[case], rules.get(case, []), fixed)
        write_csv(MODELS / "worlds" / f"worlds_{case}.csv", rows)
        summary[case] = {
            "axes": {a: [v["value_id"] for v in vals] for a, vals in axes[case].items()},
            "n_combinations": total,
            "n_consistent_worlds": len(rows),
            "n_eliminated_by_constraints": total - len(rows),
            "n_worlds_without_unsupported_hypotheses": sum(1 for r in rows if r["n_unsupported_hypotheses"] == 0),
            "n_fixed_observed": len(fixed),
            "posterior": "UNSCORED",
        }
    write_json(MODELS / "worlds" / "worlds_summary.json", {
        "note": "가능세계 후보는 분석층이며 최종 창작 스토리가 아니다. 확률은 식별 불가하므로 UNSCORED.",
        "cases": summary,
    })
    return summary
