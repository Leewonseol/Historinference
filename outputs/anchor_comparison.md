# A 전략 — 역사적 사건 하나를 앵커로 삼아 다른 사건 메커니즘을 이식

> 자동 생성 문서(`python -m historinference report`). 모든 수치는 `data/normalized`·`models`·`data/audit`에서 재계산된다. 원문 미보관(UNAVAILABLE_SOURCE_TEXT) 상태에서 로컬 요약·선행 코딩만으로 작성되었으며, 확률·빈도 추정은 하지 않는다.

각 사건을 앵커 후보로 동등하게 놓았다(최아지를 사전 승자로 고정하지 않음). 앵커의 문서화된 메커니즘 값은 그대로 두고, **값이 없는(미확인) 차원에만** 다른 사건의 메커니즘을 이식할 수 있다. 문서화된 값을 바꾸는 이식, 출처 없는 창작 요소(진범 확정 등)의 이식은 CSP에서 금지한다(실제 사건에 유죄 확정을 위조하지 않음). 이식 1건마다 '역사 덧씌우기' 심각도 3을 부과하고, 이식된 역할이 앵커에 이미 실존 인물로 있는 경우(예: 국왕·관찰사) 실존인물 귀속 위험 1을 센다.

평가 기준: 기획의도 Y1~Y6 수준(`config/objectives.toml`), 사료 충실성(2차 종합 전용 요소·논쟁 메커니즘 사실화), 인과적 정합성(CSP 위반 0·교차 사건 인과연결 수), 역사적 개연성(제도 단절점 위험), 불필요한 가정(심각도 합). hard gate: Y3≥PARTIAL, Y4≥PARTIAL, Y5≥PARTIAL, Y6≥PARTIAL.

## 앵커 원형(이식 없음)

| 설계 | 전략 | 앵커 | Y1 | Y2 | Y3 | Y4 | Y5 | Y6 | 가정 심각도 | 출처 없는 창작 | 교차 사건 인과연결 | 2차 종합 전용 | 논쟁 메커니즘의 사실화 | 시대 위험 | 역사 덧씌우기 | 실존인물 귀속 위험 | 요소 수 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| A-CHOI-001 | A | CHOI | P | P | F | F | F | F | 0 | 0 | 0 | 7 | 0 | 0 | 0 | 0 | 14 |
| A-CHO-001 | A | CHO | N | F | F | P | P | P | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 12 |
| A-YE-001 | A | YE | P | F | N | F | F | N | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 8 |
| A-GUSUN-001 | A | GUSUN | P | F | P | F | F | N | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 15 |

- **CHOI**: Y1=PARTIAL Y2=PARTIAL Y3=FULL Y4=FULL Y5=FULL Y6=FULL — hard gate 통과
- **CHO**: Y1=NONE Y2=FULL Y3=FULL Y4=PARTIAL Y5=PARTIAL Y6=PARTIAL — hard gate 통과
- **YE**: Y1=PARTIAL Y2=FULL Y3=NONE Y4=FULL Y5=FULL Y6=NONE — hard gate 미달
- **GUSUN**: Y1=PARTIAL Y2=FULL Y3=PARTIAL Y4=FULL Y5=FULL Y6=NONE — hard gate 미달

## 앵커별 이식 설계 수와 최선 대안

| 앵커 | CSP 통과 설계 | hard gate 통과 | 통과에 필요한 최소 이식 수 | 기본 Pareto 전선 내 설계 수 |
|---|---|---|---|---|
| CHOI 평산 최아지·이차망(1785–1789) | 1 | 1 | 0 | 1 |
| CHO 배천 조재항(1780/1781–1783) | 2 | 2 | 0 | 2 |
| YE 창원 이여절·조진택(1793–1795) | 150 | 84 | 3 | 2 |
| GUSUN 구순–김명신(1793) | 3 | 2 | 1 | 2 |

## 기본 설정(증거 등급 ≤D, 기본 gate) Pareto 전선의 A 설계

| 설계 | 전략 | 앵커 | Y1 | Y2 | Y3 | Y4 | Y5 | Y6 | 가정 심각도 | 출처 없는 창작 | 교차 사건 인과연결 | 2차 종합 전용 | 논쟁 메커니즘의 사실화 | 시대 위험 | 역사 덧씌우기 | 실존인물 귀속 위험 | 이식 행 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| A-YE-018 | A | YE | P | F | F | F | F | F | 13 | 0 | 4 | 1 | 0 | 0 | 3 | 0 | MB-17\|MB-24\|MB-28 |
| A-YE-017 | A | YE | P | F | F | F | F | P | 13 | 0 | 4 | 0 | 0 | 0 | 3 | 0 | MB-17\|MB-24\|MB-27 |
| A-GUSUN-003 | A | GUSUN | P | F | P | F | F | F | 5 | 0 | 2 | 1 | 0 | 0 | 1 | 0 | MB-28 |
| A-GUSUN-002 | A | GUSUN | P | F | P | F | F | P | 5 | 0 | 2 | 0 | 0 | 0 | 1 | 0 | MB-27 |
| A-CHOI-001 | A | CHOI | P | P | F | F | F | F | 0 | 0 | 0 | 7 | 0 | 0 | 0 | 0 |  |
| A-CHO-002 | A | CHO | N | F | F | F | P | P | 5 | 0 | 2 | 0 | 0 | 0 | 1 | 1 | MB-35 |
| A-CHO-001 | A | CHO | N | F | F | P | P | P | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |

- A-YE-018 이식: MB-17 O_SERVANT_RUMOR@GUSUN(행랑 하인을 통한 소문 유포(보고된 진술)); MB-24 X_DETAINED_RELEASED@CHOI(무고 피의자 구금 후 석방); MB-28 P_VICTIM_FAMILY_PETITION@CHOI(피해자 가족의 고발·격쟁)

- A-YE-017 이식: MB-17 O_SERVANT_RUMOR@GUSUN(행랑 하인을 통한 소문 유포(보고된 진술)); MB-24 X_DETAINED_RELEASED@CHOI(무고 피의자 구금 후 석방); MB-27 P_SPOUSE_PETITION_REPRESSED@CHOI(피의자 처의 격쟁과 억압 명령)

- A-GUSUN-003 이식: MB-28 P_VICTIM_FAMILY_PETITION@CHOI(피해자 가족의 고발·격쟁)

- A-GUSUN-002 이식: MB-27 P_SPOUSE_PETITION_REPRESSED@CHOI(피의자 처의 격쟁과 억압 명령)

- A-CHO-002 이식: MB-35 S_ROYAL_DOUBT_OF_REVERIFICATION@CHOI(안핵 결론 자체를 국왕이 재의문)

## 증거 등급·gate 민감도

증거 등급 컷오프 B는 공식 기사 의역·선행 코딩만, C는 연구 요약까지, D는 2차 종합(Chamang 보고서)까지 허용한다.

| 등급 컷오프 | gate 변형 | gate 통과 앵커 | 이식 없이 통과한 앵커 | Pareto 내 A 설계 |
|---|---|---|---|---|
| B | default | CHO\|CHOI | CHO | 1 |
| B | Y3_FULL | CHO\|CHOI | CHO | 1 |
| B | Y6_FULL | NONE | NONE | 0 |
| B | no_Y6_gate | CHO\|CHOI\|GUSUN | CHO\|GUSUN | 2 |
| C | default | CHO\|CHOI\|GUSUN\|YE | CHO\|CHOI | 8 |
| C | Y3_FULL | CHO\|CHOI\|YE | CHO\|CHOI | 7 |
| C | Y6_FULL | NONE | NONE | 0 |
| C | no_Y6_gate | CHO\|CHOI\|GUSUN\|YE | CHO\|CHOI\|GUSUN | 10 |
| D | default | CHO\|CHOI\|GUSUN\|YE | CHO\|CHOI | 7 |
| D | Y3_FULL | CHO\|CHOI\|YE | CHO\|CHOI | 5 |
| D | Y6_FULL | CHOI\|GUSUN\|YE | CHOI | 3 |
| D | no_Y6_gate | CHO\|CHOI\|GUSUN\|YE | CHO\|CHOI\|GUSUN | 9 |

## 해석

- **CHOI 평산 최아지·이차망(1785–1789)** — Y1=PARTIAL Y2=PARTIAL Y3=FULL Y4=FULL Y5=FULL Y6=FULL; 2차 종합 전용 요소 7개; 이식 없이 hard gate 통과.
- **CHO 배천 조재항(1780/1781–1783)** — Y1=NONE Y2=FULL Y3=FULL Y4=PARTIAL Y5=PARTIAL Y6=PARTIAL; 2차 종합 전용 요소 0개; 이식 없이 hard gate 통과.
- **YE 창원 이여절·조진택(1793–1795)** — Y1=PARTIAL Y2=FULL Y3=NONE Y4=FULL Y5=FULL Y6=NONE; 2차 종합 전용 요소 0개; gate 미달 Y3, Y6.
- **GUSUN 구순–김명신(1793)** — Y1=PARTIAL Y2=FULL Y3=PARTIAL Y4=FULL Y5=FULL Y6=NONE; 2차 종합 전용 요소 0개; gate 미달 Y6.
- 증거 등급을 B(공식 기사 의역·선행 코딩)로 제한하면 이식 없이 gate를 통과하는 앵커는 `CHO`이다. CHOI의 강점(피해자 가족 격쟁·재검증의 재의문)은 상당 부분 2차 종합(D) 근거에 기대므로 원문 확보(RQ-CH-01/02) 전까지 잠정적이다.
- 어떤 앵커도 Y1(진범 규명)을 FULL로 만들 수 없다: 네 사건 모두 진범이 증거로 확정된 기록이 없고, A 전략은 실제 사건에 유죄 확정을 이식하지 않는다.
