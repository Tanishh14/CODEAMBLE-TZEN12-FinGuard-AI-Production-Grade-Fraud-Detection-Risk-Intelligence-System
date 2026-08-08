from fastapi import APIRouter, BackgroundTasks
from ..models.schemas import TransactionInput, DecisionOutput, EvidencePack
from ..services import validation, evidence, audit, decision_engine

router = APIRouter()


@router.post("/submit_transaction", response_model=DecisionOutput)
async def submit_transaction(tx: TransactionInput, background_tasks: BackgroundTasks):
    # Build evidence inside PII isolation boundary
    ev: EvidencePack = evidence.build_evidence(tx)

    # Run validation gate
    checks = validation.run_all_checks(ev)
    if not checks["ok"]:
        # Log and escalate (background)
        background_tasks.add_task(audit.log_case, ev, checks)
        return DecisionOutput(case_id=ev.case_id, fraud_probability=0.0, decision="escalate", evidence=ev)

    # Decision (stub): combine signals
    decision = decision_engine.decide(ev)

    # Audit log (background)
    background_tasks.add_task(audit.log_case, ev, decision)

    return decision


@router.get("/explain/{case_id}")
async def explain(case_id: str):
    # Placeholder: return stored evidence/llm explanation
    return {"case_id": case_id, "explanation": "Not implemented in scaffold"}
