"""
Optional bridges for host apps (no heavy imports of domain stacks).

Use :func:`parse_mak_access_bridge` on ``evidence`` dicts that expose MPK hooks.
"""

from .governance_vaults import (
    atom_result_to_vault_record,
    athena_result_to_vault_record,
    pharaoh_result_to_vault_record,
)
from .first_order_evidence import parse_mak_access_bridge

__all__ = [
    "atom_result_to_vault_record",
    "athena_result_to_vault_record",
    "pharaoh_result_to_vault_record",
    "parse_mak_access_bridge",
]
