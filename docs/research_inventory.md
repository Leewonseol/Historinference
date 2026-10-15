# 데이터·사료 인벤토리 (0단계)

> 자동 생성 문서(`python -m historinference report`). 모든 수치는 `data/normalized`·`models`·`data/audit`에서 재계산된다. 원문 미보관(UNAVAILABLE_SOURCE_TEXT) 상태에서 로컬 요약·선행 코딩만으로 작성되었으며, 확률·빈도 추정은 하지 않는다.

## 상태 요약

| 항목 | 값 | 비고 |
|---|---|---|
| 공식 출처 레지스터(원문 위치) | 22건 | 원문 로컬 확보 0건 / NOT_RETRIEVED 22건 |
| 로컬 근거 문서 | 12건 | 의역·요약·선행 코딩(원문 전사 아님) |
| 문장 단위 근거(span) | 306건 | 등급 B=226, C=42, D=38; 원문 직접 인용 0건 |
| 메커니즘 코딩 행 | 82행 | 확인(1/0) 53행 · 미확인(NA) 29행 · 코딩 비율 64.6% |
| 사건×코드 적용률 | 39/76 칸 | 51.3% (1/0 근거가 하나 이상 있는 칸) |
| 확인 코딩의 근거 등급 | B=32, C=12, D=9 | A=원문 직접(0), B=공식 기사 의역·선행 코딩, C=연구 요약, D=2차 종합 |
| 검증 감사(validate) | 오류 0 · 경고 2 | data/audit/validation_findings.csv |
| 테스트(pytest, 로컬 Python 실행) | 통과 88 / 실패 0 / 오류 0 / 건너뜀 0 | data/audit/test_results.json (Oracle 실행 아님) |
| 연구자 요청 | 21건 | REQUEST_FOR_RESEARCHER.md |

## 공식 출처 레지스터 22건 — 오프라인 회수 상태

외부 사이트 접속은 오프라인 규칙에 따라 실행하지 않았다. URL은 provenance 포인터이며 열람 가능한 원문이 아니다. `retrieval_status=NOT_RETRIEVED`는 자료 부재가 아니라 미확보를 뜻한다.

| ID | 사건 | 사료 | 음력 날짜/범위 | 제목(레지스터) | 출처 유형 | 보고 주체 | 권·편 | 중복 그룹 | 도메인 정책 | 레지스터 상태 | 로컬 원문 | 근거 span(등급) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| CH-001 | CHOI | 심리록 | 1785-1789 | 평산 최아지 옥 | PRIMARY_COMPILED_JUDICIAL | 정조 판부·도신 계문·형조 회계(편찬) | 권8 황해도 「평산 최아지 옥」 | CH-ROYAL-ORDERS | APPROVED_OFFICIAL_PRIMARY | WEB_SEARCH_FULL_TEXT | UNAVAILABLE_SOURCE_TEXT | 32 (C8, D24) |
| CH-002 | CHOI | 추관지 | 1787;1789 | 평산 최 조이 옥안 | PRIMARY_COMPILED_JUDICIAL | 공초·검안·정조 판부(편찬) | 권2 상복부·윤상·살자부 「중보: 최 조이 옥안」 | CH-ROYAL-ORDERS | APPROVED_OFFICIAL_PRIMARY | WEB_OPEN_FULL_TEXT | UNAVAILABLE_SOURCE_TEXT | 36 (D36) |
| CH-003 | CHOI | 정조실록 | 1787-04-16 | 이곤수 안핵 및 지방 관원 처분 | PRIMARY_ANNALS | 양서 암행어사 이곤수 복명·실록 편찬자 | 정조실록 23권 정조 11년 4월 16일 | CH-OFFICIAL | APPROVED_OFFICIAL_PRIMARY | WEB_OPEN_FULL_TEXT | UNAVAILABLE_SOURCE_TEXT | 8 (B5, C1, D2) |
| CH-007 | CHOI | 장서각 왕실족보 | 시기 미상 | 순평군파 선원속보 | GENEALOGY | 장서각 소장 왕실 족보 | 순평군파 선원속보 | CH-GENEALOGY | APPROVED_INSTITUTIONAL_HOLDING | PREVIOUS_RESEARCH_LINK_RECHECK | UNAVAILABLE_SOURCE_TEXT | 1 (C1) |
| JH-001 | CHO | 심리록 | 1780-1783 | 백천 조재항 옥 | PRIMARY_COMPILED_JUDICIAL | 정조 판부(편찬) | NA | JH-ROYAL-ORDERS | APPROVED_OFFICIAL_PRIMARY | WEB_SEARCH_FULL_TEXT | UNAVAILABLE_SOURCE_TEXT | 3 (C3) |
| JH-002 | CHO | 추관지 | 1781-1783 | 조재항 옥안 | PRIMARY_COMPILED_JUDICIAL | 공초·정조 판부(편찬) | NA | JH-ROYAL-ORDERS | APPROVED_OFFICIAL_PRIMARY | WEB_OPEN_FULL_TEXT | UNAVAILABLE_SOURCE_TEXT | 3 (C3) |
| JH-003 | CHO | 정조실록 | 1783-06-03 | 조재항 석방 및 이가원 처분 | PRIMARY_ANNALS | 정조 판부·실록 편찬자 | 정조실록 15권 정조 7년 6월 3일 | JH-OFFICIAL | APPROVED_OFFICIAL_PRIMARY | WEB_OPEN_FULL_TEXT | UNAVAILABLE_SOURCE_TEXT | 21 (B10, C11) |
| YE-001 | YE | 정조실록 | 1789-07-14 | 단천 부사 이여절 관직 관련 | PRIMARY_ANNALS | 실록 편찬자(인사 기사) | NA | YE-CAREER | APPROVED_OFFICIAL_PRIMARY | WEB_SEARCH_FULL_TEXT | UNAVAILABLE_SOURCE_TEXT | 1 (C1) |
| YE-002 | YE | 정조실록 | 1793-06-13 | 정대용의 창원 부사 이여절 평가 | PRIMARY_ANNALS | 도신 정대용 평가(레지스터 제목) | NA | YE-CAREER | APPROVED_OFFICIAL_PRIMARY | WEB_SEARCH_FULL_TEXT | UNAVAILABLE_SOURCE_TEXT | 1 (C1) |
| YE-003 | YE | 정조실록 | 1794-09-08 | 이여절 불법 형벌 혐의에 대한 조진택 조사보고 | PRIMARY_ANNALS | 관찰사 조진택 조사보고(레지스터 제목) | NA | YE-INQUIRY | APPROVED_OFFICIAL_PRIMARY | WEB_SEARCH_FULL_TEXT | UNAVAILABLE_SOURCE_TEXT | 3 (C3) |
| YE-004 | YE | 정조실록 | 1795-06-04 | 유경이 이여절 남살 31명 보고 | PRIMARY_ANNALS | 유경 보고(레지스터 제목) | NA | YE-INQUIRY | APPROVED_OFFICIAL_PRIMARY | WEB_OPEN_FULL_TEXT | UNAVAILABLE_SOURCE_TEXT | 7 (B1, C6) |
| YE-005 | YE | 정조실록 | 1795-06-11 | 조진택의 이여절 두둔성 조사 질책·별도 안핵 | PRIMARY_ANNALS | 정조 질책·실록 편찬자 | NA | YE-INQUIRY | APPROVED_OFFICIAL_PRIMARY | WEB_OPEN_FULL_TEXT | UNAVAILABLE_SOURCE_TEXT | 8 (B2, C6) |
| YE-006 | YE | 정조실록 | 1795-08-24 | 이여절 사건 중앙 심리·장살 25명 언급 | PRIMARY_ANNALS | 중앙 심리(레지스터 제목) | NA | YE-INQUIRY | APPROVED_OFFICIAL_PRIMARY | WEB_OPEN_FULL_TEXT | UNAVAILABLE_SOURCE_TEXT | 5 (B1, C4) |
| YE-007 | YE | 정조실록 | 1795-09-21 | 조진택 삭직·이여절 위원 유배 | PRIMARY_ANNALS | 정조 처분(레지스터 제목) | NA | YE-JUDGMENT | APPROVED_OFFICIAL_PRIMARY | WEB_SEARCH_FULL_TEXT | UNAVAILABLE_SOURCE_TEXT | 4 (B1, C3) |
| GS-001 | GUSUN | 정조실록 | 1793-05-12 | 이형원 장계·정조 1차 판단 | PRIMARY_ANNALS | 충청도 관찰사 이형원 장계·정조 | NA | GS-REPORT | APPROVED_OFFICIAL_PRIMARY | IMPORTED_FROM_VERIFIED_REPO | UNAVAILABLE_SOURCE_TEXT | 28 (B27, C1) |
| GS-002 | GUSUN | 비변사등록 | 1793-05-27 | 이조원 구순 사건 별단·엄핵 청구 | PRIMARY_DELIBERATION_RECORD | 암행어사 이조원·비변사 | NA | GS-INQUIRY | APPROVED_OFFICIAL_PRIMARY | IMPORTED_FROM_VERIFIED_REPO | UNAVAILABLE_SOURCE_TEXT | 21 (B20, C1) |
| GS-003 | GUSUN | 정조실록 | 1793-05-27 | 이조원 복명에 대한 정조의 비판 | PRIMARY_ANNALS | 암행어사 이조원·정조 | NA | GS-INQUIRY | APPROVED_OFFICIAL_PRIMARY | IMPORTED_FROM_VERIFIED_REPO | UNAVAILABLE_SOURCE_TEXT | 7 (B6, C1) |
| GS-004 | GUSUN | 승정원일기 | 1793-05-28 | 홍대협 안핵 차하 | PRIMARY_DIARY | 정조·홍대협(승정원일기) | NA | GS-APPOINT | APPROVED_OFFICIAL_PRIMARY | IMPORTED_FROM_VERIFIED_REPO | UNAVAILABLE_SOURCE_TEXT | 7 (B6, C1) |
| GS-005 | GUSUN | 비변사등록 | 1793-06-11 | 윤노동 별단과 처분 보류 | PRIMARY_DELIBERATION_RECORD | 암행어사 윤노동·비변사 | NA | GS-INQUIRY | APPROVED_OFFICIAL_PRIMARY | IMPORTED_FROM_VERIFIED_REPO | UNAVAILABLE_SOURCE_TEXT | 13 (B12, C1) |
| GS-006 | GUSUN | 정조실록 | 1793-06-13 | 홍대협 안핵 복명·최종 정조 심리 | PRIMARY_ANNALS | 안핵어사 홍대협·증인 공초·정조 | NA | GS-JUDGMENT | APPROVED_OFFICIAL_PRIMARY | WEB_OPEN_FULL_TEXT | UNAVAILABLE_SOURCE_TEXT | 135 (B132, C3) |
| GS-007 | GUSUN | 정조실록 | 1793-06-13 | 윤노동 암행 범위 이탈 파직 | PRIMARY_ANNALS | 정조 | NA | GS-PROCEDURE | APPROVED_OFFICIAL_PRIMARY | IMPORTED_FROM_VERIFIED_REPO | UNAVAILABLE_SOURCE_TEXT | 3 (B3) |
| GS-008 | GUSUN | 정조실록 | 1793-06-16 | 이형원 인사 후속조치 | PRIMARY_ANNALS | 정조 | NA | GS-FOLLOWUP | APPROVED_OFFICIAL_PRIMARY | IMPORTED_FROM_VERIFIED_REPO | UNAVAILABLE_SOURCE_TEXT | 2 (B2) |

**독립성 원칙**: 같은 `shared_origin_group`(예: CH-ROYAL-ORDERS의 심리록·추관지, JH-ROYAL-ORDERS)은 동일 판부·공초를 공유할 수 있으므로 독립 증인 2건으로 계수하지 않는다. GuSoon의 실록·비변사등록 동일 단계 기록도 별도 attestation으로 보존하되 독립 근원으로 단정하지 않는다.

## 로컬 근거 문서(실제로 저장소에 있는 파일)

| carrier | 경로 | 종류 | 증거 등급 | 주의 |
|---|---|---|---|---|
| LOC-ANNALS-DIGEST | research/official_annals_article_digests.md | RESEARCH_ASSISTANT_PARAPHRASE_OF_OFFICIAL_ARTICLE | B | 원문 전사 아님; 직접 인용으로 표시 금지 |
| LOC-EVIDENCE-PACK | research/offline_evidence_pack.md | RESEARCH_SUMMARY_WITH_OFFICIAL_REFERENCE | C | 원문 발췌 미포함; 고신뢰 승격 금지 |
| LOC-CLAIM-SEEDS | research/offline_claim_seeds.csv | RESEARCH_SUMMARY_WITH_OFFICIAL_REFERENCE | C | offline_primary_verbatim=NO 전 행 |
| LOC-REGISTER | research/source_register.csv | REGISTER_METADATA | C | 제목·초점 문구는 조사원 작성 메타데이터; 기사 원문 아님 |
| LOC-BRIEF | research/research_brief.md | RESEARCH_PLANNING_NOTE | C | 계획 문서; 사실 근거로는 보조적으로만 사용 |
| LOC-CHAMANG | research/imported/chamang/pyeongsan_case_report.md | IMPORTED_SECONDARY_SYNTHESIS | D | 원문 전사 아님; 비승인 도메인 참고문헌(S1~S3·N1)은 증거로 채택하지 않음 |
| LOC-GUSUN-00 | research/imported/gusun/00_INPUT_MANIFEST.csv | IMPORTED_PREVIOUS_CODED_DATA | B | 메타데이터 |
| LOC-GUSUN-01 | research/imported/gusun/01_confirmed_facts.csv | IMPORTED_PREVIOUS_CODED_DATA | B | 공식 원문과 재대조 전 최고 확실성 부여 금지 |
| LOC-GUSUN-02 | research/imported/gusun/02_institutional_normative_features.csv | IMPORTED_PREVIOUS_CODED_DATA | CONTEXT | 일부 출처가 승인 원문 도메인 밖(encykorea·moleg); 유효기간 1793까지 검증 |
| LOC-GUSUN-03 | research/imported/gusun/03_environment_1793.csv | IMPORTED_PREVIOUS_CODED_DATA | CONTEXT | 김명신 개인 감염 증명 아님 |
| LOC-GUSUN-04 | research/imported/gusun/04_source_records.csv | IMPORTED_PREVIOUS_CODED_DATA | B | 출처 색인 |
| LOC-GUSUN-05 | research/imported/gusun/05_source_faithful_propositions_AUDIT_ONLY.csv | IMPORTED_PREVIOUS_CODED_DATA | B | 감사용 명제; 확정 사실 아님 |

## 파일 해시(sha256)

가져온 GuSoon/Chamang 파일은 `data/raw_index/imported_checksums.csv`에 고정했고 테스트가 변경 여부를 검사한다.

| 경로 | bytes | sha256(앞 16자) | checksum 고정 | 역할 |
|---|---|---|---|---|
| research/imported/chamang/pyeongsan_case_report.md | 27324 | c2c3753a6014a249… | 고정됨 | IMPORTED_SECONDARY_SYNTHESIS(Chamang-Inference; read-only copy) |
| research/imported/gusun/00_INPUT_MANIFEST.csv | 1030 | 3f1681b68434d2b7… | 고정됨 | IMPORTED_PREVIOUS_CODED_DATA(GuSoon-Inference; read-only copy) |
| research/imported/gusun/01_confirmed_facts.csv | 18090 | 868bb0b5ec3ca371… | 고정됨 | IMPORTED_PREVIOUS_CODED_DATA(GuSoon-Inference; read-only copy) |
| research/imported/gusun/02_institutional_normative_features.csv | 7451 | d205145d5654c2d7… | 고정됨 | IMPORTED_PREVIOUS_CODED_DATA(GuSoon-Inference; read-only copy) |
| research/imported/gusun/03_environment_1793.csv | 1363 | b989ada695297a31… | 고정됨 | IMPORTED_PREVIOUS_CODED_DATA(GuSoon-Inference; read-only copy) |
| research/imported/gusun/04_source_records.csv | 3038 | f75a000299e1c7ea… | 고정됨 | IMPORTED_PREVIOUS_CODED_DATA(GuSoon-Inference; read-only copy) |
| research/imported/gusun/05_source_faithful_propositions_AUDIT_ONLY.csv | 57206 | 0f0039813bd2cc7c… | 고정됨 | IMPORTED_PREVIOUS_CODED_DATA(GuSoon-Inference; read-only copy) |
| research/official_annals_article_digests.md | 5018 | 0bf3de4d60c5c9b6… | - | RESEARCHER_SUPPLIED_LOCAL_NOTE |
| research/offline_claim_seeds.csv | 3562 | ddd341c029b44e15… | - | RESEARCHER_SUPPLIED_LOCAL_NOTE |
| research/offline_evidence_pack.md | 8572 | 179b90f65bf971dc… | - | RESEARCHER_SUPPLIED_LOCAL_NOTE |
| research/research_brief.md | 6092 | 9e3dfb1757fabf4b… | - | RESEARCHER_SUPPLIED_LOCAL_NOTE |
| research/source_register.csv | 8416 | 60b1a1810706f290… | - | RESEARCHER_SUPPLIED_LOCAL_NOTE |

## GuSoon 출처 레코드 ↔ 레지스터 대응

| GuSoon ID | 레지스터 ID | 음력 날짜 | 근거 |
|---|---|---|---|
| SRC3_001 | GS-001 | 1793-05-12 | IDENTICAL_URL |
| SRC3_002 | GS-002 | 1793-05-27 | IDENTICAL_URL |
| SRC3_003 | GS-003 | 1793-05-27 | IDENTICAL_URL |
| SRC3_004 | GS-004 | 1793-05-28 | IDENTICAL_URL |
| SRC3_005 | GS-005 | 1793-06-11 | IDENTICAL_URL |
| SRC3_006 | GS-006 | 1793-06-13 | IDENTICAL_URL |
| SRC3_007 | GS-007 | 1793-06-13 | IDENTICAL_URL |
| SRC3_008 | GS-008 | 1793-06-16 | IDENTICAL_URL |

## 검색·수집 미완료 (NOT_RETRIEVED / NOT_COLLECTED)

- 《일성록》·《승정원일기》·《비변사등록》·《심리록》·《추관지》·《홍재전서》·《흠흠신서》의 날짜별 확장 검색은 **실행하지 않았다**(오프라인 규칙). 필요한 원문은 `REQUEST_FOR_RESEARCHER.md`에 기록했다.
- 재현 방법: 연구자가 공식 사이트(sillok.history.go.kr, db.history.go.kr, sjw.history.go.kr)에서 레지스터 URL의 기사를 열람하여 원문·국역 문단을 로컬 파일로 제공 → `data/curated/source_spans.csv`에 `span_kind=VERBATIM_ORIGINAL`, 등급 A로 추가 → `python -m historinference all` 재실행.
- 이전 세션 초기에 오프라인 규칙 공지 전 외부 접속·검색을 시도한 기록이 있으나, 공식 사이트는 접속 거부되었고 검색 결과는 **일체 증거로 채택하지 않았다**(데이터에 반영 없음).
- 비승인 전재(위키문헌·shidianguji 등)는 출처로 등록하지 않았다. Chamang 보고서 속 비승인 참고문헌(S1~S3·N1)은 legacy 서지로만 남는다.
