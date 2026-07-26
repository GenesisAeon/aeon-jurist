from aeon_jurist.classifier import PersonhoodClassifier, Query


def test_whanganui_river_is_the_closest_match() -> None:
    """A river query worded like the Whanganui case should retrieve it."""
    clf = PersonhoodClassifier()
    finding = clf.analyze(
        Query(
            subject="river",
            claims=["granted legal personhood", "guardianship", "river rights"],
        )
    )
    assert finding.similar_cases
    assert finding.similar_cases[0] == "Whanganui River (NZ, 2017)"


def test_level_is_subject_based_not_outcome_based() -> None:
    """An AI query gets P2 even though the only AI precedent was not granted.

    This mirrors the original TS code exactly: `level` is a fixed lookup
    on `subject`, independent of what the retrieved precedent's `granted`
    value is.
    """
    clf = PersonhoodClassifier()
    finding = clf.analyze(Query(subject="ai", claims=["should this AI have rights"]))
    assert finding.level == "P2"


def test_unknown_subject_gets_p0() -> None:
    clf = PersonhoodClassifier()
    finding = clf.analyze(Query(subject="org", claims=["a corporation"]))
    assert finding.level == "P0"


def test_confidence_is_bounded() -> None:
    clf = PersonhoodClassifier()
    finding = clf.analyze(Query(subject="forest", claims=["ancient forest rights"]))
    assert 0.0 <= finding.confidence <= 0.95


def test_empty_precedent_set_falls_back_to_none() -> None:
    """With no precedents at all, there's nothing to retrieve."""
    clf = PersonhoodClassifier(precedents=[])
    finding = clf.analyze(Query(subject="tree", claims=["ancient tree"]))
    assert finding.similar_cases == []
    assert finding.rationale.endswith("top=none")
    assert finding.confidence == 0.4
