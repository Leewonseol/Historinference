# Offline evidence pack — four Joseon judicial cases

Prepared 2026-10-16. **This is an offline, source-attributed research digest, not a full transcription of original historical documents.** Claude Code must not try to visit linked URLs. The original texts NOT included in repository are unavailable to the offline model and must not be simulated. Authorized sources: official Joseon Annals, NIKH Korean History Database and Seungjeongwon archives. The 22-row `research/source_register.csv` lists verified-institution site locations, not complete captured texts.

## Files now actually present in Historinference
- `research/imported/gusun/00_INPUT_MANIFEST.csv` – dataset manifest from original GuSoon repo
- `research/imported/gusun/01_confirmed_facts.csv` – prior coding, not original historical manuscript
- `research/imported/gusun/02_institutional_normative_features.csv` – context claims, period validity restrictions
- `research/imported/gusun/03_environment_1793.csv` – context data
- `research/imported/gusun/04_source_records.csv` – original link index
- `research/imported/gusun/05_source_faithful_propositions_AUDIT_ONLY.csv` – audit propositions, **not indisputably proven facts**; preserve audit status
- `research/imported/chamang/pyeongsan_case_report.md` – previous research narrative, **not verbatim official text**

## Evidentiary code
- `RESEARCH_SUMMARY_WITH_OFFICIAL_REFERENCE`: synthesis attributed to official source, underlying exact excerpt not included offline.
- `IMPORTED_PREVIOUS_CODED_DATA`: earlier structured dataset. Must reconcile to official text before assigning highest certainty.
- `SOURCE_TEXT_NOT_STORED`: URL exists but actual source text not copied. Do not hallucinate.
- `DISPUTED_OFFICIAL_JUDGMENT`: a historical official's assertion is documented; does NOT conclusively prove the assertion's factual content.
- `FICTION_ONLY`: permissible construction only in the synthetic story layer.

## CHOI: 平山 崔阿只 / 李次望 (1785–1789)
Official record locations:
- CH-001 `심리록` https://db.history.go.kr/joseon/item/level.do?levelId=jlawb_420_0080_0040_0030
- CH-002 `추관지` https://db.history.go.kr/joseon/item/level.do?levelId=jlawb_200r_0020_0020_0050_0090_0080
- CH-003 `정조실록` https://sillok.history.go.kr/id/kva_11104016_003

Source-anchored digest (not primary text):
- A woman identified as 박씨 died in Pyeongsan; conflicting accounts concerned self-inflicted wounds vs homicide and the role of 최아지, 이차망 and 조광진. [CH-001, CH-002; RESEARCH_SUMMARY_WITH_OFFICIAL_REFERENCE]
- Initial investigations and reassessment led to 이차망 being accused/detained; wife 민씨 petitioned; investigator 이곤수 later examined contradictory statements and 왕명 ordered release in 1787. [CH-001..003]
- 1789 reconsideration raised 30 separate questions (adultery and murder) and scrutinized reliability of interrogations and statements. DO NOT treat 1787 'guilt of other person' as final established physical truth. [CH-001,CH-002]
- The specific claim that 이차망 was a descendant of 순평군 is *wife 민씨's petition*, not independent genealogical proof; the precise Seungjeongwon primary text is **not stored** here.
- Kinship of 최아지/조씨 household and officers, bribery involving 군교 조봉원, five nyang, concealment, and collusive reporting were all previously discussed as **claims/official concerns**, not universally proven conspiracies. Exact primary paragraphs must be requested if feature-level coding needs them.
- Do not infer 이차망's age, legal status, property, formal noble registration, or blood kinship with 최아지 without original span.

## CHO: 白川 趙載恒 (1780–1783)
- JH-001 `심리록` https://db.history.go.kr/joseon/item/level.do?levelId=jlawb_420_0020_0120_0040
- JH-002 `추관지` https://db.history.go.kr/joseon/item/level.do?levelId=jlawb_200_0020_0020_0050_0080_0080
- JH-003 `정조실록` https://sillok.history.go.kr/id/kva_10706003_004

Source-anchored digest:
- 조재항 was accused of causing wife 윤씨's death; informer 이가원 was held responsible in royal judgment for manipulating reports, testimony and village opinion, including circulating a song. [JH-001..003; OFFICIAL_JUDGMENT, NOT automatically independent factual finding]
- Review eventually led to order to release 조재항, punish 이가원 and hold provincial governor 조상진 responsible. [JH-003]
- No established separate true *killer* of 윤씨. Do not reframe the malicious accuser as the deceased's proven murderer, nor assert coordination between governor and informer absent evidence.

## YE: 李汝節 / 趙鎭宅 (1793–1795)
- YE-003 `정조실록` https://sillok.history.go.kr/id/kva_11809008_002
- YE-004 `정조실록` https://sillok.history.go.kr/id/kva_11906004_006
- YE-005 `정조실록` https://sillok.history.go.kr/id/kva_11906011_001
- YE-006 `정조실록` https://sillok.history.go.kr/id/kva_11908024_003
- YE-007 `정조실록` https://sillok.history.go.kr/id/kva_11909021_001

Source-anchored digest:
- 창원부사 이여절 was investigated for abusive punishment causing deaths; former governor 조진택's supervisory investigation/report was sharply questioned and characterized by 정조 as serving the official's defense. [YE-003..005; differentiate administrative failure from secret prearranged collusion]
- A 1795 June investigation reported **31** persons dead, while an August review discussed **25** killed by beating. Treat as two differently scoped *attributed count claims* until original passages, categories and date ranges are reconciled. [YE-004,YE-006]
- 유경 was assigned to special inquiry and final sanctions included 이여절's exile and 조진택's dismissal (verify each execution against source). [YE-005,YE-007]
- No established *replacement murderer falsely convicted in this same incident*. Separate 1801 黃基運 mistaken-identification event MUST NOT be fused into 1795 case.

## GUSUN: 具純 / 金明信 (1793)
Core originals indexed in `research/imported/gusun/04_source_records.csv`:
- GS-001 `정조실록` https://sillok.history.go.kr/id/kva_11705012_003
- GS-002 `비변사등록` https://db.history.go.kr/common/compareViewer.do?levelId=bb_181r_001_05_0510&type=joseon
- GS-003 `정조실록` https://sillok.history.go.kr/id/kva_11705027_002
- GS-004 `승정원일기` https://sjw.history.go.kr/search/inspectionDayList.do?wday=17930528L0
- GS-005 `비변사등록` https://db.history.go.kr/common/compareViewer.do?levelId=bb_181r_001_06_0070&type=joseon
- GS-006 `정조실록` https://sillok.history.go.kr/id/kva_11706013_003

Source-anchored digest:
- 구순's accusations concerning theft led to 김명신's detention under military/provincial investigation; 김명신 died; distinct reports from 이형원, 이조원, 윤노동 and special inspector 홍대협 conflicted on substantive details. [GS-001..006; prior normalized propositions locally imported]
- Ultimate royal judgment and sanctions must be coded against June 13 original account; **direct causal mechanism of 김명신's death is not conclusively fixed** by this digest. [GS-006]
- Do not treat different administrative authors' statements as interchangeable independent objective facts.
- Date-context rules: 1792 revised forensic handbook must not be backdated to the 1780s cases; 1786 enforcement of 대전통편 must not be backdated to events in 1785.

## What requires new researcher-supplied primary texts
1. Full original/authorized translation of CH-001 and CH-002, paragraph/span-level with dates. Particularly claims concerning 조광진, 사단, 조봉원, relatives of examiners, money, 이차망 status.
2. Full original JH-001 and JH-002 to distinguish described witness manipulation from official claims.
3. YE-003..007 to reconcile 31 vs 25 and identify individuals and exact dispositions.
4. GS-006 original if normalized GuSoon dataset does not contain faithful quote for every coded action.
5. Explicit issue-date/record URL for 1786 민씨's 순평군 petition, not just secondary report.
6. Missing 《일성록》 and other same-event records: must remain `NOT_COLLECTED`, not silently assumed absent.

**No automatic evidence upgrading:** Imported reports/code and this digest support research planning and low-confidence claim registers; direct original passage is necessary for high-confidence historical truth and any authored allegation of intentional corruption. Citations retained here are source locations, not local verified article transcriptions.
