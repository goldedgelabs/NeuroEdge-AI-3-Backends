# backend-python/engines/PhoneSecurityEngine.py

from typing import Any, Dict
from backend_python.db.db_manager import db
from backend_python.core.event_bus import event_bus
from backend_python.utils.logger import logger

class PhoneSecurityEngine:
    name = "PhoneSecurityEngine"

    def __init__(self):
        self.device_status = {}

    async def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Scan and secure phone devices.
        """
        device_id = input_data.get("device_id", "unknown_device")
        status_record = {
            "collection": "phone_security",
            "id": device_id,
            "threat_level": input_data.get("threat_level", "low"),
            "scanned_at": input_data.get("scanned_at"),
            "actions_taken": input_data.get("actions_taken", []),
            "source": self.name
        }

        # Save to DB (edge)
        await db.set(status_record["collection"], status_record["id"], status_record, "edge")

        # Publish DB update event
        event_bus.publish("db:update", {
            "collection": status_record["collection"],
            "key": status_record["id"],
            "value": status_record,
            "source": self.name
        })

        logger.log(f"[{self.name}] DB updated: {status_record['collection']}:{status_record['id']}")
        return status_record

    async def recover(self, error: Exception):
        logger.error(f"[{self.name}] Recovery from error: {error}")
