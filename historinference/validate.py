"""Step 6: machine audits over the normalized tables.

Every check is a pure function ``check_xxx(tables) -> list[Finding]`` so the
test-suite can inject defects into an in-memory copy and confirm detection.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass

from . import dates
from .io import split
from .normalize import GRADE_ORDER, domain_policy

CODEBOOK = {
    "E01", "E02", "E03", "E04", "E05", "E06", "E07",
    "F01", "F02", "F03", "F04", "F05", "F06",
    "R01", "R02", "R03", "R04", "R05", "R06",
}
CLAIM_STATUSES = {"DOCUMENTED_ACT", "RECORDED_TESTIMONY", "OFFICIAL_JUDGMENT", "CONTESTED", "HYPOTHESIS", "UNKNOWN"}
RELATION_TYPES_REQUIRED = {"KINSHIP", "MARRIAGE", "PATRONAGE", "BRIBERY", "COMMAND", "TESTIMONY_INFLUENCE", "INFORMATION_TRANSFER"}
RELATION_TYPES_EXTRA = {"ALLEGED_ILLICIT_LIAISON", "HOUSEHOLD_SERVICE", "ACQUAINTANCE", "ACQUAINTANCE_DENIED", "CONFLICT"}
PERSON_ATTRIBUTES = {"gender", "age_range", "residence", "status_claimed", "status_verified", "office", "occupation", "kinship_marriage", "death"}
FORBIDDEN_ATTRIBUTES = {"birth_year", "birth_date", "age"}
FAULT_TYPES = {"NA", "DELIBERATE_COLLUSION", "DELIBERATE_PER_JUDGMENT", "NEGLIGENT_SUPERVISION", "ERRONEOUS_REPORT",
               "UNRESOLVED_DELIBERATE_VS_NEGLIGENT", "NOT_DELIBERATE_PER_INSPECTOR"}
LAYERS = {"OBSERVED_ACT", "RECORDED_STATEMENT", "OFFICIAL_JUDGMENT", "CONTEXT"}
IN_SCOPE_CASES = {"CHOI", "CHO", "YE", "GUSUN"}
ROW_KEYS = {
    "cases": "case_id", "persons": "person_id", "person_aliases": "alias_id", "person_attributes": "attr_id",
    "identity_separations": "sep_id", "institutions": "inst_id", "events": "event_id", "attestations": "att_id",
    "claims": "claim_id", "evidence_items": "item_id", "relations": "rel_id", "decisions": "decision_id",
    "mechanism_codes": "code_row_id", "case_outcomes": "case_id", "episodes": "episode_id",
    "source_spans": "span_id", "sources": "source_id", "appointments": "appt_id", "normative_rules": "rule_id",
}


@dataclass
class Finding:
    check: str
    severity: str  # ERROR | WARN
    table: str
    row: str
    message: str


def _f(check, severity, table, row, message):
    return Finding(check, severity, table, row, message)


def _span_index(t):
    return {s["span_id"]: s for s in t["source_spans"]}


def _person_case(pid: str) -> str:
    if pid.startswith("GUSUN-"):
        return "GUSUN"
    return pid.split("-", 1)[0]


# ------------------------------------------------------------------ V01
def check_source_integrity(t) -> list[Finding]:
    out = []
    sources = {s["source_id"] for s in t["sources"]}
    spans = _span_index(t)
    seen = set()
    for s in t["source_spans"]:
        if s["span_id"] in seen:
            out.append(_f("V01", "ERROR", "source_spans", s["span_id"], "중복 span_id"))
        seen.add(s["span_id"])
        for sid in split(s["source_id"]):
            if sid not in sources:
                out.append(_f("V01", "ERROR", "source_spans", s["span_id"], f"존재하지 않는 source_id {sid}"))
        if s["carrier_id"] not in sources:
            out.append(_f("V01", "ERROR", "source_spans", s["span_id"], f"존재하지 않는 carrier {s['carrier_id']}"))
    for table, key in ROW_KEYS.items():
        for row in t.get(table, []):
            for col in ("span_ids", "basis_span_ids"):
                if col not in row:
                    continue
                for sp in split(row[col]):
                    if sp not in spans:
                        out.append(_f("V01", "ERROR", table, row.get(key, "?"), f"존재하지 않는 span {sp}"))
    for s in t["sources"]:
        pol = domain_policy(s.get("url", ""))
        if pol == "FORBIDDEN_UNVERIFIED_REDISTRIBUTION":
            out.append(_f("V01", "ERROR", "sources", s["source_id"], "비승인 전재 사이트 출처"))
        if s.get("is_local_carrier") == "0" and pol not in ("APPROVED_OFFICIAL_PRIMARY", "APPROVED_INSTITUTIONAL_HOLDING", "NO_URL"):
            out.append(_f("V01", "ERROR", "sources", s["source_id"], f"승인되지 않은 원문 도메인 {s.get('url_domain')}"))
        if s.get("is_local_carrier") == "0" and s.get("offline_text_status") != "UNAVAILABLE_SOURCE_TEXT" and s.get("local_path", "NA") == "NA":
            out.append(_f("V01", "ERROR", "sources", s["source_id"], "로컬 원문 없이 원문 확보로 표시"))
    for x in t.get("source_crosswalk", []):
        if x["register_source_id"] == "UNMATCHED":
            out.append(_f("V01", "ERROR", "source_crosswalk", x["gusun_record_id"], "GuSoon 출처 레코드가 레지스터와 불일치"))
    return out


# ------------------------------------------------------------------ V02
def check_coding_evidence(t) -> list[Finding]:
    out = []
    spans = _span_index(t)
    unit_tables = {
        "EVENT": "events", "CLAIM": "claims", "PERSON": "persons", "RELATION": "relations",
        "EPISODE": "episodes", "DECISION": "decisions", "EVIDENCE": "evidence_items",
    }
    unit_ids = {u: {r[ROW_KEYS[tab]] for r in t[tab]} for u, tab in unit_tables.items()}
    claims = {c["claim_id"]: c for c in t["claims"]}
    for c in t["mechanism_codes"]:
        rid = c["code_row_id"]
        if c["code"] not in CODEBOOK:
            out.append(_f("V02", "ERROR", "mechanism_codes", rid, f"코드북에 없는 코드 {c['code']}"))
        if c["value"] not in {"1", "0", "NA"}:
            out.append(_f("V02", "ERROR", "mechanism_codes", rid, f"허용되지 않는 값 {c['value']}"))
        if c["claim_status"] not in CLAIM_STATUSES:
            out.append(_f("V02", "ERROR", "mechanism_codes", rid, f"claim_status 어휘 위반 {c['claim_status']}"))
        if c.get("fault_type", "NA") not in FAULT_TYPES:
            out.append(_f("V02", "ERROR", "mechanism_codes", rid, f"fault_type 어휘 위반 {c['fault_type']}"))
        if c["unit_type"] not in unit_tables:
            out.append(_f("V02", "ERROR", "mechanism_codes", rid, f"단위 유형 오류 {c['unit_type']}"))
        elif c["unit_id"] not in unit_ids[c["unit_type"]]:
            out.append(_f("V02", "ERROR", "mechanism_codes", rid, f"존재하지 않는 단위 {c['unit_id']}"))
        sp = split(c["span_ids"])
        if c["value"] in {"1", "0"}:
            if not sp:
                out.append(_f("V02", "ERROR", "mechanism_codes", rid, "증거 없는 1/0 코딩"))
            if c["claim_status"] in {"HYPOTHESIS", "UNKNOWN"}:
                out.append(_f("V02", "ERROR", "mechanism_codes", rid, "가설/미상 상태로 1/0 코딩"))
            usable = [s for s in sp if s in spans and GRADE_ORDER.get(spans[s]["evidence_grade"], 9) <= GRADE_ORDER["D"]]
            if sp and not usable:
                out.append(_f("V02", "ERROR", "mechanism_codes", rid, "코딩 근거 span의 등급이 D보다 낮음(링크·맥락 전용)"))
            for s in sp:
                if s in spans and spans[s]["case_id"] not in (c["case_id"], "ALL"):
                    out.append(_f("V02", "ERROR", "mechanism_codes", rid, f"다른 사건의 span {s} 사용"))
        if c["value"] == "0" and "부재 판단" not in c["rationale"]:
            out.append(_f("V02", "ERROR", "mechanism_codes", rid, "0 코딩에는 부재를 명시적으로 지지하는 근거 설명('부재 판단') 필요"))
        if c["unit_type"] == "CLAIM" and c["value"] == "1":
            cl = claims.get(c["unit_id"])
            if cl and cl["claim_status"] == "HYPOTHESIS":
                out.append(_f("V02", "ERROR", "mechanism_codes", rid, "가설 주장을 근거로 1 코딩"))
    return out


# ------------------------------------------------------------------ V03
def check_person_attributes(t) -> list[Finding]:
    out = []
    spans = _span_index(t)
    persons = {p["person_id"]: p for p in t["persons"]}
    for a in t["person_attributes"]:
        rid = a["attr_id"]
        if a["attribute"] in FORBIDDEN_ATTRIBUTES:
            out.append(_f("V03", "ERROR", "person_attributes", rid, f"근거 없는 생년/연령 속성 {a['attribute']} 금지"))
        elif a["attribute"] not in PERSON_ATTRIBUTES:
            out.append(_f("V03", "ERROR", "person_attributes", rid, f"허용되지 않는 속성 {a['attribute']}"))
        if a["person_id"] not in persons:
            out.append(_f("V03", "ERROR", "person_attributes", rid, f"없는 인물 {a['person_id']}"))
        sp = split(a["span_ids"])
        if not sp:
            out.append(_f("V03", "ERROR", "person_attributes", rid, "근거 없는 인물 속성"))
        for s in sp:
            if s in spans and spans[s]["case_id"] not in (_person_case(a["person_id"]), "ALL"):
                out.append(_f("V03", "ERROR", "person_attributes", rid, f"다른 사건 span {s}"))
        if a["attribute"] == "status_verified" and a["claim_status"] != "DOCUMENTED_ACT":
            out.append(_f("V03", "ERROR", "person_attributes", rid, "입증된 신분은 DOCUMENTED_ACT 근거 필요"))
        if a["attribute"] == "status_verified":
            grades = [spans[s]["evidence_grade"] for s in sp if s in spans]
            if not grades or min(GRADE_ORDER.get(g, 9) for g in grades) > GRADE_ORDER["B"]:
                out.append(_f("V03", "ERROR", "person_attributes", rid, "입증된 신분에는 B 이상 근거 필요"))
        if a["attribute"] == "age_range" and a["value"] not in ("NA", "") and a["derivation"] not in ("DIRECT",):
            out.append(_f("V03", "ERROR", "person_attributes", rid, "연령 범위는 직접 근거만 허용"))
        if a["claim_status"] not in CLAIM_STATUSES:
            out.append(_f("V03", "ERROR", "person_attributes", rid, "claim_status 어휘 위반"))
    return out


# ------------------------------------------------------------------ V04
def check_identity(t) -> list[Finding]:
    out = []
    ids = [p["person_id"] for p in t["persons"]]
    if len(ids) != len(set(ids)):
        out.append(_f("V04", "ERROR", "persons", "*", "중복 person_id"))
    for p in t["persons"]:
        if _person_case(p["person_id"]) != p["case_id"]:
            out.append(_f("V04", "ERROR", "persons", p["person_id"], "person_id 접두어와 case_id 불일치"))
    # aliases: same surface mapped to two different persons in one case
    surface_map: dict[tuple[str, str], set[str]] = {}
    for a in t["person_aliases"]:
        case = _person_case(a["person_id"])
        surface_map.setdefault((case, a["surface"]), set()).add(a["person_id"])
    for (case, surface), pids in surface_map.items():
        if len(pids) > 1:
            out.append(_f("V04", "ERROR", "person_aliases", surface, f"동일 표기가 여러 인물에 연결 {sorted(pids)}"))
    persons = {p["person_id"]: p for p in t["persons"]}
    for s in t["identity_separations"]:
        a, b = s["person_a"], s["person_b"]
        if s["decision"].startswith("DISTINCT") and a == b:
            out.append(_f("V04", "ERROR", "identity_separations", s["sep_id"], "구별해야 할 인물이 같은 ID로 병합됨"))
        if s["decision"].startswith("DISTINCT"):
            pa, pb = persons.get(a), persons.get(b)
            if pa and pb and pa["name_hanja"] not in ("NA", "") and pa["name_hanja"] == pb["name_hanja"]:
                out.append(_f("V04", "ERROR", "identity_separations", s["sep_id"], "구별 인물의 한자 표기가 동일"))
    # cross-case references in relational tables
    person_cols = {
        "events": ("actor_ids", "target_ids"), "relations": ("source_person", "target_person"),
        "attestations": ("speaker_id",), "decisions": ("decider_id", "target_id"),
        "person_attributes": ("person_id",),
    }
    for table, cols in person_cols.items():
        key = ROW_KEYS[table]
        for row in t[table]:
            case = row.get("case_id") or _person_case(row.get("person_id", ""))
            for col in cols:
                for pid in split(row.get(col, "")):
                    if pid.startswith("LOC-") or pid == "SOURCE_TEXT":
                        continue
                    if pid not in persons:
                        out.append(_f("V04", "ERROR", table, row[key], f"없는 인물 참조 {pid}"))
                    elif persons[pid]["case_id"] != case:
                        out.append(_f("V04", "ERROR", table, row[key], f"다른 사건 인물 참조 {pid}(사건 간 병합 금지)"))
    return out


# ------------------------------------------------------------------ V05
def check_temporal(t, edges: list[dict] | None = None) -> list[Finding]:
    out = []
    events = {e["event_id"]: e for e in t["events"]}
    for e in t["events"]:
        if e["calendar"] not in ("LUNAR", "SOLAR", "UNKNOWN"):
            out.append(_f("V05", "ERROR", "events", e["event_id"], "calendar 미표기"))
        iv = dates.interval(e["date_start"], e["date_end"])
        if e["date_precision"] != "UNKNOWN" and iv is None:
            out.append(_f("V05", "ERROR", "events", e["event_id"], "날짜 해석 불가"))
        if iv and iv[0] and iv[1] and iv[0] > iv[1]:
            out.append(_f("V05", "ERROR", "events", e["event_id"], "date_start가 date_end보다 늦음"))
    for o in t["event_order"]:
        a, b = events.get(o["before_id"]), events.get(o["after_id"])
        if not a or not b:
            out.append(_f("V05", "ERROR", "event_order", o["before_id"], "없는 사건 순서 참조"))
            continue
        if a["case_id"] != b["case_id"]:
            out.append(_f("V05", "ERROR", "event_order", o["before_id"], "사건 간 순서 연결 금지"))
        ia, ib = dates.interval(a["date_start"], a["date_end"]), dates.interval(b["date_start"], b["date_end"])
        if ia and ib and ia[0] and ib[1] and ia[0] > ib[1]:
            out.append(_f("V05", "ERROR", "event_order", f"{o['before_id']}>{o['after_id']}", "명시 순서가 날짜와 모순"))
        if o["basis"] == "EXPLICIT_SEQUENCE" and not split(o["span_ids"]):
            out.append(_f("V05", "ERROR", "event_order", o["before_id"], "근거 없는 명시 순서"))
    if edges is not None:
        out += _cycle_findings(edges)
        for e in edges:
            if e["basis"] not in ("EXPLICIT_SEQUENCE", "DATE_COMPARISON"):
                out.append(_f("V05", "ERROR", "partial_order", e["before_id"], "근거 유형 없는 순서 생성"))
            if e["basis"] == "DATE_COMPARISON":
                a, b = events[e["before_id"]], events[e["after_id"]]
                if not dates.strictly_before(dates.interval(a["date_start"], a["date_end"]), dates.interval(b["date_start"], b["date_end"])):
                    out.append(_f("V05", "ERROR", "partial_order", e["before_id"], "확정되지 않은 날짜 순서를 생성"))
    return out


def _cycle_findings(edges) -> list[Finding]:
    graph: dict[str, list[str]] = {}
    for e in edges:
        graph.setdefault(e["before_id"], []).append(e["after_id"])
    state: dict[str, int] = {}
    cycles = []

    def visit(n, stack):
        state[n] = 1
        for m in graph.get(n, []):
            if state.get(m) == 1:
                cycles.append(stack + [m])
            elif state.get(m) is None:
                visit(m, stack + [m])
        state[n] = 2

    for n in list(graph):
        if state.get(n) is None:
            visit(n, [n])
    return [_f("V05", "ERROR", "partial_order", c[0], f"순환: {'>'.join(c)}") for c in cycles]


# ------------------------------------------------------------------ V06
def check_death_constraints(t) -> list[Finding]:
    out = []
    deaths = {}
    for a in t["person_attributes"]:
        if a["attribute"] == "death":
            hi = None
            for token in a["time_scope"].replace("~", " ").split():
                b = dates.upper(token)
                if b and (hi is None or b > hi):
                    hi = b
            if hi:
                deaths[a["person_id"]] = hi
    for e in t["events"]:
        iv = dates.interval(e["date_start"], e["date_end"])
        if not iv or not iv[0]:
            continue
        for pid in split(e["actor_ids"]):
            if pid in deaths and iv[0] > deaths[pid]:
                out.append(_f("V06", "ERROR", "events", e["event_id"], f"사망({deaths[pid]}) 뒤 인물 {pid}의 행위"))
    for o in t["decisions"]:
        lo = dates.lower(o["date"])
        for pid in split(o["decider_id"]):
            if pid in deaths and lo and lo > deaths[pid]:
                out.append(_f("V06", "ERROR", "decisions", o["decision_id"], f"사망 뒤 인물 {pid}의 결정"))
    return out


# ------------------------------------------------------------------ V07
def check_norms(t) -> list[Finding]:
    out = []
    rules = {r["rule_id"]: r for r in t["normative_rules"]}
    for e in t["events"]:
        iv = dates.interval(e["date_start"], e["date_end"])
        for nid in split(e["norm_refs"]):
            r = rules.get(nid)
            if r is None:
                out.append(_f("V07", "ERROR", "events", e["event_id"], f"없는 규범 {nid}"))
                continue
            if not iv:
                continue
            valid_from = dates.lower(r["valid_from"])
            if r["breakpoint_kind"] == "HARD_ENACTMENT" and valid_from and iv[1] and iv[1] < valid_from:
                out.append(_f("V07", "ERROR", "events", e["event_id"], f"시행 전 규범 소급 적용: {r['name']}({r['valid_from']})"))
            through = dates.upper(r["verified_through"])
            if through and iv[0] and iv[0] > through:
                out.append(_f("V07", "WARN", "events", e["event_id"], f"규범 검증 범위({r['verified_through']}) 밖 시점에 적용: {r['name']}"))
    return out


# ------------------------------------------------------------------ V08
def check_order_execution(t) -> list[Finding]:
    out = []
    for d in t["decisions"]:
        if d["order_or_execution"] != "ORDER":
            out.append(_f("V08", "ERROR", "decisions", d["decision_id"], "결정 표는 명령(ORDER)만 기록"))
        if d["execution_status"] == "EXECUTED":
            out.append(_f("V08", "ERROR", "decisions", d["decision_id"], "집행 근거 없이 EXECUTED 표시(명령과 집행 혼동)"))
        if d["execution_status"] not in ("NOT_RETRIEVED", "RECORDED_FOLLOWUP", "SUPERSEDED"):
            out.append(_f("V08", "ERROR", "decisions", d["decision_id"], "집행 상태 어휘 위반"))
    for e in t["events"]:
        if e["order_or_execution"] == "ORDER" and e["layer"] != "OBSERVED_ACT":
            out.append(_f("V08", "ERROR", "events", e["event_id"], "명령 사건의 층위 오류"))
    return out


# ------------------------------------------------------------------ V09
def check_layers(t) -> list[Finding]:
    """Source text vs inference: hypotheses never sit in the observed layer."""
    out = []
    for e in t["events"]:
        if e["layer"] not in LAYERS:
            out.append(_f("V09", "ERROR", "events", e["event_id"], f"층위 어휘 위반 {e['layer']}"))
        if e["claim_status"] not in CLAIM_STATUSES:
            out.append(_f("V09", "ERROR", "events", e["event_id"], "claim_status 어휘 위반"))
        if e["layer"] == "OBSERVED_ACT" and e["claim_status"] in ("HYPOTHESIS", "UNKNOWN"):
            out.append(_f("V09", "ERROR", "events", e["event_id"], "가설이 관측 층에 혼입"))
        if not split(e["span_ids"]):
            out.append(_f("V09", "ERROR", "events", e["event_id"], "근거 없는 사건"))
    atts = {a["att_id"]: a for a in t["attestations"]}
    for c in t["claims"]:
        if c["claim_status"] not in CLAIM_STATUSES:
            out.append(_f("V09", "ERROR", "claims", c["claim_id"], "claim_status 어휘 위반"))
        if c["claim_status"] == "HYPOTHESIS":
            att = atts.get(c["att_id"])
            if not att or att["att_mode"] not in ("ROYAL_DOUBT",):
                out.append(_f("V09", "ERROR", "claims", c["claim_id"], "가설 주장은 사료 속 의문 제기(ROYAL_DOUBT)로만 기록"))
        if not split(c["span_ids"]):
            out.append(_f("V09", "ERROR", "claims", c["claim_id"], "근거 없는 주장"))
    for r in t["relations"]:
        if r["rel_type"] not in RELATION_TYPES_REQUIRED | RELATION_TYPES_EXTRA:
            out.append(_f("V09", "ERROR", "relations", r["rel_id"], f"관계 유형 오류 {r['rel_type']}"))
        if not split(r["span_ids"]) or not r["time_scope"] or r["claim_status"] not in CLAIM_STATUSES:
            out.append(_f("V09", "ERROR", "relations", r["rel_id"], "관계는 출처·시점·주장상태를 모두 포함해야 함"))
        if r["rel_type"] == "KINSHIP" and r["claim_status"] in ("DOCUMENTED_ACT", "RECORDED_TESTIMONY", "OFFICIAL_JUDGMENT") \
                and "NA" in (r["source_person"], r["target_person"]):
            out.append(_f("V09", "ERROR", "relations", r["rel_id"], "상대가 미식별인 친족관계를 확정 상태로 코딩"))
    return out


# ------------------------------------------------------------------ V10
def check_case_separation(t) -> list[Finding]:
    out = []
    cases = {c["case_id"]: c for c in t["cases"]}
    for table in ("events", "claims", "relations", "decisions", "mechanism_codes", "attestations"):
        key = ROW_KEYS[table]
        for row in t[table]:
            if row["case_id"] not in IN_SCOPE_CASES:
                out.append(_f("V10", "ERROR", table, row[key], f"범위 밖 사건 {row['case_id']} 데이터 혼입"))
    for e in t["events"]:
        if e["case_id"] == "YE":
            y = dates.year_of(e["date_start"])
            if y and y >= 1796:
                out.append(_f("V10", "ERROR", "events", e["event_id"], "1801 황기운 등 후대 별도 사건을 YE에 융합"))
    if cases.get("YE1801_HWANG", {}).get("in_scope") == "1":
        out.append(_f("V10", "ERROR", "cases", "YE1801_HWANG", "별도 사건을 분석 범위에 포함"))
    # same-date (1793-06-13) GUSUN and YE material must not share events/spans
    spans = _span_index(t)
    for e in t["events"]:
        for sp in split(e["span_ids"]):
            if sp in spans and spans[sp]["case_id"] not in (e["case_id"], "ALL"):
                out.append(_f("V10", "ERROR", "events", e["event_id"], f"다른 사건 span {sp}"))
    for c in t["claims"]:
        for sp in split(c["span_ids"]):
            if sp in spans and spans[sp]["case_id"] not in (c["case_id"], "ALL"):
                out.append(_f("V10", "ERROR", "claims", c["claim_id"], f"다른 사건 span {sp}"))
    return out


# ------------------------------------------------------------------ V11
def check_case_invariants(t) -> list[Finding]:
    """Interpretive guard-rails stated in CLAUDE.md step 3."""
    out = []
    claims = {c["claim_id"]: c for c in t["claims"]}
    outcomes = {o["case_id"]: o for o in t["case_outcomes"]}
    # CHOI: 1787 conclusion must stay contested because of the 1789 re-questioning
    c = claims.get("CL-CH-04")
    if not c or c["claim_status"] != "CONTESTED":
        out.append(_f("V11", "ERROR", "claims", "CL-CH-04", "1787 안핵 결론이 1789 재의문 없이 확정됨"))
    if not any(e["event_id"] == "EV-CH-15" for e in t["events"]):
        out.append(_f("V11", "ERROR", "events", "EV-CH-15", "1789 재의문 사건 누락"))
    # CHO: accuser manipulation must not become proof of murder
    for r in t["relations"]:
        if r["case_id"] == "CHO" and r["source_person"] == "CHO-P03" and r["target_person"] == "CHO-P02" \
                and r["rel_type"] not in ("KINSHIP",):
            out.append(_f("V11", "ERROR", "relations", r["rel_id"], "고발자-사망자 관계를 친족 외로 확정(살해자 오인 위험)"))
    if outcomes.get("CHO", {}).get("historical_culprit_status", "").startswith("CONFIRMED"):
        out.append(_f("V11", "ERROR", "case_outcomes", "CHO", "윤씨 사망 진범 확정 금지"))
    # YE: 31 and 25 kept as separate attributed claims
    counts = [c for c in t["claims"] if c.get("conflict_group") == "CG-YE-COUNT"]
    if len(counts) < 2:
        out.append(_f("V11", "ERROR", "claims", "CG-YE-COUNT", "31/25 수치를 하나로 합침"))
    for c in t["claims"]:
        if "31" in c["proposition"] and "25" in c["proposition"]:
            out.append(_f("V11", "ERROR", "claims", c["claim_id"], "31과 25를 한 주장으로 병합"))
    # GUSUN: direct causation of Kim's death stays unresolved
    if outcomes.get("GUSUN", {}).get("historical_culprit_status") != "UNRESOLVED_DIRECT_CAUSATION":
        out.append(_f("V11", "ERROR", "case_outcomes", "GUSUN", "김명신 사망 직접 인과 미확정 상태 누락"))
    if "GS-CL-CF042" not in claims:
        out.append(_f("V11", "ERROR", "claims", "GS-CL-CF042", "정조의 직접 인과 불확실 판단 누락"))
    for o in t["case_outcomes"]:
        if o["historical_culprit_status"].startswith("CONFIRMED"):
            out.append(_f("V11", "ERROR", "case_outcomes", o["case_id"], "역사적 실체 범인 확정 금지(당시 판단과 분리)"))
    # official deliberate collusion must never be coded as established
    for c in t["mechanism_codes"]:
        if c.get("fault_type") == "DELIBERATE_COLLUSION" and c["value"] == "1":
            out.append(_f("V11", "ERROR", "mechanism_codes", c["code_row_id"], "관료의 고의적 공모를 입증 없이 코딩"))
    return out


# ------------------------------------------------------------------ V12
def check_checksums(t, expected: list[dict], actual: dict[str, str]) -> list[Finding]:
    out = []
    for row in expected:
        got = actual.get(row["path"])
        if got is None:
            out.append(_f("V12", "ERROR", "imported_checksums", row["path"], "가져온 원본 파일 누락"))
        elif got != row["sha256"]:
            out.append(_f("V12", "ERROR", "imported_checksums", row["path"], "가져온 GuSoon/Chamang 파일이 변경됨(checksum 불일치)"))
    return out


ALL_CHECKS = [
    check_source_integrity, check_coding_evidence, check_person_attributes, check_identity,
    check_temporal, check_death_constraints, check_norms, check_order_execution, check_layers,
    check_case_separation, check_case_invariants,
]


def run_all(t, edges=None, expected_checksums=None, actual_checksums=None) -> list[Finding]:
    findings: list[Finding] = []
    for check in ALL_CHECKS:
        if check is check_temporal:
            findings += check(t, edges)
        else:
            findings += check(t)
    if expected_checksums is not None and actual_checksums is not None:
        findings += check_checksums(t, expected_checksums, actual_checksums)
    return findings


def findings_rows(findings: list[Finding]) -> list[dict]:
    return [asdict(f) for f in findings]
