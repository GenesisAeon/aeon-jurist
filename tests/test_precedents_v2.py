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
        if f["ausgang"] == "gewaehrt" and f["entitaetstyp"] != "software_rolle":
            assert f["kriterien"]["K-AGN"] == "nein", f["id"]


def test_j7_secular_river_and_sentience_cases():
    # K-CUL is not a necessary condition (Turag), animal grants rest on interests, not agency
    assert by_id("BD-TURAG-2020")["kriterien"]["K-CUL"] == "nein"
    assert by_id("BD-TURAG-2020")["ausgang"] == "gewaehrt"
    for i in ("AR-CECILIA-2016", "EC-ESTRELLITA-2022", "PK-KAAVAN-2020"):
        assert by_id(i)["kriterien"]["K-INT"] == "ja" and by_id(i)["kriterien"]["K-AGN"] == "nein", i
    for i in ("US-WY-DAO-2021", "MH-DAO-2022"):
        assert by_id(i)["entitaetstyp"] == "software_rolle" and by_id(i)["kriterien"]["K-INT"] == "nein", i


def test_j5_los_cedros_and_mar_menor_court_confirmation():
    cand = {c["id"] for c in DATA["kandidaten"]}
    assert by_id("EC-LOSCEDROS-2021")["prueftiefe"] == "volltext"
    assert by_id("EC-LOSCEDROS-2021")["kriterien"]["K-AGN"] == "nein"
    assert "142/2024" in by_id("ES-MM-2022")["anmerkung"]
    assert not {"EC-LOSCEDROS-2021", "ES-MM-TC"} & cand
    # Sandra stays overturned despite secondary claims to the contrary
    assert by_id("AR-SANDRA-2015")["status_heute"] == "aufgehoben"
