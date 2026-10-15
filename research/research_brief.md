# Four-case evidence brief — preliminary source collection

**Research date:** 2026-10-16. **Status:** source discovery / pre-coding. **Not a completed full-text collection or coded dataset.** See [source_register.csv](source_register.csv) for links and verification distinctions.

## Research scope and domains

The project follows source locations present in `GuSoon-Inference`: `sillok.history.go.kr` (조선왕조실록), `db.history.go.kr` (한국사데이터베이스: 심리록/추관지/비변사등록), `sjw.history.go.kr` (승정원일기), `encykorea.aks.ac.kr` (historical institution context), `contents.history.go.kr` (우리역사넷), supplemented with `Chamang-Inference` case provenance. New candidate sources must be corroborated against original records. Avoid treating historical compilations of the same royal decision as independent witnesses.

### CHOI — 平山 崔阿只・李次望

**1785–1789**, 황해도 평산. Records of the death of 박씨, initial reports of self-inflicted injury, family accusations, claim that 이차망 conspired with 최아지, detention, his wife 민씨's petitions, appointment of 안핵어사 이곤수, eventual release order for 이차망 in 1787. **Critical twist:** 정조's 1789 thirty doubts concerning murder/sexual claims raised questions about 1787 evidence and interrogation, so 1787 version is **not** final omniscient ground truth. Evidence of bribery and kinship ties to magistrates remains attributed/contested. Distinguish royal-kin descendant claim for 이차망 from genealogically verified status. **Source locators:** CH-001..008. Existing full preliminary report: [Chamang-Inference report](https://github.com/Leewonseol/Chamang-Inference/blob/main/reports/pyeongsan_case_report.md). Need targeted verification of original dates, each person's age/office/status, 1789 decision *versus execution*.

### CHO — 白川 趙載恒

**1780–1783**, 황해도 백천/배천. Death of wife 윤씨 and accusation by 이가원; manipulated testimony and circulated song alleged in official final decision. 조재항 was detained for homicide, ultimately released; denunciation of 관찰사 조상진 for relying on earlier reports. **The accusation maker is not proven killer of 윤씨**, nor is official conspiracy with the informer established. Source locators JH-001..003. Need identity checking for 이가원·이간원 variants and detailed primary span extraction.

### YE — 李汝節・趙鎭宅

**1793–1795** 창원 사건; earlier career evidence only context. Reports of unlawful beating resulting in deaths, reports by governor 조진택 downplaying responsibility, royal criticism of the provincial investigation and independent special inquest by 유경. **1795-06-04 reports 31 dead and 1795-08-24 reports 25:** preserve as two source-attributed values until accounting scope understood. 1793-06-13 이여절 promotion and 구순 심리 are unrelated even though same-date chronicles. 1801 황기운 mistaken identification is a **separate** criminal episode and cannot make 1795 case a proven wrongful homicide conviction. Source locators YE-001..009; later 1843 precedent is later retrospective evidence only.

### GUSUN — 具純・金明信

**1793**, 충청도 청주 덕평/공주 병영 network. Personal falling-out, theft accusation, arrest and detention of 김명신, his death, divergent reporting by 이형원/이조원/윤노동, 홍대협 special inquiry, final royal decision. **Important ambiguity:** officials disagree over theft extent, 김명신's treatment and proximate cause of death. 정조 did not make direct causation certain. Use [GuSoon source pack](https://github.com/Leewonseol/GuSoon-Inference/tree/main/gusun_clean_restart_csv_pack) and preserve source provenance, no imputed fatal torture. Source locators GS-001..008.

## Collection quality and blockers

- **28 registered locator records, not 28 complete copied texts.** Earlier GuSoon source file with 8 official records was imported as a vetted inventory; not a fresh full transcription. Chamang reports and CSV are prior prepared materials, not independent archival originals.
- Primary text excerpts must be pinned to *article-level URLs and original phrases* before receiving `DOCUMENTED_ACT` or `OFFICIAL_JUDGMENT`. If web search only provides partial excerpts, label `SEARCH_SNIPPET_ONLY` at statement level.
- CHOI and CHO have detailed multi-year judicial dossiers. YE has procedural corruption details but lacks documented falsely accused substitute murderer; GUSUN has detention/death but uncertain cause and short 1793 span.
- No case currently proves **every** desired element, in particular 'actual killer punished + government collusion + wrongful accused exonerated', without interpretative gaps.
- No spurious posterior probability or training an ML model on n=4.
- Ingestion should prioritize public-domain historical source text when reuse is permitted, compare edition/version provenance and extraction integrity; preserve source dates and translations separately.

## Initial research questions
1. For CHOI, what were the prosecutor/inspection officer kinship relations, and is the five-nyang bribery assertion corroborated or rejected? Who exactly did what on which date?
2. For CHO, exactly how did fabricated evidence move from an informer to an official report; was there any direct agreement with officials?
3. For YE, which officeholder reported 31 and 25 deaths, over what time horizon, and what were the victim profiles? Did any falsely accused person arise in **the same 1795 event**?
4. For GUSUN, trace original sequence from the 1793-02 allegations to the June decrees; isolate what was actually proven vs reported.

## Collection-before-coding handoff
Treat each URL as **a retrieval lead**, not an authenticated claim. Claude Code first runs source retrieval & logging, then derives atomic claims from retrieved paragraphs, with separate event/source/claim/evidentiary status and identity tracking. Add institutional rules with validity ranges, *not* frequency-based priors.
