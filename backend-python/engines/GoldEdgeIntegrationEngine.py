from utils.logger import log
from db.dbManager import db
from core.eventBus import eventBus

class GoldEdgeIntegrationEngine:
    name = "GoldEdgeIntegrationEngine"

    def __init__(self):
        self.integrations = {}

    async def add_integration(self, integration_id, config):
        self.integrations[integration_id] = config
        # Write to DB and emit event
        await db.set("gold_edge_integrations", integration_id, config, storage="edge")
        eventBus.publish("db:update", {
            "collection": "gold_edge_integrations",
            "key": integration_id,
            "value": config,
            "source": self.name
        })
        log(f"[{self.name}] Integration added: {integration_id}")
        return {"success": True, "integration_id": integration_id}

    async def update_integration(self, integration_id, config):
        if integration_id in self.integrations:
            self.integrations[integration_id].update(config)
            await db.set("gold_edge_integrations", integration_id, self.integrations[integration_id], storage="edge")
            eventBus.publish("db:update", {
                "collection": "gold_edge_integrations",
                "key": integration_id,
                "value": self.integrations[integration_id],
                "source": self.name
            })
            log(f"[{self.name}] Integration updated: {integration_id}")
            return {"success": True}
        return {"success": False, "message": "Integration not found"}

    async def remove_integration(self, integration_id):
        if integration_id in self.integrations:
            del self.integrations[integration_id]
            await db.delete("gold_edge_integrations", integration_id)
            eventBus.publish("db:delete", {
                "collection": "gold_edge_integrations",
                "key": integration_id,
                "source": self.name
            })
            log(f"[{self.name}] Integration removed: {integration_id}")
            return {"success": True}
        return {"success": False, "message": "Integration not found"}

    async def recover(self, err):
        log(f"[{self.name}] Recovered from error: {err}")
