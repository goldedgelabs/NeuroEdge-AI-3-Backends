# backend-python/agents/HealthMonitoringAgent.py

from ..core.dbManager import db
from ..core.eventBus import eventBus
from ..utils.logger import logger
import time

class HealthMonitoringAgent:
    name = "HealthMonitoringAgent"

    def __init__(self):
        # Subscribe to DB events
        eventBus.subscribe("db:update", self.handle_db_update)
        eventBus.subscribe("db:delete", self.handle_db_delete)

    async def check_system_health(self):
        """
        Perform basic health checks for the system.
        """
        health_report = {
            "timestamp": time.time(),
            "status": "healthy",
            "metrics": {
                "cpu_usage": 45,  # Placeholder example
                "memory_usage": 65,  # Placeholder example
                "active_agents": 71
            }
        }

        # Save health report to DB
        report_id = f"health_{int(time.time()*1000)}"
        await db.set("system_health", report_id, health_report, target="edge")
        eventBus.publish("db:update", {"collection": "system_health", "key": report_id, "value": health_report, "source": self.name})

        logger.log(f"[HealthMonitoringAgent] Health report saved: {report_id}")
        return health_report

    async def handle_db_update(self, event: dict):
        logger.log(f"[HealthMonitoringAgent] DB update received: {event.get('collection')}:{event.get('key')}")

    async def handle_db_delete(self, event: dict):
        logger.log(f"[HealthMonitoringAgent] DB delete received: {event.get('collection')}:{event.get('key')}")

    async def recover(self, error: Exception):
        logger.error(f"[HealthMonitoringAgent] Recovering from error: {error}")
