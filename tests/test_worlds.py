"""Step 4: possible-world candidates (CSP), UNSCORED, observed acts fixed."""

import pytest

from historinference import worlds


@pytest.fixture(scope="module")
def generated(tables):
    axes, rules = worlds.load_axes()
    out = {}
    for case in ("CHOI", "CHO", "YE", "GUSUN"):
        fixed = [e["event_id"] for e in tables["events"] if e["case_id"] == case and e["layer"] == "OBSERVED_ACT"]
        rows, total = worlds.enumerate_case(case, axes[case], rules.get(case, []), fixed)
        out[case] = (rows, total, axes[case], rules.get(case, []))
    return out


def test_every_world_is_unscored(generated):
    for rows, *_ in generated.values():
        assert rows
        assert all(r["posterior"] == "UNSCORED" and r["likelihood"] == "UNSCORED" for r in rows)
        assert all(r["layer"] == "WORLD_CANDIDATE_NOT_STORY" for r in rows)


def test_every_world_satisfies_constraints(generated):
    for rows, total, axes, rules in generated.values():
        assert len(rows) <= total
        for r in rows:
            assert worlds.satisfies({a: r[a] for a in axes}, rules) == []


def test_constraints_remove_inconsistent_worlds(generated):
    rows, total, axes, rules = generated["CHOI"]
    assert total > len(rows)
    for r in rows:
        if r["A1_DEATH_MODE"] == "SELF_INFLICTED":
            assert r["A2_PERPETRATOR"] == "NONE"
        if r["A3_JO_CONFESSION"] == "TRUE":
            assert r["A2_PERPETRATOR"] in ("CHOI_AND_JO", "JO_ONLY")


def test_observed_acts_fixed_across_worlds(generated):
    for rows, *_ in generated.values():
        assert len({r["fixed_observed_ids"] for r in rows}) == 1


def test_third_party_never_named(generated):
    for rows, *_ in generated.values():
        for r in rows:
            if any("UNNAMED" in str(v) for v in r.values()):
                assert r["requires_unnamed_identity"] == 1


def test_choi_keeps_1789_alternatives(generated):
    rows, *_ = generated["CHOI"]
    assert any(r["A3_JO_CONFESSION"] == "UNRELIABLE" for r in rows)
    assert any(r["A1_DEATH_MODE"] == "SELF_INFLICTED" for r in rows)
    assert any(r["A2_PERPETRATOR"] == "THIRD_PARTY_UNNAMED" for r in rows)


def test_unsupported_collusion_is_flagged(generated):
    rows, *_ = generated["YE"]
    flagged = [r for r in rows if r["C2_GOVERNOR"] == "COLLUSIVE_SHIELDING"]
    assert flagged and all(r["n_unsupported_hypotheses"] >= 1 for r in flagged)
