from fastapi import FastAPI, HTTPException
from .api.routes import router as api_router
from .config import settings

app = FastAPI(title="FinGuard AI - Backend", version="0.1.0")


@app.on_event("startup")
async def startup_event():
    # Initialize connections (DB, cache, messaging)
    # These are lightweight stubs in this scaffold.
    app.state.settings = settings


@app.on_event("shutdown")
async def shutdown_event():
    # Clean up resources
    pass


app.include_router(api_router, prefix="/api")


@app.get("/health")
async def health():
    return {"status": "ok"}
