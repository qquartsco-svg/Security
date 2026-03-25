from __future__ import annotations

from typing import Mapping, Tuple

from .contracts import ChannelReading


def normalize_channel_weights(raw: Mapping[str, float]) -> dict[str, float]:
    """Return non-negative weights summing to 1.0; empty → uniform."""
    if not raw:
        return {}
    pos = {k: max(0.0, float(v)) for k, v in raw.items()}
    s = sum(pos.values())
    if s <= 0.0:
        n = len(pos)
        return {k: 1.0 / n for k in pos}
    return {k: v / s for k, v in pos.items()}


def compute_resonance_index(
    readings: Tuple[ChannelReading, ...],
    weights: Mapping[str, float],
) -> float:
    """
    Ω_res: weighted sum of match * quality, normalized by weight coverage.

    Channels present in readings but missing from weights get weight 0 unless
    weights is empty (then uniform over readings).
    """
    if not readings:
        return 0.0
    w = normalize_channel_weights(dict(weights))
    if not w:
        u = 1.0 / len(readings)
        w = {r.channel_id: u for r in readings}

    num = 0.0
    den = 0.0
    for r in readings:
        wi = w.get(r.channel_id, 0.0)
        if wi <= 0.0:
            continue
        m = max(0.0, min(1.0, r.match_score))
        q = max(0.0, min(1.0, r.quality))
        num += wi * m * q
        den += wi
    if den <= 0.0:
        return 0.0
    return max(0.0, min(1.0, num / den))
