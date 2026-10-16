# 상태 보고

> 자동 생성 문서(`python -m historinference report`). 모든 수치는 `data/normalized`·`models`·`data/audit`에서 재계산된다. 원문 미보관(UNAVAILABLE_SOURCE_TEXT) 상태에서 로컬 요약·선행 코딩만으로 작성되었으며, 확률·빈도 추정은 하지 않는다.

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
