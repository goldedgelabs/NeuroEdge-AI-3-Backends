# backend-python/agents/SecurityAuditAgent.py

from ..core.dbManager import db
from ..core.eventBus import eventBus
from ..utils.logger import logger

class SecurityAuditAgent:
    name = "SecurityAuditAgent"

    def __init__(self):
        # Subscribe to DB events
        eventBus.subscribe("db:update", self.handle_db_update)
        eventBus.subscribe("db:delete", self.handle_db_delete)

    async def audit_security(self, collection: str):
        """
        Perform a security audit on a given collection.
        """
        records = await db.get_all(collection, target="edge")
        audit_results = []

        for record in records:
            issues = []
            if "password" in record and not record.get("password"):
                issues.append("Missing password")
            if "access_level" in record and record["access_level"] not in ["user", "admin", "super"]:
                issues.append("Invalid access level")
            audit_results.append({"id": record.get("id"), "issues": issues})

        # Save audit results
        audit_id = f"audit_{collection}_{int(time.time()*1000)}"
        await db.set("security_audits", audit_id, audit_results, target="edge")
        eventBus.publish("db:update", {"collection": "security_audits", "key": audit_id, "value": audit_results, "source": self.name})

        logger.log(f"[SecurityAuditAgent] Security audit completed for {collection}, saved as {audit_id}")
        return audit_results

    async def handle_db_update(self, event: dict):
        logger.log(f"[SecurityAuditAgent] DB update received: {event.get('collection')}:{event.get('key')}")

    async def handle_db_delete(self, event: dict):
        logger.log(f"[SecurityAuditAgent] DB delete received: {event.get('collection')}:{event.get('key')}")

    async def recover(self, error: Exception):
        logger.error(f"[SecurityAuditAgent] Recovering from error: {error}")
