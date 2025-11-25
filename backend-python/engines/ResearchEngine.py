# backend-python/engines/ResearchEngine.py

from typing import Any, Dict
from backend_python.db.db_manager import db
from backend_python.core.event_bus import event_bus
from backend_python.utils.logger import logger

class ResearchEngine:
    name = "ResearchEngine"

    def __init__(self):
        self.research_store = []

    async def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process research input and generate output.
        """
        record_id = input_data.get("id", "default_research_id")
        research_record = {
            "collection": "research",
            "id": record_id,
            "data": input_data.get("data", {}),
            "notes": input_data.get("notes", ""),
            "timestamp": input_data.get("timestamp"),
            "source": self.name
        }

        # Save to DB (edge)
        await db.set(research_record["collection"], research_record["id"], research_record, "edge")

        # Publish DB update event
        event_bus.publish("db:update", {
            "collection": research_record["collection"],
            "key": research_record["id"],
            "value": research_record,
            "source": self.name
        })

        logger.log(f"[{self.name}] DB updated: {research_record['collection']}:{research_record['id']}")
        return research_record

    async def recover(self, error: Exception):
        logger.error(f"[{self.name}] Recovery from error: {error}")
