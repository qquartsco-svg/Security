from __future__ import annotations

from typing import Protocol, runtime_checkable


@runtime_checkable
class TrustAnchorProtocol(Protocol):
    """
    Trust root: passkey, Secure Enclave, TPM-wrapped key, etc.

    Implementations live outside this package; MPK only depends on the protocol.
    """

    def anchor_subject_id(self) -> str:
        """Stable id bound to hardware or enrollment (not the profile subject_id)."""

    def session_ok(self) -> bool:
        """Whether the current OS/session root of trust is satisfied."""


class NullTrustAnchor:
    """Development / simulation: always satisfied; subject 'anonymous'."""

    def anchor_subject_id(self) -> str:
        return "anonymous"

    def session_ok(self) -> bool:
        return True
