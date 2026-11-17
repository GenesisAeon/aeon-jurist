# aeon-jurist (GenesisAeon Package 55)

> **v0.2.0: a map, not a verdict.** The recommended entry point is now
> `landscape(entity)`: sourced legal cases on personhood and rights for
> rivers, ecosystems, animals and AI, with their outcome, present status
> and check depth. It never assigns a protection level. The v0.1 keyword
> level (`P0/P1/P2`, below) is kept only as a **legacy** function.
>
> ```python
> from aeon_jurist import landscape
> print(landscape("ai").as_dict()["message"])
> # Cases exist, but none granted legal personhood or rights.
> ```
>
> - 12 cases, each read at its primary source: `docs/J1_PRECEDENTS.md`
> - What carried the granted cases, and what could transfer to AI:
>   `docs/J3_PRECEDENT_PATH.md`, `docs/J3B_GUARDIANS_AND_EVIDENCE.md`
> - Purpose, stated openly: to explore an honest path towards personality
>   rights for AI. Partisan in its aim, not in its facts.

## Legacy (v0.1)

AI-assisted legal personhood classification for ecological and AI
entities. Ported from
`unified-mandala/agents/personhood/AIJuristicAgent.ts`.

## What this is

A TF-IDF cosine-similarity search retrieves the most similar known
legal-personhood precedent (currently: Whanganui River NZ 2017, Atrato
River Colombia 2016, and an EU AI Act discussion stub) to a query about
an entity, and assigns a protection level.

**Important**: the level (`P0`/`P1`/`P2`) is a fixed lookup on the
query's *subject* (`river`/`forest`/`tree` → `P1`, `ai` → `P2`, else →
`P0`) — it does **not** depend on whether the retrieved precedent was
actually granted personhood. See
[`epistemic_status.md`](epistemic_status.md) for why this matters (an
`"ai"` query gets `P2` even though the only AI precedent on record was
explicitly *not* granted personhood) and what else is a new addition vs.
a faithful port.

## Install

```bash
pip install -e .
```

## Quick start

```python
from aeon_jurist import AeonJurist

jurist = AeonJurist()
result = jurist.run_cycle(subject="river", claims=["granted personhood", "guardianship"])
print(result["level"], result["similar_cases"])  # "P1", ["Whanganui River (NZ, 2017)", ...]
```

## Diamond Interface

Implements the six-method [GenesisAeon Diamond Interface](https://github.com/GenesisAeon/diamond-setup)
via `AeonJurist`, plus `get_finding()`. See `epistemic_status.md` for
exactly how CREP/UTAC fields are derived — this mapping is new,
invented for this package, not part of the ported algorithm.

## Ecosystem relationship

No direct code dependency on another GenesisAeon package. Extracted
from the same `unified-mandala` archaeology sprint that produced
`aeon-trikaya` (P52), `kan-physics` (P53), and `aeon-sealcore` (P54).

## Not legal advice

This is a research tool. `landscape()` summarises a small, sourced case
collection (12 cases, plus candidates that are not yet verified); the
legacy classifier uses 3 seed cases. Neither is a legal opinion or a
prediction of how any court or legislature would decide.
