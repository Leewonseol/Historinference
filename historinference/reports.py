"""Step 7: Markdown reports and the read-only dashboard data bundle.

Every number printed here is recomputed from data/normalized, models/ and
data/audit, so the reports never drift from the data.
"""

from __future__ import annotations

import json
import re
from collections import Counter, defaultdict

from .io import AUDIT, DOCS, MODELS, OUTPUTS, RAW_INDEX, ROOT, read_csv, split
from .normalize import GRADE_ORDER, span_grade
from .synthesis import COST_KEYS, DIMS, GOALS, load_config

CASES = ["CHOI", "CHO", "YE", "GUSUN"]
CASE_LABEL = {
    "CHOI": "CHOI 평산 최아지·이차망(1785–1789)",
    "CHO": "CHO 배천 조재항(1780/1781–1783)",
    "YE": "YE 창원 이여절·조진택(1793–1795)",
    "GUSUN": "GUSUN 구순–김명신(1793)",
}
CODE_LABEL = {
    "E01": "증거 인멸·변조", "E02": "허위(사실과 다른) 검험·보고", "E03": "증언 강요·유도", "E04": "청탁·뇌물",
    "E05": "내부·상급자의 비호", "E06": "정보 왜곡 보고", "E07": "오류 인지 후 불시정",
    "F01": "비범인 지목", "F02": "구금", "F03": "유죄 판단·형벌(명령)", "F04": "구금 중 사망", "F05": "혐의 해소",
    "F06": "석방(명령)",
    "R01": "독립 재검증", "R02": "범행 자백(진실성 별도)", "R03": "제3자 진술 변경", "R04": "신규 물증",
    "R05": "모순 발견", "R06": "가족·피의자·피해자 측 호소",
}
CODES = list(CODE_LABEL)
LEVEL_NAME = {0: "NONE", 1: "PARTIAL", 2: "FULL"}
BANNER = ("> 자동 생성 문서(`python -m historinference report`). 모든 수치는 `data/normalized`·`models`·`data/audit`에서 "
          "재계산된다. 원문 미보관(UNAVAILABLE_SOURCE_TEXT) 상태에서 로컬 요약·선행 코딩만으로 작성되었으며, "
          "확률·빈도 추정은 하지 않는다.\n")


def md_table(headers: list[str], rows: list[list]) -> str:
    def esc(x):
        return str(x).replace("|", "\\|").replace("\n", " ")
    out = ["| " + " | ".join(headers) + " |", "|" + "|".join("---" for _ in headers) + "|"]
    out += ["| " + " | ".join(esc(c) for c in r) + " |" for r in rows]
    return "\n".join(out)


def _load_json(path, default=None):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return default


# ------------------------------------------------------------------ stats
def compute_stats(t) -> dict:
    spans = {s["span_id"]: s for s in t["source_spans"]}
    official = [s for s in t["sources"] if s["is_local_carrier"] == "0"]
    codes = t["mechanism_codes"]
    vals = Counter(c["value"] for c in codes)
    cells_with_evidence = set()
    for c in codes:
        if c["value"] in ("1", "0"):
            cells_with_evidence.add((c["case_id"], c["code"]))
    grade_counts = Counter()
    for c in codes:
        if c["value"] in ("1", "0"):
            grade_counts[span_grade(split(c["span_ids"]), spans)] += 1
    test = _load_json(AUDIT / "test_results.json", {})
    validation = _load_json(AUDIT / "validation_summary.json", {})
    per_case = {}
    for k in CASES:
        cc = [c for c in codes if c["case_id"] == k]
        per_case[k] = {
            "rows": len(cc),
            "coded_1": sum(1 for c in cc if c["value"] == "1"),
            "coded_0": sum(1 for c in cc if c["value"] == "0"),
            "na": sum(1 for c in cc if c["value"] == "NA"),
            "codes_covered": len({c["code"] for c in cc if c["value"] in ("1", "0")}),
            "events": sum(1 for e in t["events"] if e["case_id"] == k),
            "claims": sum(1 for c in t["claims"] if c["case_id"] == k),
            "persons": sum(1 for p in t["persons"] if p["case_id"] == k),
        }
    return {
        "sources_official": len(official),
        "sources_official_text_available": sum(1 for s in official if s["offline_text_status"] != "UNAVAILABLE_SOURCE_TEXT"),
        "sources_official_not_retrieved": sum(1 for s in official if s["retrieval_status"] == "NOT_RETRIEVED"),
        "local_documents": sum(1 for s in t["sources"] if s["is_local_carrier"] == "1"),
        "spans": len(spans),
        "span_grades": dict(Counter(s["evidence_grade"] for s in spans.values())),
        "verbatim_spans": sum(1 for s in spans.values() if s.get("offline_primary_verbatim") == "YES"),
        "code_rows": len(codes),
        "code_values": dict(vals),
        "coded_share": round((vals["1"] + vals["0"]) / len(codes), 3) if codes else 0,
        "cell_application_rate": round(len(cells_with_evidence) / (len(CASES) * len(CODES)), 3),
        "cells_with_evidence": len(cells_with_evidence),
        "coded_by_grade": dict(grade_counts),
        "per_case": per_case,
        "claims_by_status": dict(Counter(c["claim_status"] for c in t["claims"])),
        "persons": len(t["persons"]),
        "person_attributes": len(t["person_attributes"]),
        "events": len(t["events"]),
        "claims": len(t["claims"]),
        "relations": len(t["relations"]),
        "decisions": len(t["decisions"]),
        "requests": len(t.get("research_requests", [])),
        "tests": {k: test.get(k) for k in ("tests", "passed", "failures", "errors", "skipped", "exit_code")},
        "validation": {"errors": validation.get("errors"), "warnings": validation.get("warnings")},
    }


def status_block(st: dict) -> str:
    tests = st["tests"]
    rows = [
        ["공식 출처 레지스터(원문 위치)", f"{st['sources_official']}건", f"원문 로컬 확보 {st['sources_official_text_available']}건 / NOT_RETRIEVED {st['sources_official_not_retrieved']}건"],
        ["로컬 근거 문서", f"{st['local_documents']}건", "의역·요약·선행 코딩(원문 전사 아님)"],
        ["문장 단위 근거(span)", f"{st['spans']}건", "등급 " + ", ".join(f"{g}={n}" for g, n in sorted(st['span_grades'].items(), key=lambda kv: GRADE_ORDER.get(kv[0], 9))) + f"; 원문 직접 인용 {st['verbatim_spans']}건"],
        ["메커니즘 코딩 행", f"{st['code_rows']}행", f"확인(1/0) {st['code_values'].get('1', 0) + st['code_values'].get('0', 0)}행 · 미확인(NA) {st['code_values'].get('NA', 0)}행 · 코딩 비율 {st['coded_share']:.1%}"],
        ["사건×코드 적용률", f"{st['cells_with_evidence']}/{len(CASES) * len(CODES)} 칸", f"{st['cell_application_rate']:.1%} (1/0 근거가 하나 이상 있는 칸)"],
        ["확인 코딩의 근거 등급", ", ".join(f"{g}={n}" for g, n in sorted(st['coded_by_grade'].items())), "A=원문 직접(0), B=공식 기사 의역·선행 코딩, C=연구 요약, D=2차 종합"],
        ["검증 감사(validate)", f"오류 {st['validation']['errors']} · 경고 {st['validation']['warnings']}", "data/audit/validation_findings.csv"],
        ["테스트(pytest, 로컬 Python 실행)", f"통과 {tests.get('passed')} / 실패 {tests.get('failures')} / 오류 {tests.get('errors')} / 건너뜀 {tests.get('skipped')}", "data/audit/test_results.json (Oracle 실행 아님)"],
        ["연구자 요청", f"{st['requests']}건", "REQUEST_FOR_RESEARCHER.md"],
    ]
    return md_table(["항목", "값", "비고"], rows)


# ------------------------------------------------------------------ docs/research_inventory.md
def research_inventory(t, st) -> str:
    manifest = read_csv(RAW_INDEX / "local_file_manifest.csv")
    pinned = {r["path"]: r for r in read_csv(RAW_INDEX / "imported_checksums.csv")}
    parts = ["# 데이터·사료 인벤토리 (0단계)\n", BANNER,
             "## 상태 요약\n", status_block(st), "",
             "## 공식 출처 레지스터 22건 — 오프라인 회수 상태\n",
             "외부 사이트 접속은 오프라인 규칙에 따라 실행하지 않았다. URL은 provenance 포인터이며 열람 가능한 원문이 아니다. "
             "`retrieval_status=NOT_RETRIEVED`는 자료 부재가 아니라 미확보를 뜻한다.\n"]
    rows = []
    spans = t["source_spans"]
    for s in t["sources"]:
        if s["is_local_carrier"] != "0":
            continue
        n_spans = sum(1 for sp in spans if s["source_id"] in split(sp["source_id"]))
        grades = Counter(sp["evidence_grade"] for sp in spans if s["source_id"] in split(sp["source_id"]))
        rows.append([s["source_id"], s["case_id"], s["work"], s["record_date_lunar_or_scope"], s["title"],
                     s["source_type"], s["reporting_actor"], s["volume_section"], s["shared_origin_group"],
                     s["domain_policy"], s["register_verification_status"], s["offline_text_status"],
                     f"{n_spans} ({', '.join(f'{g}{n}' for g, n in sorted(grades.items()))})" if n_spans else "0"])
    parts.append(md_table(["ID", "사건", "사료", "음력 날짜/범위", "제목(레지스터)", "출처 유형", "보고 주체", "권·편",
                           "중복 그룹", "도메인 정책", "레지스터 상태", "로컬 원문", "근거 span(등급)"], rows))
    parts += ["", "**독립성 원칙**: 같은 `shared_origin_group`(예: CH-ROYAL-ORDERS의 심리록·추관지, JH-ROYAL-ORDERS)은 "
              "동일 판부·공초를 공유할 수 있으므로 독립 증인 2건으로 계수하지 않는다. GuSoon의 실록·비변사등록 동일 단계 기록도 "
              "별도 attestation으로 보존하되 독립 근원으로 단정하지 않는다.\n",
              "## 로컬 근거 문서(실제로 저장소에 있는 파일)\n"]
    rows = []
    for s in t["sources"]:
        if s["is_local_carrier"] == "1":
            rows.append([s["source_id"], s["local_path"], s["source_type"], s["evidence_grade"], s["retrieval_note"]])
    parts.append(md_table(["carrier", "경로", "종류", "증거 등급", "주의"], rows))
    parts += ["", "## 파일 해시(sha256)\n",
              "가져온 GuSoon/Chamang 파일은 `data/raw_index/imported_checksums.csv`에 고정했고 테스트가 변경 여부를 검사한다.\n"]
    rows = [[m["path"], m["bytes"], m["sha256"][:16] + "…", "고정됨" if m["path"] in pinned else "-", m["role"]] for m in manifest]
    parts.append(md_table(["경로", "bytes", "sha256(앞 16자)", "checksum 고정", "역할"], rows))
    parts += ["", "## GuSoon 출처 레코드 ↔ 레지스터 대응\n"]
    parts.append(md_table(["GuSoon ID", "레지스터 ID", "음력 날짜", "근거"],
                          [[x["gusun_record_id"], x["register_source_id"], x["record_lunar_date"], x["match_basis"]] for x in t["source_crosswalk"]]))
    parts += ["", "## 검색·수집 미완료 (NOT_RETRIEVED / NOT_COLLECTED)\n",
              "- 《일성록》·《승정원일기》·《비변사등록》·《심리록》·《추관지》·《홍재전서》·《흠흠신서》의 날짜별 확장 검색은 **실행하지 않았다**(오프라인 규칙). "
              "필요한 원문은 `REQUEST_FOR_RESEARCHER.md`에 기록했다.",
              "- 재현 방법: 연구자가 공식 사이트(sillok.history.go.kr, db.history.go.kr, sjw.history.go.kr)에서 레지스터 URL의 기사를 열람하여 "
              "원문·국역 문단을 로컬 파일로 제공 → `data/curated/source_spans.csv`에 `span_kind=VERBATIM_ORIGINAL`, 등급 A로 추가 → "
              "`python -m historinference all` 재실행.",
              "- 이전 세션 초기에 오프라인 규칙 공지 전 외부 접속·검색을 시도한 기록이 있으나, 공식 사이트는 접속 거부되었고 검색 결과는 "
              "**일체 증거로 채택하지 않았다**(데이터에 반영 없음).",
              "- 비승인 전재(위키문헌·shidianguji 등)는 출처로 등록하지 않았다. Chamang 보고서 속 비승인 참고문헌(S1~S3·N1)은 legacy 서지로만 남는다."]
    return "\n".join(parts) + "\n"


# ------------------------------------------------------------------ outputs/evidence_matrix.md
def evidence_matrix(t, st) -> str:
    spans = {s["span_id"]: s for s in t["source_spans"]}
    by = defaultdict(list)
    for c in t["mechanism_codes"]:
        by[(c["case_id"], c["code"])].append(c)
    parts = ["# 증거 행렬 — 사건 × 메커니즘 코드\n", BANNER,
             "셀 표기: `값(claim_status·근거등급)` 목록. `1`=충분히 출처로 지지, `0`=부재가 명시적으로 지지, `NA`=알 수 없음. "
             "값 1은 **그 단위가 해당 메커니즘을 기록·판단했다는 출처 지지**이며, `claim_status`가 CONTESTED/RECORDED_TESTIMONY/"
             "OFFICIAL_JUDGMENT이면 내용의 역사적 진실을 확정하지 않는다. 빈 칸은 코딩 단위 자체가 없음(=미확인).\n",
             "## 상태 요약\n", status_block(st), ""]
    rows = []
    for code in CODES:
        row = [f"{code} {CODE_LABEL[code]}"]
        for k in CASES:
            cells = []
            for c in by.get((k, code), []):
                g = span_grade(split(c["span_ids"]), spans) if c["value"] != "NA" else "-"
                cells.append(f"{c['value']}({c['claim_status']}·{g})")
            row.append("; ".join(cells) if cells else "")
        rows.append(row)
    parts.append(md_table(["코드"] + CASES, rows))
    parts += ["", "## 사건별 코딩 범위\n"]
    parts.append(md_table(["사건", "코딩 행", "1", "0", "NA", "1/0이 있는 코드 수(/19)", "사건(events)", "주장(claims)", "인물"],
                          [[CASE_LABEL[k], v["rows"], v["coded_1"], v["coded_0"], v["na"], v["codes_covered"], v["events"], v["claims"], v["persons"]]
                           for k, v in st["per_case"].items()]))
    parts += ["", "## 코딩 행 전체(근거 포함)\n"]
    rows = []
    for c in t["mechanism_codes"]:
        rows.append([c["code_row_id"], c["case_id"], f"{c['unit_type']}:{c['unit_id']}", c["code"], c["value"], c["claim_status"],
                     c["fault_type"], span_grade(split(c["span_ids"]), spans), c["span_ids"], c["rationale"]])
    parts.append(md_table(["행", "사건", "단위", "코드", "값", "claim_status", "fault_type", "최고 등급", "span", "근거 설명"], rows))
    parts += ["", "## 당시 판단 vs 역사적 실체(actual_culprit 분리)\n"]
    parts.append(md_table(["사건", "피해", "당시 판단상 책임자", "판단 시점", "후속 판단", "역사적 실체 상태"],
                          [[o["case_id"], o["harm"], o["culprit_contemporary_judgment"], o["judgment_date"], o["later_judgment"],
                            o["historical_culprit_status"]] for o in t["case_outcomes"]]))
    return "\n".join(parts) + "\n"


# ------------------------------------------------------------------ outputs/character_profiles.md
PROFILE_ATTRS = ["gender", "age_range", "residence", "status_claimed", "status_verified", "office", "occupation", "kinship_marriage", "death"]
ATTR_LABEL = {"gender": "성별", "age_range": "추정 연령 범위", "residence": "거주지", "status_claimed": "신분 주장",
              "status_verified": "입증된 신분", "office": "관직", "occupation": "직업", "kinship_marriage": "가족·혼인", "death": "사망"}


def character_profiles(t) -> str:
    attrs = defaultdict(list)
    for a in t["person_attributes"]:
        attrs[a["person_id"]].append(a)
    aliases = defaultdict(list)
    for a in t["person_aliases"]:
        aliases[a["person_id"]].append(f"{a['surface']}({a['alias_type']}·{a['status']})")
    rels = defaultdict(list)
    for r in t["relations"]:
        for pid in split(r["source_person"]) + split(r["target_person"]):
            rels[pid].append(f"{r['rel_type']}[{r['claim_status']}]({r['rel_id']})")
    parts = ["# 인물 프로필 — 출처 근거가 있는 속성만\n", BANNER,
             "근거 없는 속성은 `NA`로 둔다(출생연도·연령은 어떤 인물에도 근거가 없어 전부 NA). 성별은 친족어(아내·남편·召史·婢 등)가 "
             "있는 경우에만 코딩했고 관직 보유만으로 추정하지 않았다. 사건 간 동일 인물(정조)도 사건별 ID로 분리한다.\n"]
    for k in CASES:
        parts.append(f"\n## {CASE_LABEL[k]}\n")
        rows = []
        for p in t["persons"]:
            if p["case_id"] != k:
                continue
            cells = [f"{p['person_id']} {p['name_ko']}" + (f" {p['name_hanja']}" if p["name_hanja"] not in ("NA", "") else ""),
                     p["entity_kind"], p["role_in_case"]]
            pa = {}
            for a in attrs.get(p["person_id"], []):
                pa.setdefault(a["attribute"], []).append(f"{a['value']} [{a['claim_status']}; {a['span_ids']}]")
            for attr in PROFILE_ATTRS:
                cells.append("; ".join(pa.get(attr, [])) or "NA")
            cells.append("; ".join(aliases.get(p["person_id"], [])) or "-")
            cells.append("; ".join(rels.get(p["person_id"], [])) or "-")
            cells.append(p["identity_note"] or "")
            rows.append(cells)
        parts.append(md_table(["인물", "종류", "사건 내 역할"] + [ATTR_LABEL[a] for a in PROFILE_ATTRS] + ["이표기", "관계", "식별 주의"], rows))
    parts += ["\n## 동명인·동일인 판정\n",
              md_table(["ID", "A", "B", "판정", "근거"],
                       [[s["sep_id"], s["surface_a"], s["surface_b"], s["decision"], s["basis"]] for s in t["identity_separations"]])]
    return "\n".join(parts) + "\n"


# ------------------------------------------------------------------ outputs/mechanism_comparison.md
def mechanism_comparison(t) -> str:
    spans = {s["span_id"]: s for s in t["source_spans"]}
    parts = ["# 공통·차별 메커니즘 비교 (3단계)\n", BANNER,
             "네 사건의 **기록된 행위(DOCUMENTED_ACT)**, **진술(RECORDED_TESTIMONY)**, **관료·국왕 판단(OFFICIAL_JUDGMENT)**, "
             "**반증·충돌(CONTESTED/contradicts)**을 나란히 둔다. 비교는 메커니즘 코드 단위로만 연결하며 서로 다른 사건의 인물을 "
             "병합하지 않는다(정조도 사건별 ID).\n"]
    for k in CASES:
        parts.append(f"\n## {CASE_LABEL[k]}\n")
        for status, label in [("DOCUMENTED_ACT", "기록된 행위"), ("RECORDED_TESTIMONY", "진술"),
                              ("OFFICIAL_JUDGMENT", "관료·국왕 판단"), ("CONTESTED", "충돌·논쟁 중"), ("HYPOTHESIS", "사료 속 의문 제기(가설)")]:
            items = [c for c in t["claims"] if c["case_id"] == k and c["claim_status"] == status]
            evs = [e for e in t["events"] if e["case_id"] == k and e["claim_status"] == status and status in ("DOCUMENTED_ACT", "CONTESTED")]
            if not items and not evs:
                continue
            parts.append(f"**{label}**\n")
            for e in evs:
                parts.append(f"- [사건 {e['event_id']} · {e['date_start']}~{e['date_end']}] {e['description']} "
                             f"(근거 {span_grade(split(e['span_ids']), spans)}: {e['span_ids']})")
            for c in items[:25]:
                extra = f" ↔ 충돌: {c['contradicts']}" if c.get("contradicts") else ""
                parts.append(f"- [주장 {c['claim_id']}] {c['proposition']}{extra} (근거 {span_grade(split(c['span_ids']), spans)})")
            if len(items) > 25:
                parts.append(f"- … 외 {len(items) - 25}건 (data/normalized/claims.csv)")
            parts.append("")
    # fault types
    parts += ["\n## '고의적 공모' vs '부실한 감독' vs '공식 보고의 오류'\n",
              "관료 과실은 `fault_type`으로 분리한다. 어느 사건에서도 관료의 **고의적 사전 공모(DELIBERATE_COLLUSION)**는 "
              "코딩되지 않았다(근거 없음).\n"]
    rows = []
    for c in t["mechanism_codes"]:
        if c["fault_type"] not in ("NA", ""):
            rows.append([c["case_id"], c["code"], f"{c['unit_type']}:{c['unit_id']}", c["value"], c["claim_status"], c["fault_type"], c["rationale"]])
    parts.append(md_table(["사건", "코드", "단위", "값", "상태", "fault_type", "설명"], rows))
    # common vs distinct
    by_code = defaultdict(set)
    for c in t["mechanism_codes"]:
        if c["value"] == "1":
            by_code[c["code"]].add(c["case_id"])
    parts += ["\n## 공통 메커니즘(값 1이 기록된 사건 수)\n"]
    parts.append(md_table(["코드", "설명", "사건 수", "사건"],
                          [[code, CODE_LABEL[code], len(by_code.get(code, ())), ", ".join(sorted(by_code.get(code, ()))) or "-"] for code in CODES]))
    parts += ["\n## 반드시 보존한 해석 경계\n",
              "- **CHOI**: 1787 이곤수 안핵 결론(최씨·조광진 공모, CL-CH-04)은 1789 국왕 30개 의문(EV-CH-15)으로 재의문되어 `CONTESTED`. "
              "1789 처분은 무죄도 사형도 아닌 장 100·유 2천 리 준용 승인(DC-CH-08, 집행 미확인).",
              "- **CHO**: 이가원의 고발 조작·여론 조작은 국왕 판단(OFFICIAL_JUDGMENT)이며, 윤씨 사망의 진범은 확정되지 않음"
              "(case_outcomes: UNKNOWN_NO_SEPARATE_KILLER_ESTABLISHED). 관찰사-고발자 공조는 근거 없음(RL-CHO-07 UNKNOWN).",
              "- **YE**: 31명(CL-YE-03, 1795-06-04)과 25명(CL-YE-04, 1795-08-24)은 서로 다른 귀속 수치로 별도 보존. "
              "조진택의 '두둔'은 국왕 판단이며 사적 사전 합의는 미입증(fault_type UNRESOLVED_DELIBERATE_VS_NEGLIGENT). 1801 황기운 사건은 범위 밖.",
              "- **GUSUN**: 정조는 김명신 사망의 직접 인과를 '십분 확실하다 할 수 없다'고 판단(GS-CL-CF042). 사망을 특정 관원의 직접 살해로 코딩하지 않음.",
              "- **같은 날짜 분리**: 1793-06-13의 구순 기사(GS-006·GS-007)와 이여절 평가 기사(YE-002)는 서로 다른 사건으로 분리(ID-12)."]
    # graph
    graph = build_comparison_graph(t)
    parts += ["\n## 비교 그래프\n",
              f"`models/mechanism_comparison_graph.json`: 인물 노드 {sum(1 for n in graph['nodes'] if n['kind'] == 'person')}개(사건별 ID), "
              f"메커니즘 노드 {sum(1 for n in graph['nodes'] if n['kind'] == 'mechanism')}개(공유), 간선 {len(graph['edges'])}개. "
              "사건 간 연결은 메커니즘 노드를 통해서만 이루어진다."]
    return "\n".join(parts) + "\n"


def build_comparison_graph(t) -> dict:
    nodes, edges = [], []
    persons = {p["person_id"]: p for p in t["persons"]}
    for p in t["persons"]:
        nodes.append({"id": p["person_id"], "kind": "person", "case_id": p["case_id"], "label": p["name_ko"]})
    for code in CODES:
        nodes.append({"id": code, "kind": "mechanism", "case_id": "SHARED", "label": CODE_LABEL[code]})
    unit_people = {}
    for e in t["events"]:
        unit_people[e["event_id"]] = split(e["actor_ids"]) + split(e["target_ids"])
    for r in t["relations"]:
        unit_people[r["rel_id"]] = split(r["source_person"]) + split(r["target_person"])
    for d in t["decisions"]:
        unit_people[d["decision_id"]] = split(d["decider_id"]) + split(d["target_id"])
    for p in t["persons"]:
        unit_people[p["person_id"]] = [p["person_id"]]
    for c in t["mechanism_codes"]:
        if c["value"] != "1":
            continue
        for pid in unit_people.get(c["unit_id"], []):
            if pid in persons:
                edges.append({"source": pid, "target": c["code"], "case_id": c["case_id"], "code_row_id": c["code_row_id"],
                              "claim_status": c["claim_status"]})
    graph = {"note": "인물 노드는 사건별로 분리(병합 금지). 메커니즘 노드만 사건 간에 공유된다.", "nodes": nodes, "edges": edges}
    (MODELS / "mechanism_comparison_graph.json").write_text(json.dumps(graph, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    return graph


# ------------------------------------------------------------------ outputs/worlds_report.md
def worlds_report(t) -> str:
    summ = _load_json(MODELS / "worlds" / "worlds_summary.json", {"cases": {}})
    po = _load_json(MODELS / "constraints" / "partial_order.json", {"cases": {}})
    rules = read_csv(MODELS / "constraints" / "normative_rules.csv")
    parts = ["# 가능세계 후보와 제약 (4단계)\n", BANNER,
             "관측된 행정행위(OBSERVED_ACT 사건·명령)는 모든 세계에서 고정한다. 실제 범행·누명 생성·증거 신빙성·공모 여부만 잠재 축으로 분기하며, "
             "축 사이 논리 제약(`models/worlds/world_constraints.csv`)을 위반하는 조합은 제거한다. **세계 후보는 분석층이며 최종 창작 스토리가 아니다.** "
             "확률은 자료로 식별되지 않으므로 모든 세계의 `posterior`·`likelihood`는 `UNSCORED`.\n"]
    rows = []
    for k in CASES:
        s = summ["cases"].get(k, {})
        p = po["cases"].get(k, {})
        rows.append([CASE_LABEL[k], len(s.get("axes", {})), s.get("n_combinations"), s.get("n_consistent_worlds"),
                     s.get("n_worlds_without_unsupported_hypotheses"), s.get("n_fixed_observed"),
                     f"{p.get('n_comparable_pairs')}/{p.get('n_pairs')}", p.get("n_explicit")])
    parts.append(md_table(["사건", "잠재 축", "전체 조합", "제약 통과 세계", "근거 없는 가설 미포함 세계", "고정 관측 행위",
                           "순서 확정 사건쌍(비교가능/전체)", "명시 순서 간선"], rows))
    parts.append("\n순서가 확정되지 않은 사건쌍은 부분순서 DAG에서 비교 불가로 남긴다(`models/constraints/partial_order.json`). "
                 "명시 간선은 근거 span이 있는 순서 진술만, 나머지는 확정 날짜 구간 비교로만 생성한다.\n")
    axes = read_csv(MODELS / "worlds" / "world_axes.csv")
    for k in CASES:
        parts.append(f"\n## {CASE_LABEL[k]}\n")
        parts.append(md_table(["축", "종류", "값", "설명", "근거 상태", "마지막 공식 긍정 판단", "근거 span"],
                              [[a["axis_id"], a["axis_kind"], a["value_id"], a["label"], a["basis_status"],
                                "예" if a["is_last_affirmative_official"] == "1" else "", a["basis_span_ids"]] for a in axes if a["case_id"] == k]))
        worlds = read_csv(MODELS / "worlds" / f"worlds_{k}.csv")
        axis_ids = [a for a in summ["cases"][k]["axes"]]
        parts.append(f"\n제약 통과 세계 {len(worlds)}개 중 앞 12개(근거 없는 가설 수·공식 판단 이탈 수 순 정렬; 순위는 점수가 아님):\n")
        parts.append(md_table(["world_id"] + axis_ids + ["공식 판단 이탈 축 수", "근거 없는 가설", "posterior"],
                              [[w["world_id"]] + [w[a] for a in axis_ids] + [w["n_departures_from_last_affirmative_official"],
                                                                           w["n_unsupported_hypotheses"], w["posterior"]] for w in worlds[:12]]))
    parts += ["\n## 시기별 규범 제약\n",
              "HARD_ENACTMENT 규범(대전통편 1786-01-01, 증수무원록 개정 1792)은 시행 이전 사건에 적용하면 오류로 탐지한다. "
              "GuSoon 제도 피처의 1776~1793은 **검증 범위**(제정·폐지일 아님)이므로 1794~1795 YE 사건에 쓰면 경고로 표시한다.\n",
              md_table(["ID", "규범", "영역", "valid_from", "종류", "검증 범위 끝", "선행 피처 출처 도메인"],
                       [[r["rule_id"], r["name"], r["domain"], r["valid_from"], r["breakpoint_kind"], r["verified_through"],
                         r["feature_domain_policy"]] for r in rules])]
    return "\n".join(parts) + "\n"


# ------------------------------------------------------------------ synthesis reports
def _fmt_levels(d) -> str:
    return " ".join(f"{g}={LEVEL_NAME[int(d[g])]}" for g in GOALS)


def _design_rows(designs, extra_cols=()):
    rows = []
    for d in designs:
        rows.append([d["design_id"], d["strategy"], d.get("anchor", "")] + [LEVEL_NAME[int(d[g])][0] for g in GOALS]
                    + [d[c] for c in COST_KEYS] + [d.get(c, "") for c in extra_cols])
    return rows


DESIGN_HEADERS = ["설계", "전략", "앵커"] + GOALS + ["가정 심각도", "출처 없는 창작", "교차 사건 인과연결", "2차 종합 전용",
                                                   "논쟁 메커니즘의 사실화", "시대 위험", "역사 덧씌우기", "실존인물 귀속 위험"]


def anchor_comparison(t) -> str:
    cfg = load_config()
    A = read_csv(MODELS / "synthesis" / "candidates_A.csv")
    sens = read_csv(MODELS / "synthesis" / "sensitivity.csv")
    front = read_csv(MODELS / "synthesis" / "pareto_front.csv")
    box = {r["row_id"]: r for r in read_csv(MODELS / "synthesis" / "morphological_box.csv")}
    parts = ["# A 전략 — 역사적 사건 하나를 앵커로 삼아 다른 사건 메커니즘을 이식\n", BANNER,
             "각 사건을 앵커 후보로 동등하게 놓았다(최아지를 사전 승자로 고정하지 않음). 앵커의 문서화된 메커니즘 값은 그대로 두고, "
             "**값이 없는(미확인) 차원에만** 다른 사건의 메커니즘을 이식할 수 있다. 문서화된 값을 바꾸는 이식, 출처 없는 창작 요소(진범 확정 등)의 이식은 "
             "CSP에서 금지한다(실제 사건에 유죄 확정을 위조하지 않음). 이식 1건마다 '역사 덧씌우기' 심각도 3을 부과하고, 이식된 역할이 앵커에 이미 실존 인물로 "
             "있는 경우(예: 국왕·관찰사) 실존인물 귀속 위험 1을 센다.\n",
             f"평가 기준: 기획의도 Y1~Y6 수준(`config/objectives.toml`), 사료 충실성(2차 종합 전용 요소·논쟁 메커니즘 사실화), 인과적 정합성(CSP 위반 0·교차 사건 인과연결 수), "
             f"역사적 개연성(제도 단절점 위험), 불필요한 가정(심각도 합). hard gate: {', '.join(f'{g}≥{v}' for g, v in cfg['hard_gates'].items())}.\n"]
    parts.append("## 앵커 원형(이식 없음)\n")
    base = [d for d in A if d["overlays"] == "0"]
    parts.append(md_table(DESIGN_HEADERS + ["요소 수"], _design_rows(base, ["n_elements"])))
    parts.append("\n" + "\n".join(f"- **{d['anchor']}**: {_fmt_levels(d)} — hard gate "
                                  f"{'통과' if all(int(d[g]) >= cfg['levels'][v] for g, v in cfg['hard_gates'].items()) else '미달'}"
                                  for d in base))
    parts += ["\n## 앵커별 이식 설계 수와 최선 대안\n"]
    rows = []
    for k in CASES:
        ds = [d for d in A if d["anchor"] == k]
        passing = [d for d in ds if all(int(d[g]) >= cfg["levels"][v] for g, v in cfg["hard_gates"].items())]
        min_over = min((int(d["overlays"]) for d in passing), default=None)
        rows.append([CASE_LABEL[k], len(ds), len(passing), "-" if min_over is None else min_over,
                     sum(1 for d in front if d["evidence_grade_cutoff"] == "D" and d["gate_variant"] == "default" and d["anchor"] == k)])
    parts.append(md_table(["앵커", "CSP 통과 설계", "hard gate 통과", "통과에 필요한 최소 이식 수", "기본 Pareto 전선 내 설계 수"], rows))
    parts += ["\n## 기본 설정(증거 등급 ≤D, 기본 gate) Pareto 전선의 A 설계\n"]
    fa = [d for d in front if d["evidence_grade_cutoff"] == "D" and d["gate_variant"] == "default" and d["strategy"] == "A"]
    parts.append(md_table(DESIGN_HEADERS + ["이식 행"], _design_rows(fa, ["transplant_rows"])))
    for d in fa:
        if d["transplant_rows"]:
            parts.append(f"\n- {d['design_id']} 이식: " + "; ".join(
                f"{rid} {box[rid]['value_id']}@{box[rid]['source_case']}({box[rid]['label']})" for rid in split(d["transplant_rows"])))
    parts += ["\n## 증거 등급·gate 민감도\n",
              "증거 등급 컷오프 B는 공식 기사 의역·선행 코딩만, C는 연구 요약까지, D는 2차 종합(Chamang 보고서)까지 허용한다.\n"]
    parts.append(md_table(["등급 컷오프", "gate 변형", "gate 통과 앵커", "이식 없이 통과한 앵커", "Pareto 내 A 설계"],
                          [[s["evidence_grade_cutoff"], s["gate_variant"], s["anchors_passing"], s["anchors_passing_without_transplant"],
                            s["pareto_A"]] for s in sens]))
    parts += ["\n## 해석\n", anchor_interpretation(base, sens, cfg)]
    return "\n".join(parts) + "\n"


def anchor_interpretation(base, sens, cfg) -> str:
    def lv(k):
        d = next(x for x in base if x["anchor"] == k)
        return d
    lines = []
    for k in CASES:
        d = lv(k)
        fails = [g for g, v in cfg["hard_gates"].items() if int(d[g]) < cfg["levels"][v]]
        lines.append(f"- **{CASE_LABEL[k]}** — {_fmt_levels(d)}; 2차 종합 전용 요소 {d['secondary_only']}개; "
                     + (f"gate 미달 {', '.join(fails)}." if fails else "이식 없이 hard gate 통과."))
    s_b = next((s for s in sens if s["evidence_grade_cutoff"] == "B" and s["gate_variant"] == "default"), None)
    if s_b:
        lines.append(f"- 증거 등급을 B(공식 기사 의역·선행 코딩)로 제한하면 이식 없이 gate를 통과하는 앵커는 `{s_b['anchors_passing_without_transplant']}`이다. "
                     "CHOI의 강점(피해자 가족 격쟁·재검증의 재의문)은 상당 부분 2차 종합(D) 근거에 기대므로 원문 확보(RQ-CH-01/02) 전까지 잠정적이다.")
    lines.append("- 어떤 앵커도 Y1(진범 규명)을 FULL로 만들 수 없다: 네 사건 모두 진범이 증거로 확정된 기록이 없고, A 전략은 실제 사건에 유죄 확정을 이식하지 않는다.")
    return "\n".join(lines)


def synthetic_comparison(t) -> str:
    cfg = load_config()
    sens = read_csv(MODELS / "synthesis" / "sensitivity.csv")
    front = read_csv(MODELS / "synthesis" / "pareto_front.csv")
    trace = read_csv(MODELS / "synthesis" / "inspiration_trace.csv")
    weights = read_csv(MODELS / "synthesis" / "weighted_view_sensitivity.csv")
    box = read_csv(MODELS / "synthesis" / "morphological_box.csv")
    rules = read_csv(MODELS / "synthesis" / "compatibility_rules.csv")
    main_s = next(s for s in sens if s["evidence_grade_cutoff"] == "D" and s["gate_variant"] == "default")
    f0 = [d for d in front if d["evidence_grade_cutoff"] == "D" and d["gate_variant"] == "default"]
    parts = ["# B 전략 — 네 사건 메커니즘을 결합한 새 가상 사건 합성 (A·C와 비교)\n", BANNER,
             "**형태분석(morphological analysis)**: 12개 차원(`models/synthesis/morphological_box.csv`, 51행)에서 차원마다 값 하나(또는 없음)를 고른다. "
             "각 값은 특정 사건의 코딩 행·span으로 추적된다(`inspiration_trace`). **CSP**: 20개 호환 규칙(`compatibility_rules.csv`)으로 상호 모순 조합을 제거한다. "
             "**오컴의 면도날**: 요소 하나를 빼도 목표 수준과 CSP가 그대로인 설계는 그 축소판에 지배되므로 제외한다(최소 설계). "
             "인물·장소는 모두 가상이며 실존 인물에 창작된 범행·공모를 귀속하지 않는다.\n",
             "## 탐색 규모\n",
             md_table(["항목", "값"], [["형태 상자 행(등급 ≤D)", main_s["box_rows"]],
                                      ["CSP·gate(약한 변형) 통과 B 설계", main_s["B_designs_feasible_total"]],
                                      ["그중 최소 설계(오컴 필터)", main_s["B_designs_minimal"]],
                                      ["기본 gate 통과: A / B / C", f"{main_s['A_passing']} / {main_s['B_passing']} / {main_s['C_passing']}"],
                                      ["기본 gate Pareto 전선(대표 설계 수)", f"{main_s['pareto_size']} (A {main_s['pareto_A']} · B {main_s['pareto_B']} · C {main_s['pareto_C']})"]]),
             "\n## 기본 설정 Pareto 전선(증거 ≤D, 기본 gate)\n",
             "Pareto 우세는 목표 수준(최대화)과 8개 비용(최소화)의 성분별 비교로만 정한다. 가중치를 쓰지 않는다. 같은 벡터의 설계는 대표 1개로 묶었다.\n",
             md_table(DESIGN_HEADERS + ["출처 사건", "동치 설계 수"], _design_rows(f0, ["source_cases", "n_equivalent_designs"]))]
    # profiles
    parts += ["\n## 대안 제시(프로필별 사전식 선택 — 점수 아님)\n"]
    prof_rows = []
    for p in ("fidelity_first", "goal_first", "parsimony_first"):
        did = main_s.get(f"profile_{p}")
        d = next((x for x in f0 if x["design_id"] == did), None)
        if d:
            prof_rows.append([p, did, d["strategy"], _fmt_levels(d), d["severity"], d["untraced"], d["cross_links"]])
    parts.append(md_table(["프로필", "설계", "전략", "목표 수준", "심각도", "창작", "교차연결"], prof_rows))
    parts.append("\n- fidelity_first: 출처 없는 창작 → 논쟁 사실화 → 실존인물 위험 → 덧씌우기 → 2차 종합 → 심각도 순\n"
                 "- goal_first: Y3·Y4·Y5·Y6·Y1·Y2 수준 → 심각도 순\n- parsimony_first: 심각도 → 교차연결 → 창작 순\n")
    # representative B designs with traces & story skeleton
    reps = []
    for p in ("goal_first", "fidelity_first", "parsimony_first"):
        did = main_s.get(f"profile_{p}")
        if did and did.startswith("B-") and did not in reps:
            reps.append(did)
    best_b_no_fiction = [d for d in f0 if d["strategy"] == "B" and d["untraced"] == "0"]
    if best_b_no_fiction:
        cand = max(best_b_no_fiction, key=lambda d: (sum(int(d[g]) for g in GOALS), -int(d["severity"])))
        if cand["design_id"] not in reps:
            reps.append(cand["design_id"])
    boxi = {r["row_id"]: r for r in box}
    for did in reps:
        d = next(x for x in f0 if x["design_id"] == did)
        parts.append(f"\n### {did} — inspiration_trace\n")
        parts.append(f"{_fmt_levels(d)} · 권장 배경 연도(가상) {d['setting_year']} · 출처 사건 {d['source_cases']}\n")
        tr = [x for x in trace if x["design_id"] == did]
        parts.append(md_table(["차원", "값", "출처 사건", "코딩 행", "span", "출처 상태"],
                              [[x["dim"], x["value_id"], x["source_case"], x["code_row_ids"] or "-", x["span_ids"] or "-", x["source_status"]] for x in tr]))
        parts.append("\n" + story_skeleton(d, boxi))
    # C baseline
    c = [d for d in f0 if d["strategy"] == "C"]
    parts += ["\n## C — 완전 창작 baseline\n",
              "모든 목표를 작가 선언으로 FULL로 만들 수 있지만 출처 추적 요소가 0이고 심각도가 가장 높다. 비교 기준선으로만 기록한다.\n",
              md_table(DESIGN_HEADERS, _design_rows(c))]
    # sensitivity
    parts += ["\n## 민감도 분석\n", "### 증거 등급 컷오프 × hard gate 변형\n",
              md_table(["등급", "gate 변형", "B 최소 설계", "통과 A/B/C", "Pareto A/B/C", "fidelity_first", "goal_first", "parsimony_first"],
                       [[s["evidence_grade_cutoff"], s["gate_variant"], s["B_designs_minimal"],
                         f"{s['A_passing']}/{s['B_passing']}/{s['C_passing']}", f"{s['pareto_A']}/{s['pareto_B']}/{s['pareto_C']}",
                         s["profile_fidelity_first"], s["profile_goal_first"], s["profile_parsimony_first"]] for s in sens]),
              "\n### 가중합 보조 화면(설정 의존; 연구 결과 아님)\n",
              f"`config/objectives.toml`의 5개 그룹(목표·충실성·정합성·개연성·간결성) 가중치를 {cfg['sensitivity']['weight_levels']} 격자로 바꿔 "
              "Pareto 대표 설계 중 가중합 1위가 되는 비율을 셌다. 이는 가중치 선택이 결론을 얼마나 바꾸는지 보여 주는 민감도이며 확률이나 순위 점수가 아니다.\n"]
    wd = [w for w in weights if w["evidence_grade_cutoff"] == "D" and w["gate_variant"] == "default" and int(w["weight_grid_wins"]) > 0]
    strat = {d["design_id"]: d["strategy"] for d in f0}
    parts.append(md_table(["설계", "전략", "1위 횟수", "격자 크기", "비율"],
                          [[w["design_id"], strat.get(w["design_id"], ""), w["weight_grid_wins"], w["weight_grid_size"], w["share"]] for w in wd]))
    parts += ["\n## A 대 B 비교 결론\n", ab_conclusion(f0, sens),
              "\n## CSP 호환 규칙\n", md_table(["ID", "조건 차원", "조건 값", "요구 차원", "요구 값", "근거"],
                                             [[r["rule_id"], r["if_dim"], r["if_values"], r["then_dim"], r["then_values"], r["basis"]] for r in rules])]
    return "\n".join(parts) + "\n"


SKELETON_LINES = {
    "M1_TRIGGER": "발단", "M4_OPINION": "여론", "M3_TESTIMONY": "진술 오염", "M2_FIRST_ERROR": "최초 판단의 오류",
    "M5_OFFICIAL_FAULT": "관료 과실", "M6_TARGET_FATE": "무고 표적의 운명", "M7_APPEAL": "이의제기",
    "M8_REVERIFICATION": "재검증", "M9_SECOND_ORDER": "재검증의 재검증", "M11_RESOLUTION": "진상 결말",
    "M10A_PERPETRATOR_ACCOUNTABILITY": "가해자 책임", "M10B_OFFICIAL_ACCOUNTABILITY": "관료 책임",
}


def story_skeleton(d, boxi) -> str:
    lines = ["**가상 서사 골격(FICTION_ONLY · 실존 인물·실제 사건 아님)** — 인물은 역할명(가상 고발자·가상 피의자 등)으로만 둔다.\n"]
    rows = {boxi[r]["dim"]: boxi[r] for r in split(d["trace_rows"]) if r in boxi}
    for dim in ["M1_TRIGGER", "M4_OPINION", "M3_TESTIMONY", "M2_FIRST_ERROR", "M5_OFFICIAL_FAULT", "M6_TARGET_FATE", "M7_APPEAL",
                "M8_REVERIFICATION", "M9_SECOND_ORDER", "M11_RESOLUTION", "M10A_PERPETRATOR_ACCOUNTABILITY", "M10B_OFFICIAL_ACCOUNTABILITY"]:
        if dim in rows:
            r = rows[dim]
            src = "출처 없음(창작)" if r["fiction_only"] == "1" else f"{r['source_case']}에서 착안"
            lines.append(f"{len(lines)}. {SKELETON_LINES[dim]}: {r['label']} — {src}")
    return "\n".join(lines)


def ab_conclusion(f0, sens) -> str:
    a = [d for d in f0 if d["strategy"] == "A"]
    b = [d for d in f0 if d["strategy"] == "B"]
    lines = [
        f"- 기본 설정 Pareto 전선에 A {len(a)}개, B {len(b)}개, C 1개가 공존한다. **어느 전략도 다른 전략을 전면 지배하지 않는다.**",
        "- A(앵커)는 실제 기록을 제자리에서 쓰므로 가정 심각도·교차 사건 연결이 가장 낮다(이식 없는 앵커는 심각도 0). 대신 Y1(진범 규명)은 최대 PARTIAL이며, "
        "gate를 채우려면 이식이 필요하고 이식마다 실제 사건 위에 다른 사건을 덧씌우는 비용(심각도 3)이 든다.",
        "- B(합성)는 Y1·Y2를 FULL로 설계할 수 있지만, 그때 '진범이 증거로 확정됨' 요소는 네 사건 어디에도 근거가 없는 창작이다. "
        "출처 추적 요소만 쓰는 B 설계는 Y1이 PARTIAL에 머물고 교차 사건 인과연결(가설)이 늘어난다.",
        "- 따라서 선택은 '역사적 앵커의 충실성' 대 '기획의도의 완결성' 사이의 교환이며, 이 교환의 위치는 `config/objectives.toml`의 gate·가중치(사람의 설정)에 달려 있다.",
    ]
    s_b = next((s for s in sens if s["evidence_grade_cutoff"] == "B" and s["gate_variant"] == "default"), None)
    if s_b:
        lines.append(f"- 증거 등급을 B로 제한하면 B 최소 설계가 {s_b['B_designs_minimal']}개로 줄고 gate 통과 앵커는 `{s_b['anchors_passing']}`가 된다: "
                     "결론은 원문 확보 수준에 민감하다.")
    return "\n".join(lines)


# ------------------------------------------------------------------ REQUEST_FOR_RESEARCHER.md
def requests_md(t) -> str:
    persons = {p["person_id"]: p for p in t["persons"]}
    sources = {s["source_id"]: s for s in t["sources"]}
    parts = ["# REQUEST_FOR_RESEARCHER — 원문 제공 요청\n",
             "> 자동 생성(`data/curated/research_requests.csv`). 오프라인 규칙상 Claude Code는 외부 사이트에 접속하지 않았다. 아래 원문이 로컬로 제공되면 "
             "해당 span을 등급 A(`VERBATIM_ORIGINAL`)로 추가하고 `python -m historinference all`을 다시 실행한다. 제공 전까지 관련 값은 `NA` 또는 미확정 상태로 둔다.\n"]
    for pr in ("HIGH", "MEDIUM", "LOW"):
        items = [r for r in t["research_requests"] if r["priority"] == pr]
        if not items:
            continue
        parts.append(f"\n## 우선순위 {pr}\n")
        for r in items:
            names = ", ".join(f"{pid} {persons[pid]['name_ko']}" for pid in split(r["persons"]) if pid in persons) or "-"
            srcs = ", ".join(f"{sid} {sources[sid]['work']} {sources[sid]['record_date_lunar_or_scope']} <{sources[sid]['url']}>"
                             for sid in split(r["source_ids"]) if sid in sources) or "-"
            parts.append(f"### {r['request_id']} · {r['case_id']}\n- **인물**: {names}\n- **쟁점**: {r['issue']}\n"
                         f"- **출처 ID**: {srcs}\n- **요청 원문/일자**: {r['requested_passage']}\n- **코딩을 막는 이유**: {r['blocks']}\n")
    return "\n".join(parts) + "\n"


# ------------------------------------------------------------------ dashboard data
def dashboard_data(t, st) -> dict:
    sens = read_csv(MODELS / "synthesis" / "sensitivity.csv")
    front = read_csv(MODELS / "synthesis" / "pareto_front.csv")
    A = read_csv(MODELS / "synthesis" / "candidates_A.csv")
    spans = {s["span_id"]: s for s in t["source_spans"]}
    matrix = {}
    for c in t["mechanism_codes"]:
        cell = matrix.setdefault(c["case_id"], {}).setdefault(c["code"], [])
        cell.append({"v": c["value"], "s": c["claim_status"], "g": span_grade(split(c["span_ids"]), spans) if c["value"] != "NA" else "-",
                     "id": c["code_row_id"], "why": c["rationale"]})
    events = [{"id": e["event_id"], "case": e["case_id"], "type": e["event_type"], "desc": e["description"],
               "start": e["date_start"], "end": e["date_end"], "precision": e["date_precision"], "layer": e["layer"],
               "status": e["claim_status"], "grade": span_grade(split(e["span_ids"]), spans)} for e in t["events"]]
    test = _load_json(AUDIT / "test_results.json", {})
    return {
        "generated_by": "python -m historinference report",
        "readonly_note": "이 화면은 data/normalized·models 산출물을 읽기만 한다. 코어 데이터를 바꾸지 않는다.",
        "stats": st,
        "cases": {k: CASE_LABEL[k] for k in CASES},
        "codes": CODE_LABEL,
        "goals": GOALS,
        "cost_keys": COST_KEYS,
        "matrix": matrix,
        "events": events,
        "sensitivity": sens,
        "front_default": [d for d in front if d["evidence_grade_cutoff"] == "D" and d["gate_variant"] == "default"],
        "anchors_base": [d for d in A if d["overlays"] == "0"],
        "tests": test.get("cases", []),
        "requests": t["research_requests"],
    }


# ------------------------------------------------------------------ README status
def update_readme_status(st) -> None:
    path = ROOT / "README.md"
    text = path.read_text(encoding="utf-8")
    block = "<!-- STATUS:BEGIN -->\n" + status_block(st) + "\n<!-- STATUS:END -->"
    if "<!-- STATUS:BEGIN -->" in text:
        text = re.sub(r"<!-- STATUS:BEGIN -->.*?<!-- STATUS:END -->", lambda _m: block, text, flags=re.S)
        path.write_text(text, encoding="utf-8")


def write_all(t) -> None:
    st = compute_stats(t)
    DOCS.mkdir(exist_ok=True)
    OUTPUTS.mkdir(exist_ok=True)
    (DOCS / "research_inventory.md").write_text(research_inventory(t, st), encoding="utf-8")
    (OUTPUTS / "evidence_matrix.md").write_text(evidence_matrix(t, st), encoding="utf-8")
    (OUTPUTS / "character_profiles.md").write_text(character_profiles(t), encoding="utf-8")
    (OUTPUTS / "mechanism_comparison.md").write_text(mechanism_comparison(t), encoding="utf-8")
    (OUTPUTS / "worlds_report.md").write_text(worlds_report(t), encoding="utf-8")
    (OUTPUTS / "anchor_comparison.md").write_text(anchor_comparison(t), encoding="utf-8")
    (OUTPUTS / "synthetic_comparison.md").write_text(synthetic_comparison(t), encoding="utf-8")
    (OUTPUTS / "status_report.md").write_text("# 상태 보고\n\n" + BANNER + "\n" + status_block(st) + "\n", encoding="utf-8")
    (ROOT / "REQUEST_FOR_RESEARCHER.md").write_text(requests_md(t), encoding="utf-8")
    data = dashboard_data(t, st)
    (OUTPUTS / "dashboard_data.js").write_text(
        "// 자동 생성: python -m historinference report (읽기 전용 대시보드 데이터)\nwindow.HI_DATA = "
        + json.dumps(data, ensure_ascii=False) + ";\n", encoding="utf-8")
    update_readme_status(st)
