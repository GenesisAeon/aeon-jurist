# aeon-jurist (GenesisAeon Package 55)

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

This is a research tool exploring whether TF-IDF-based retrieval over a
tiny (3-case) precedent set can usefully categorize personhood queries.
It is not a legal opinion, does not scale beyond its 3 seed cases, and
should not inform real legal or policy decisions.
