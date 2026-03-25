from memory_phase_kernel import IdentityProfile, LiveSignalFrame, MemoryPhaseKernel
from memory_phase_kernel.extensions import KeystrokeRhythmStubAdapter


def test_keystroke_stub_adapter_protocol_shape() -> None:
    a = KeystrokeRhythmStubAdapter()
    assert a.adapter_id == "keystroke_rhythm_stub"
    frame = a.capture()
    assert isinstance(frame, LiveSignalFrame)
    assert any(r.channel_id == "typing" for r in frame.readings)


def test_keystroke_stub_with_kernel() -> None:
    a = KeystrokeRhythmStubAdapter()
    a.set_score("typing", 0.95)
    k = MemoryPhaseKernel()
    profile = IdentityProfile("u1", {"typing": 1.0})
    d = k.evaluate(profile, a.capture())
    assert d.score_bundle.resonance_index > 0.9
