"""Known legal-personhood precedents.

Ported from the 3 case files in unified-mandala's
``data/personhood/cases/`` (read in full, not summarized from memory):
``river_whanganui_nz.md``, ``colombia_atria_river.md`` (filename has a
typo in the source repo — the river is Atrato, not "Atria" — kept as
the correct name here), and ``eu_ai_act_discussion_stub.md``.

Only 2 of these are actual granted-personhood rulings; the third is
explicitly self-labeled a "stub" in its own filename and describes a
non-grant. ``source`` citations for the two real cases were not present
in the original markdown files (they only had a one-line description
and tags) — added here as the well-established, independently
verifiable statute/judgment references for these cases.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class LegalPrecedent:
    """A single legal-personhood precedent case."""

    name: str
    entity_type: str  # "river" | "forest" | "tree" | "ai" | "org"
    jurisdiction: str
    year: int | None
    granted: bool
    reasoning: str
    source: str
    tags: tuple[str, ...] = field(default_factory=tuple)


KNOWN_PRECEDENTS: list[LegalPrecedent] = [
    LegalPrecedent(
        name="Whanganui River (NZ, 2017)",
        entity_type="river",
        jurisdiction="NZ",
        year=2017,
        granted=True,
        reasoning=(
            "Granted legal personhood with representation by Māori iwi; "
            "establishes guardianship and river rights."
        ),
        source="Te Awa Tupua (Whanganui River Claims Settlement) Act 2017",
        tags=("river", "personhood", "guardianship", "statute"),
    ),
    LegalPrecedent(
        name="Atrato River (Colombia, 2016)",
        entity_type="river",
        jurisdiction="CO",
        year=2016,
        granted=True,
        reasoning=(
            "Constitutional court recognized the river as a subject of "
            "rights; community guardians established."
        ),
        source="Constitutional Court of Colombia, Judgment T-622 of 2016",
        tags=("river", "rights", "guardians"),
    ),
    LegalPrecedent(
        name="EU AI Act (stub)",
        entity_type="ai",
        jurisdiction="EU",
        year=None,
        granted=False,
        reasoning=(
            "Debate on AI liability and agency; no general personhood for "
            "AI, but accountability structures discussed."
        ),
        source="EU AI Act discussion (stub entry - no formal citation in source data)",
        tags=("ai", "liability", "accountability"),
    ),
]
