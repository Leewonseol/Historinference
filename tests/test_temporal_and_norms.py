"""Partial order, death constraints, norm anachronism, order vs execution."""

from conftest import errors
from historinference import constraints, validate


def test_real_temporal_checks_pass(tables, edges):
    assert errors(validate.check_temporal(tables, edges)) == []
    assert errors(validate.check_death_constraints(tables)) == []
    assert errors(validate.check_norms(tables)) == []
    assert errors(validate.check_order_execution(tables)) == []


def test_partial_order_leaves_unknown_pairs_incomparable(tables, edges):
    summary = constraints.summarize(tables, edges)
    assert summary["CHOI"]["n_incomparable_pairs"] > 0
    assert summary["CHO"]["n_incomparable_pairs"] > 0
    # 1785 inquest vs father's accusation: order unknown, so no edge either way
    pairs = {(e["before_id"], e["after_id"]) for e in edges}
    assert ("EV-CH-02", "EV-CH-03") not in pairs and ("EV-CH-03", "EV-CH-02") not in pairs


def test_cycle_is_detected(mutable, edges):
    bad = list(edges) + [{"before_id": "EV-GS-16", "after_id": "EV-GS-01", "basis": "EXPLICIT_SEQUENCE", "span_ids": "x", "case_id": "GUSUN"}]
    assert any("순환" in f.message for f in errors(validate.check_temporal(mutable, bad)))


def test_invented_order_is_detected(mutable, edges):
    bad = list(edges) + [{"before_id": "EV-CH-02", "after_id": "EV-CH-03", "basis": "DATE_COMPARISON", "span_ids": "", "case_id": "CHOI"}]
    assert any("확정되지 않은" in f.message for f in errors(validate.check_temporal(mutable, bad)))


def test_explicit_order_contradicting_dates_is_detected(mutable):
    mutable["event_order"].append({"before_id": "EV-GS-16", "after_id": "EV-GS-01", "basis": "EXPLICIT_SEQUENCE",
                                   "span_ids": "GS-S01", "note": "bad"})
    assert any("모순" in f.message for f in errors(validate.check_temporal(mutable, None)))


def test_cross_case_order_is_detected(mutable):
    mutable["event_order"].append({"before_id": "EV-YE-02", "after_id": "EV-GS-16", "basis": "EXPLICIT_SEQUENCE",
                                   "span_ids": "YE-S14", "note": "same day"})
    assert any("사건 간" in f.message for f in errors(validate.check_temporal(mutable, None)))


def test_action_after_death_is_detected(mutable):
    # 조광진 died 1788 (瘐死): make him act in 1789
    ev = next(e for e in mutable["events"] if e["event_id"] == "EV-CH-15")
    ev["actor_ids"] = "CHOI-P06"
    assert any("사망" in f.message for f in errors(validate.check_death_constraints(mutable)))


def test_1792_manual_backdated_to_1785_is_detected(mutable):
    ev = next(e for e in mutable["events"] if e["event_id"] == "EV-CH-02")
    ev["norm_refs"] = "N02"
    assert any("소급" in f.message for f in errors(validate.check_norms(mutable)))


def test_1786_code_backdated_to_1785_is_detected(mutable):
    ev = next(e for e in mutable["events"] if e["event_id"] == "EV-CH-01")
    ev["date_end"] = "1785-11"
    ev["norm_refs"] = "N01"
    assert any("대전통편" in f.message for f in errors(validate.check_norms(mutable)))


def test_norm_outside_verified_range_is_warning_not_error(tables):
    findings = validate.check_norms(tables)
    assert findings and all(f.severity == "WARN" for f in findings)


def test_orders_are_not_executions(tables):
    for d in tables["decisions"]:
        assert d["order_or_execution"] == "ORDER"
        assert d["execution_status"] != "EXECUTED"


def test_order_execution_confusion_is_detected(mutable):
    mutable["decisions"][0]["execution_status"] = "EXECUTED"
    assert errors(validate.check_order_execution(mutable), "V08")


def test_dates_keep_calendar(tables):
    assert {e["calendar"] for e in tables["events"]} <= {"LUNAR", "UNKNOWN"}
    assert all(e["date_precision"] in {"DAY", "MONTH", "YEAR", "RANGE", "UNKNOWN"} for e in tables["events"])
