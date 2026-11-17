"""J1: contract tests for data/precedents_v2.json (sourced case collection)."""
import json
from pathlib import Path

DATA = json.loads((Path(__file__).resolve().parents[1] / "src" / "aeon_jurist" / "data" / "precedents_v2.json").read_text(encoding="utf-8"))
W = DATA["werte"]
CRITERIA = {"K-INT", "K-REP", "K-STA", "K-DUT", "K-CUL", "K-AGN"}


def by_id(i):
    return next(f for f in DATA["faelle"] if f["id"] == i)


def test_every_case_has_source_and_check_depth():
    for f in DATA["faelle"]:
        q = f["primaerquelle"]
        assert q["url"].startswith("http"), f["id"]
        assert q["abgerufen_am"] and q["art"], f["id"]
        assert f["prueftiefe"] in W["prueftiefe"], f["id"]
        assert f["zitat"].strip(), f["id"]


def test_allowed_values_and_full_criteria():
    for f in DATA["faelle"]:
        assert f["ausgang"] in W["ausgang"], f["id"]
        assert f["status_heute"] in W["status_heute"], f["id"]
        assert set(f["kriterien"]) == CRITERIA, f["id"]
        assert all(v in W["kriterium"] for v in f["kriterien"].values()), f["id"]


def test_ids_unique_and_candidates_separate():
    ids = [f["id"] for f in DATA["faelle"]]
    cids = [c["id"] for c in DATA["kandidaten"]]
    assert len(ids) == len(set(ids))
    assert not set(ids) & set(cids)
    for c in DATA["kandidaten"]:
        assert "primaerquelle" not in c, c["id"]


def test_no_ai_case_counts_as_granted():
    # H1 precondition: no AI precedent may silently signal protection.
    for f in DATA["faelle"]:
        if f["entitaetstyp"] == "ki":
            assert f["ausgang"] != "gewaehrt", f["id"]


def test_known_statuses_are_not_flattened():
    # H2 precondition: stayed / overturned cases keep their status.
    assert by_id("IN-GY-2017")["status_heute"] == "ausgesetzt"
    assert by_id("AR-SANDRA-2015")["ausgang"] == "aufgehoben"
    assert by_id("EU-EP-2017")["status_heute"] == "nicht_umgesetzt"


def test_nature_cases_do_not_require_agency():
    # The asymmetry J3 builds on: granted nature cases never rest on K-AGN.
    for f in DATA["faelle"]:
        if f["ausgang"] == "gewaehrt":
            assert f["kriterien"]["K-AGN"] == "nein", f["id"]
