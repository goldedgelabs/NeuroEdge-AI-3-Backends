from core.EngineBase import EngineBase
from db.db_manager import db
from event_bus import event_bus
import datetime

class MonitoringEngine(EngineBase):
    async def run(self, input_data):
        """
        Monitors system health, logs, performance metrics.
        """
        metric_id = f"metric_{int(datetime.datetime.utcnow().timestamp())}"
        metrics = input_data.get("metrics", {"cpu": 0, "memory": 0, "disk": 0})

        record = {
            "collection": "system_metrics",
            "id": metric_id,
            "metrics": metrics,
            "timestamp": datetime.datetime.utcnow().isoformat()
        }

        # Save to DB
        await db.set(record["collection"], record["id"], record, "edge")

        # Publish event
        await event_bus.publish("db:update", record)

        return record

    async def get_metrics(self, since: str = None):
        """
        Retrieve metrics optionally filtered by timestamp
        """
        all_metrics = await db.getAll("system_metrics", "edge")
        if since:
            all_metrics = [m for m in all_metrics if m["timestamp"] >= since]
        return all_metrics
