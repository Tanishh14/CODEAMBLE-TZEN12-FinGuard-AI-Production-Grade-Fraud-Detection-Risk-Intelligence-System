"""Append-only audit log stub.

In production this writes to PostgreSQL with append-only guarantees.
"""
import logging
from ..models.schemas import EvidencePack

log = logging.getLogger("finguard.audit")


async def log_case(evidence: EvidencePack, metadata: dict):
    # Lightweight placeholder: log to app logger.
    log.info("AUDIT CASE %s %s", evidence.case_id, metadata)
