"""Database connection stub. Replace with async DB client (asyncpg/SQLAlchemy) in production."""
import logging

log = logging.getLogger("finguard.db")


class DBClient:
    def __init__(self, dsn: str = ""):
        self.dsn = dsn

    async def connect(self):
        log.info("DB connect stub: %s", self.dsn)

    async def close(self):
        log.info("DB close stub")

    async def insert_audit(self, payload: dict):
        log.info("DB insert audit stub: %s", payload)


db_client = DBClient()
