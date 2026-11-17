# Epistemic Status — aeon-jurist (P55)

## Update v0.2.0 (17 Nov 2026)
- The flaw described below (level by subject keyword, "ai" always P2) is no longer the
  recommended behaviour. `landscape()` derives nothing from keywords except which entity
  types to show, and it never outputs a level. The legacy classifier is unchanged, so its
  behaviour stays reproducible.
- Case data now comes from `src/aeon_jurist/data/precedents_v2.json`: only cases whose
  wording was read at a primary source (or an identified copy of one) are records; check
  depth is stored per case. Blocked official sites are listed in `docs/J1_PRECEDENTS.md`.
- The analyses in `docs/J3*.md` separate LAW (sourced) from ARGUMENT (reasoning). They were
  written by an AI about AI; that potential bias is disclosed in both documents.

Status: EXPLORATORY — Pre-Alpha, faithful port + honestly-scoped Diamond wrapper.

## What this package is

Ported from `unified-mandala/agents/personhood/AIJuristicAgent.ts` (76
lines — the entire file is the real logic, no dead weight). A TF-IDF
cosine-similarity search retrieves the most similar known legal-personhood
precedent to a query about a given entity ("river"/"forest"/"tree"/"ai"/
"org"), and assigns a protection level.

## Correction to the source prompt's assumed design

The prompt that requested this extraction (`p55_and_go_governance_prompts.md`)
suggested porting this as a **trained `MultinomialNB` classifier** predicting
a `personhood_score` (probability of "granted"). That is not what the
original TypeScript code does, and would have been a different algorithm,
not a port. Verified directly against `AIJuristicAgent.ts`:

- `level` (P0/P1/P2) is a **fixed lookup on the query's `subject`** —
  `river`/`forest`/`tree` → `P1`, `ai` → `P2`, everything else → `P0`.
  It is **not** derived from the retrieved precedent's `granted` field or
  from the similarity score at all.
- The TF-IDF cosine search only feeds `confidence` (a bounded transform
  of the top similarity score) and `similar_cases` (the retrieved case
  names above a 0.12 threshold).
- There is no training step, no probability model, no `granted`
  prediction anywhere in the original code.

`classifier.py` ports this faithfully (`analyze()`/`tfidfCosine()` →
`PersonhoodClassifier.analyze()`), using scikit-learn's `TfidfVectorizer`
+ `cosine_similarity` as an idiomatic implementation of the same
algorithm class. Numeric parity with the hand-rolled TS implementation
isn't guaranteed (tokenization/smoothing differ slightly), but the
retrieval approach and the classification rule are identical — verified
directly with `test_level_is_subject_based_not_outcome_based`, which
would fail immediately if this package quietly reverted to the prompt's
proposed (different) design.

**Real consequence worth flagging explicitly**: because `level` ignores
outcome, a query with `subject="ai"` always gets `"P2"` — a real, if
modest, protection category — even though the *only* AI precedent in
this package's data (`EU AI Act (stub)`) explicitly documents a
**non-grant** ("no general personhood for AI"). This is not a bug
introduced by this port; it is exactly what the original TS code does.
Whether that's the intended behavior of the original design (a category
assignment, not an outcome prediction) or an oversight is not something
this port can resolve — flagged for Johann's judgment, not silently
"fixed" to be outcome-based.

## Precedent data — verified against the real source files, not assumed

`unified-mandala/data/personhood/cases/` has exactly 3 files, all read in
full before writing `precedents.py`:

- `river_whanganui_nz.md` → Whanganui River (NZ, 2017) — a real, granted
  personhood case. The source markdown was a one-line description with
  tags, no formal citation; the statute reference (*Te Awa Tupua
  (Whanganui River Claims Settlement) Act 2017*) was added here as the
  well-established, independently verifiable real citation, not
  invented.
- `colombia_atria_river.md` → Atrato River (Colombia, 2016) — likewise a
  real, granted case. Note: the **filename** has a typo ("Atria" instead
  of "Atrato") in the original `unified-mandala` repo; the river's actual
  name (Atrato) is used correctly in `precedents.py`. Citation added the
  same way (*Constitutional Court of Colombia, Judgment T-622 of 2016*).
- `eu_ai_act_discussion_stub.md` → explicitly self-labeled a "stub" in
  its own filename, not a citable ruling — a discussion of AI liability
  with an explicit non-grant, kept as `granted=False` with a plain note
  that no formal citation exists in the source data.

**Only 3 precedents total, 2 of them real rulings.** The prompt's own
`to_zenodo_record()` template text mentioned "Ganges IN, Amazon EC" as
additional precedents — those do **not** exist anywhere in the actual
`unified-mandala` data. Not included here; the Zenodo description and
`test_system.py::test_run_cycle_and_diamond_interface` both explicitly
check that "Ganges" does not appear, as a guard against silently
reintroducing that fabrication in a future edit.

## Diamond Interface mapping (new, not from the original TS code)

`AeonJurist`'s CREP/UTAC mapping is an interpretive layer added for this
package — `AIJuristicAgent.ts` only returns a `Finding`
(level/confidence/similar_cases/rationale), nothing CREP-shaped.
`C` = confidence; `R` = the raw top similarity score (reverse-derived
from confidence's clamping formula); `E` = 0.5, neutral — no emergence
concept exists in the source algorithm; `P` = an arbitrary ordinal
mapping of level (P0→0.0, P1→0.5, P2→1.0), chosen for lack of any
inherent order between the categories in the original code.
`H_star=0.7` in `get_utac_state()` is likewise an invented threshold,
not derived from anything in the source. None of this is disguised as
more principled than it is.

## What was NOT ported

- No TypeScript build tooling was ported — `agents/personhood/` had no
  local `package.json`/`tsconfig.json` of its own (it relied on the
  monorepo's shared `tsconfig.agents.json`), confirming this was always
  a loose file, not a standalone package. A full Python port made more
  sense than wrapping a TS CLI (per the source prompt's own decision
  rule: <300 lines and portable → Python port).
- No tests existed for `agents/personhood/` in the original repo — all
  tests here (`test_classifier.py`, `test_system.py`) are new.

## Verbindung zum Ökosystem

No direct code dependency on any other GenesisAeon package (unlike
`aeon-sealcore`, which genuinely wraps `aeon-trikaya`). The CREP/UTAC
mapping is a fresh interpretive layer, not a real integration with
`aeon-trikaya` (P52)'s Trikaya state machine — no PRÄSENZ/LEERE/
AUFLÖSUNG vocabulary is used here, unlike the source prompt's
suggestion, specifically because that vocabulary belongs to a different
package's real, discrete lookup and reusing it here without the same
underlying logic would misrepresent both.
