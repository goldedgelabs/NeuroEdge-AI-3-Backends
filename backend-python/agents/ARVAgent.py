# backend-python/agents/ARVAgent.py

from backend_python.db.db_manager import DBManager
from backend_python.core.event_bus import EventBus
from backend_python.utils.logger import Logger

db = DBManager()
event_bus = EventBus()
logger = Logger()

class ARVAgent:
    name = "ARVAgent"

    def __init__(self):
        # Initialization logic if needed
        logger.log(f"[ARVAgent] Initialized")

    async def run(self, data: dict):
        """
        Main method to process input data.
        """
        # Example processing
        result = {"collection": "arv_data", "id": data.get("id", "unknown"), "payload": data}
        
        # Write to DB and emit event
        await db.set(result["collection"], result["id"], result, storage="edge")
        event_bus.publish("db:update", {"collection": result["collection"], "key": result["id"], "value": result, "source": self.name})
        
        logger.log(f"[ARVAgent] DB updated → {result['collection']}:{result['id']}")
        return result

    async def handleDBUpdate(self, data: dict):
        """
        React to DB updates
        """
        logger.log(f"[ARVAgent] Received DB update: {data}")

    async def recover(self, error: Exception):
        """
        Recovery logic if run() fails
        """
        logger.error(f"[ARVAgent] Error recovered: {error}")
        return {"error": "Recovered from failure"}
