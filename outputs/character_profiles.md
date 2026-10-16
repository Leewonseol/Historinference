# 인물 프로필 — 출처 근거가 있는 속성만

> 자동 생성 문서(`python -m historinference report`). 모든 수치는 `data/normalized`·`models`·`data/audit`에서 재계산된다. 원문 미보관(UNAVAILABLE_SOURCE_TEXT) 상태에서 로컬 요약·선행 코딩만으로 작성되었으며, 확률·빈도 추정은 하지 않는다.

근거 없는 속성은 `NA`로 둔다(출생연도·연령은 어떤 인물에도 근거가 없어 전부 NA). 성별은 친족어(아내·남편·召史·婢 등)가 있는 경우에만 코딩했고 관직 보유만으로 추정하지 않았다. 사건 간 동일 인물(정조)도 사건별 ID로 분리한다.


## CHOI 평산 최아지·이차망(1785–1789)

| 인물 | 종류 | 사건 내 역할 | 성별 | 추정 연령 범위 | 거주지 | 신분 주장 | 입증된 신분 | 관직 | 직업 | 가족·혼인 | 사망 | 이표기 | 관계 | 식별 주의 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| CHOI-P01 박씨 朴召史 | PERSON | 피해자(사망자) | F [DOCUMENTED_ACT; CH-S20\|CH-S03] | NA | NA | NA | NA | NA | NA | 조광선의 아내(CHOI-P05); 박장혁의 딸; 박용해의 누이 [RECORDED_TESTIMONY; CH-S20\|CH-S27\|CH-S28] | 1785년 무렵 사망(성옥 1785-11; 사망일 미상) [DOCUMENTED_ACT; CH-S06\|CH-S31] | 박녀(NAME·ATTESTED_IN_SECONDARY); 朴女(NAME·ATTESTED_IN_SECONDARY); 朴召史(NAME·ATTESTED_IN_SECONDARY); 박소사(NAME·ATTESTED_IN_SECONDARY) | MARRIAGE[RECORDED_TESTIMONY](RL-CH-01); KINSHIP[DOCUMENTED_ACT](RL-CH-03); KINSHIP[RECORDED_TESTIMONY](RL-CH-06); KINSHIP[RECORDED_TESTIMONY](RL-CH-07) | 사인 미확정 |
| CHOI-P02 최아지 崔阿只 | PERSON | 피의자(1787 공식결론상 공모자; 1789 재의문) | F [DOCUMENTED_ACT; CH-S21\|CH-S03] | NA | NA | NA | NA | NA | NA | 조광선의 계모·박씨의 시어머니 [RECORDED_TESTIMONY; CH-S21\|CH-S03] | NA | 崔阿只(NAME·ATTESTED_IN_SECONDARY); 崔女(NAME·ATTESTED_IN_SECONDARY); 崔召史(NAME·ATTESTED_IN_SECONDARY); 최 조이(NAME·ATTESTED_IN_SECONDARY); 시어머니 최씨(ROLE_TERM·ATTESTED_IN_OFFICIAL_PARAPHRASE) | KINSHIP[RECORDED_TESTIMONY](RL-CH-02); KINSHIP[DOCUMENTED_ACT](RL-CH-03); ALLEGED_ILLICIT_LIAISON[CONTESTED](RL-CH-08); ALLEGED_ILLICIT_LIAISON[CONTESTED](RL-CH-09); KINSHIP[UNKNOWN](RL-CH-13) | 실록 의역은 '시어머니 최씨' |
| CHOI-P03 이차망 李次望 | PERSON | 피의·구금 후 석방된 자 | M [DOCUMENTED_ACT; CH-S07\|CH-S23] | NA | NA | 순평군 후손이라는 주장(민씨 청원 속 주장; 원문 미보관) [CONTESTED; CH-S09\|CH-S53] | NA | NA | NA | 민씨(CHOI-P04)의 남편 [RECORDED_TESTIMONY; CH-S07\|CH-S23] | NA | - | MARRIAGE[RECORDED_TESTIMONY](RL-CH-04); ALLEGED_ILLICIT_LIAISON[CONTESTED](RL-CH-09); INFORMATION_TRANSFER[CONTESTED](RL-CH-16) | 조광진과 동일시 금지 |
| CHOI-P04 민씨 閔女 | PERSON | 이차망의 처·청원자 | F [DOCUMENTED_ACT; CH-S07\|CH-S23] | NA | NA | NA | NA | NA | NA | NA | NA | - | MARRIAGE[RECORDED_TESTIMONY](RL-CH-04) |  |
| CHOI-P05 조광선 趙匡善 | PERSON | 박씨의 남편 | M [DOCUMENTED_ACT; CH-S20] | NA | NA | NA | NA | NA | NA | 박씨의 남편; 최아지의 의붓아들 [RECORDED_TESTIMONY; CH-S20\|CH-S21] | NA | - | MARRIAGE[RECORDED_TESTIMONY](RL-CH-01); KINSHIP[RECORDED_TESTIMONY](RL-CH-02); KINSHIP[RECORDED_TESTIMONY](RL-CH-05) | 조광진과 다른 사람 |
| CHOI-P06 조광진 趙匡辰 | PERSON | 1787 안핵의 주요 피의자·자백자 | NA | NA | NA | NA | NA | NA | NA | 조광선의 친족(구체 촌수 미상) [RECORDED_TESTIMONY; CH-S24] | 1788년 옥중 병사(瘐死)로 기술 [OFFICIAL_JUDGMENT; CH-S41] | 조광신(TRANSLATION_VARIANT·ATTESTED_IN_SECONDARY) | KINSHIP[RECORDED_TESTIMONY](RL-CH-05); ALLEGED_ILLICIT_LIAISON[CONTESTED](RL-CH-08); TESTIMONY_INFLUENCE[RECORDED_TESTIMONY](RL-CH-10); INFORMATION_TRANSFER[CONTESTED](RL-CH-16) | 국역 변이 조광신; 1788 사망 |
| CHOI-P07 사단 四丹 | PERSON | 핵심 진술자(비) | F [RECORDED_TESTIMONY; CH-S25\|CH-S52] | NA | NA | 관련 집안의 비(婢) [RECORDED_TESTIMONY; CH-S25] | NA | NA | NA | NA | NA | - | TESTIMONY_INFLUENCE[RECORDED_TESTIMONY](RL-CH-10); TESTIMONY_INFLUENCE[CONTESTED](RL-CH-11); HOUSEHOLD_SERVICE[RECORDED_TESTIMONY](RL-CH-17) |  |
| CHOI-P08 사단의 어미 | UNNAMED_PERSON | 진술자(사단 모녀) | NA | NA | NA | NA | NA | NA | NA | NA | NA | - | - | 이름 미상 |
| CHOI-P09 조봉원 趙鳳元 | PERSON | 군교·진술 개입 주장 대상 | NA | NA | NA | NA | NA | NA | 군교 [RECORDED_TESTIMONY; CH-S26] | NA | NA | - | TESTIMONY_INFLUENCE[CONTESTED](RL-CH-11); BRIBERY[UNKNOWN](RL-CH-12) |  |
| CHOI-P10 박장혁 朴長赫 | PERSON | 피해자 부친·고발자 | M [DOCUMENTED_ACT; CH-S27] | NA | NA | NA | NA | NA | NA | NA | NA | - | KINSHIP[RECORDED_TESTIMONY](RL-CH-06) |  |
| CHOI-P11 박용해 朴龍海 | PERSON | 피해자 오빠·격쟁자 | M [DOCUMENTED_ACT; CH-S28] | NA | NA | NA | NA | NA | NA | NA | NA | - | KINSHIP[RECORDED_TESTIMONY](RL-CH-07) |  |
| CHOI-P12 이곤수 李崑秀 | PERSON | 1787 평산 안핵 담당 암행어사 | NA | NA | NA | NA | NA | 양서 암행어사(1787 복명); 평산 안핵 담당 [DOCUMENTED_ACT; CH-S01\|CH-S03\|CH-S37] | NA | NA | NA | - | COMMAND[DOCUMENTED_ACT](RL-CH-14); INFORMATION_TRANSFER[DOCUMENTED_ACT](RL-CH-15) |  |
| CHOI-P13 엄사만 嚴思晩 | PERSON | 황해도 전 관찰사(1787 파직 명령 대상) | NA | NA | NA | NA | NA | 황해도 전 관찰사(전 도신) [DOCUMENTED_ACT; CH-S04\|CH-S29] | NA | NA | NA | - | - |  |
| CHOI-P14 홍병찬 洪秉纘 | PERSON | 황해도 전전 관찰사(1787 삭직 명령 대상) | NA | NA | NA | NA | NA | 황해도 전전 관찰사(전 도신) [DOCUMENTED_ACT; CH-S04\|CH-S29] | NA | NA | NA | - | - |  |
| CHOI-P15 정경증 鄭景曾 | PERSON | 검험관(초검/복검 배정 미확정) | NA | NA | NA | NA | NA | 검험관(초검 또는 복검) [RECORDED_TESTIMONY; CH-S30] | NA | NA | NA | - | - |  |
| CHOI-P16 이단회 李端會 | PERSON | 검험관(초검/복검 배정 미확정) | NA | NA | NA | NA | NA | 검험관(초검 또는 복검) [RECORDED_TESTIMONY; CH-S30] | NA | NA | NA | - | - |  |
| CHOI-K 정조 正祖 | PERSON | 국왕·최종 판단자 | NA | NA | NA | NA | NA | NA | NA | NA | NA | - | COMMAND[DOCUMENTED_ACT](RL-CH-14); INFORMATION_TRANSFER[DOCUMENTED_ACT](RL-CH-15) | 사건별 ID 유지(교차 사건 병합 금지) |

## CHO 배천 조재항(1780/1781–1783)

| 인물 | 종류 | 사건 내 역할 | 성별 | 추정 연령 범위 | 거주지 | 신분 주장 | 입증된 신분 | 관직 | 직업 | 가족·혼인 | 사망 | 이표기 | 관계 | 식별 주의 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| CHO-P01 조재항 趙載恒 | PERSON | 피고인 남편(석방) | M [DOCUMENTED_ACT; JH-S01] | NA | 배천군 [DOCUMENTED_ACT; JH-S01] | NA | NA | NA | NA | 윤씨(CHO-P02)의 남편 [DOCUMENTED_ACT; JH-S01] | NA | - | MARRIAGE[DOCUMENTED_ACT](RL-CHO-01) |  |
| CHO-P02 윤씨 尹氏 | PERSON | 사망한 아내 | F [DOCUMENTED_ACT; JH-S01\|JH-S09] | NA | NA | NA | NA | NA | NA | NA | 사망(일자·사인 미상) [DOCUMENTED_ACT; JH-S01\|JH-S11] | - | MARRIAGE[DOCUMENTED_ACT](RL-CHO-01); KINSHIP[OFFICIAL_JUDGMENT](RL-CHO-02) | 사인 미확정 |
| CHO-P03 이가원 李可遠 | PERSON | 고발자·먼 친척 | NA | NA | NA | NA | NA | NA | NA | 윤씨의 먼 친척 [OFFICIAL_JUDGMENT; JH-S01\|JH-S03] | NA | 이간원(TITLE_VARIANT·REGISTER_NOTE_UNVERIFIED) | KINSHIP[OFFICIAL_JUDGMENT](RL-CHO-02); TESTIMONY_INFLUENCE[OFFICIAL_JUDGMENT](RL-CHO-03); INFORMATION_TRANSFER[OFFICIAL_JUDGMENT](RL-CHO-04); PATRONAGE[UNKNOWN](RL-CHO-07) | 레지스터 표기 변이 이간원 |
| CHO-P04 조상진 趙尙鎭 | PERSON | 도백(관찰사) | NA | NA | NA | NA | NA | 도백(배천 관할 도의 관찰사) [DOCUMENTED_ACT; JH-S07\|JH-S09] | NA | NA | NA | 도백 조상진(ROLE_TERM·ATTESTED_IN_OFFICIAL_PARAPHRASE) | COMMAND[DOCUMENTED_ACT](RL-CHO-05); INFORMATION_TRANSFER[OFFICIAL_JUDGMENT](RL-CHO-06); PATRONAGE[UNKNOWN](RL-CHO-07) |  |
| CHO-P05 조재풍 趙載豊 | PERSON | 기사 인명(역할 미상) | NA | NA | NA | NA | NA | NA | NA | NA | NA | - | - | 조재항과의 관계 미상; 이름 글자 공유로 친족 추정 금지 |
| CHO-P06 배조이 裵召史 | PERSON | 증인으로 언급 | F [RECORDED_TESTIMONY; JH-S09] | NA | NA | NA | NA | NA | NA | NA | NA | - | TESTIMONY_INFLUENCE[OFFICIAL_JUDGMENT](RL-CHO-03) |  |
| CHO-P07 나막동 羅莫同 | PERSON | 증인으로 언급 | NA | NA | NA | NA | NA | NA | NA | NA | NA | - | TESTIMONY_INFLUENCE[OFFICIAL_JUDGMENT](RL-CHO-03) |  |
| CHO-P08 점렬 點烈 | PERSON | 증인으로 언급 | NA | NA | NA | NA | NA | NA | NA | NA | NA | - | TESTIMONY_INFLUENCE[OFFICIAL_JUDGMENT](RL-CHO-03) |  |
| CHO-P09 막덕 莫德 | PERSON | 증인으로 언급 | NA | NA | NA | NA | NA | NA | NA | NA | NA | - | TESTIMONY_INFLUENCE[OFFICIAL_JUDGMENT](RL-CHO-03) |  |
| CHO-P10 하위 가담자들 | GROUP | 경중에 따라 처벌 명령 대상 | NA | NA | NA | NA | NA | NA | NA | NA | NA | - | - | 구성원 미상 |
| CHO-K 정조 正祖 | PERSON | 국왕·최종 판단자 | NA | NA | NA | NA | NA | NA | NA | NA | NA | - | COMMAND[DOCUMENTED_ACT](RL-CHO-05); INFORMATION_TRANSFER[OFFICIAL_JUDGMENT](RL-CHO-06) | 사건별 ID 유지 |

## YE 창원 이여절·조진택(1793–1795)

| 인물 | 종류 | 사건 내 역할 | 성별 | 추정 연령 범위 | 거주지 | 신분 주장 | 입증된 신분 | 관직 | 직업 | 가족·혼인 | 사망 | 이표기 | 관계 | 식별 주의 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| YE-P01 이여절 李汝節 | PERSON | 창원부사·남형 혐의자 | NA | NA | NA | NA | NA | 단천 부사(1789-07-14 기사 시점) [DOCUMENTED_ACT; YE-S13]; 창원 부사(1793-06-13 평가 시점 및 조사 대상 시점) [DOCUMENTED_ACT; YE-S14\|YE-S04] | NA | NA | NA | - | COMMAND[DOCUMENTED_ACT](RL-YE-01); PATRONAGE[OFFICIAL_JUDGMENT](RL-YE-03) | 1801 사건과 동일인이나 사건 융합 금지 |
| YE-P02 조진택 趙鎭宅 | PERSON | 관찰사(감독 조사·보고) | NA | NA | NA | NA | NA | 관찰사(창원 관할 도; 1795 시점 전 관찰사) [DOCUMENTED_ACT; YE-S05\|YE-S15] | NA | NA | NA | - | COMMAND[DOCUMENTED_ACT](RL-YE-01); INFORMATION_TRANSFER[DOCUMENTED_ACT](RL-YE-02); PATRONAGE[OFFICIAL_JUDGMENT](RL-YE-03) |  |
| YE-P03 유경 | PERSON | 특별 조사(안핵) 담당 | NA | NA | NA | NA | NA | 특별 조사(안핵) 담당 [DOCUMENTED_ACT; YE-S08\|YE-S10] | NA | NA | NA | - | COMMAND[DOCUMENTED_ACT](RL-YE-04); INFORMATION_TRANSFER[DOCUMENTED_ACT](RL-YE-05) | 한자 미보관 |
| YE-P04 정대용 | PERSON | 1793 이여절 평가자 | NA | NA | NA | NA | NA | NA | NA | NA | NA | - | INFORMATION_TRANSFER[DOCUMENTED_ACT](RL-YE-06) | 한자·관직 미보관 |
| YE-P05 사망자들 | GROUP | 남형 사망자(31/25 귀속 수치) | NA | NA | NA | NA | NA | NA | NA | NA | NA | - | - | 이름 일부 확인이라는 레지스터 메모만 있음 |
| YE-P06 조사관들 | GROUP | 감영 측 조사관 | NA | NA | NA | NA | NA | NA | NA | NA | NA | - | - | 구성원 미상 |
| YE-K 정조 正祖 | PERSON | 국왕·질책·처분 | NA | NA | NA | NA | NA | NA | NA | NA | NA | - | INFORMATION_TRANSFER[DOCUMENTED_ACT](RL-YE-02); COMMAND[DOCUMENTED_ACT](RL-YE-04); INFORMATION_TRANSFER[DOCUMENTED_ACT](RL-YE-05); INFORMATION_TRANSFER[DOCUMENTED_ACT](RL-YE-06) | 사건별 ID 유지 |

## GUSUN 구순–김명신(1793)

| 인물 | 종류 | 사건 내 역할 | 성별 | 추정 연령 범위 | 거주지 | 신분 주장 | 입증된 신분 | 관직 | 직업 | 가족·혼인 | 사망 | 이표기 | 관계 | 식별 주의 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| GUSUN-P01 구순 具純 | PERSON | 전 부사·도난 고발자 | NA | NA | 청주 덕평 [RECORDED_TESTIMONY; GS-P-V3P0001] | NA | NA | 전 부사 [DOCUMENTED_ACT; GS-P-V3P0001] | NA | NA | NA | - | ACQUAINTANCE[RECORDED_TESTIMONY](RL-GS-01); CONFLICT[RECORDED_TESTIMONY](RL-GS-02); HOUSEHOLD_SERVICE[RECORDED_TESTIMONY](RL-GS-03); INFORMATION_TRANSFER[RECORDED_TESTIMONY](RL-GS-11); INFORMATION_TRANSFER[OFFICIAL_JUDGMENT](RL-GS-12); PATRONAGE[CONTESTED](RL-GS-14); PATRONAGE[OFFICIAL_JUDGMENT](RL-GS-15); ACQUAINTANCE_DENIED[RECORDED_TESTIMONY](RL-GS-16) |  |
| GUSUN-P02 김명신 金明信 | PERSON | 도적 괴수로 지목·구금 중 사망 | NA | NA | NA | NA | NA | NA | NA | 아내가 김명신 사후 따라 죽었다고 보고됨 [RECORDED_TESTIMONY; GS-P-V3P0025\|GS-P-V3P0105] | 1793-05-12 보고 이전 구금·조사 뒤 사망 [DOCUMENTED_ACT; GS-F-CF027\|GS-F-CF029] | 풍각 김생원(HONORIFIC·RESOLVED_BY_PRIOR_REPO); 풍각 김상제(HONORIFIC·RESOLVED_BY_PRIOR_REPO) | ACQUAINTANCE[RECORDED_TESTIMONY](RL-GS-01); CONFLICT[RECORDED_TESTIMONY](RL-GS-02); MARRIAGE[RECORDED_TESTIMONY](RL-GS-07) | 풍각 김생원·풍각 김상제(선행 저장소 확정) |
| GUSUN-P03 김명신의 아내 | UNNAMED_PERSON | 김명신 사후 사망 보고 | F [RECORDED_TESTIMONY; GS-P-V3P0025] | NA | NA | NA | NA | NA | NA | NA | 김명신 사후 사망 보고 [RECORDED_TESTIMONY; GS-P-V3P0025\|GS-P-V3P0105] | - | MARRIAGE[RECORDED_TESTIMONY](RL-GS-07) |  |
| GUSUN-P04 명업 | PERSON | 구순 집 계집종의 남편·증인 | NA | NA | NA | NA | NA | NA | NA | 구순 집 계집종의 남편·바깥사랑 거주 [RECORDED_TESTIMONY; GS-P-V3P0046] | NA | - | HOUSEHOLD_SERVICE[RECORDED_TESTIMONY](RL-GS-03); TESTIMONY_INFLUENCE[RECORDED_TESTIMONY](RL-GS-17) |  |
| GUSUN-P05 나복 | PERSON | 도난 소식 전달자 | NA | NA | NA | NA | NA | NA | NA | NA | NA | - | - |  |
| GUSUN-P06 이진욱 | PERSON | 병영 장교·증인 | NA | NA | NA | NA | NA | NA | 병영 장교 [RECORDED_TESTIMONY; GS-P-V3P0061] | NA | NA | - | COMMAND[RECORDED_TESTIMONY](RL-GS-08); COMMAND[RECORDED_TESTIMONY](RL-GS-09) |  |
| GUSUN-P07 한재욱 | PERSON | 병영 비장(한 비장·한가) | NA | NA | NA | NA | NA | 병영 비장 [DOCUMENTED_ACT; GS-F-CF048\|GS-P-V3P0112] | NA | NA | NA | 한 비장(ROLE_TERM·RESOLVED_BY_PRIOR_REPO); 병영 비장 한가(ROLE_TERM·RESOLVED_BY_PRIOR_REPO) | COMMAND[RECORDED_TESTIMONY](RL-GS-08); COMMAND[RECORDED_TESTIMONY](RL-GS-10); TESTIMONY_INFLUENCE[CONTESTED](RL-GS-13); ACQUAINTANCE_DENIED[RECORDED_TESTIMONY](RL-GS-16) | 선행 저장소 확정(ID02·ID03) |
| GUSUN-P08 조계완 | PERSON | 병영 장교·증인 | NA | NA | NA | NA | NA | NA | 병영 장교 [RECORDED_TESTIMONY; GS-P-V3P0069\|GS-P-V3P0071] | NA | NA | - | COMMAND[RECORDED_TESTIMONY](RL-GS-08) |  |
| GUSUN-P09 변지돌 | PERSON | 체포 지시 대상 | NA | NA | NA | NA | NA | NA | NA | NA | NA | - | KINSHIP[RECORDED_TESTIMONY](RL-GS-04); KINSHIP[RECORDED_TESTIMONY](RL-GS-05) |  |
| GUSUN-P10 정원돌 | PERSON | 체포 지시 대상 | NA | NA | NA | NA | NA | NA | NA | NA | NA | 원돌(NAME·RESOLVED_BY_PRIOR_REPO) | KINSHIP[RECORDED_TESTIMONY](RL-GS-04) | 원돌(선행 저장소 확정 ID11) |
| GUSUN-P11 재돌 | PERSON | 변지돌의 아우 | NA | NA | NA | NA | NA | NA | NA | 변지돌의 아우; 자미덕의 남편 [RECORDED_TESTIMONY; GS-P-V3P0061] | NA | - | KINSHIP[RECORDED_TESTIMONY](RL-GS-05); MARRIAGE[RECORDED_TESTIMONY](RL-GS-06) |  |
| GUSUN-P12 자미덕 | PERSON | 재돌의 처·구류·사주 주장 진술자 | F [RECORDED_TESTIMONY; GS-P-V3P0061] | NA | NA | NA | NA | NA | NA | 재돌의 처 [RECORDED_TESTIMONY; GS-P-V3P0061] | NA | - | MARRIAGE[RECORDED_TESTIMONY](RL-GS-06); TESTIMONY_INFLUENCE[CONTESTED](RL-GS-13) | 윤노동 보고의 '변가의 처'와의 동일성 미검증 |
| GUSUN-P13 이집거 | PERSON | 대질 상대 | NA | NA | NA | NA | NA | NA | NA | NA | NA | - | - |  |
| GUSUN-P14 김갑득 | PERSON | 흥덕 김생원·체포됨 | NA | NA | NA | NA | NA | NA | NA | NA | NA | 흥덕 김생원(HONORIFIC·RESOLVED_BY_PRIOR_REPO) | - |  |
| GUSUN-P15 유제희 | PERSON | 병영 아전·탐문 기록자 | NA | NA | NA | NA | NA | NA | 병영 아전 [RECORDED_TESTIMONY; GS-P-V3P0085] | NA | NA | - | COMMAND[RECORDED_TESTIMONY](RL-GS-10); INFORMATION_TRANSFER[OFFICIAL_JUDGMENT](RL-GS-12) |  |
| GUSUN-P16 이광섭 | PERSON | 충청도 병마절도사(병사) | NA | NA | NA | NA | NA | 충청도 병마절도사 [DOCUMENTED_ACT; GS-F-CF025] | NA | NA | NA | 병사(ROLE_TERM·RESOLVED_BY_PRIOR_REPO) | COMMAND[RECORDED_TESTIMONY](RL-GS-09); INFORMATION_TRANSFER[RECORDED_TESTIMONY](RL-GS-11); PATRONAGE[OFFICIAL_JUDGMENT](RL-GS-15) | 공초의 '병사'(선행 저장소 확정 ID01) |
| GUSUN-P17 이문협 | PERSON | 청주 영장 | NA | NA | NA | NA | NA | 청주 영장 [DOCUMENTED_ACT; GS-P-V3P0012] | NA | NA | NA | - | - |  |
| GUSUN-P18 이형원 | PERSON | 충청도 관찰사 | NA | NA | NA | NA | NA | 충청도 관찰사(1793-06-13 파직 명령; 1793-06-16 유임) [DOCUMENTED_ACT; GS-F-CF049\|GS-F-CF050] | NA | NA | NA | - | - |  |
| GUSUN-P19 이조원 | PERSON | 호서 암행어사 | NA | NA | NA | NA | NA | 호서 암행어사 [DOCUMENTED_ACT; GS-F-CF032\|GS-F-CF033] | NA | NA | NA | - | - |  |
| GUSUN-P20 윤노동 | PERSON | 호서 암행어사 | NA | NA | NA | NA | NA | 호서 암행어사 [DOCUMENTED_ACT; GS-F-CF029\|GS-P-V3P0155] | NA | NA | NA | - | - |  |
| GUSUN-P21 홍대협 | PERSON | 공주 안핵어사 | NA | NA | NA | NA | NA | 공주 안핵어사(1793-05-28 차하) [DOCUMENTED_ACT; GS-F-CF035] | NA | NA | NA | - | COMMAND[DOCUMENTED_ACT](RL-GS-18) |  |
| GUSUN-P22 김성손 | PERSON | 큰 도적 지목 요구 명단 | NA | NA | NA | NA | NA | NA | NA | NA | NA | - | - |  |
| GUSUN-P23 김흥득 | PERSON | 큰 도적 지목 요구 명단 | NA | NA | NA | NA | NA | NA | NA | NA | NA | - | - |  |
| GUSUN-P24 병영의 하급 보조자 | ROLE_SURFACE | 이조원 보고의 구순 가객 | NA | NA | NA | NA | NA | NA | NA | NA | NA | - | PATRONAGE[CONTESTED](RL-GS-14) | 한재욱 동일성 UNRESOLVED(선행 ID04) |
| GUSUN-K 정조 正祖 | PERSON | 국왕·판단·처분 | NA | NA | NA | NA | NA | NA | NA | NA | NA | - | COMMAND[DOCUMENTED_ACT](RL-GS-18) | 사건별 ID 유지 |

## 동명인·동일인 판정

| ID | A | B | 판정 | 근거 |
|---|---|---|---|---|
| ID-01 | 조광선 趙匡善 | 조광진 趙匡辰 | DISTINCT | 한자가 다른 별개 인물로 기술됨 |
| ID-02 | 이차망 | 조광진 | DISTINCT | 레지스터 경고: 이차망과 조광진 이름 동일시 금지 |
| ID-03 | 조광진 | 조광신 | SAME_PERSON_ALIAS | 일부 국역 표기 변이 |
| ID-04 | 이가원 李可遠 | 이간원 | SAME_PERSON_ALIAS_UNVERIFIED | 레지스터 메모(기사 제목 표기 변이); 원문 대조 필요 |
| ID-05 | 조재항 趙載恒 | 조재풍 趙載豊 | DISTINCT_RELATION_UNKNOWN | 이름 글자 공유만으로 친족 관계 추정 금지 |
| ID-06 | 정조(CHOI) | 정조(CHO/YE/GUSUN) | SAME_HISTORICAL_PERSON_CASE_SCOPED_IDS | 동일 국왕이나 비교 그래프에서 사건 간 노드 병합 금지 |
| ID-07 | 이여절(YE 1793-1795) | 이여절(1801 황기운 사건) | SAME_NAME_SEPARATE_CASE | 1801 사건은 범위 밖 별도 사건; 사건 융합 금지 |
| ID-08 | 이여절 단천부사(1789) | 이여절 창원부사(1793) | PRESUMED_SAME_BY_REGISTER_UNVERIFIED | 레지스터가 경력 배경으로 같은 사례 묶음에 등록; 동일인 원문 검증 미완 |
| ID-09 | 병영의 하급 보조자 | 한재욱 | UNRESOLVED_DO_NOT_MERGE | 선행 저장소 identity_register ID04 미해결 유지 |
| ID-10 | 병영의 염탐 담당자 | 유제희 | UNRESOLVED_DO_NOT_MERGE | 선행 저장소 ID06 미해결 유지 |
| ID-11 | 자미덕 | 변가의 처(윤노동 보고) | UNRESOLVED_DO_NOT_MERGE | 윤노동 보고 표현과 공초 인물의 동일성은 로컬 자료로 검증되지 않음 |
| ID-12 | 1793-06-13 구순 기사 인물 | 1793-06-13 이여절 기사 인물 | SAME_DATE_NOT_SAME_CASE | 같은 날 실록 기사라는 이유로 사건 병합 금지 |
| ID-13 | 풍각 김생원·풍각 김상제 | 김명신 | SAME_PERSON_RESOLVED_BY_PRIOR_REPO | 선행 저장소 ID05·ID10 |
| ID-14 | 한 비장·한가 | 한재욱 | SAME_PERSON_RESOLVED_BY_PRIOR_REPO | 선행 저장소 ID02·ID03 |
| ID-15 | 병사 | 이광섭 | SAME_PERSON_RESOLVED_BY_PRIOR_REPO | 선행 저장소 ID01 |
