"""TF-IDF cosine-similarity personhood classifier.

Faithful port of ``unified-mandala/agents/personhood/AIJuristicAgent.ts``'s
``analyze()``/``tfidfCosine()``. The original hand-rolled its own TF-IDF
cosine similarity in TypeScript; this uses scikit-learn's
``TfidfVectorizer`` + ``cosine_similarity`` as an idiomatic
implementation of the *same algorithm class* (numeric parity with the
original is not guaranteed - tokenization/smoothing differ - but the
retrieval approach and the classification rule below are identical).

Important, verified against the source rather than assumed: the
``level`` (P0/P1/P2) is a **fixed lookup on ``subject``**, not derived
from the similarity search or from whether the closest precedent was
actually granted. The TF-IDF search only feeds ``confidence`` and
``similar_cases``. This means, e.g., an ``"ai"`` query always gets
``"P2"`` even though the only AI precedent in ``precedents.py``
explicitly was *not* granted personhood - see ``epistemic_status.md``.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from .precedents import KNOWN_PRECEDENTS, LegalPrecedent

_LEVEL_BY_SUBJECT = {"river": "P1", "forest": "P1", "tree": "P1", "ai": "P2"}
_SIMILARITY_THRESHOLD = 0.12
_TOP_K = 8


@dataclass
class Query:
    """A personhood-classification request."""

    subject: str  # "ai" | "river" | "forest" | "tree" | "org"
    claims: list[str] = field(default_factory=list)
    context: str = ""


@dataclass
class Finding:
    """Result of a personhood classification."""

    level: str
    confidence: float
    similar_cases: list[str]
    rationale: str


class PersonhoodClassifier:
    """TF-IDF cosine-similarity retrieval + subject-based level lookup."""

    def __init__(self, precedents: list[LegalPrecedent] | None = None) -> None:
        self._precedents: list[LegalPrecedent] = (
            list(KNOWN_PRECEDENTS) if precedents is None else list(precedents)
        )
        self._vectorizer = TfidfVectorizer(ngram_range=(1, 2))
        docs = [f"{p.entity_type} {p.reasoning}" for p in self._precedents]
        self._doc_matrix = self._vectorizer.fit_transform(docs) if docs else None

    def analyze(self, query: Query) -> Finding:
        """Classify *query* against the known precedents."""
        joined = " ".join([query.subject, *query.claims, query.context]).strip()

        sims: list[tuple[str, float]] = []
        if self._doc_matrix is not None and joined:
            q_vec = self._vectorizer.transform([joined])
            scores = cosine_similarity(q_vec, self._doc_matrix)[0]
            ranked = sorted(
                zip((p.name for p in self._precedents), scores, strict=True),
                key=lambda item: item[1],
                reverse=True,
            )
            sims = ranked[:_TOP_K]

        top_ids = [name for name, score in sims if score > _SIMILARITY_THRESHOLD]
        top_score = float(sims[0][1]) if sims else 0.0
        top_name = sims[0][0] if sims else "none"

        level = _LEVEL_BY_SUBJECT.get(query.subject, "P0")
        confidence = min(0.95, 0.4 + min(0.4, top_score))
        rationale = f"Selected by policy criteria & tfidf_cosine; top={top_name}"

        return Finding(
            level=level,
            confidence=confidence,
            similar_cases=top_ids,
            rationale=rationale,
        )
