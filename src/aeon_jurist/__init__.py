"""aeon-jurist — AI-assisted legal personhood classification (GenesisAeon P55).

Ported from unified-mandala/agents/personhood/AIJuristicAgent.ts. See
epistemic_status.md for what the classifier actually does (a fixed
subject-to-level lookup plus TF-IDF similarity retrieval) vs. what a
naive reading of "AI-assisted legal classification" might suggest.
"""

__version__ = "0.1.0"

from .classifier import Finding, PersonhoodClassifier, Query
from .precedents import KNOWN_PRECEDENTS, LegalPrecedent
from .system import AeonJurist

__all__ = [
    "AeonJurist",
    "Finding",
    "KNOWN_PRECEDENTS",
    "LegalPrecedent",
    "PersonhoodClassifier",
    "Query",
]
