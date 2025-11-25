from core.EngineBase import EngineBase
from db.db_manager import db
from event_bus import event_bus
from utils.logger import logger

class HealthEngine(EngineBase):
    """
    Handles health-related computations: patient data, analytics, and predictions.
    """

    async def add_patient_record(self, patient_id: str, record: dict):
        """
        Add or update a patient record.
        """
        record_data = {
            "id": patient_id,
            "collection": "health",
            "record": record
        }

        # Write to DB
        await db.set("health", patient_id, record_data, "edge")
        await event_bus.publish("db:update", {
            "collection": "health",
            "key": patient_id,
            "value": record_data,
            "source": "HealthEngine"
        })

        logger.log(f"[HealthEngine] Patient record updated: {patient_id}")
        return record_data

    async def get_patient_record(self, patient_id: str):
        """
        Retrieve patient record from edge DB.
        """
        record = await db.get("health", patient_id, "edge")
        logger.log(f"[HealthEngine] Retrieved patient record: {patient_id}")
        return record

    async def run(self, input_data: dict):
        """
        Main entry point:
        {
            "action": "add" | "get",
            "patient_id": str,
            "record": dict (optional)
        }
        """
        action = input_data.get("action")
        patient_id = input_data.get("patient_id")

        if action == "add":
            record = input_data.get("record", {})
            return await self.add_patient_record(patient_id, record)
        elif action == "get":
            return await self.get_patient_record(patient_id)
        else:
            return {"error": f"Unknown action: {action}"}
