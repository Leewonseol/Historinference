# 코드북 (2단계)

이 코드북은 `data/curated/*.csv`의 모든 값에 적용된다. 검증 규칙은 `historinference/validate.py`가 기계적으로 집행하고 `tests/`가 결함 주입으로 확인한다.

## 1. 코딩 단위

사건 전체를 한 행으로 코딩하지 않는다. `data/curated/mechanism_codes.csv`의 각 행은 다음 단위 중 하나를 가리킨다.

| unit_type | 가리키는 표 | 예 |
|---|---|---|
| EVENT | `events.csv` | EV-CH-02 초검·복검 自刺 판단 |
| CLAIM | `claims.csv` | CL-JH-07 조상진 피상 보고(국왕 판단) |
| PERSON | `persons.csv` | GUSUN-P02 김명신 |
| RELATION | `relations.csv` | RL-GS-13 한재욱→자미덕 진술 영향(CONTESTED) |
| EPISODE | `episodes.csv` | CHO-E2 반복 조사 구간 |
| DECISION | `decisions.csv` | DC-YE-04 이여절 위원 유배(명령) |
| EVIDENCE | `evidence_items.csv` | EI-CH-01 혈의 |

## 2. 값

| 값 | 뜻 | 요구 조건 |
|---|---|---|
| `1` | 그 단위가 해당 메커니즘을 **기록·판단했다는 것이 출처로 충분히 지지됨** | `span_ids` 1개 이상, 등급 D 이상, 같은 사건 span, `claim_status`가 HYPOTHESIS·UNKNOWN 아님 |
| `0` | 메커니즘의 **부재가 출처로 명시적으로 지지됨** | 위 조건 + `rationale`에 '부재 판단' 명시(예: 정조가 김명신은 곤장을 맞지 않았다고 판단 → E03=0) |
| `NA` | 알 수 없음 | 근거 부재·원문 미보관·주장만 존재하는 경우의 기본값 |

값 1은 **내용의 역사적 진실을 뜻하지 않는다.** 진실성 층위는 `claim_status`가 담는다.

## 3. claim_status

| 값 | 뜻 |
|---|---|
| DOCUMENTED_ACT | 출처가 보고·명령·격쟁·구금·자백 같은 **행위의 발생**을 기록 |
| RECORDED_TESTIMONY | 누군가의 진술이 **기록되었음**(진술 내용의 참은 미확정) |
| OFFICIAL_JUDGMENT | 관원·국왕의 판단·평가가 기록됨(판단 내용이 사실이라는 뜻 아님) |
| CONTESTED | 서로 충돌하는 출처·판단이 있음(예: 1787 결론 vs 1789 재의문) |
| HYPOTHESIS | 사료 안에서 제기된 의문·가설(예: 1789 정조의 제3자 가능성 질문). 1/0 코딩 금지 |
| UNKNOWN | 판단 불가 |

`claims.csv`의 HYPOTHESIS는 사료 속 의문 제기(`att_mode=ROYAL_DOUBT`)로만 만들 수 있다. 분석자가 만든 가설은 정규화 표가 아니라 `models/worlds/`의 세계 후보 층에만 둔다.

## 4. 메커니즘 코드 (모두 다중 선택)

| 코드 | 이름 | 코딩 기준 |
|---|---|---|
| E01 | 증거 인멸·변조 | 물증을 없애거나 바꾼 행위가 기록·판단됨. '주장된 물증이 없었다'는 판단은 E01 아님 |
| E02 | 허위(사실과 다른) 검험·보고 | 후속 판단이 앞선 검험·보고를 사실과 다르다고 봄. 고의 여부는 `fault_type` |
| E03 | 증언 강요·유도 | 진술 종용·사주·위협·지시의 기록(진술자의 주장 포함, 상태로 구분) |
| E04 | 청탁·뇌물 | 관원 대상 청탁·뇌물 기록. 단순 이득 동기는 해당 없음 |
| E05 | 내부·상급자의 비호 | 상급자·지휘관이 하급자·고발자 편을 들었다는 판단 |
| E06 | 정보 왜곡 보고 | 여론·보고 과정에서 정보가 과장·축소·조작되었다는 판단 |
| E07 | 오류 인지 후 불시정 | 오류를 알고도 바로잡지 않았다는 출처 판단 |
| F01 | 비범인 지목 | 범인으로 지목되었으나 후속 판단에서 혐의가 부정됨 |
| F02 | 구금 | 구금 기록(석방 명령이 전제하는 구금은 `note`·derivation으로 표시) |
| F03 | 유죄 판단·형벌(명령) | 형벌·처분 **명령**. 집행은 `decisions.execution_status`로 분리 |
| F04 | 구금 중 사망 | 구금 상태에서의 사망 기록(직접 인과는 별도) |
| F05 | 혐의 해소 | 공식 판단으로 혐의가 풀림(사후 포함) |
| F06 | 석방(명령) | 석방 명령 |
| R01 | 독립 재검증 | 기존 조사와 분리된 조사자(안핵·암행어사)의 조사 |
| R02 | 범행 자백 | 범행 자백의 기록. 자백의 진실성은 `claim_status` |
| R03 | 제3자 진술 변경 | 증인의 진술 번복 기록 |
| R04 | 신규 물증 | 재조사에서 새 물증 확보 기록 |
| R05 | 모순 발견 | 진술·보고 간 모순을 지적한 기록 |
| R06 | 가족·피의자·피해자 측 호소 | 격쟁·상언·고발 기록 |

### fault_type (관료 과실의 성격 분리)

`DELIBERATE_COLLUSION`(고의적 사전 공모; 현재 0건) · `DELIBERATE_PER_JUDGMENT`(판단상 고의, 공모 아님) · `NEGLIGENT_SUPERVISION`(부실한 감독·태만) · `ERRONEOUS_REPORT`(공식 보고의 오류) · `UNRESOLVED_DELIBERATE_VS_NEGLIGENT`(구분 불가) · `NOT_DELIBERATE_PER_INSPECTOR` · `NA`.

## 5. 인물 속성

`person_attributes.csv`는 근거가 있는 속성만 행으로 둔다. 행이 없는 속성은 `NA`이다.

| attribute | 규칙 |
|---|---|
| gender | 친족어(아내·남편·召史·婢·처 등)가 있을 때만(`derivation=KINSHIP_TERM`). 관직 보유로 추정 금지 |
| age_range | 직접 근거만. 현재 0건 |
| birth_year / age | **금지**(검증기가 거부) |
| residence | 출처에 기재된 거주지 |
| status_claimed | 신분 **주장**(예: 이차망 순평군 후손 주장 = CONTESTED) |
| status_verified | DOCUMENTED_ACT + 등급 B 이상 근거 필요. 현재 0건 |
| office / occupation | 기사 시점의 관직·직업(재임 기간은 `appointments.tenure_*`=NOT_RETRIEVED) |
| kinship_marriage | 가족·혼인 관계(촌수 미상이면 명시) |
| death | 사망 시점 범위(사망 뒤 행위 검사에 사용) |

## 6. 관계 유형

필수 7종: KINSHIP · MARRIAGE · PATRONAGE · BRIBERY · COMMAND · TESTIMONY_INFLUENCE · INFORMATION_TRANSFER. 보조: ALLEGED_ILLICIT_LIAISON · HOUSEHOLD_SERVICE · ACQUAINTANCE · ACQUAINTANCE_DENIED · CONFLICT. 모든 관계 행은 `span_ids`·`time_scope`·`claim_status`를 가져야 하며, 상대가 미식별(NA)인 친족관계는 확정 상태로 코딩할 수 없다.

## 7. 증거 등급

| 등급 | 운반 문서 | 의미 |
|---|---|---|
| A | (없음) | 연구자가 로컬로 제공한 공식 원문 직접 인용. 현재 0건 |
| B | `official_annals_article_digests.md`, GuSoon `01`·`05` | 공식 기사 의역(PARAPHRASE_ONLY) 또는 출처충실 선행 코딩 |
| C | `offline_evidence_pack.md`, `offline_claim_seeds.csv`, `source_register.csv`, `research_brief.md` | 공식 출처 위치를 밝힌 연구 요약·레지스터 메타데이터 |
| D | `imported/chamang/pyeongsan_case_report.md` | 선행 2차 종합 보고서 |
| CONTEXT | GuSoon `02`·`03` | 제도·환경 맥락(코딩 근거 불가) |
| X | 레지스터 URL 자체 | 링크만 존재(근거 불가) |

`span_grade`는 한 항목의 근거 span 중 가장 높은 등급이다. 합성 비교는 B·C·D 컷오프별로 다시 계산한다.

## 8. 날짜

모든 날짜는 사료의 역법(대부분 LUNAR) 그대로 `YYYY`, `YYYY-MM`, `YYYY-MM-DD`로 적고 정밀도(`DAY/MONTH/YEAR/RANGE/UNKNOWN`)와 근거(`date_basis`)를 둔다. 양력 환산은 저장소에 환산표가 없어 수행하지 않았다(NOT_COMPUTED). 순서가 확정되지 않은 사건쌍에는 순서를 만들지 않는다.

## 9. 목표함수 Y1~Y6

수준 규칙은 `config/objectives.toml`에 있다(사람이 수정하는 설계 기준). Y3·Y4·Y5·Y6은 hard gate(초깃값 PARTIAL 이상), Y1·Y2는 결말 설계 목표다. 실제 사건(A 전략)에는 진범 확정을 이식할 수 없으므로 Y1 FULL은 B·C의 창작 요소로만 가능하다.
