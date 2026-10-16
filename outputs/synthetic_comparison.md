# B 전략 — 네 사건 메커니즘을 결합한 새 가상 사건 합성 (A·C와 비교)

> 자동 생성 문서(`python -m historinference report`). 모든 수치는 `data/normalized`·`models`·`data/audit`에서 재계산된다. 원문 미보관(UNAVAILABLE_SOURCE_TEXT) 상태에서 로컬 요약·선행 코딩만으로 작성되었으며, 확률·빈도 추정은 하지 않는다.

**형태분석(morphological analysis)**: 12개 차원(`models/synthesis/morphological_box.csv`, 51행)에서 차원마다 값 하나(또는 없음)를 고른다. 각 값은 특정 사건의 코딩 행·span으로 추적된다(`inspiration_trace`). **CSP**: 20개 호환 규칙(`compatibility_rules.csv`)으로 상호 모순 조합을 제거한다. **오컴의 면도날**: 요소 하나를 빼도 목표 수준과 CSP가 그대로인 설계는 그 축소판에 지배되므로 제외한다(최소 설계). 인물·장소는 모두 가상이며 실존 인물에 창작된 범행·공모를 귀속하지 않는다.

## 탐색 규모

| 항목 | 값 |
|---|---|
| 형태 상자 행(등급 ≤D) | 51 |
| CSP·gate(약한 변형) 통과 B 설계 | 580128 |
| 그중 최소 설계(오컴 필터) | 16932 |
| 기본 gate 통과: A / B / C | 89 / 11424 / 1 |
| 기본 gate Pareto 전선(대표 설계 수) | 51 (A 7 · B 43 · C 1) |

## 기본 설정 Pareto 전선(증거 ≤D, 기본 gate)

Pareto 우세는 목표 수준(최대화)과 8개 비용(최소화)의 성분별 비교로만 정한다. 가중치를 쓰지 않는다. 같은 벡터의 설계는 대표 1개로 묶었다.

| 설계 | 전략 | 앵커 | Y1 | Y2 | Y3 | Y4 | Y5 | Y6 | 가정 심각도 | 출처 없는 창작 | 교차 사건 인과연결 | 2차 종합 전용 | 논쟁 메커니즘의 사실화 | 시대 위험 | 역사 덧씌우기 | 실존인물 귀속 위험 | 출처 사건 | 동치 설계 수 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| B-013736 | B | NONE | F | F | F | F | F | F | 13 | 1 | 2 | 3 | 0 | 0 | 0 | 0 | CHOI\|FICTION\|YE | 2 |
| B-013258 | B | NONE | F | F | F | F | F | F | 13 | 1 | 3 | 1 | 0 | 0 | 0 | 0 | CHO\|CHOI\|FICTION | 8 |
| C-000001 | C | NONE | F | F | F | F | F | F | 22 | 11 | 0 | 0 | 0 | 0 | 0 | 0 | FICTION | 1 |
| B-013708 | B | NONE | F | F | F | F | F | P | 13 | 1 | 2 | 2 | 0 | 0 | 0 | 0 | CHOI\|FICTION\|YE | 2 |
| B-013254 | B | NONE | F | F | F | F | F | P | 13 | 1 | 3 | 0 | 0 | 0 | 0 | 0 | CHO\|CHOI\|FICTION | 14 |
| B-014107 | B | NONE | F | F | F | P | F | F | 12 | 1 | 2 | 3 | 0 | 0 | 0 | 0 | CHOI\|FICTION\|YE | 2 |
| B-013327 | B | NONE | F | F | F | P | F | F | 12 | 1 | 3 | 1 | 0 | 0 | 0 | 0 | CHO\|CHOI\|FICTION | 12 |
| B-014051 | B | NONE | F | F | F | P | F | P | 12 | 1 | 2 | 2 | 0 | 0 | 0 | 0 | CHOI\|FICTION\|YE | 2 |
| B-013319 | B | NONE | F | F | F | P | F | P | 12 | 1 | 3 | 0 | 0 | 0 | 0 | 0 | CHO\|CHOI\|FICTION | 15 |
| B-013367 | B | NONE | F | F | F | P | P | P | 11 | 1 | 2 | 0 | 0 | 0 | 0 | 0 | CHO\|FICTION | 3 |
| B-000011 | B | NONE | P | F | F | F | F | F | 11 | 0 | 2 | 2 | 1 | 0 | 0 | 0 | CHO\|CHOI | 4 |
| B-007086 | B | NONE | P | F | F | F | F | F | 13 | 0 | 3 | 1 | 1 | 0 | 0 | 0 | CHO\|CHOI\|YE | 14 |
| A-YE-018 | A | YE | P | F | F | F | F | F | 13 | 0 | 4 | 1 | 0 | 0 | 3 | 0 | CHOI\|GUSUN\|YE | 3 |
| B-000003 | B | NONE | P | F | F | F | F | P | 11 | 0 | 2 | 1 | 1 | 0 | 0 | 0 | CHO\|CHOI | 5 |
| B-007056 | B | NONE | P | F | F | F | F | P | 13 | 0 | 3 | 0 | 1 | 0 | 0 | 0 | CHO\|CHOI\|YE | 14 |
| A-YE-017 | A | YE | P | F | F | F | F | P | 13 | 0 | 4 | 0 | 0 | 0 | 3 | 0 | CHOI\|GUSUN\|YE | 3 |
| B-007483 | B | NONE | P | F | F | P | F | F | 12 | 0 | 3 | 1 | 1 | 0 | 0 | 0 | CHO\|CHOI\|YE | 7 |
| B-007423 | B | NONE | P | F | F | P | F | P | 12 | 0 | 3 | 0 | 1 | 0 | 0 | 0 | CHO\|CHOI\|YE | 7 |
| A-GUSUN-003 | A | GUSUN | P | F | P | F | F | F | 5 | 0 | 2 | 1 | 0 | 0 | 1 | 0 | CHOI\|GUSUN | 1 |
| B-010423 | B | NONE | P | F | P | F | F | F | 11 | 0 | 2 | 1 | 0 | 0 | 0 | 0 | CHOI\|GUSUN | 4 |
| A-GUSUN-002 | A | GUSUN | P | F | P | F | F | P | 5 | 0 | 2 | 0 | 0 | 0 | 1 | 0 | CHOI\|GUSUN | 1 |
| B-010419 | B | NONE | P | F | P | F | F | P | 11 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | CHOI\|GUSUN | 4 |
| B-010477 | B | NONE | P | F | P | P | F | F | 10 | 0 | 2 | 1 | 0 | 0 | 0 | 0 | CHOI\|GUSUN | 4 |
| B-010469 | B | NONE | P | F | P | P | F | P | 10 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | CHOI\|GUSUN | 4 |
| A-CHOI-001 | A | CHOI | P | P | F | F | F | F | 0 | 0 | 0 | 7 | 0 | 0 | 0 | 0 | CHOI | 1 |
| B-001823 | B | NONE | P | P | F | F | F | F | 9 | 0 | 0 | 4 | 1 | 0 | 0 | 0 | CHOI | 2 |
| B-002435 | B | NONE | P | P | F | F | F | F | 9 | 0 | 1 | 2 | 1 | 0 | 0 | 0 | CHO\|CHOI | 4 |
| B-008886 | B | NONE | P | P | F | F | F | F | 12 | 0 | 3 | 1 | 1 | 0 | 0 | 0 | CHO\|CHOI\|YE | 14 |
| B-001767 | B | NONE | P | P | F | F | F | P | 9 | 0 | 0 | 3 | 1 | 0 | 0 | 0 | CHOI | 2 |
| B-002427 | B | NONE | P | P | F | F | F | P | 9 | 0 | 1 | 1 | 1 | 0 | 0 | 0 | CHO\|CHOI | 5 |
| B-008856 | B | NONE | P | P | F | F | F | P | 12 | 0 | 3 | 0 | 1 | 0 | 0 | 0 | CHO\|CHOI\|YE | 14 |
| B-009283 | B | NONE | P | P | F | P | F | F | 11 | 0 | 3 | 1 | 1 | 0 | 0 | 0 | CHO\|CHOI\|YE | 7 |
| B-009223 | B | NONE | P | P | F | P | F | P | 11 | 0 | 3 | 0 | 1 | 0 | 0 | 0 | CHO\|CHOI\|YE | 7 |
| B-012443 | B | NONE | P | P | P | F | F | F | 10 | 0 | 2 | 1 | 0 | 0 | 0 | 0 | CHOI\|GUSUN | 4 |
| B-012439 | B | NONE | P | P | P | F | F | P | 10 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | CHOI\|GUSUN | 4 |
| B-012497 | B | NONE | P | P | P | P | F | F | 9 | 0 | 2 | 1 | 0 | 0 | 0 | 0 | CHOI\|GUSUN | 2 |
| B-012489 | B | NONE | P | P | P | P | F | P | 9 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | CHOI\|GUSUN | 2 |
| B-003374 | B | NONE | N | F | F | F | F | F | 11 | 0 | 2 | 1 | 0 | 0 | 0 | 0 | CHO\|CHOI | 4 |
| B-003370 | B | NONE | N | F | F | F | F | P | 11 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | CHO\|CHOI | 7 |
| A-CHO-002 | A | CHO | N | F | F | F | P | P | 5 | 0 | 2 | 0 | 0 | 0 | 1 | 1 | CHO\|CHOI | 1 |
| B-003443 | B | NONE | N | F | F | P | F | F | 10 | 0 | 2 | 1 | 0 | 0 | 0 | 0 | CHO\|CHOI | 4 |
| B-003435 | B | NONE | N | F | F | P | F | P | 10 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | CHO\|CHOI | 5 |
| A-CHO-001 | A | CHO | N | F | F | P | P | P | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | CHO | 1 |
| B-003852 | B | NONE | N | P | F | F | F | F | 10 | 0 | 1 | 3 | 0 | 0 | 0 | 0 | CHO\|CHOI | 2 |
| B-005166 | B | NONE | N | P | F | F | F | F | 10 | 0 | 2 | 1 | 0 | 0 | 0 | 0 | CHO\|CHOI | 4 |
| B-003824 | B | NONE | N | P | F | F | F | P | 10 | 0 | 1 | 2 | 0 | 0 | 0 | 0 | CHO\|CHOI | 2 |
| B-005162 | B | NONE | N | P | F | F | F | P | 10 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | CHO\|CHOI | 7 |
| B-004223 | B | NONE | N | P | F | P | F | F | 9 | 0 | 1 | 3 | 0 | 0 | 0 | 0 | CHO\|CHOI | 2 |
| B-005235 | B | NONE | N | P | F | P | F | F | 9 | 0 | 2 | 1 | 0 | 0 | 0 | 0 | CHO\|CHOI | 4 |
| B-004167 | B | NONE | N | P | F | P | F | P | 9 | 0 | 1 | 2 | 0 | 0 | 0 | 0 | CHO\|CHOI | 2 |
| B-005227 | B | NONE | N | P | F | P | F | P | 9 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | CHO\|CHOI | 5 |

## 대안 제시(프로필별 사전식 선택 — 점수 아님)

| 프로필 | 설계 | 전략 | 목표 수준 | 심각도 | 창작 | 교차연결 |
|---|---|---|---|---|---|---|
| fidelity_first | A-CHO-001 | A | Y1=NONE Y2=FULL Y3=FULL Y4=PARTIAL Y5=PARTIAL Y6=PARTIAL | 0 | 0 | 0 |
| goal_first | B-013736 | B | Y1=FULL Y2=FULL Y3=FULL Y4=FULL Y5=FULL Y6=FULL | 13 | 1 | 2 |
| parsimony_first | A-CHOI-001 | A | Y1=PARTIAL Y2=PARTIAL Y3=FULL Y4=FULL Y5=FULL Y6=FULL | 0 | 0 | 0 |

- fidelity_first: 출처 없는 창작 → 논쟁 사실화 → 실존인물 위험 → 덧씌우기 → 2차 종합 → 심각도 순
- goal_first: Y3·Y4·Y5·Y6·Y1·Y2 수준 → 심각도 순
- parsimony_first: 심각도 → 교차연결 → 창작 순


### B-013736 — inspiration_trace

Y1=FULL Y2=FULL Y3=FULL Y4=FULL Y5=FULL Y6=FULL · 권장 배경 연도(가상) 1789 · 출처 사건 CHOI|FICTION|YE

| 차원 | 값 | 출처 사건 | 코딩 행 | span | 출처 상태 |
|---|---|---|---|---|---|
| M1_TRIGGER | T_RUMOR_ACCUSATION | CHOI | MC-CH-26 | CH-S33\|CH-S52 | RECORDED_TESTIMONY |
| M3_TESTIMONY | W_URGED_SERVANT | CHOI | MC-CH-03 | CH-S38 | RECORDED_TESTIMONY |
| M2_FIRST_ERROR | D_PROVINCIAL_NEGLIGENT | CHOI | MC-CH-02 | CH-S04 | OFFICIAL_JUDGMENT |
| M6_TARGET_FATE | X_DETAINED_RELEASED | CHOI | MC-CH-12\|MC-CH-17 | CH-S34\|CH-S07\|CH-S13 | DOCUMENTED_ACT |
| M7_APPEAL | P_VICTIM_FAMILY_PETITION | CHOI | MC-CH-25\|MC-CH-26 | CH-S27\|CH-S28\|CH-S33 | DOCUMENTED_ACT |
| M8_REVERIFICATION | V_SPECIAL_INSPECTOR | CHOI | MC-CH-18 | CH-S03\|CH-S12 | DOCUMENTED_ACT |
| M9_SECOND_ORDER | S_ROYAL_DOUBT_OF_REVERIFICATION | CHOI | MC-CH-22 | CH-S08\|CH-S14\|CH-S42 | DOCUMENTED_ACT |
| M11_RESOLUTION | U_FICTIONAL_PROVEN_CULPRIT | FICTION | - | - | FICTION_ONLY |
| M10A_PERPETRATOR_ACCOUNTABILITY | K_PERPETRATOR_EXILED | YE | MC-YE-07 | YE-S19\|YE-S08 | DOCUMENTED_ACT |
| M10B_OFFICIAL_ACCOUNTABILITY | K_OFFICIAL_SANCTIONED | YE | MC-YE-08 | YE-S19 | DOCUMENTED_ACT |

**가상 서사 골격(FICTION_ONLY · 실존 인물·실제 사건 아님)** — 인물은 역할명(가상 고발자·가상 피의자 등)으로만 둔다.

1. 발단: 간통 소문과 피해자 가족 고발 — CHOI에서 착안
2. 진술 오염: 종용받은 비(婢)의 지목 — CHOI에서 착안
3. 최초 판단의 오류: 도신의 불성실 조사 — CHOI에서 착안
4. 무고 표적의 운명: 무고 피의자 구금 후 석방 — CHOI에서 착안
5. 이의제기: 피해자 가족의 고발·격쟁 — CHOI에서 착안
6. 재검증: 별도 안핵(암행어사) — CHOI에서 착안
7. 재검증의 재검증: 안핵 결론 자체를 국왕이 재의문 — CHOI에서 착안
8. 진상 결말: 진범이 증거로 확정됨(어느 사건에서도 기록 없음) — 출처 없음(창작)
9. 가해자 책임: 가해 관원 유배 — YE에서 착안
10. 관료 책임: 관찰사 삭직 — YE에서 착안

### B-000011 — inspiration_trace

Y1=PARTIAL Y2=FULL Y3=FULL Y4=FULL Y5=FULL Y6=FULL · 권장 배경 연도(가상) 1785 · 출처 사건 CHO|CHOI

| 차원 | 값 | 출처 사건 | 코딩 행 | span | 출처 상태 |
|---|---|---|---|---|---|
| M1_TRIGGER | T_KIN_INFORMER_GAIN | CHO | MC-JH-08 | JH-S01\|JH-S03 | OFFICIAL_JUDGMENT |
| M2_FIRST_ERROR | D_PROVINCIAL_NEGLIGENT | CHOI | MC-CH-02 | CH-S04 | OFFICIAL_JUDGMENT |
| M6_TARGET_FATE | X_DETAINED_RELEASED | CHOI | MC-CH-12\|MC-CH-17 | CH-S34\|CH-S07\|CH-S13 | DOCUMENTED_ACT |
| M7_APPEAL | P_VICTIM_FAMILY_PETITION | CHOI | MC-CH-25\|MC-CH-26 | CH-S27\|CH-S28\|CH-S33 | DOCUMENTED_ACT |
| M8_REVERIFICATION | V_SPECIAL_INSPECTOR | CHOI | MC-CH-18 | CH-S03\|CH-S12 | DOCUMENTED_ACT |
| M9_SECOND_ORDER | S_ROYAL_DOUBT_OF_REVERIFICATION | CHOI | MC-CH-22 | CH-S08\|CH-S14\|CH-S42 | DOCUMENTED_ACT |
| M11_RESOLUTION | U_CONFESSION_LATER_DOUBTED | CHOI | MC-CH-19 | CH-S39\|CH-S48 | CONTESTED |
| M10A_PERPETRATOR_ACCOUNTABILITY | K_ACCUSER_PUNISHED | CHO | MC-JH-13 | JH-S08\|JH-S18 | DOCUMENTED_ACT |
| M10B_OFFICIAL_ACCOUNTABILITY | K_OFFICIAL_SANCTIONED | CHO | - | JH-S08\|JH-S18 | DOCUMENTED_ACT |

**가상 서사 골격(FICTION_ONLY · 실존 인물·실제 사건 아님)** — 인물은 역할명(가상 고발자·가상 피의자 등)으로만 둔다.

1. 발단: 피해자 먼 친척의 이득 목적 고발 — CHO에서 착안
2. 최초 판단의 오류: 도신의 불성실 조사 — CHOI에서 착안
3. 무고 표적의 운명: 무고 피의자 구금 후 석방 — CHOI에서 착안
4. 이의제기: 피해자 가족의 고발·격쟁 — CHOI에서 착안
5. 재검증: 별도 안핵(암행어사) — CHOI에서 착안
6. 재검증의 재검증: 안핵 결론 자체를 국왕이 재의문 — CHOI에서 착안
7. 진상 결말: 자백으로 종결 후 재의문 — CHOI에서 착안
8. 가해자 책임: 조작 고발자 처벌 — CHO에서 착안
9. 관료 책임: 관찰사 파직 — CHO에서 착안

## C — 완전 창작 baseline

모든 목표를 작가 선언으로 FULL로 만들 수 있지만 출처 추적 요소가 0이고 심각도가 가장 높다. 비교 기준선으로만 기록한다.

| 설계 | 전략 | 앵커 | Y1 | Y2 | Y3 | Y4 | Y5 | Y6 | 가정 심각도 | 출처 없는 창작 | 교차 사건 인과연결 | 2차 종합 전용 | 논쟁 메커니즘의 사실화 | 시대 위험 | 역사 덧씌우기 | 실존인물 귀속 위험 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| C-000001 | C | NONE | F | F | F | F | F | F | 22 | 11 | 0 | 0 | 0 | 0 | 0 | 0 |

## 민감도 분석

### 증거 등급 컷오프 × hard gate 변형

| 등급 | gate 변형 | B 최소 설계 | 통과 A/B/C | Pareto A/B/C | fidelity_first | goal_first | parsimony_first |
|---|---|---|---|---|---|---|---|
| B | default | 360 | 22/120/1 | 1/11/1 | A-CHO-001 | C-000001 | A-CHO-001 |
| B | Y3_FULL | 360 | 11/45/1 | 1/7/1 | A-CHO-001 | C-000001 | A-CHO-001 |
| B | Y6_FULL | 360 | 0/0/1 | 0/0/1 | C-000001 | C-000001 | C-000001 |
| B | no_Y6_gate | 360 | 266/360/1 | 2/20/1 | A-GUSUN-001 | C-000001 | A-GUSUN-001 |
| C | default | 3760 | 197/2000/1 | 8/13/1 | A-CHOI-001 | C-000001 | A-CHOI-001 |
| C | Y3_FULL | 3760 | 189/800/1 | 7/9/1 | A-CHOI-001 | C-000001 | A-CHOI-001 |
| C | Y6_FULL | 3760 | 0/0/1 | 0/0/1 | C-000001 | C-000001 | C-000001 |
| C | no_Y6_gate | 3760 | 219/3760/1 | 10/24/1 | A-GUSUN-001 | C-000001 | A-GUSUN-001 |
| D | default | 16932 | 89/11424/1 | 7/43/1 | A-CHO-001 | B-013736 | A-CHOI-001 |
| D | Y3_FULL | 16932 | 59/4712/1 | 5/35/1 | A-CHO-001 | B-013736 | A-CHOI-001 |
| D | Y6_FULL | 16932 | 44/5508/1 | 3/21/1 | B-012497 | B-013736 | A-CHOI-001 |
| D | no_Y6_gate | 16932 | 132/16932/1 | 9/63/1 | A-GUSUN-001 | B-013736 | A-CHOI-001 |

### 가중합 보조 화면(설정 의존; 연구 결과 아님)

`config/objectives.toml`의 5개 그룹(목표·충실성·정합성·개연성·간결성) 가중치를 [0.0, 1.0, 2.0] 격자로 바꿔 Pareto 대표 설계 중 가중합 1위가 되는 비율을 셌다. 이는 가중치 선택이 결론을 얼마나 바꾸는지 보여 주는 민감도이며 확률이나 순위 점수가 아니다.

| 설계 | 전략 | 1위 횟수 | 격자 크기 | 비율 |
|---|---|---|---|---|
| A-CHO-001 | A | 96 | 242 | 0.3967 |
| C-000001 | C | 56 | 242 | 0.2314 |
| A-CHOI-001 | A | 51 | 242 | 0.2107 |
| B-013258 | B | 24 | 242 | 0.0992 |
| B-013254 | B | 6 | 242 | 0.0248 |
| B-012489 | B | 6 | 242 | 0.0248 |
| B-013736 | B | 3 | 242 | 0.0124 |

## A 대 B 비교 결론

- 기본 설정 Pareto 전선에 A 7개, B 43개, C 1개가 공존한다. **어느 전략도 다른 전략을 전면 지배하지 않는다.**
- A(앵커)는 실제 기록을 제자리에서 쓰므로 가정 심각도·교차 사건 연결이 가장 낮다(이식 없는 앵커는 심각도 0). 대신 Y1(진범 규명)은 최대 PARTIAL이며, gate를 채우려면 이식이 필요하고 이식마다 실제 사건 위에 다른 사건을 덧씌우는 비용(심각도 3)이 든다.
- B(합성)는 Y1·Y2를 FULL로 설계할 수 있지만, 그때 '진범이 증거로 확정됨' 요소는 네 사건 어디에도 근거가 없는 창작이다. 출처 추적 요소만 쓰는 B 설계는 Y1이 PARTIAL에 머물고 교차 사건 인과연결(가설)이 늘어난다.
- 따라서 선택은 '역사적 앵커의 충실성' 대 '기획의도의 완결성' 사이의 교환이며, 이 교환의 위치는 `config/objectives.toml`의 gate·가중치(사람의 설정)에 달려 있다.
- 증거 등급을 B로 제한하면 B 최소 설계가 360개로 줄고 gate 통과 앵커는 `CHO|CHOI`가 된다: 결론은 원문 확보 수준에 민감하다.

## CSP 호환 규칙

| ID | 조건 차원 | 조건 값 | 요구 차원 | 요구 값 | 근거 |
|---|---|---|---|---|---|
| CR-01 | M10A_PERPETRATOR_ACCOUNTABILITY | K_ACCUSER_PUNISHED | M1_TRIGGER | T_KIN_INFORMER_GAIN\|T_GRUDGE_NAMING | 처벌될 조작 고발자가 있어야 함(피해자 가족의 선의 고발은 제외) |
| CR-02 | M10A_PERPETRATOR_ACCOUNTABILITY | K_PERPETRATOR_EXILED | M1_TRIGGER\|M11_RESOLUTION | T_OFFICIAL_VIOLENCE\|U_FICTIONAL_PROVEN_CULPRIT | 가해자가 특정되어야 유배 가능 |
| CR-03 | M6_TARGET_FATE | X_DETAINED_RELEASED\|X_DIED_IN_CUSTODY | M1_TRIGGER\|M3_TESTIMONY\|M4_OPINION | T_KIN_INFORMER_GAIN\|T_GRUDGE_NAMING\|W_URGED_SERVANT\|W_PROCURED_WITNESSES\|W_COACHED_DETAINEE\|W_THREAT_RETRACTION\|O_VILLAGE_SONG\|O_RUMOR_ACCUMULATION\|O_SERVANT_RUMOR | 무고 표적이 생기려면 악의적 고발 또는 진술·여론 오염 경로가 필요(YE 원사건에는 무고 대체범 없음) |
| CR-04 | M9_SECOND_ORDER | S_ROYAL_DOUBT_OF_REVERIFICATION | M8_REVERIFICATION | V_SPECIAL_INSPECTOR\|V_ROYAL_REVIEW | 재검증을 다시 의심하려면 선행 재검증 필요 |
| CR-05 | M9_SECOND_ORDER | S_CONFLICTING_INSPECTORS | M8_REVERIFICATION | V_SPECIAL_INSPECTOR | 복수 조사자 충돌은 별도 조사자 필요 |
| CR-06 | M9_SECOND_ORDER | S_CENTRAL_REEVALUATION | M8_REVERIFICATION | V_SPECIAL_INSPECTOR | 안핵 재평가는 안핵 필요 |
| CR-07 | M11_RESOLUTION | U_NO_SEPARATE_CULPRIT | M10A_PERPETRATOR_ACCOUNTABILITY | K_ACCUSER_PUNISHED\|K_NONE | 진범 미확정이면 범행자 유배·의문 속 형벌 불가(고발자 처벌은 가능) |
| CR-08 | M11_RESOLUTION | U_CONFESSION_LATER_DOUBTED | M9_SECOND_ORDER | S_ROYAL_DOUBT_OF_REVERIFICATION | 자백 재의문은 2차 의심 구조 필요 |
| CR-09 | M3_TESTIMONY | W_COACHED_DETAINEE | M6_TARGET_FATE | X_DETAINED_RELEASED\|X_DIED_IN_CUSTODY | 지목 유도는 무고 표적 필요 |
| CR-10 | M4_OPINION | O_VILLAGE_SONG | M1_TRIGGER | T_KIN_INFORMER_GAIN\|T_GRUDGE_NAMING\|T_RUMOR_ACCUSATION | 노래 유포는 고발 측 여론전 필요 |
| CR-11 | M5_OFFICIAL_FAULT | F_SUPERIOR_SHIELDING_ALLEGED | M1_TRIGGER\|M2_FIRST_ERROR | T_OFFICIAL_VIOLENCE\|D_INQUEST_MISJUDGED\|D_REVERSED_FIRST_REPORT | 두둔할 하급 관원의 과오 필요 |
| CR-12 | M5_OFFICIAL_FAULT | F_SIDING_COMMANDER | M1_TRIGGER | T_KIN_INFORMER_GAIN\|T_GRUDGE_NAMING | 편들 고발자 필요 |
| CR-13 | M2_FIRST_ERROR | D_DEFENSIVE_REPORT | M1_TRIGGER\|M5_OFFICIAL_FAULT | T_OFFICIAL_VIOLENCE\|F_SUPERIOR_SHIELDING_ALLEGED | 면책성 보고는 방어할 관원 필요 |
| CR-14 | M7_APPEAL | P_SPOUSE_PETITION_REPRESSED | M6_TARGET_FATE | X_DETAINED_RELEASED\|X_DIED_IN_CUSTODY | 피의자 처의 호소는 구금된 피의자 필요 |
| CR-15 | M7_APPEAL | P_KIN_ACCUSATION_HEARD | M1_TRIGGER | T_KIN_INFORMER_GAIN | 친척 고발 경로 필요 |
| CR-16 | M11_RESOLUTION | U_CAUSATION_UNRESOLVED | M6_TARGET_FATE | X_DIED_IN_CUSTODY | 직접 인과 미확정은 구금 중 사망 구조 |
| CR-17 | M11_RESOLUTION | U_OFFICIAL_PERPETRATOR_CONTESTED | M1_TRIGGER | T_OFFICIAL_VIOLENCE | 관원 가해 구조 필요 |
| CR-18 | M5_OFFICIAL_FAULT | F_COLLUSION_FICTION | M2_FIRST_ERROR | D_INQUEST_MISJUDGED\|D_PROVINCIAL_NEGLIGENT\|D_DEFENSIVE_REPORT\|D_REVERSED_FIRST_REPORT | 공모는 왜곡된 공식 판단으로 드러나야 함 |
| CR-19 | M1_TRIGGER | T_RUMOR_ACCUSATION | M3_TESTIMONY\|M4_OPINION | W_URGED_SERVANT\|W_PROCURED_WITNESSES\|W_COACHED_DETAINEE\|W_THREAT_RETRACTION\|O_VILLAGE_SONG\|O_RUMOR_ACCUMULATION\|O_SERVANT_RUMOR | 선의 고발에서 무고가 생기려면 진술·여론 오염 경로 필요 |
| CR-20 | M11_RESOLUTION | U_FICTIONAL_PROVEN_CULPRIT | M10A_PERPETRATOR_ACCOUNTABILITY | K_PERPETRATOR_EXILED\|K_ACCUSER_PUNISHED | 확정 진범은 책임 처분과 짝 |
