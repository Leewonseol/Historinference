"""Step 0-1: build the inventory-backed normalized tables.

Inputs (all local):
  research/source_register.csv            official source locators (22 rows)
  research/imported/gusun/*.csv           prior GuSoon coded data (read-only)
  data/curated/*.csv                      hand-coded tables for this project

Outputs: data/normalized/<table>.csv (+ .parquet when duckdb is installed),
data/raw_index/local_file_manifest.csv (sha256 of every local evidence file).
"""

from __future__ import annotations

from urllib.parse import urlparse

from . import io
from .io import CURATED, NORMALIZED, RAW_INDEX, RESEARCH, ROOT, read_csv, split, write_csv

GUSUN_DIR = RESEARCH / "imported" / "gusun"
CHAMANG_DIR = RESEARCH / "imported" / "chamang"

APPROVED_PRIMARY_DOMAINS = {"sillok.history.go.kr", "db.history.go.kr", "sjw.history.go.kr"}
APPROVED_INSTITUTIONAL_HOLDINGS = {"jsg.aks.ac.kr"}
FORBIDDEN_DOMAINS = {"wikisource.org", "zh.wikisource.org", "ko.wikisource.org", "shidianguji.com", "www.shidianguji.com"}

GRADE_ORDER = {"A": 0, "B": 1, "C": 2, "D": 3, "CONTEXT": 4, "X": 9}

# GuSoon 01_confirmed_facts: who is speaking in each fact (read from the
# statement wording; kept explicit so the import is auditable).
GUSUN_FACT_SPEAKERS = {
    **{f"CF{n:03d}": "GUSUN-P04" for n in range(1, 7)},       # 명업
    **{f"CF{n:03d}": "GUSUN-P06" for n in range(7, 13)},      # 이진욱
    **{f"CF{n:03d}": "GUSUN-P12" for n in range(13, 18)},     # 자미덕
    "CF018": "GUSUN-P07", "CF019": "GUSUN-P07",                # 한재욱
    "CF020": "GUSUN-P15",                                       # 유제희
    "CF021": "GUSUN-P06", "CF022": "SOURCE_TEXT", "CF023": "GUSUN-P06",
    "CF024": "GUSUN-P08",                                       # 조계완
    **{f"CF{n:03d}": "GUSUN-P18" for n in range(25, 29)},     # 이형원
    "CF029": "GUSUN-P20",                                       # 윤노동
    "CF030": "GUSUN-K", "CF031": "GUSUN-K",
    "CF032": "GUSUN-P19",                                       # 이조원
    "CF033": "GUSUN-K", "CF034": "GUSUN-K", "CF035": "GUSUN-K",
    "CF036": "GUSUN-K",                                         # 비변사 청 → 정조 윤허
    "CF037": "GUSUN-P21", "CF038": "GUSUN-P21",                # 홍대협
    "CF039": "GUSUN-K", "CF040": "GUSUN-P21|GUSUN-K",
    **{f"CF{n:03d}": "GUSUN-K" for n in range(41, 45)},
    "CF045": "GUSUN-P21|GUSUN-K",
    **{f"CF{n:03d}": "GUSUN-K" for n in range(46, 51)},
}

GUSUN_LEVEL_TO_STATUS = {
    "RECORDED_TESTIMONY": "RECORDED_TESTIMONY",
    "RECORDED_NESTED_TESTIMONY": "RECORDED_TESTIMONY",
    "DOCUMENTED_SOURCE_IDENTIFICATION": "DOCUMENTED_ACT",
    "DOCUMENTED_OFFICIAL_EVALUATION": "OFFICIAL_JUDGMENT",
    "DOCUMENTED_OFFICIAL_REPORT": "OFFICIAL_JUDGMENT",
    "DOCUMENTED_INSPECTOR_REPORT": "OFFICIAL_JUDGMENT",
    "DOCUMENTED_ROYAL_JUDGMENT": "OFFICIAL_JUDGMENT",
    "DOCUMENTED_ROYAL_JUDGMENT_AND_ORDER": "DOCUMENTED_ACT",
    "DOCUMENTED_ROYAL_ORDER": "DOCUMENTED_ACT",
    "DOCUMENTED_COURT_ACTION": "DOCUMENTED_ACT",
    "DOCUMENTED_OFFICIAL_ACTION": "DOCUMENTED_ACT",
    "DOCUMENTED_OFFICIAL_FINDING": "OFFICIAL_JUDGMENT",
    "DOCUMENTED_OFFICIAL_AND_ROYAL_JUDGMENT": "OFFICIAL_JUDGMENT",
}

GUSUN_CONFLICT_GROUPS = {
    "CF030": "CG-GS-THEFT", "CF032": "CG-GS-THEFT", "CF038": "CG-GS-THEFT", "CF039": "CG-GS-THEFT",
    "CF027": "CG-GS-DEATH", "CF029": "CG-GS-DEATH", "CF040": "CG-GS-DEATH", "CF042": "CG-GS-DEATH",
    "CF016": "CG-GS-COACHING", "CF017": "CG-GS-COACHING", "CF018": "CG-GS-COACHING",
    "CF010": "CG-GS-IRON", "CF044": "CG-GS-IRON",
}

ATT_MODE_FROM_STATUS = {
    "RECORDED_TESTIMONY": "TESTIMONY",
    "OFFICIAL_JUDGMENT": "OFFICIAL_REPORT_OR_JUDGMENT",
    "DOCUMENTED_ACT": "ROYAL_ORDER_OR_RECORD",
}

CURATED_TABLES = [
    "cases", "persons", "person_aliases", "person_attributes", "identity_separations",
    "institutions", "events", "event_order", "attestations", "claims", "evidence_items",
    "relations", "decisions", "mechanism_codes", "case_outcomes", "episodes", "research_requests",
]


def domain_of(url: str) -> str:
    if not url:
        return ""
    return urlparse(url).netloc.lower()


def domain_policy(url: str) -> str:
    dom = domain_of(url)
    if not dom:
        return "NO_URL"
    if any(dom == f or dom.endswith("." + f) for f in FORBIDDEN_DOMAINS):
        return "FORBIDDEN_UNVERIFIED_REDISTRIBUTION"
    if dom in APPROVED_PRIMARY_DOMAINS:
        return "APPROVED_OFFICIAL_PRIMARY"
    if dom in APPROVED_INSTITUTIONAL_HOLDINGS:
        return "APPROVED_INSTITUTIONAL_HOLDING"
    return "NOT_APPROVED_CONTEXT_ONLY"


# ---------------------------------------------------------------- sources
def build_sources() -> list[dict]:
    register = read_csv(RESEARCH / "source_register.csv")
    annotations = {r["source_id"]: r for r in read_csv(CURATED / "source_annotations.csv")}
    local_docs = read_csv(CURATED / "local_documents.csv")
    rows = []
    for r in register:
        ann = annotations.get(r["source_id"], {})
        rows.append({
            "source_id": r["source_id"],
            "case_id": r["case_id"],
            "work": r["work"],
            "title": r["title"],
            "record_date_lunar_or_scope": r["source_date_lunar_or_scope"],
            "calendar": "LUNAR" if r["source_date_lunar_or_scope"][:1].isdigit() else "UNKNOWN",
            "source_type": ann.get("source_type", "UNKNOWN"),
            "reporting_actor": ann.get("reporting_actor", "NA"),
            "volume_section": ann.get("volume_section", "NA"),
            "volume_basis": ann.get("volume_basis", "NA"),
            "url": r["url"],
            "url_domain": domain_of(r["url"]),
            "domain_policy": domain_policy(r["url"]),
            "register_verification_status": r["verification_status"],
            "register_offline_content_status": r.get("offline_content_status", ""),
            "offline_text_status": "UNAVAILABLE_SOURCE_TEXT",
            "retrieval_status": "NOT_RETRIEVED",
            "retrieval_note": "오프라인 규칙: 외부 URL 접근 금지; 원문은 연구자 제공 시 data/raw_index에 등록",
            "shared_origin_group": r["shared_origin_group"],
            "research_focus": r["research_focus"],
            "epistemic_warning": r["epistemic_warning"],
            "local_path": "NA",
            "evidence_grade": "X",
            "copyright_note": ann.get("copyright_note", "메타데이터만 저장"),
            "is_local_carrier": "0",
        })
    for d in local_docs:
        rows.append({
            "source_id": d["carrier_id"],
            "case_id": "ALL",
            "work": d["doc_kind"],
            "title": d["role"],
            "record_date_lunar_or_scope": "2026-10-16 수집 문서",
            "calendar": "SOLAR_MODERN",
            "source_type": d["doc_kind"],
            "reporting_actor": "연구 담당자/선행 저장소",
            "volume_section": "NA",
            "volume_basis": "NA",
            "url": "",
            "url_domain": "",
            "domain_policy": "LOCAL_FILE",
            "register_verification_status": "LOCAL_FILE_PRESENT" if (ROOT / d["path"]).exists() else "LOCAL_FILE_MISSING",
            "register_offline_content_status": "",
            "offline_text_status": "LOCAL_SUMMARY_OR_PRIOR_DATA_NOT_VERBATIM",
            "retrieval_status": "LOCAL",
            "retrieval_note": d["note"],
            "shared_origin_group": "LOCAL-" + d["carrier_id"],
            "research_focus": d["role"],
            "epistemic_warning": d["note"],
            "local_path": d["path"],
            "evidence_grade": d["evidence_grade"],
            "copyright_note": "저장소 내부 연구 자료",
            "is_local_carrier": "1",
        })
    return rows


def build_source_crosswalk(sources: list[dict]) -> list[dict]:
    """Map GuSoon SRC3_xxx record IDs to register IDs by identical URL."""
    by_url = {s["url"]: s["source_id"] for s in sources if s["url"]}
    rows = []
    for r in read_csv(GUSUN_DIR / "04_source_records.csv"):
        rows.append({
            "gusun_record_id": r["source_record_id"],
            "register_source_id": by_url.get(r["source_url"], "UNMATCHED"),
            "source_url": r["source_url"],
            "record_lunar_date": r["record_lunar_date"],
            "match_basis": "IDENTICAL_URL" if r["source_url"] in by_url else "NO_MATCH",
        })
    return rows


# ---------------------------------------------------------------- spans
def build_spans(local_docs: dict, crosswalk: list[dict]) -> list[dict]:
    xwalk = {r["gusun_record_id"]: r["register_source_id"] for r in crosswalk}
    spans = []
    for s in read_csv(CURATED / "source_spans.csv"):
        row = dict(s)
        row["evidence_grade"] = local_docs[s["carrier_id"]]["evidence_grade"]
        row["offline_primary_verbatim"] = "NO"
        row["imported_from"] = "data/curated/source_spans.csv"
        spans.append(row)
    for p in read_csv(GUSUN_DIR / "05_source_faithful_propositions_AUDIT_ONLY.csv"):
        obj = p["object_or_content"].strip()
        text = f"{p['reporting_actor']}({p['attestation_mode']}): {p['subject']} — {p['predicate']}"
        if obj:
            text += f" [{obj}]"
        spans.append({
            "span_id": f"GS-P-{p['prop_id']}",
            "case_id": "GUSUN",
            "source_id": xwalk.get(p["source_record_id"], "UNMATCHED"),
            "carrier_id": "LOC-GUSUN-05",
            "carrier_locator": p["prop_id"],
            "span_kind": "CODED_PROPOSITION",
            "text_ko": text,
            "original_fragment": "",
            "original_fragment_status": "NONE",
            "evidence_grade": local_docs["LOC-GUSUN-05"]["evidence_grade"],
            "offline_primary_verbatim": "NO",
            "imported_from": "research/imported/gusun/05_source_faithful_propositions_AUDIT_ONLY.csv",
        })
    for f in read_csv(GUSUN_DIR / "01_confirmed_facts.csv"):
        spans.append({
            "span_id": f"GS-F-{f['fact_id']}",
            "case_id": "GUSUN",
            "source_id": xwalk.get(f["source_record_id"], "UNMATCHED"),
            "carrier_id": "LOC-GUSUN-01",
            "carrier_locator": f["fact_id"] + (f" ({f['source_prop_ids']})" if f["source_prop_ids"] else ""),
            "span_kind": "CODED_FACT_BUNDLE",
            "text_ko": f["confirmed_statement"],
            "original_fragment": "",
            "original_fragment_status": "NONE",
            "evidence_grade": local_docs["LOC-GUSUN-01"]["evidence_grade"],
            "offline_primary_verbatim": "NO",
            "imported_from": "research/imported/gusun/01_confirmed_facts.csv",
        })
    return spans


# ---------------------------------------------------------------- GUSUN claims
def build_gusun_attestations_claims() -> tuple[list[dict], list[dict]]:
    atts, claims = [], []
    for f in read_csv(GUSUN_DIR / "01_confirmed_facts.csv"):
        fid = f["fact_id"]
        status = GUSUN_LEVEL_TO_STATUS.get(f["confirmation_level"], "UNKNOWN")
        speaker = GUSUN_FACT_SPEAKERS.get(fid, "NA")
        atts.append({
            "att_id": f"GS-AT-{fid}",
            "case_id": "GUSUN",
            "speaker_id": speaker,
            "att_mode": ATT_MODE_FROM_STATUS.get(status, "UNKNOWN"),
            "record_date": f["record_lunar_date"],
            "context": f"{f['fact_category']} ({f['confirmation_level']})",
            "span_ids": f"GS-F-{fid}",
        })
        claims.append({
            "claim_id": f"GS-CL-{fid}",
            "case_id": "GUSUN",
            "att_id": f"GS-AT-{fid}",
            "proposition": f["confirmed_statement"],
            "claim_status": status,
            "truth_status": f["underlying_claim_status"],
            "conflict_group": GUSUN_CONFLICT_GROUPS.get(fid, ""),
            "contradicts": "",
            "span_ids": f"GS-F-{fid}",
        })
    # explicit contradictions inside conflict groups (preserved, not merged)
    pairs = {("CF030", "CF039"), ("CF032", "CF039"), ("CF016", "CF018"), ("CF017", "CF018"), ("CF010", "CF044")}
    by_id = {c["claim_id"]: c for c in claims}
    for a, b in pairs:
        ca, cb = by_id[f"GS-CL-{a}"], by_id[f"GS-CL-{b}"]
        ca["contradicts"] = "|".join(filter(None, [ca["contradicts"], cb["claim_id"]]))
        cb["contradicts"] = "|".join(filter(None, [cb["contradicts"], ca["claim_id"]]))
    return atts, claims


# ---------------------------------------------------------------- appointments
def build_appointments(attributes: list[dict]) -> list[dict]:
    rows = []
    for a in attributes:
        if a["attribute"] != "office":
            continue
        rows.append({
            "appt_id": a["attr_id"].replace("PA-", "AP-"),
            "person_id": a["person_id"],
            "case_id": a["person_id"].rsplit("-", 1)[0],
            "office": a["value"],
            "time_scope": a["time_scope"],
            "claim_status": a["claim_status"],
            "tenure_start": "NOT_RETRIEVED",
            "tenure_end": "NOT_RETRIEVED",
            "span_ids": a["span_ids"],
            "note": "재임 시점 확인값(time_scope)이며 임명·체직 일자는 원문 미보관",
        })
    return rows


# ---------------------------------------------------------------- normative rules
def build_normative_rules() -> list[dict]:
    features = {f["feature_id"]: f for f in read_csv(GUSUN_DIR / "02_institutional_normative_features.csv")}
    rows = []
    for r in read_csv(io.MODELS / "constraints" / "normative_rules_curated.csv"):
        feat = features.get(r["gusun_feature_id"], {})
        rows.append({
            **r,
            "feature_name": feat.get("feature_name", "UNMATCHED"),
            "feature_source_url": feat.get("source_url", ""),
            "feature_domain_policy": domain_policy(feat.get("source_url", "")),
            "feature_valid_from": feat.get("valid_from", ""),
            "feature_valid_to": feat.get("valid_to", ""),
        })
    return rows


# ---------------------------------------------------------------- manifest
def build_local_manifest() -> list[dict]:
    rows = []
    for path in sorted((RESEARCH).rglob("*")):
        if path.is_file():
            rows.append({
                "path": io.rel(path),
                "bytes": path.stat().st_size,
                "sha256": io.sha256_file(path),
                "role": _role_for(path),
            })
    return rows


def _role_for(path) -> str:
    p = io.rel(path)
    if "imported/gusun" in p:
        return "IMPORTED_PREVIOUS_CODED_DATA(GuSoon-Inference; read-only copy)"
    if "imported/chamang" in p:
        return "IMPORTED_SECONDARY_SYNTHESIS(Chamang-Inference; read-only copy)"
    return "RESEARCHER_SUPPLIED_LOCAL_NOTE"


# ---------------------------------------------------------------- driver
def build_tables() -> dict[str, list[dict]]:
    """Build all normalized tables in memory (no files written)."""
    tables: dict[str, list[dict]] = {}
    sources = build_sources()
    crosswalk = build_source_crosswalk(sources)
    local_docs = {d["carrier_id"]: d for d in read_csv(CURATED / "local_documents.csv")}
    tables["sources"] = sources
    tables["source_crosswalk"] = crosswalk
    tables["source_spans"] = build_spans(local_docs, crosswalk)
    for name in CURATED_TABLES:
        tables[name] = read_csv(CURATED / f"{name}.csv")
    g_atts, g_claims = build_gusun_attestations_claims()
    tables["attestations"] = tables["attestations"] + g_atts
    tables["claims"] = tables["claims"] + g_claims
    tables["appointments"] = build_appointments(tables["person_attributes"])
    tables["normative_rules"] = build_normative_rules()
    return tables


def build_all(write_parquet: bool = True) -> dict[str, list[dict]]:
    tables = build_tables()
    NORMALIZED.mkdir(parents=True, exist_ok=True)
    for name, rows in tables.items():
        write_csv(NORMALIZED / f"{name}.csv", rows)
    write_csv(RAW_INDEX / "local_file_manifest.csv", build_local_manifest())
    if write_parquet:
        write_parquet_files(list(tables))
    return tables


def write_parquet_files(names: list[str]) -> bool:
    try:
        import duckdb  # optional dependency
    except ImportError:
        return False
    con = duckdb.connect()
    for name in names:
        src = NORMALIZED / f"{name}.csv"
        dst = NORMALIZED / f"{name}.parquet"
        con.execute(
            f"COPY (SELECT * FROM read_csv('{src.as_posix()}', header=true, all_varchar=true)) "
            f"TO '{dst.as_posix()}' (FORMAT PARQUET)"
        )
    con.close()
    return True


def load_normalized() -> dict[str, list[dict]]:
    tables = {}
    for path in sorted(NORMALIZED.glob("*.csv")):
        tables[path.stem] = read_csv(path)
    return tables


def index(rows: list[dict], key: str) -> dict[str, dict]:
    return {r[key]: r for r in rows}


def span_grade(span_ids: list[str], spans: dict[str, dict]) -> str:
    grades = [spans[s]["evidence_grade"] for s in span_ids if s in spans]
    if not grades:
        return "X"
    return min(grades, key=lambda g: GRADE_ORDER.get(g, 9))


__all__ = ["build_all", "load_normalized", "split", "span_grade", "GRADE_ORDER"]
