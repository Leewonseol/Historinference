# 증거 행렬 — 사건 × 메커니즘 코드

> 자동 생성 문서(`python -m historinference report`). 모든 수치는 `data/normalized`·`models`·`data/audit`에서 재계산된다. 원문 미보관(UNAVAILABLE_SOURCE_TEXT) 상태에서 로컬 요약·선행 코딩만으로 작성되었으며, 확률·빈도 추정은 하지 않는다.

셀 표기: `값(claim_status·근거등급)` 목록. `1`=충분히 출처로 지지, `0`=부재가 명시적으로 지지, `NA`=알 수 없음. 값 1은 **그 단위가 해당 메커니즘을 기록·판단했다는 출처 지지**이며, `claim_status`가 CONTESTED/RECORDED_TESTIMONY/OFFICIAL_JUDGMENT이면 내용의 역사적 진실을 확정하지 않는다. 빈 칸은 코딩 단위 자체가 없음(=미확인).

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
| 테스트(pytest, 로컬 Python 실행) | 통과 89 / 실패 0 / 오류 0 / 건너뜀 0 | data/audit/test_results.json (Oracle 실행 아님) |
| 연구자 요청 | 21건 | REQUEST_FOR_RESEARCHER.md |

| 코드 | CHOI | CHO | YE | GUSUN |
|---|---|---|---|---|
| E01 증거 인멸·변조 | NA(HYPOTHESIS·-) | NA(OFFICIAL_JUDGMENT·-) |  | NA(UNKNOWN·-) |
| E02 허위(사실과 다른) 검험·보고 | 1(CONTESTED·D); 1(OFFICIAL_JUDGMENT·B) | 1(OFFICIAL_JUDGMENT·B) | NA(CONTESTED·-) | 1(OFFICIAL_JUDGMENT·B); 1(OFFICIAL_JUDGMENT·B) |
| E03 증언 강요·유도 | 1(RECORDED_TESTIMONY·D); 1(CONTESTED·D); NA(HYPOTHESIS·-) | 1(OFFICIAL_JUDGMENT·B) | NA(UNKNOWN·-) | 1(CONTESTED·B); 1(RECORDED_TESTIMONY·B); 0(OFFICIAL_JUDGMENT·B) |
| E04 청탁·뇌물 | NA(UNKNOWN·-) | NA(OFFICIAL_JUDGMENT·-) |  | NA(UNKNOWN·-) |
| E05 내부·상급자의 비호 | NA(UNKNOWN·-) | NA(UNKNOWN·-) | 1(OFFICIAL_JUDGMENT·B) | 1(OFFICIAL_JUDGMENT·B); NA(CONTESTED·-) |
| E06 정보 왜곡 보고 | NA(UNKNOWN·-) | 1(OFFICIAL_JUDGMENT·B) | 1(OFFICIAL_JUDGMENT·C) | 1(OFFICIAL_JUDGMENT·B); 1(OFFICIAL_JUDGMENT·B); 0(OFFICIAL_JUDGMENT·B) |
| E07 오류 인지 후 불시정 | NA(UNKNOWN·-) | NA(UNKNOWN·-) | NA(UNKNOWN·-) | NA(UNKNOWN·-) |
| F01 비범인 지목 | 1(OFFICIAL_JUDGMENT·C) | 1(OFFICIAL_JUDGMENT·B) | NA(UNKNOWN·-) | 1(OFFICIAL_JUDGMENT·B) |
| F02 구금 | 1(DOCUMENTED_ACT·C) | 1(DOCUMENTED_ACT·B) |  | 1(DOCUMENTED_ACT·B) |
| F03 유죄 판단·형벌(명령) | 1(DOCUMENTED_ACT·D); NA(UNKNOWN·-) | NA(UNKNOWN·-); 1(DOCUMENTED_ACT·B) | 1(DOCUMENTED_ACT·C); 1(DOCUMENTED_ACT·C) | 1(DOCUMENTED_ACT·B); 1(DOCUMENTED_ACT·B) |
| F04 구금 중 사망 | 1(OFFICIAL_JUDGMENT·D) |  |  | 1(DOCUMENTED_ACT·B) |
| F05 혐의 해소 | 1(OFFICIAL_JUDGMENT·C) | 1(OFFICIAL_JUDGMENT·B) |  | 1(OFFICIAL_JUDGMENT·B) |
| F06 석방(명령) | 1(DOCUMENTED_ACT·C) | 1(DOCUMENTED_ACT·B) |  | NA(DOCUMENTED_ACT·-) |
| R01 독립 재검증 | 1(DOCUMENTED_ACT·B) | NA(UNKNOWN·-) | 1(DOCUMENTED_ACT·C) | 1(DOCUMENTED_ACT·B) |
| R02 범행 자백(진실성 별도) | 1(CONTESTED·D) |  |  | NA(UNKNOWN·-) |
| R03 제3자 진술 변경 | 1(RECORDED_TESTIMONY·D) | NA(UNKNOWN·-) |  | 1(RECORDED_TESTIMONY·B); 1(RECORDED_TESTIMONY·B) |
| R04 신규 물증 | NA(RECORDED_TESTIMONY·-) |  |  | NA(UNKNOWN·-) |
| R05 모순 발견 | 1(DOCUMENTED_ACT·C); 1(DOCUMENTED_ACT·C) | 1(DOCUMENTED_ACT·B) | 1(DOCUMENTED_ACT·B); 1(DOCUMENTED_ACT·C) | 1(DOCUMENTED_ACT·B) |
| R06 가족·피의자·피해자 측 호소 | 1(DOCUMENTED_ACT·C); 1(DOCUMENTED_ACT·D); 1(DOCUMENTED_ACT·D) | NA(UNKNOWN·-) | NA(UNKNOWN·-) | NA(UNKNOWN·-) |

## 사건별 코딩 범위

| 사건 | 코딩 행 | 1 | 0 | NA | 1/0이 있는 코드 수(/19) | 사건(events) | 주장(claims) | 인물 |
|---|---|---|---|---|---|---|---|---|
| CHOI 평산 최아지·이차망(1785–1789) | 26 | 18 | 0 | 8 | 13 | 16 | 17 | 17 |
| CHO 배천 조재항(1780/1781–1783) | 17 | 9 | 0 | 8 | 9 | 9 | 10 | 11 |
| YE 창원 이여절·조진택(1793–1795) | 12 | 7 | 0 | 5 | 5 | 7 | 6 | 7 |
| GUSUN 구순–김명신(1793) | 27 | 17 | 2 | 8 | 12 | 16 | 51 | 25 |

## 코딩 행 전체(근거 포함)

| 행 | 사건 | 단위 | 코드 | 값 | claim_status | fault_type | 최고 등급 | span | 근거 설명 |
|---|---|---|---|---|---|---|---|---|---|
| MC-CH-01 | CHOI | EVENT:EV-CH-02 | E02 | 1 | CONTESTED | ERRONEOUS_REPORT | D | CH-S32\|CH-S40\|CH-S30 | 1787 왕명이 검험관의 오류 책임을 따짐; 1789 재의문이 결박흔·방어흔 부재 기록을 다시 문제 삼아 오류 여부 자체가 CONTESTED |
| MC-CH-02 | CHOI | EVENT:EV-CH-05 | E02 | 1 | OFFICIAL_JUDGMENT | NEGLIGENT_SUPERVISION | B | CH-S04\|CH-S54 | 1787 실록 의역: 전 도신들이 조사를 성실히 하지 않은 책임으로 처분(이차망 혐의 고착은 2차 종합) |
| MC-CH-03 | CHOI | RELATION:RL-CH-10 | E03 | 1 | RECORDED_TESTIMONY | NA | D | CH-S38 | 사단이 조광진의 종용으로 이차망을 지목했다고 진술(진술 기록이며 종용의 사실성은 미확정) |
| MC-CH-04 | CHOI | RELATION:RL-CH-11 | E03 | 1 | CONTESTED | NA | D | CH-S26\|CH-S51 | 조봉원 개입 주장; 1789 의문이 증거 충분성을 물음 |
| MC-CH-05 | CHOI | CLAIM:CL-CH-08 | E03 | NA | HYPOTHESIS | NA | D | CH-S45 | 조사자 유도 가능성은 1789 국왕의 의문(가설) |
| MC-CH-06 | CHOI | CLAIM:CL-CH-13 | E04 | NA | UNKNOWN | NA | C | CH-S10\|CH-S51 | 뇌물·5냥은 주장/관의 우려로만 논의; 원문 미보관 → 요청 RQ-CH-03 |
| MC-CH-07 | CHOI | RELATION:RL-CH-13 | E05 | NA | UNKNOWN | NA | C | CH-S10 | 관원-조씨 가문 친족관계 주장만 존재; 관원 미식별 |
| MC-CH-08 | CHOI | EVIDENCE:EI-CH-01 | E01 | NA | HYPOTHESIS | NA | D | CH-S46 | 혈의 위장 여부는 1789 의문(가설) |
| MC-CH-09 | CHOI | EPISODE:CHOI-E2 | E06 | NA | UNKNOWN | NA | B | CH-S04 | 정보 왜곡 의도에 대한 출처 판단 없음(불성실 조사만 기록) |
| MC-CH-10 | CHOI | EPISODE:CHOI-E3 | E07 | NA | UNKNOWN | NA | D | CH-S35\|CH-S36 | 1786 격쟁 억압은 기록되나 당시 오류 인지 여부는 출처 없음 |
| MC-CH-11 | CHOI | PERSON:CHOI-P03 | F01 | 1 | OFFICIAL_JUDGMENT | NA | C | CH-S07\|CH-S13\|CH-S44 | 1787 왕명 석방과 혐의 전가 판단; 실체 진실은 미확정 |
| MC-CH-12 | CHOI | EVENT:EV-CH-06 | F02 | 1 | DOCUMENTED_ACT | NA | C | CH-S34\|CH-S07\|CH-S55 | 이차망·최아지 구금(칼) |
| MC-CH-13 | CHOI | DECISION:DC-CH-08 | F03 | 1 | DOCUMENTED_ACT | NA | D | CH-S43 | 최아지에 대한 장 100·유 2천 리 준용 승인(명령; 집행 미확인) |
| MC-CH-14 | CHOI | PERSON:CHOI-P03 | F03 | NA | UNKNOWN | NA | C | CH-S07 | 이차망의 유죄 판결·형벌 기록 없음(부재 명시 아님) |
| MC-CH-15 | CHOI | EVENT:EV-CH-13 | F04 | 1 | OFFICIAL_JUDGMENT | NA | D | CH-S41 | 조광진 옥중 병사(瘐死) 기술; 피의자(자백자) 사망 |
| MC-CH-16 | CHOI | PERSON:CHOI-P03 | F05 | 1 | OFFICIAL_JUDGMENT | NA | C | CH-S07\|CH-S13 | 1787 석방으로 혐의 해소(1789 재검토 대상은 최아지·조광진 결론) |
| MC-CH-17 | CHOI | DECISION:DC-CH-06 | F06 | 1 | DOCUMENTED_ACT | NA | C | CH-S13\|CH-S07\|CH-S40 | 석방 명령(집행 미확인) |
| MC-CH-18 | CHOI | EVENT:EV-CH-12 | R01 | 1 | DOCUMENTED_ACT | NA | B | CH-S03\|CH-S12\|CH-S37 | 암행어사 이곤수의 별도 안핵 |
| MC-CH-19 | CHOI | EVENT:EV-CH-10 | R02 | 1 | CONTESTED | NA | D | CH-S39\|CH-S48 | 범행 자백 기록; 자백 진실성은 1789에 의심 |
| MC-CH-20 | CHOI | EVENT:EV-CH-09 | R03 | 1 | RECORDED_TESTIMONY | NA | D | CH-S38 | 사단의 진술 변경 |
| MC-CH-21 | CHOI | EVIDENCE:EI-CH-03 | R04 | NA | RECORDED_TESTIMONY | NA | D | CH-S49 | 상립 단서는 진술 속 단서; 신규 물증 확보 여부 미상 |
| MC-CH-22 | CHOI | EVENT:EV-CH-15 | R05 | 1 | DOCUMENTED_ACT | NA | C | CH-S08\|CH-S14\|CH-S42 | 1789 국왕이 30개 의문으로 모순을 제기(의문 내용은 가설) |
| MC-CH-23 | CHOI | EVENT:EV-CH-12 | R05 | 1 | DOCUMENTED_ACT | NA | C | CH-S07 | 이곤수가 상충 진술을 검토 |
| MC-CH-24 | CHOI | EVENT:EV-CH-07 | R06 | 1 | DOCUMENTED_ACT | NA | C | CH-S07\|CH-S35 | 민씨(피의자 가족) 격쟁 |
| MC-CH-25 | CHOI | EVENT:EV-CH-04 | R06 | 1 | DOCUMENTED_ACT | NA | D | CH-S28\|CH-S33 | 박용해(피해자 가족) 격쟁 |
| MC-CH-26 | CHOI | EVENT:EV-CH-03 | R06 | 1 | DOCUMENTED_ACT | NA | D | CH-S27\|CH-S33 | 박장혁(피해자 가족) 고발 |
| MC-JH-01 | CHO | CLAIM:CL-JH-07 | E02 | 1 | OFFICIAL_JUDGMENT | NEGLIGENT_SUPERVISION | B | JH-S07\|JH-S16 | 기존 문서 답습식 피상적 보고라는 국왕 판단; 의도적 은폐 합의 미확인 |
| MC-JH-02 | CHO | CLAIM:CL-JH-04 | E03 | 1 | OFFICIAL_JUDGMENT | NA | B | JH-S05\|JH-S14 | 이가원의 증인 추가·진술 지시(국왕 판단) |
| MC-JH-03 | CHO | CLAIM:CL-JH-03 | E06 | 1 | OFFICIAL_JUDGMENT | DELIBERATE_PER_JUDGMENT | B | JH-S04\|JH-S13 | 고발자의 노래 유포를 통한 여론 조작(국왕 판단; 관원 아님) |
| MC-JH-04 | CHO | CLAIM:CL-JH-02 | E04 | NA | OFFICIAL_JUDGMENT | NA | B | JH-S03 | 이득 도모 동기는 판단되었으나 관원 청탁·뇌물은 기록 없음 |
| MC-JH-05 | CHO | RELATION:RL-CHO-07 | E05 | NA | UNKNOWN | NA | B | JH-S19\|JH-S10 | 관찰사-고발자 공조 근거 없음(부재 명시가 아니므로 0 아님) |
| MC-JH-06 | CHO | EVIDENCE:EI-JH-01 | E01 | NA | OFFICIAL_JUDGMENT | NA | B | JH-S06\|JH-S15 | 혈의가 흔적이 없다는 판단은 물증 인멸·변조의 증거가 아님(주장된 물증의 부재) |
| MC-JH-07 | CHO | EPISODE:CHO-E2 | E07 | NA | UNKNOWN | NA | B | JH-S07\|JH-S16 | 재조사 명령 뒤 피상 보고는 기록되나 오류 인지 여부 출처 없음 |
| MC-JH-08 | CHO | PERSON:CHO-P01 | F01 | 1 | OFFICIAL_JUDGMENT | NA | B | JH-S03\|JH-S08\|JH-S22 | 고발 조작 판단과 석방; 윤씨 사망의 별도 진범은 미확정 |
| MC-JH-09 | CHO | EVENT:EV-JH-03 | F02 | 1 | DOCUMENTED_ACT | NA | B | JH-S08\|JH-S17 | 석방 명령이 구금을 전제(기간·장소 미보관) |
| MC-JH-10 | CHO | PERSON:CHO-P01 | F03 | NA | UNKNOWN | NA | C | JH-S20 | 초기 유죄 주장과 최종 석방 구별; 유죄 판결 기록 미보관 |
| MC-JH-11 | CHO | PERSON:CHO-P01 | F05 | 1 | OFFICIAL_JUDGMENT | NA | B | JH-S08\|JH-S22 | 국왕 판단으로 혐의 해소 |
| MC-JH-12 | CHO | DECISION:DC-JH-01 | F06 | 1 | DOCUMENTED_ACT | NA | B | JH-S08\|JH-S17 | 석방 명령(집행 미확인) |
| MC-JH-13 | CHO | DECISION:DC-JH-02 | F03 | 1 | DOCUMENTED_ACT | NA | B | JH-S08\|JH-S18 | 고발자 이가원 형장 후 유배 명령 |
| MC-JH-14 | CHO | EVENT:EV-JH-04 | R01 | NA | UNKNOWN | NA | B | JH-S12\|JH-S07 | 네 차례 조사는 기록되나 조사자의 독립성(별도 어사 파견) 여부 미보관 |
| MC-JH-15 | CHO | EVENT:EV-JH-09 | R05 | 1 | DOCUMENTED_ACT | NA | B | JH-S06\|JH-S14 | 진술 상호 모순과 혈의 부재 지적 |
| MC-JH-16 | CHO | EPISODE:CHO-E2 | R03 | NA | UNKNOWN | NA | C | JH-S14 | 증인 진술 변경 여부 미보관 |
| MC-JH-17 | CHO | EPISODE:CHO-E1 | R06 | NA | UNKNOWN | NA | B | JH-S01 | 피고·가족 호소 기록 미보관(고발자는 피해자의 먼 친척) |
| MC-YE-01 | YE | CLAIM:CL-YE-05 | E05 | 1 | OFFICIAL_JUDGMENT | UNRESOLVED_DELIBERATE_VS_NEGLIGENT | B | YE-S01\|YE-S02\|YE-S12 | 상급자(관찰사) 조사가 수령을 두둔했다는 국왕 판단; 사적 사전 합의 미입증 |
| MC-YE-02 | YE | EVENT:EV-YE-04 | E06 | 1 | OFFICIAL_JUDGMENT | UNRESOLVED_DELIBERATE_VS_NEGLIGENT | C | YE-S05\|YE-S15\|YE-S12 | 면책성 보고가 변호에 봉사했다는 성격 규정 |
| MC-YE-03 | YE | EVENT:EV-YE-04 | E02 | NA | CONTESTED | NA | C | YE-S15\|YE-S06 | 전염병 사망 주장의 허위 여부를 직접 판정한 원문 미보관 |
| MC-YE-04 | YE | EVENT:EV-YE-03 | E03 | NA | UNKNOWN | NA | B | YE-S03 | 신문 구절 미보관 |
| MC-YE-05 | YE | EPISODE:YE-E2 | E07 | NA | UNKNOWN | NA | B | YE-S01 | 오류 인지 후 불시정 여부 미보관 |
| MC-YE-06 | YE | EPISODE:YE-E1 | F01 | NA | UNKNOWN | NA | C | YE-S09 | 동일 사건 내 무고 대체 범인 확인되지 않음(부재 명시가 아니므로 NA) |
| MC-YE-07 | YE | DECISION:DC-YE-04 | F03 | 1 | DOCUMENTED_ACT | NA | C | YE-S19\|YE-S08 | 이여절 위원 유배 명령(집행 미확인) |
| MC-YE-08 | YE | DECISION:DC-YE-03 | F03 | 1 | DOCUMENTED_ACT | NA | C | YE-S19\|YE-S08 | 조진택 삭직 명령(행정 처분) |
| MC-YE-09 | YE | EVENT:EV-YE-05 | R01 | 1 | DOCUMENTED_ACT | NA | C | YE-S08\|YE-S10\|YE-S16 | 유경의 특별 조사 |
| MC-YE-10 | YE | EVENT:EV-YE-06 | R05 | 1 | DOCUMENTED_ACT | NA | B | YE-S01\|YE-S12 | 감영 조사의 문제점 지적 |
| MC-YE-11 | YE | EVENT:EV-YE-07 | R05 | 1 | DOCUMENTED_ACT | NA | C | YE-S07\|YE-S18 | 중앙 심리의 안핵 재평가(25명 언급) |
| MC-YE-12 | YE | EPISODE:YE-E3 | R06 | NA | UNKNOWN | NA | B | YE-S03 | 유족 호소 기록 미보관 |
| MC-GS-01 | GUSUN | RELATION:RL-GS-13 | E03 | 1 | CONTESTED | NA | B | GS-F-CF016\|GS-F-CF017\|GS-F-CF018\|GS-P-V3P0042 | 자미덕 진술·윤노동 보고 vs 한재욱 부인 |
| MC-GS-02 | GUSUN | RELATION:RL-GS-17 | E03 | 1 | RECORDED_TESTIMONY | NA | B | GS-P-V3P0054 | 명업이 위협이 두려워 진술을 바꿨다고 진술 |
| MC-GS-03 | GUSUN | PERSON:GUSUN-P02 | E03 | 0 | OFFICIAL_JUDGMENT | NA | B | GS-F-CF041\|GS-P-V3P0106 | 정조는 김명신이 곤장을 맞지 않았고 평범한 신문도 받지 않았다고 판단(김명신 대상 강압 신문의 부재 판단) |
| MC-GS-04 | GUSUN | EVENT:EV-GS-10 | E02 | 1 | OFFICIAL_JUDGMENT | ERRONEOUS_REPORT | B | GS-F-CF030\|GS-F-CF039\|GS-P-V3P0152 | 5월 도신 장계(도난 없음)와 6월 최종 판단(도난 실재)이 현격히 다름 |
| MC-GS-05 | GUSUN | EVENT:EV-GS-12 | E02 | 1 | OFFICIAL_JUDGMENT | NEGLIGENT_SUPERVISION | B | GS-F-CF033\|GS-P-V3P0032 | 이조원이 직접 안핵 없이 전문을 서계에 붙였다는 비판 |
| MC-GS-06 | GUSUN | PERSON:GUSUN-P01 | E06 | 1 | OFFICIAL_JUDGMENT | DELIBERATE_PER_JUDGMENT | B | GS-P-V3P0134\|GS-P-V3P0143 | 홍대협: 과장·의혹 확대로 날조 옥사 사주; 정조: 성명 제공 |
| MC-GS-07 | GUSUN | EPISODE:GUSUN-E2 | E06 | 1 | OFFICIAL_JUDGMENT | NA | B | GS-P-V3P0100\|GS-P-V3P0150 | 아전의 거짓 보고를 이광섭이 살피지 않음 |
| MC-GS-08 | GUSUN | CLAIM:GS-CL-CF045 | E06 | 0 | OFFICIAL_JUDGMENT | NA | B | GS-F-CF045\|GS-P-V3P0146 | 정조는 구순이 지세 호칭을 스스로 만들어냈다는 죄를 인정하지 않음(해당 날조의 부재 판단) |
| MC-GS-09 | GUSUN | RELATION:RL-GS-15 | E05 | 1 | OFFICIAL_JUDGMENT | NOT_DELIBERATE_PER_INSPECTOR | B | GS-P-V3P0148\|GS-P-V3P0138 | 병사가 구순 편을 들었다는 정조 판단; 홍대협은 평민을 해치려는 의도는 아니었다고 평가 |
| MC-GS-10 | GUSUN | RELATION:RL-GS-14 | E05 | NA | CONTESTED | NA | B | GS-P-V3P0027\|GS-P-V3P0124 | 하급 보조자=구순 가객 주장(이조원); 동일인 미해결 |
| MC-GS-11 | GUSUN | EPISODE:GUSUN-E3 | E04 | NA | UNKNOWN | NA | C | GS-S03 | 청탁·뇌물 기록 없음 |
| MC-GS-12 | GUSUN | EVIDENCE:EI-GS-01 | E01 | NA | UNKNOWN | NA | B | GS-F-CF010\|GS-F-CF044 | 증거 인멸·변조 기록 없음 |
| MC-GS-13 | GUSUN | EPISODE:GUSUN-E4 | E07 | NA | UNKNOWN | NA | B | GS-F-CF049\|GS-F-CF050 | 오류 인지 후 불시정 여부 미보관(파직 후 유임은 별도 인사) |
| MC-GS-14 | GUSUN | PERSON:GUSUN-P02 | F01 | 1 | OFFICIAL_JUDGMENT | NA | B | GS-F-CF043\|GS-P-V3P0144 | 구순의 성명 제공으로 김명신이 횡액을 입었다는 정조 판단 |
| MC-GS-15 | GUSUN | EVENT:EV-GS-08 | F02 | 1 | DOCUMENTED_ACT | NA | B | GS-F-CF027 | 달포 이상 구금 |
| MC-GS-16 | GUSUN | EVENT:EV-GS-09 | F04 | 1 | DOCUMENTED_ACT | NA | B | GS-F-CF027\|GS-F-CF029\|GS-S05 | 구금 중 사망(직접 인과 미확정) |
| MC-GS-17 | GUSUN | PERSON:GUSUN-P02 | F05 | 1 | OFFICIAL_JUDGMENT | NA | B | GS-F-CF043\|GS-P-V3P0147 | 사후 원통함 인정·구순 감사 정배로 사죄(사후적 혐의 해소) |
| MC-GS-18 | GUSUN | PERSON:GUSUN-P02 | F06 | NA | DOCUMENTED_ACT | NA | B | GS-F-CF027 | 사망으로 석방 불가(코드 비해당) |
| MC-GS-19 | GUSUN | DECISION:DC-GS-07 | F03 | 1 | DOCUMENTED_ACT | NA | B | GS-F-CF046 | 고발자 구순 정배 |
| MC-GS-20 | GUSUN | DECISION:DC-GS-08 | F03 | 1 | DOCUMENTED_ACT | NA | B | GS-F-CF047 | 병사 이광섭 유배 |
| MC-GS-21 | GUSUN | EVENT:EV-GS-15 | R01 | 1 | DOCUMENTED_ACT | NA | B | GS-F-CF035\|GS-F-CF037 | 홍대협 독립 안핵 |
| MC-GS-22 | GUSUN | EVENT:EV-GS-05 | R03 | 1 | RECORDED_TESTIMONY | NA | B | GS-F-CF017 | 자미덕이 거짓 진술했다고 진술 변경 |
| MC-GS-23 | GUSUN | RELATION:RL-GS-17 | R03 | 1 | RECORDED_TESTIMONY | NA | B | GS-P-V3P0054 | 명업 진술 변경 |
| MC-GS-24 | GUSUN | EVENT:EV-GS-16 | R05 | 1 | DOCUMENTED_ACT | NA | B | GS-P-V3P0152 | 도신 장계와 안핵 보고의 현격한 차이 지적 |
| MC-GS-25 | GUSUN | EVENT:EV-GS-16 | R02 | NA | UNKNOWN | NA | B | GS-F-CF038 | 실제 절도범 자백 기록 없음 |
| MC-GS-26 | GUSUN | EVIDENCE:EI-GS-02 | R04 | NA | UNKNOWN | NA | B | GS-F-CF027 | 장물 미발견은 신규 물증이 아님 |
| MC-GS-27 | GUSUN | EPISODE:GUSUN-E4 | R06 | NA | UNKNOWN | NA | B | GS-P-V3P0123 | 도 전체 공분 보고는 유족 호소가 아님 |

## 당시 판단 vs 역사적 실체(actual_culprit 분리)

| 사건 | 피해 | 당시 판단상 책임자 | 판단 시점 | 후속 판단 | 역사적 실체 상태 |
|---|---|---|---|---|---|
| CHOI | 박씨 사망 | 최아지·조광진 공모 살해(1787 안핵·국왕 판단) | 1787-04 | 1789-06 국왕이 30개 의문으로 재의문; 사형 전제 옥안 불성립·장 100·유 2천 리 준용 | UNRESOLVED_CONTESTED |
| CHO | 윤씨 사망 | 조재항 혐의는 고발 조작으로 판단·석방(사인 판정 없음) | 1783-06-03 | NA | UNKNOWN_NO_SEPARATE_KILLER_ESTABLISHED |
| YE | 창원 다수 사망(31/25) | 이여절의 남형(유경 보고·국왕 판단) | 1795-06 | 1795-09-21 이여절 유배·조진택 삭직(명령) | OFFICIAL_JUDGMENT_CONTESTED_BY_GOVERNOR_REPORT |
| GUSUN | 김명신 구금 중 사망 및 무고 | 구순(성명 제공·갈등)·이광섭(편들기·과도한 조치) 책임; 사망은 전염병 | 1793-06-13 | 1793-06-16 이형원 유임(인사) | UNRESOLVED_DIRECT_CAUSATION |
