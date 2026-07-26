"""Diamond Interface wrapper for aeon-jurist (GenesisAeon P55).

The CREP/UTAC mapping below is a **new interpretive layer added for
this package** — it does not exist in the original
``AIJuristicAgent.ts``, which only returns a ``Finding`` (level,
confidence, similar_cases, rationale). See ``epistemic_status.md`` for
the full reasoning behind each field; nothing here is a disguised
constant or a hidden stub.
"""

from __future__ import annotations

from dataclasses import asdict
from typing import Any

from diamond_setup.protocol import (
    CREPState,
    DiamondPackage,
    UTACState,
    ZenodoCreator,
    ZenodoRecord,
)

from .classifier import Finding, PersonhoodClassifier, Query
from .precedents import LegalPrecedent

_LEVEL_ORDINAL = {"P0": 0.0, "P1": 0.5, "P2": 1.0}


class AeonJurist(DiamondPackage):  # type: ignore[misc]
    """Diamond Interface for the legal-personhood classifier (P55)."""

    PACKAGE_ID: int = 55

    def __init__(self, precedents: list[LegalPrecedent] | None = None) -> None:
        super().__init__()
        self._classifier = PersonhoodClassifier(precedents)
        self._query: Query | None = None
        self._last: Finding | None = None

    def run_cycle(
        self,
        subject: str = "org",
        claims: list[str] | None = None,
        context: str = "",
    ) -> dict[str, Any]:
        self._query = Query(subject=subject, claims=list(claims or []), context=context)
        return super().run_cycle()  # type: ignore[no-any-return]

    def _run_cycle(self) -> dict[str, Any]:
        assert self._query is not None
        self._last = self._classifier.analyze(self._query)
        return asdict(self._last)

    def _build_crep_state(self) -> CREPState:
        assert self._last is not None
        top_score = 0.0
        if self._last.similar_cases:
            # Reverse-derive the raw top similarity from confidence's formula
            # (confidence = min(0.95, 0.4 + min(0.4, top_score))).
            top_score = min(0.4, self._last.confidence - 0.4)
        return CREPState(
            C=self._last.confidence,
            R=max(0.0, top_score) / 0.4 if top_score > 0 else 0.0,
            E=0.5,  # neutral - no emergence concept in the source algorithm
            P=_LEVEL_ORDINAL.get(self._last.level, 0.0),
        )

    def _build_utac_state(self) -> UTACState:
        assert self._last is not None
        return UTACState(
            H=self._last.confidence,
            H_star=0.7,  # invented threshold, not from the original TS code
            K_eff=float(max(1, len(self._last.similar_cases))),
        )

    def _build_phase_events(self) -> list[dict[str, Any]]:
        if self._last is None:
            return []
        if self._last.level in ("P1", "P2"):
            return [
                {
                    "type": "personhood_category_assigned",
                    "level": self._last.level,
                    "confidence": self._last.confidence,
                }
            ]
        return []

    def _build_zenodo_record(self) -> ZenodoRecord:
        return ZenodoRecord(
            title="aeon-jurist — P55: AI-assisted legal personhood classification",
            description=(
                "TF-IDF cosine-similarity retrieval of ecological/AI entity "
                "descriptions against known legal personhood precedents "
                "(Whanganui River NZ 2017, Atrato River Colombia 2016; plus "
                "an EU AI Act discussion stub documenting a non-grant for "
                "AI). The protection level (P0/P1/P2) is a fixed lookup on "
                "the query subject, not derived from precedent outcomes - "
                "see epistemic_status.md. GenesisAeon P55."
            ),
            creators=[ZenodoCreator(name="Römer, Johann", affiliation="MOR Research Collective")],
        )

    def get_finding(self) -> dict[str, Any]:
        """Return the last classification result (level/confidence/etc.)."""
        if self._last is None:
            return {}
        return asdict(self._last)
