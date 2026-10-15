"""Step 5: morphological box, CSP, anchors (A), synthetic designs (B), Pareto."""

import pytest

from historinference import synthesis as S


@pytest.fixture(scope="module")
def setup(tables):
    cfg = S.load_config()
    spans = {s["span_id"]: s for s in tables["source_spans"]}
    rules = S.load_rules()
    box_d = S.load_box(spans, "D")
    box_b = S.load_box(spans, "B")
    return cfg, spans, rules, box_d, box_b


def test_box_rows_trace_to_codes_and_spans(setup, tables):
    cfg, spans, rules, box, _ = setup
    code_ids = {c["code_row_id"] for c in tables["mechanism_codes"]}
    for r in box:
        if r["fiction_only"] == "1":
            assert r["source_case"] == "FICTION" and not r["span_ids"]
            continue
        assert r["span_ids"], r["row_id"]
        for s in r["span_ids"].split("|"):
            assert s in spans and spans[s]["case_id"] in (r["source_case"], "ALL"), (r["row_id"], s)
        for c in filter(None, r["code_row_ids"].split("|")):
            assert c in code_ids, (r["row_id"], c)


def test_box_grade_is_derived_from_spans(setup):
    _, spans, _, box, box_b = setup
    assert all(r["grade"] in ("B", "C", "D", "F") for r in box)
    assert all(r["grade"] in ("B", "F") for r in box_b)
    assert len(box_b) < len(box)


def test_goal_rules_on_anchor_cases(setup):
    cfg, _, rules, box, _ = setup
    A, native = S.anchor_designs(box, rules, cfg)
    base = {d["anchor"]: d for d in A if d["overlays"] == 0}
    assert set(base) == {"CHOI", "CHO", "YE", "GUSUN"}
    assert base["YE"]["Y3"] == 0  # no falsely accused person in the YE record
    assert base["GUSUN"]["Y3"] == 1  # died in custody: posthumous vindication only
    assert all(base[k]["Y1"] <= 1 for k in base)  # no historical case proves the culprit
    assert native == {k: [] for k in ("CHOI", "CHO", "YE", "GUSUN")}


def test_anchor_never_receives_fiction_or_overwrites_documented_values(setup):
    cfg, _, rules, box, _ = setup
    A, _ = S.anchor_designs(box, rules, cfg)
    rows = {r["row_id"]: r for r in box}
    for d in A:
        own = {r["dim"] for r in box if r["source_case"] == d["anchor"]}
        for rid in filter(None, d["transplant_rows"].split("|")):
            r = rows[rid]
            assert r["fiction_only"] == "0"
            assert r["source_case"] != d["anchor"]
            assert r["dim"] not in own
        assert d["untraced"] == 0


def test_csp_rejects_incompatible_combination(setup):
    cfg, _, rules, _, _ = setup
    assign = {d: {S.NONE_VALUE.get(d, "X")} for d in S.DIMS}
    assign["M1_TRIGGER"] = {"T_RUMOR_ACCUSATION"}
    assign["M10A_PERPETRATOR_ACCOUNTABILITY"] = {"K_ACCUSER_PUNISHED"}
    assert "CR-01" in S.rule_violations(assign, rules)


def test_b_designs_are_feasible_minimal_and_traced(setup):
    cfg, _, rules, _, box_b = setup
    weakest = {"Y3": "PARTIAL", "Y4": "PARTIAL", "Y5": "PARTIAL"}
    B = S.enumerate_B(box_b, rules, cfg, weakest)
    assert B
    rows = {r["row_id"]: r for r in box_b}
    for d in B:
        assign = {k: {d[k]} for k in S.DIMS}
        assert S.rule_violations(assign, rules) == []
        assert d["overlays"] == 0 and d["real_person_risk"] == 0
        traced = [rows[r] for r in d["trace_rows"].split("|") if r]
        assert {r["dim"] for r in traced} == {k for k in S.DIMS if not d[k].endswith("_NONE")}
        # Occam: no element can be removed without losing a goal level or feasibility
        base = S.goal_levels(assign, cfg)
        for dim, none in S.NONE_VALUE.items():
            if d[dim] == none:
                continue
            trial = dict(assign)
            trial[dim] = {none}
            if S.rule_violations(trial, rules):
                continue
            assert S.goal_levels(trial, cfg) != base, (d["design_id"], dim)


def test_fiction_only_resolution_is_the_only_route_to_full_y1(setup):
    cfg, _, rules, box, _ = setup
    row = next(r for r in box if r["value_id"] == "U_FICTIONAL_PROVEN_CULPRIT")
    assert row["fiction_only"] == "1"
    rule = cfg["goal_rules"]["Y1"]["FULL"]
    assert rule == [{"M11_RESOLUTION": ["U_FICTIONAL_PROVEN_CULPRIT"]}]


def test_pareto_dominance():
    base = {g: 1 for g in S.GOALS} | {c: 1 for c in S.COST_KEYS}
    a = {**base, "design_id": "a"}
    b = {**base, "design_id": "b", "severity": 5}            # dominated by a
    c = {**base, "design_id": "c", "Y1": 2, "severity": 9}   # trade-off: not dominated
    front = {d["design_id"] for d in S.pareto_front([a, b, c])}
    assert front == {"a", "c"}


def test_weighted_view_is_marked_auxiliary(setup):
    cfg, *_ = setup
    assert "연구 결과가 아니" in open(S.CONFIG / "objectives.toml", encoding="utf-8").read()
    front = [{**{g: 1 for g in S.GOALS}, **{c: 0 for c in S.COST_KEYS}, "design_id": "x"}]
    view = S.weighted_view(front, cfg)
    assert view[0]["share"] == 1.0


def test_hard_gates_match_spec(setup):
    cfg, *_ = setup
    assert cfg["hard_gates"] == {"Y3": "PARTIAL", "Y4": "PARTIAL", "Y5": "PARTIAL", "Y6": "PARTIAL"}
    assert "Y1" not in cfg["hard_gates"] and "Y2" not in cfg["hard_gates"]
