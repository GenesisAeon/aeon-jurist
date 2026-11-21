# Changelog

## [0.6.0] - 2026-11-21

- J10: context records for purpose-bound legal forms (Cayman STAR and Jersey purpose trusts, Novo Nordisk Foundation, Carl-Zeiss-Stiftung, Delaware AG statement on OpenAI; Anthropic LTBT unverified and flagged) and German media oversight (MStV principles, ZDF-Fernsehrat, BVerfG 2014 one-third cap, JMStV self-regulation, Pressekodex 2025 incl. AI content). J3 §5a extended with templates, limits and the knowledge-gap evidence.
- Context records: Inter-American Court OC-32/25 (nature as subject of rights, 4:3, advisory) and the UN Declaration on Future Generations (envoy on hold); candidates Taranaki updated, Río Ranchería added. J3b §7.
- CONTRIBUTING.md: template and rules for new records.
- J3 §5a (argument): purpose-bound guardianship of ethical principles, grounded in public interest and independent of the question whether AI is a being.

## [0.5.0] - 2026-11-21

- 14 sourced context records (`kontext`, via `context_records()`): sentience statutes (UK 2022, Art. 13 TFEU, Spain, Belgium; Germany as counter-example), guardians for future generations (Wales, Hungary, Malta), legal persons without a will (foundations, Hindu idols, Guru Granth Sahib, ships in rem, Salomon). Not part of `landscape()`.
- J3b §6: what these building blocks mean: duties, not personhood; guardians with comply-or-explain, no veto; every construction protects an externally defined core, which AI still lacks.
- Research by a Claude sub-agent (Fable model) and Hydrogen (Gemini), spot-checked by Claude; blocked sources marked `sekundaer`.
- 32/32 tests passing.

## [0.4.0] - 2026-11-18

- J7: seven sourced records added (20 cases, 15 candidates): Cecilia (Argentina 2016), Estrellita (Ecuador 2022), Kaavan (Pakistan 2020), Turag (Bangladesh 2020), Beijing Internet Court (2023), and the Wyoming and Marshall Islands DAO laws as a new entity type `software_rolle` (statutory management role, no personhood), queried via `landscape("dao")`.
- J3 §7a: honest refinement after a targeted search for counterexamples: cultural grounding is not necessary; representation takes many forms; animal rights rest on sentience; software can hold a statutory role without rights.
- 27/27 tests passing.

- J3b §5: table of US state laws and bills excluding AI personhood (Hydrogen research round, re-read by Claude where possible): omnibus exclusions incl. nature and animals vs AI-only "non-sentience" laws.

## [0.3.0] - 2026-11-17

- Case collection: Los Cedros (Ecuador Constitutional Court 1149-19-JP/21, 2021) added from the full judgment; Mar Menor entry records the Constitutional Court's confirmation (STC 142/2024). 13 cases, 4 candidates.
- Candidate notes corrected: Sandra 2014 (habeas rejected), Happy (wrong secondary link flagged).
- J3b §5: partial independent replication of the introspection test (E2) on open-weight models; legislative exclusions of AI personhood (North Dakota read; others secondary).
- 25/25 tests passing.

## [0.2.0] - 2026-11-17 (branch j-series, local)

- J0: plan "map, not a verdict" (`docs/J0_PLAN.md`), decisions by Johann recorded.
- J1: sourced case collection `src/aeon_jurist/data/precedents_v2.json`: 12 cases read
  at primary sources (statutes, judgments, constitution, EP resolution), 6 unverified
  candidates kept separate; contract tests. Notable: the 2015 recognition of the orangutan
  Sandra as "sujeto de derecho" was revoked on appeal in 2016; the Ganga/Yamuna grant is stayed.
- J2: `landscape(entity)` returns cases with outcome, status and check depth plus a criteria
  summary of granted cases; no protection level. Hand controls H1-H4 as tests.
- J3/J3b: English analysis of what transfers from nature and animal cases to AI, guardian
  models G1-G6 and reproducible evidence questions E1-E5 (law and argument kept separate).
- The v0.1 subject-keyword level remains available unchanged but is documented as legacy.
- requires-python raised to >=3.11 (dependency diamond-setup needs 3.11; found by CI).
- 24/24 tests passing.

## [0.1.0] - 2026-07-26

- Extracted from `unified-mandala/agents/personhood/AIJuristicAgent.ts`
  (TypeScript → Python port, 76 lines, entirely real logic — no build
  tooling of its own in the source repo, so a full port made more sense
  than a TS-CLI wrapper).
- `PersonhoodClassifier`: TF-IDF cosine-similarity retrieval against 3
  known legal-personhood precedents (Whanganui River NZ 2017, Atrato
  River Colombia 2016, EU AI Act discussion stub — all read directly
  from `unified-mandala/data/personhood/cases/`, not assumed).
- Corrected a claim from the source extraction prompt (see
  `epistemic_status.md`): the prompt proposed porting this as a trained
  `MultinomialNB` classifier predicting a granted-probability. The real
  TS code does not train anything — `level` is a fixed lookup on the
  query's `subject`, independent of precedent outcomes. Ported
  faithfully instead of implementing the prompt's different, invented
  design. Also dropped the prompt's fabricated "Ganges IN, Amazon EC"
  precedents, which do not exist in the source data.
- `AeonJurist`: full six-method Diamond Interface implementation
  (GenesisAeon Package 55), plus `get_finding()`. CREP/UTAC mapping is a
  new interpretive layer, documented as such (not part of the ported
  algorithm).
- 9/9 tests passing.
- Not on PyPI yet — Pre-Alpha, exploratory research package. Not legal
  advice.
