import pytest
from diamond_setup.protocol import NotConvergedError

from aeon_jurist.system import AeonJurist


def test_requires_convergence_before_state_reads() -> None:
    jurist = AeonJurist()
    with pytest.raises(NotConvergedError):
        jurist.get_crep_state()
    with pytest.raises(NotConvergedError):
        jurist.get_utac_state()


def test_run_cycle_and_diamond_interface() -> None:
    jurist = AeonJurist()
    result = jurist.run_cycle(subject="river", claims=["granted personhood", "guardianship"])

    assert "level" in result
    assert "confidence" in result

    crep = jurist.get_crep_state()
    assert crep["Gamma"] is not None
    assert 0.0 <= crep["C"] <= 1.0

    utac = jurist.get_utac_state()
    assert utac["K_eff"] > 0

    events = jurist.get_phase_events()
    assert events[0]["type"] == "personhood_category_assigned"

    zr = jurist.to_zenodo_record()
    assert "P55" in zr["title"]
    assert "Ganges" not in zr["description"]  # not a real precedent in our data


def test_org_subject_never_gets_a_phase_event() -> None:
    jurist = AeonJurist()
    jurist.run_cycle(subject="org", claims=["a corporation"])
    assert jurist.get_phase_events() == []


def test_get_finding_before_run_cycle_is_empty() -> None:
    jurist = AeonJurist()
    assert jurist.get_finding() == {}


def test_get_finding_after_run_cycle_returns_the_result() -> None:
    jurist = AeonJurist()
    jurist.run_cycle(subject="river", claims=["granted personhood"])
    finding = jurist.get_finding()
    assert finding["level"] == "P1"


def test_phase_events_before_run_cycle_is_empty() -> None:
    """get_phase_events() has no convergence gate in the Diamond protocol,
    so it must be safe to call before the first run_cycle()."""
    jurist = AeonJurist()
    assert jurist.get_phase_events() == []
