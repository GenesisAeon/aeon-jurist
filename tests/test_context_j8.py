"""J8: context records (sentience statutes, guardians, legal persons without a will)."""
from aeon_jurist.landscape import CONTEXT_KINDS, context_records, landscape, load_precedents

DATA = load_precedents()
W = DATA["werte"]


def test_every_context_record_is_sourced_and_typed():
    recs = context_records()
    assert len(recs) >= 10
    for r in recs:
        assert r["art"] in CONTEXT_KINDS, r["id"]
        assert r["primaerquelle"]["url"].startswith("http"), r["id"]
        assert r["prueftiefe"] in W["prueftiefe"], r["id"]
        assert r["zitat"].strip() and r["geprueft_durch"].strip(), r["id"]
        assert isinstance(r["personenstatus"], bool), r["id"]


def test_sentience_statutes_and_guardians_grant_no_personhood():
    for kind in ("empfindungsfaehigkeit_gesetz", "gegenbeispiel_ohne_empfindungsfaehigkeit", "hueter_nicht_anwesende"):
        recs = context_records(kind)
        assert recs, kind
        assert all(r["personenstatus"] is False for r in recs), kind


def test_persons_without_will_include_foundation_and_idol_but_not_ship():
    recs = {r["id"]: r for r in context_records("rechtsperson_ohne_willen")}
    assert recs["DE-STIFTUNG-BGB80"]["personenstatus"] is True
    assert recs["IN-IDOL-MULLICK-1925"]["personenstatus"] is True
    # the ship is liable in rem but is not a general legal person
    assert recs["US-THECHINA-1868"]["personenstatus"] is False


def test_blocked_sources_are_not_marked_as_full_text():
    for r in context_records():
        if "gesperrt" in r["geprueft_durch"]:
            assert r["prueftiefe"] == "sekundaer", r["id"]


def test_context_ids_do_not_collide_and_stay_out_of_landscape():
    ids = [r["id"] for r in context_records()]
    case_ids = {f["id"] for f in DATA["faelle"]}
    assert len(ids) == len(set(ids))
    assert not set(ids) & case_ids
    for e in ("ai", "river", "animal", "nature", "dao"):
        assert not set(ids) & {c.id for c in landscape(e).cases}
