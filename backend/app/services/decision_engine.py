"""Decision engine stub: combines model signals and returns calibrated probability."""
from ..models.schemas import EvidencePack, DecisionOutput


def decide(evidence: EvidencePack) -> DecisionOutput:
    # Placeholder scoring logic; in prod this would call GNN/anomaly models
    base_score = evidence.features.get("amount_norm", 0.0) % 100 / 100.0
    # simple calibration stub
    calibrated = min(max(base_score * 1.0, 0.0), 1.0)
    decision = "block" if calibrated > 0.8 else "allow"
    return DecisionOutput(case_id=evidence.case_id, fraud_probability=calibrated * 100.0, decision=decision, evidence=evidence)
