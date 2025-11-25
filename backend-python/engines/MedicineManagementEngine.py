from core.EngineBase import EngineBase
from db.db_manager import db
from event_bus import event_bus
from utils.logger import logger

class MedicineManagementEngine(EngineBase):
    """
    Handles medicines, dosages, manufacturers, and related medical data.
    """

    async def add_medicine(self, medicine_id: str, data: dict):
        """
        Add or update medicine information.
        """
        record_data = {
            "id": medicine_id,
            "collection": "medicine",
            "data": data
        }

        # Write to DB
        await db.set("medicine", medicine_id, record_data, "edge")
        await event_bus.publish("db:update", {
            "collection": "medicine",
            "key": medicine_id,
            "value": record_data,
            "source": "MedicineManagementEngine"
        })

        logger.log(f"[MedicineManagementEngine] Medicine updated: {medicine_id}")
        return record_data

    async def get_medicine(self, medicine_id: str):
        """
        Retrieve medicine data from edge DB.
        """
        record = await db.get("medicine", medicine_id, "edge")
        logger.log(f"[MedicineManagementEngine] Retrieved medicine: {medicine_id}")
        return record

    async def run(self, input_data: dict):
        """
        Main entry point:
        {
            "action": "add" | "get",
            "medicine_id": str,
            "data": dict (optional)
        }
        """
        action = input_data.get("action")
        medicine_id = input_data.get("medicine_id")

        if action == "add":
            data = input_data.get("data", {})
            return await self.add_medicine(medicine_id, data)
        elif action == "get":
            return await self.get_medicine(medicine_id)
        else:
            return {"error": f"Unknown action: {action}"}
