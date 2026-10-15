# REQUEST_FOR_RESEARCHER — 원문 제공 요청

> 자동 생성(`data/curated/research_requests.csv`). 오프라인 규칙상 Claude Code는 외부 사이트에 접속하지 않았다. 아래 원문이 로컬로 제공되면 해당 span을 등급 A(`VERBATIM_ORIGINAL`)로 추가하고 `python -m historinference all`을 다시 실행한다. 제공 전까지 관련 값은 `NA` 또는 미확정 상태로 둔다.


## 우선순위 HIGH

### RQ-CH-01 · CHOI
- **인물**: CHOI-P01 박씨, CHOI-P02 최아지, CHOI-P03 이차망, CHOI-P06 조광진, CHOI-P07 사단
- **쟁점**: 1785~1789 전 과정의 문장 단위 원문·국역 대조
- **출처 ID**: CH-001 심리록 1785-1789 <https://db.history.go.kr/joseon/item/level.do?allViewYn=Y&levelId=jlawb_420_0080_0040_0030>, CH-002 추관지 1787;1789 <https://db.history.go.kr/joseon/item/level.do?levelId=jlawb_200r_0020_0020_0050_0090_0080>
- **요청 원문/일자**: 심리록 권8 「평산 최아지 옥」 및 추관지 「최 조이 옥안」 전문(원문+국역; 문단·일자 표시)
- **코딩을 막는 이유**: CHOI 코딩 26행 중 다수가 2차 종합(D등급) 근거에 의존(MC-CH-03·12·13·15·19·20·25·26 등); 증거 등급 B 컷오프에서 CHOI 앵커 탈락

### RQ-CH-02 · CHOI
- **인물**: CHOI-P06 조광진, CHOI-P07 사단
- **쟁점**: 조광진의 사단 종용·형 7도 자백·1788 瘐死의 원문 구절
- **출처 ID**: CH-002 추관지 1787;1789 <https://db.history.go.kr/joseon/item/level.do?levelId=jlawb_200r_0020_0020_0050_0090_0080>
- **요청 원문/일자**: 1787 이곤수 안핵 공초(사단·조광진)와 1789 형조 회계의 '작년에 이미 죽었다' 구절
- **코딩을 막는 이유**: R02·R03·F04 코딩(현재 D등급)과 사망 후 행위 검사(조광진 사망 일자)

### RQ-CH-03 · CHOI
- **인물**: CHOI-P09 조봉원
- **쟁점**: 군교 조봉원 관련 뇌물·5냥·위협 주장의 원문과 주장자
- **출처 ID**: CH-001 심리록 1785-1789 <https://db.history.go.kr/joseon/item/level.do?allViewYn=Y&levelId=jlawb_420_0080_0040_0030>, CH-002 추관지 1787;1789 <https://db.history.go.kr/joseon/item/level.do?levelId=jlawb_200r_0020_0020_0050_0090_0080>
- **요청 원문/일자**: 조봉원·5냥·매수가 언급된 공초·판부 문장
- **코딩을 막는 이유**: E04 뇌물 코딩이 NA(UNKNOWN); RL-CH-12 관계 미식별

### RQ-CHO-01 · CHO
- **인물**: CHO-P01 조재항, CHO-P02 윤씨, CHO-P03 이가원
- **쟁점**: 심리록·추관지 조재항 옥안 전문과 연도 충돌(1780 庚子 vs 1781 辛丑)
- **출처 ID**: JH-001 심리록 1780-1783 <https://db.history.go.kr/joseon/item/level.do?levelId=jlawb_420_0020_0120_0040>, JH-002 추관지 1781-1783 <https://db.history.go.kr/joseon/item/level.do?levelId=jlawb_200_0020_0020_0050_0080_0080>, JH-003 정조실록 1783-06-03 <https://sillok.history.go.kr/id/kva_10706003_004>
- **요청 원문/일자**: 심리록 「백천 조재항 옥」·추관지 「조재항 옥안」 전문 및 실록 1783-06-03 원문
- **코딩을 막는 이유**: CL-JH-09/10 날짜 충돌; EV-JH-01·02 범위 날짜

### RQ-CHO-02 · CHO
- **인물**: CHO-P01 조재항
- **쟁점**: 조재항 구금 사실·기간·장소
- **출처 ID**: JH-001 심리록 1780-1783 <https://db.history.go.kr/joseon/item/level.do?levelId=jlawb_420_0020_0120_0040>, JH-002 추관지 1781-1783 <https://db.history.go.kr/joseon/item/level.do?levelId=jlawb_200_0020_0020_0050_0080_0080>
- **요청 원문/일자**: 구금·옥중 신문을 기술한 원문 구절
- **코딩을 막는 이유**: F02 코딩이 석방 명령에서 전제 추론된 상태(EV-JH-03)

### RQ-YE-01 · YE
- **인물**: YE-P01 이여절, YE-P03 유경, YE-P05 사망자들
- **쟁점**: 31명(1795-06-04)과 25명(1795-08-24) 수치의 집계 범위·피해자 명단
- **출처 ID**: YE-004 정조실록 1795-06-04 <https://sillok.history.go.kr/id/kva_11906004_006>, YE-006 정조실록 1795-08-24 <https://sillok.history.go.kr/id/kva_11908024_003>
- **요청 원문/일자**: 두 기사 전문(원문+국역)과 사망자 이름 부분
- **코딩을 막는 이유**: CL-YE-03/04 SOURCE_RECONCILIATION 축 미해결

### RQ-YE-02 · YE
- **인물**: YE-P02 조진택
- **쟁점**: 1794-09-08 조진택 보고의 면책 논리 원문과 1795-06-11 질책 원문
- **출처 ID**: YE-003 정조실록 1794-09-08 <https://sillok.history.go.kr/id/kva_11809008_002>, YE-005 정조실록 1795-06-11 <https://sillok.history.go.kr/id/kva_11906011_001>
- **요청 원문/일자**: 두 기사 원문
- **코딩을 막는 이유**: E02(허위 보고) NA; 고의/태만 구분(fault_type UNRESOLVED)

### RQ-YE-03 · YE
- **인물**: YE-P01 이여절, YE-P02 조진택
- **쟁점**: 1795-09-21 처분 원문과 집행
- **출처 ID**: YE-007 정조실록 1795-09-21 <https://sillok.history.go.kr/id/kva_11909021_001>
- **요청 원문/일자**: 조진택 삭직·이여절 위원 유배 기사 및 후속 집행 기록
- **코딩을 막는 이유**: DC-YE-03/04 execution NOT_RETRIEVED; 레지스터 '삭직' vs 근거집 'dismissal' 표기 차이


## 우선순위 MEDIUM

### RQ-CH-04 · CHOI
- **인물**: CHOI-P13 엄사만, CHOI-P15 정경증, CHOI-P16 이단회
- **쟁점**: 엄사만·홍병찬 재임 기간과 검험관 정경증·이단회의 초검/복검 배정
- **출처 ID**: CH-001 심리록 1785-1789 <https://db.history.go.kr/joseon/item/level.do?allViewYn=Y&levelId=jlawb_420_0080_0040_0030>, CH-002 추관지 1787;1789 <https://db.history.go.kr/joseon/item/level.do?levelId=jlawb_200r_0020_0020_0050_0090_0080>, CH-003 정조실록 1787-04-16 <https://sillok.history.go.kr/id/kva_11104016_003>
- **요청 원문/일자**: 초검·복검 보고 주체와 각 관찰사의 재임 기간 기사
- **코딩을 막는 이유**: 검험관 역할 미확정; appointments tenure NOT_RETRIEVED

### RQ-CH-05 · CHOI
- **인물**: CHOI-P03 이차망, CHOI-P04 민씨
- **쟁점**: 민씨 격쟁(1786-01·1786-11)의 승정원일기·일성록 일자와 순평군 후손 주장 원문
- **출처 ID**: CH-007 장서각 왕실족보 시기 미상 <https://jsg.aks.ac.kr/dir/view?dataId=JSG_K2-1140>
- **요청 원문/일자**: 승정원일기·일성록 1786년 해당 일자 기사 및 장서각 선원속보 등재 면
- **코딩을 막는 이유**: 이차망 status_claimed는 CONTESTED·status_verified NA 유지; 격쟁 일자는 2차 종합 근거

### RQ-CH-06 · CHOI
- **인물**: CHOI-P02 최아지
- **쟁점**: 1789-06 장 100·유 2천 리 준용 승인 이후 실제 집행 기록
- **출처 ID**: CH-001 심리록 1785-1789 <https://db.history.go.kr/joseon/item/level.do?allViewYn=Y&levelId=jlawb_420_0080_0040_0030>, CH-002 추관지 1787;1789 <https://db.history.go.kr/joseon/item/level.do?levelId=jlawb_200r_0020_0020_0050_0090_0080>
- **요청 원문/일자**: 1789년 이후 최아지 형 집행·배소 기록
- **코딩을 막는 이유**: DC-CH-08 execution_status NOT_RETRIEVED

### RQ-CHO-03 · CHO
- **인물**: CHO-P05 조재풍, CHO-P06 배조이, CHO-P07 나막동, CHO-P08 점렬, CHO-P09 막덕
- **쟁점**: 조재풍·배조이·나막동·점렬·막덕의 역할과 진술 내용
- **출처 ID**: JH-003 정조실록 1783-06-03 <https://sillok.history.go.kr/id/kva_10706003_004>, JH-002 추관지 1781-1783 <https://db.history.go.kr/joseon/item/level.do?levelId=jlawb_200_0020_0020_0050_0080_0080>
- **요청 원문/일자**: 각 인물 공초·언급 문장
- **코딩을 막는 이유**: RL-CHO-03 사주 대상 증인 특정 불가; 인물 프로필 NA

### RQ-CHO-04 · CHO
- **인물**: CHO-P01 조재항, CHO-P04 조상진
- **쟁점**: 조재항·가족의 호소 여부와 조상진의 재임 도(道)명
- **출처 ID**: JH-001 심리록 1780-1783 <https://db.history.go.kr/joseon/item/level.do?levelId=jlawb_420_0020_0120_0040>, JH-002 추관지 1781-1783 <https://db.history.go.kr/joseon/item/level.do?levelId=jlawb_200_0020_0020_0050_0080_0080>, JH-003 정조실록 1783-06-03 <https://sillok.history.go.kr/id/kva_10706003_004>
- **요청 원문/일자**: 상언·격쟁 기록 및 조상진 관직 기사
- **코딩을 막는 이유**: R06 NA; Y6가 친척 고발 경로로만 PARTIAL

### RQ-YE-04 · YE
- **인물**: YE-P03 유경
- **쟁점**: 유경의 관직·임명 일자와 1795-06-11 '별도 안핵'의 담당자
- **출처 ID**: YE-004 정조실록 1795-06-04 <https://sillok.history.go.kr/id/kva_11906004_006>, YE-005 정조실록 1795-06-11 <https://sillok.history.go.kr/id/kva_11906011_001>
- **요청 원문/일자**: 유경 임명 기사·1795-06-11 원문
- **코딩을 막는 이유**: DC-YE-01 담당자 미특정; 유경 보고(06-04)와 별도 안핵 명령(06-11) 선후 해석

### RQ-YE-06 · YE
- **인물**: YE-P05 사망자들
- **쟁점**: 유족·피해자 측 호소 기록
- **출처 ID**: YE-004 정조실록 1795-06-04 <https://sillok.history.go.kr/id/kva_11906004_006>, YE-005 정조실록 1795-06-11 <https://sillok.history.go.kr/id/kva_11906011_001>, YE-006 정조실록 1795-08-24 <https://sillok.history.go.kr/id/kva_11908024_003>
- **요청 원문/일자**: 피해자 가족 상언·진술 구절
- **코딩을 막는 이유**: R06 NA; YE 앵커 Y6 NONE

### RQ-GS-01 · GUSUN
- **인물**: GUSUN-P02 김명신, GUSUN-P07 한재욱, GUSUN-P12 자미덕
- **쟁점**: GuSoon 선행 코딩과 1793-06-13 원문의 문장 단위 재대조
- **출처 ID**: GS-006 정조실록 1793-06-13 <https://sillok.history.go.kr/id/kva_11706013_003>
- **요청 원문/일자**: 실록 1793-06-13 구순 기사 원문(자미덕·한재욱·이진욱 공초 부분)
- **코딩을 막는 이유**: GuSoon 명제는 B등급(선행 코딩); A등급 승격 불가

### RQ-GS-02 · GUSUN
- **인물**: GUSUN-P01 구순
- **쟁점**: 구순 의금부 구금·신문 명령(5-12·5-27)의 실행 기록
- **출처 ID**: GS-001 정조실록 1793-05-12 <https://sillok.history.go.kr/id/kva_11705012_003>, GS-002 비변사등록 1793-05-27 <https://db.history.go.kr/common/compareViewer.do?levelId=bb_181r_001_05_0510&type=joseon>, GS-003 정조실록 1793-05-27 <https://sillok.history.go.kr/id/kva_11705027_002>
- **요청 원문/일자**: 의금부 신문 결과 기사
- **코딩을 막는 이유**: DC-GS-02/04 execution NOT_RETRIEVED(선행 gap G13)

### RQ-ALL-01 · ALL
- **인물**: -
- **쟁점**: 일성록·승정원일기·비변사등록의 네 사건 동일 사안 기사(검색 미실행)
- **출처 ID**: -
- **요청 원문/일자**: 각 사건 일자별 기사 목록(연구자 오프라인 제공)
- **코딩을 막는 이유**: 모든 사건 NOT_COLLECTED; 독립성 그룹 판단 보류


## 우선순위 LOW

### RQ-YE-05 · YE
- **인물**: YE-P01 이여절
- **쟁점**: 1789-07-14 단천부사와 1793 창원부사 이여절의 동일인 검증
- **출처 ID**: YE-001 정조실록 1789-07-14 <https://sillok.history.go.kr/id/kva_11307014_001>, YE-002 정조실록 1793-06-13 <https://sillok.history.go.kr/id/kva_11706013_002>
- **요청 원문/일자**: 두 기사 원문
- **코딩을 막는 이유**: ID-08 PRESUMED_SAME_BY_REGISTER_UNVERIFIED

### RQ-GS-03 · GUSUN
- **인물**: GUSUN-P02 김명신, GUSUN-P03 김명신의 아내
- **쟁점**: 김명신 유족의 이의제기 기록
- **출처 ID**: GS-001 정조실록 1793-05-12 <https://sillok.history.go.kr/id/kva_11705012_003>, GS-002 비변사등록 1793-05-27 <https://db.history.go.kr/common/compareViewer.do?levelId=bb_181r_001_05_0510&type=joseon>, GS-005 비변사등록 1793-06-11 <https://db.history.go.kr/common/compareViewer.do?levelId=bb_181r_001_06_0070&type=joseon>, GS-006 정조실록 1793-06-13 <https://sillok.history.go.kr/id/kva_11706013_003>
- **요청 원문/일자**: 유족 상언·격쟁 구절
- **코딩을 막는 이유**: R06 NA; GUSUN 앵커 Y6 NONE

### RQ-ALL-02 · ALL
- **인물**: -
- **쟁점**: 음력→양력 환산표
- **출처 ID**: -
- **요청 원문/일자**: 연구자가 승인한 환산표 파일
- **코딩을 막는 이유**: 모든 날짜 solar NOT_COMPUTED

