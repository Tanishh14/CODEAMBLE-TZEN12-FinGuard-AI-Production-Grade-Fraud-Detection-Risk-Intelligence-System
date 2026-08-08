from ..models.schemas import TransactionInput, EvidencePack
from typing import Dict


def build_evidence(tx: TransactionInput) -> EvidencePack:
    # This function runs inside the PII Isolation Boundary.
    # It extracts and aggregates non-PII features and summary metrics.
    aggregated = {
        "amount": tx.amount,
        "currency": tx.currency,
        "device_present": bool(tx.device_id),
    }

    features: Dict[str, float] = {
        "amount_norm": float(tx.amount),
        "device_flag": 1.0 if tx.device_id else 0.0,
    }

    ev = EvidencePack(aggregated=aggregated, features=features)
    return ev
