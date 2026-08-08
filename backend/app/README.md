FinGuard AI backend scaffold

This folder contains a minimal FastAPI scaffold with lightweight stubs for:
- PII-isolated evidence builder
- Validation gate (8 checks)
- Decision engine
- Audit log stub
- Redis and Kafka client stubs

To run (after installing dependencies):

1. Install: `pip install fastapi uvicorn pydantic`
2. Run: `uvicorn backend.app.main:app --reload --port 8000`
