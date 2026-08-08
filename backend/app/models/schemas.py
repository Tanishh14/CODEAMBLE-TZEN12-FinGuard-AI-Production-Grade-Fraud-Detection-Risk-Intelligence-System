from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
import uuid


class TransactionInput(BaseModel):
    transaction_id: str
    user_id: str
    account_id: str
    amount: float
    currency: str
    device_id: Optional[str] = None
    ip: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class EvidencePack(BaseModel):
    case_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    aggregated: Dict[str, Any]
    features: Dict[str, float]
    raw_schema_ok: bool = True


class DecisionOutput(BaseModel):
    case_id: str
    fraud_probability: float
    decision: str
    evidence: EvidencePack
