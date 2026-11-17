# Changelog

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
