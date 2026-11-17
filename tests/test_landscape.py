"""J2: hand controls H1-H4 for landscape() (fixed in docs/J0_PLAN.md before coding)."""
import copy

from aeon_jurist.landscape import landscape, load_precedents


def ids(ls):
    return [c.id for c in ls.cases]


def test_h1_ai_shows_only_non_grants_and_no_level():
    ls = landscape("ai")
    assert set(ids(ls)) == {"EU-EP-2017", "US-DABUS-2022", "UK-DABUS-2023", "DE-DABUS-2024", "US-THALER-2025"}
    assert all(c.outcome != "gewaehrt" for c in ls.cases)
    assert ls.in_force_grants == 0
    assert "none granted" in ls.message
    assert "level" not in ls.as_dict()


def test_h2_river_keeps_stayed_case_stayed():
    ls = landscape("river")
    rows = {c.id: c for c in ls.cases}
    assert {"NZ-TAT-2017", "CO-T622-2016", "IN-GY-2017"} <= set(rows)
    assert rows["IN-GY-2017"].status_today == "ausgesetzt"
    assert ls.in_force_grants == 2
    assert "no longer in force" in ls.message


def test_h3_weak_evidence_is_flagged():
    data = copy.deepcopy(load_precedents())
    for f in data["faelle"]:
        if f["id"] == "NZ-TAT-2017":
            f["prueftiefe"] = "sekundaer"
    rows = {c.id: c for c in landscape("river", data).cases}
    assert rows["NZ-TAT-2017"].weakly_sourced is True
    assert rows["CO-T622-2016"].weakly_sourced is False
    # translation counts as weaker than original wording
    eco = {c.id: c for c in landscape("nature").cases}
    assert eco["EC-CONST-2008"].weakly_sourced is True


def test_h4_unknown_entity_gives_empty_map_not_an_analogy():
    ls = landscape("corporation-of-mars")
    assert ls.cases == [] and ls.entity_types == ()
    assert "No comparable cases" in ls.message


def test_overturned_animal_case_is_not_a_grant():
    ls = landscape("animal")
    assert ids(ls) == ["AR-SANDRA-2015"]
    assert ls.cases[0].outcome == "aufgehoben"
    assert ls.in_force_grants == 0


def test_criteria_summary_counts_only_granted_and_shows_asymmetry():
    ls = landscape("river")
    granted = 3  # NZ, CO, IN
    for k, counts in ls.criteria_in_granted.items():
        assert sum(counts.values()) == granted, k
    assert ls.criteria_in_granted["K-AGN"]["nein"] == granted
    assert ls.criteria_in_granted["K-REP"]["ja"] == granted


def test_candidates_never_appear_as_cases():
    cand = {c["id"] for c in load_precedents()["kandidaten"]}
    for e in ("ai", "river", "animal", "nature"):
        assert not cand & set(ids(landscape(e)))
