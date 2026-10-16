# Historinference


## 1차 사료 원문 확보 단계 (아직 미완료)

외부 사이트 접속이 불가능한 Claude Code와 별개로, `scripts/collect_official_originals.py`를 만들었습니다. 공식 사료 제공처(`sillok.history.go.kr`, `db.history.go.kr`, `sjw.history.go.kr`) 22개 출처 위치만 사용합니다. 수집 도구는 **고전 한문 후보 텍스트만 추출**하고 현대 한국어 국역은 원문 파일로 재배포하지 않습니다. 웹페이지 구조에 따라 추출 실패 또는 기사 외 텍스트가 섞일 수 있어, 자동으로 내려받은 자료는 `EXTRACTED_NEEDS_COMPLETE_TEXT_QA`로 표기합니다.

GitHub **Actions → Collect official classical originals (manual) → Run workflow** 로 수동 실행하면 결과를 `official-originals-provisional` 아티팩트로 받습니다. 이 아티팩트는 자동으로 `main`에 합치지 않습니다. 실행 후 `manifest.json`을 확인하고 사이트별 원문 구간·최초/최종 글자 및 기사 완전성·재배포 조건을 대조해야 합니다. **현재 22개 사료를 전부 확보했다는 뜻이 아닙니다.** 본문을 내려받지 못하는 사료의 전체 원문은 확보되지 않은 상태로 유지합니다.

## 네 사건 시간·절차 DAG (공식 사료 재대조 보강)

- [**대화형 DAG: 4개 사건별 보기·노드 선택·공식 사료 바로가기**](docs/dag.html)
- [Mermaid DAG 원본과 35개 노드 출처표](docs/four_case_dags.md)
- [공식 사료 재대조 노트](research/official_verified_addendum.md)
- [노드·연결 데이터 35개 노드/34개 절차 연결](docs/data/four_case_dags.json)

이 시각화는 기존 코드북·합성 모델을 고치지 않고 추가한 **별도 역사적 절차 그래프**다. 실선은 자료상 선후·행정 절차 연결이며 범죄의 인과·공모를 입증하지 않는다. 원문 전체를 전사한 완성 코퍼스가 아닌 연구 요약이다. 현재 GitHub Pages 배포 여부는 별도 설정이 필요할 수 있어 [GitHub에 등록된 HTML](docs/dag.html) 및 [Mermaid 문서](docs/four_case_dags.md)를 기본 결과로 제공한다.


**네 조선 형사사건의 사료 대조와 합성사건 설계 연구** — 최아지·이차망, 조재항, 이여절·조진택, 구순–김명신

> **연구 상태:** 오프라인 구현 완료 / **원문 미확보.** 공식 출처 22건의 원문은 저장소에 없고(`UNAVAILABLE_SOURCE_TEXT`), 모든 코딩은 로컬 의역·연구 요약·선행 코딩·2차 종합에 근거한다. 확보가 필요한 원문은 [REQUEST_FOR_RESEARCHER.md](REQUEST_FOR_RESEARCHER.md)에 정리했다.

## 현재 상태 (자동 갱신)

<!-- STATUS:BEGIN -->
| 항목 | 값 | 비고 |
|---|---|---|
| 공식 출처 레지스터(원문 위치) | 22건 | 원문 로컬 확보 0건 / NOT_RETRIEVED 22건 |
| 로컬 근거 문서 | 12건 | 의역·요약·선행 코딩(원문 전사 아님) |
| 문장 단위 근거(span) | 306건 | 등급 B=226, C=42, D=38; 원문 직접 인용 0건 |
| 메커니즘 코딩 행 | 82행 | 확인(1/0) 53행 · 미확인(NA) 29행 · 코딩 비율 64.6% |
| 사건×코드 적용률 | 39/76 칸 | 51.3% (1/0 근거가 하나 이상 있는 칸) |
| 확인 코딩의 근거 등급 | B=32, C=12, D=9 | A=원문 직접(0), B=공식 기사 의역·선행 코딩, C=연구 요약, D=2차 종합 |
| 검증 감사(validate) | 오류 0 · 경고 2 | data/audit/validation_findings.csv |
| 테스트(pytest, 로컬 Python 실행) | 통과 89 / 실패 0 / 오류 0 / 건너뜀 0 | data/audit/test_results.json (Oracle 실행 아님) |
| 연구자 요청 | 21건 | REQUEST_FOR_RESEARCHER.md |
<!-- STATUS:END -->

## 재현 절차 — CLI 하나

```bash
pip install pytest duckdb        # duckdb는 선택(Parquet·SQL 교차검사)
python -m historinference all    # build → validate → worlds → synthesize → test → report
```

| 명령 | 단계 | 산출물 |
|---|---|---|
| `build` (`inventory`) | 0–2 인벤토리·정규화 | `data/normalized/*.csv`(+`.parquet`), `data/raw_index/local_file_manifest.csv` |
| `validate` | 6 감사 | `data/audit/validation_findings.csv`, `validation_summary.json` |
| `worlds` | 4 부분순서·가능세계 | `models/constraints/`, `models/worlds/` |
| `synthesize` | 5 A/B/C 비교 | `models/synthesis/` |
| `test` | 6 테스트 | `data/audit/test_results.json`, `pytest_junit.xml` |
| `report` | 7 보고서·대시보드 | `docs/`, `outputs/`, `REQUEST_FOR_RESEARCHER.md`, `outputs/dashboard_data.js` |

외부 네트워크에 접속하는 명령은 없다. 레지스터 URL은 provenance 포인터일 뿐이다.

## 보고서

- [데이터·사료 인벤토리](docs/research_inventory.md) · [코드북](docs/codebook.md) · [한계와 차단 사항](docs/limitations.md)
- [증거 행렬](outputs/evidence_matrix.md) · [인물 프로필](outputs/character_profiles.md) · [공통·차별 메커니즘](outputs/mechanism_comparison.md)
- [가능세계와 제약](outputs/worlds_report.md) · [A: 앵커 비교](outputs/anchor_comparison.md) · [B: 합성 비교](outputs/synthetic_comparison.md) · [상태 보고](outputs/status_report.md)
- [읽기 전용 대시보드 `index.html`](index.html) — 로컬에서 파일로 열면 `outputs/dashboard_data.js`를 읽어 표시한다(코어 데이터를 바꾸지 않음).
- **GitHub Pages**: `report`가 대시보드를 `docs/index.html`+`docs/dashboard_data.js`로도 복사하고 `.nojekyll`을 둔다. Settings → Pages에서 `main` / `/docs`(또는 `/ (root)`)를 고르면 Jekyll 빌드 없이 정적 대시보드가 배포된다.

## 자료 구성

| 경로 | 내용 | 증거 등급 |
|---|---|---|
| `research/source_register.csv` | 공식 출처 위치 22건(실록·한국사DB·승정원일기·장서각) | 링크만(X) |
| `research/official_annals_article_digests.md` | 조사원이 열람한 실록 기사 4건의 의역 | B |
| `research/imported/gusun/` | GuSoon-Inference 선행 코딩(사실 50·명제 156) — 읽기 전용, checksum 고정 | B / CONTEXT |
| `research/offline_evidence_pack.md`, `offline_claim_seeds.csv`, `research_brief.md` | 연구 요약·주장 씨앗 | C |
| `research/imported/chamang/pyeongsan_case_report.md` | 평산 사건 선행 2차 종합 — 읽기 전용, checksum 고정 | D |
| `data/curated/` | 이 프로젝트의 수작업 코딩(사건·인물·이표기·속성·사건·진술·주장·물증·관계·처분·메커니즘·요청) | — |
| `config/objectives.toml` | 기획의도 목표함수(Y1~Y6 수준 규칙·hard gate·가중치 격자) — 사람이 수정 | — |
| `models/synthesis/morphological_box.csv`, `compatibility_rules.csv` | 형태 상자(12차원·51행)와 CSP 규칙(20개) | — |

## 사건별 특징

| ID | 실제 사건 | 핵심 수집 범위 | 가장 중요한 불확실성 |
| --- | --- | --- | --- |
| CHOI | 1785–1789 평산 최아지·이차망 | 검험, 간통·살인 고발, 민씨 격쟁, 이곤수 안핵, 석방, 1789 재의문 | 조광진 자백과 진술번복의 진실성 |
| CHO | 1780/1781–1783 배천 조재항 | 고발자 이가원, 소문·증언 조작, 장기 수사, 석방, 관찰사 책임 | 윤씨 실제 사인 및 관리와의 공모(근거 없음) |
| YE | 1793–1795 이여절·조진택 | 남형 사망 보고, 관찰사 조사, 유경 안핵, 처분 | 사망자 31/25 보고 차이와 비호의 고의성 |
| GUSUN | 1793 구순·김명신 | 도난 혐의, 병영 수사, 구금 중 사망, 홍대협 안핵 | 사망 직접 인과와 보고 간 충돌 |

## 핵심 결과(요약)

- **앵커(A)**: 이식 없이 hard gate(Y3~Y6 ≥ PARTIAL)를 통과하는 앵커는 CHOI와 CHO다. CHOI는 목표 수준이 가장 높지만 근거의 상당 부분이 2차 종합(D등급)이어서, 증거 등급을 B로 제한하면 이식 없이 통과하는 앵커는 CHO만 남는다. YE·GUSUN은 무고인 보호(Y3)나 유족 이의제기(Y6) 기록이 없어 이식이 필요하고, 이식은 실제 사건 위에 다른 사건을 덧씌우는 비용을 낳는다. 어떤 앵커도 진범 규명(Y1)을 FULL로 만들 수 없다.
- **합성(B)**: CSP·gate를 통과하는 설계 58만여 개 중 오컴 필터를 거친 최소 설계 1만 6천여 개를 비교했다. Y1·Y2를 FULL로 만드는 B 설계는 모두 '진범이 증거로 확정됨'이라는 출처 없는 창작 요소를 하나 포함한다.
- **비교**: 기본 설정 Pareto 전선에 A·B·C가 공존하며 어느 전략도 다른 전략을 전면 지배하지 않는다. 선택은 '역사적 앵커의 충실성'과 '기획의도의 완결성' 사이의 교환이며, 그 위치는 사람이 정하는 gate·가중치에 달려 있다. 자세한 수치는 [A](outputs/anchor_comparison.md)·[B](outputs/synthetic_comparison.md) 보고서와 민감도 표를 본다.

## 원칙

- 기획의도는 목표함수(설계 기준)이며 통계학적 종속변수가 아니다. 네 사건으로 학습한 확률·빈도 추정을 하지 않는다. 가능세계의 `posterior`·`likelihood`는 `UNSCORED`.
- 원문 진술은 '진술이 기록됐다'는 관측이며 내용의 참은 미확정이다. 당시 판단(`culprit_contemporary_judgment`)과 역사적 실체(`historical_culprit_status`)를 분리한다.
- 서로 다른 사건의 인물을 병합하지 않는다(정조도 사건별 ID). 1793-06-13 같은 날짜의 구순 기사와 이여절 기사, 1795 YE 사건과 1801 황기운 사건을 합치지 않는다.
- 모든 합성 결과는 **가상 사건**이며, 실존 인물에 창작된 공모나 범행을 역사적 사실로 귀속하지 않는다.
- 원천 저장소 [GuSoon-Inference](https://github.com/Leewonseol/GuSoon-Inference)·[Chamang-Inference](https://github.com/Leewonseol/Chamang-Inference)는 수정하지 않았다. 저장소 안의 사본(`research/imported/`)은 checksum으로 고정해 테스트한다.

## 오프라인 자료 이용 원칙 (2026-10-16)

Claude Code는 외부 역사 사이트에 접속하지 않습니다. 제공 자료는 [오프라인 근거집](research/offline_evidence_pack.md), [원문 수집 전 주장 씨앗](research/offline_claim_seeds.csv), [공식 출처 레지스터](research/source_register.csv), [기존 구순 데이터](research/imported/gusun/), [평산 선행 보고서](research/imported/chamang/pyeongsan_case_report.md)입니다. 위키문헌 및 비공식 전재 사이트는 증거로 채택하지 않습니다. 원전 기사 링크는 직접 열람 가능한 텍스트를 의미하지 않으며, 미확보 원문은 임의 복원하지 않습니다.
