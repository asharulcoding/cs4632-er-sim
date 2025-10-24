import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from main import simulate


def test_patients_logged():
    rec = simulate(seed=42, minutes=60, lam=1.0, triage_cap=1, bed_cap=2, lab_cap=1)
    assert len(rec) > 0, "No patients were logged in the simulation"

def test_lab_time_nonnegative():
    rec = simulate(seed=42, minutes=60, lam=1.0, triage_cap=1, bed_cap=2, lab_cap=1)
    for r in rec:
        assert r["lab_time"] >= 0, "Lab time should never be negative"

def test_no_negative_waits():
    rec = simulate(seed=42, minutes=60, lam=1.0, triage_cap=1, bed_cap=2, lab_cap=1)
    for r in rec:
        assert r["triage_wait"] >= 0
        assert r["bed_wait"] >= 0
        assert r["total_time"] >= 0, "No negative times allowed"


