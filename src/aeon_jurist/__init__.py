"""aeon-jurist — AI-assisted legal personhood classification (GenesisAeon P55).

Ported from unified-mandala/agents/personhood/AIJuristicAgent.ts. See
epistemic_status.md for what the classifier actually does (a fixed
subject-to-level lookup plus TF-IDF similarity retrieval) vs. what a
naive reading of "AI-assisted legal classification" might suggest.

Since J2 (branch j-series) the recommended entry point is ``landscape()``:
a map of sourced cases with outcomes and status, never a protection level.
"""

__version__ = "0.1.0"

from .classifier import Finding, PersonhoodClassifier, Query
from .landscape import Landscape, landscape, load_precedents
from .precedents import KNOWN_PRECEDENTS, LegalPrecedent
from .system import AeonJurist

__all__ = [
    "AeonJurist",
    "Finding",
    "KNOWN_PRECEDENTS",
    "Landscape",
    "LegalPrecedent",
    "PersonhoodClassifier",
    "Query",
    "landscape",
    "load_precedents",
]
