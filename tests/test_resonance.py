from memory_phase_kernel import ChannelReading, compute_resonance_index, normalize_channel_weights


def test_normalize_empty() -> None:
    assert normalize_channel_weights({}) == {}


def test_resonance_uniform_weights() -> None:
    r = (
        ChannelReading("a", 1.0, 1.0),
        ChannelReading("b", 0.0, 1.0),
    )
    w = {"a": 0.5, "b": 0.5}
    assert abs(compute_resonance_index(r, w) - 0.5) < 1e-9


def test_resonance_missing_channel_zero_weight() -> None:
    r = (ChannelReading("x", 1.0, 1.0),)
    assert compute_resonance_index(r, {"y": 1.0}) == 0.0
