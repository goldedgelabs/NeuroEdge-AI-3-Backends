# ReasoningEngine.py
from core.engine_base import EngineBase
from db.db_manager import DBManager
from core.event_bus import EventBus

class ReasoningEngine(EngineBase):
    name = "ReasoningEngine"

    def __init__(self):
        super().__init__()
        self.db = DBManager()
        self.event_bus = EventBus()

    async def run(self, input_data: dict):
        """
        Main reasoning logic.
        input_data: dict containing context, facts, and optional user info
        """
        context = input_data.get("context", [])
        user_id = input_data.get("user_id", "anonymous")

        # Placeholder reasoning logic
        conclusion = f"Based on {len(context)} facts, the engine concludes XYZ"

        reasoning_record = {
            "id": f"reasoning_{user_id}",
            "collection": "reasonings",
            "user_id": user_id,
            "context": context,
            "conclusion": conclusion,
            "timestamp": input_data.get("timestamp", None)
        }

        # Save to DB
        await self.db.set(reasoning_record["collection"], reasoning_record["id"], reasoning_record, storage="edge")

        # Emit DB update event
        self.event_bus.publish("db:update", {
            "collection": reasoning_record["collection"],
            "key": reasoning_record["id"],
            "value": reasoning_record,
            "source": self.name
        })

        return reasoning_record

    async def recover(self, error: Exception):
        """
        Graceful error handling
        """
        print(f"[ReasoningEngine] Recovered from error: {error}")
        return {"error": str(error)}

# Optional direct test
if __name__ == "__main__":
    import asyncio
    engine = ReasoningEngine()
    result = asyncio.run(engine.run({"user_id": "user123", "context": ["fact1", "fact2"]}))
    print(result)
