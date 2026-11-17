"""J2: a "map, not a verdict" view over the sourced precedent collection.

For a requested entity type, ``landscape()`` returns the comparable cases with
their outcome and present status, and summarises which criteria carried the
*granted* ones. It never assigns a protection level. The old subject-keyword
level of v0.1 lives on only as ``legacy_level`` in ``classifier.py``.

Data: ``data/precedents_v2.json`` (J1), every record read at its primary
source; candidates without a read source are never shown as cases.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from functools import lru_cache
from importlib import resources
from typing import Any

CRITERIA = ("K-INT", "K-REP", "K-STA", "K-DUT", "K-CUL", "K-AGN")
WEAK_EVIDENCE = {"auszug", "sekundaer", "volltext_uebersetzung"}

# Query words -> entity types used in the data. Unknown words map to nothing.
_ALIASES = {
    "river": ("fluss",), "fluss": ("fluss",),
    "forest": ("oekosystem", "natur_allgemein"), "ecosystem": ("oekosystem", "natur_allgemein"),
    "oekosystem": ("oekosystem", "natur_allgemein"), "nature": ("natur_allgemein", "oekosystem"),
    "natur": ("natur_allgemein", "oekosystem"), "lake": ("oekosystem",), "lagoon": ("oekosystem",),
    "animal": ("tier",), "tier": ("tier",),
    "ai": ("ki",), "ki": ("ki",), "robot": ("ki",),
}


@lru_cache(maxsize=1)
def load_precedents() -> dict[str, Any]:
    """Load the J1 collection shipped with the package."""
    text = resources.files("aeon_jurist").joinpath("data/precedents_v2.json").read_text(
        encoding="utf-8"
    )
    return json.loads(text)


@dataclass
class CaseRow:
    id: str
    title: str
    jurisdiction: str
    year: int
    outcome: str
    status_today: str
    evidence: str
    weakly_sourced: bool
    note: str


@dataclass
class Landscape:
    entity: str
    entity_types: tuple[str, ...]
    cases: list[CaseRow] = field(default_factory=list)
    criteria_in_granted: dict[str, dict[str, int]] = field(default_factory=dict)
    in_force_grants: int = 0
    message: str = ""

    def as_dict(self) -> dict[str, Any]:
        return {
            "entity": self.entity,
            "entity_types": list(self.entity_types),
            "cases": [vars(c) for c in self.cases],
            "criteria_in_granted": self.criteria_in_granted,
            "in_force_grants": self.in_force_grants,
            "message": self.message,
            "disclaimer": "Map of sourced cases, not a legal assessment or prediction.",
        }


def landscape(entity: str, data: dict[str, Any] | None = None) -> Landscape:
    """Return the sourced case map for an entity type (e.g. "river", "ai", "animal")."""
    data = data if data is not None else load_precedents()
    types = _ALIASES.get(entity.strip().lower(), ())
    result = Landscape(entity=entity, entity_types=types)
    if not types:
        result.message = "No comparable cases in the collection for this entity."
        return result

    matched = [f for f in data["faelle"] if f["entitaetstyp"] in types]
    matched.sort(key=lambda f: (f["jahr"], f["id"]))
    for f in matched:
        result.cases.append(
            CaseRow(
                id=f["id"],
                title=f["titel"],
                jurisdiction=f["jurisdiktion"],
                year=f["jahr"],
                outcome=f["ausgang"],
                status_today=f["status_heute"],
                evidence=f["prueftiefe"],
                weakly_sourced=f["prueftiefe"] in WEAK_EVIDENCE,
                note=f.get("anmerkung", ""),
            )
        )

    granted = [f for f in matched if f["ausgang"] == "gewaehrt"]
    result.in_force_grants = sum(1 for f in granted if f["status_heute"] == "in_kraft")
    result.criteria_in_granted = {
        k: {v: sum(1 for f in granted if f["kriterien"][k] == v) for v in data["werte"]["kriterium"]}
        for k in CRITERIA
    }
    if not matched:
        result.message = "No comparable cases in the collection for this entity."
    elif not granted:
        result.message = "Cases exist, but none granted legal personhood or rights."
    elif result.in_force_grants < len(granted):
        result.message = "Some grants are no longer in force (stayed or overturned); see status."
    return result
