# PolicyEngine.py
from core.engine_base import EngineBase
from db.db_manager import DBManager
from core.event_bus import EventBus

class PolicyEngine(EngineBase):
    name = "PolicyEngine"

    def __init__(self):
        super().__init__()
        self.db = DBManager()
        self.event_bus = EventBus()

    async def run(self, input_data: dict):
        """
        Main entry point for the PolicyEngine.
        input_data: dict containing action details and context
        """
        # Example: process policy rules
        policy_result = {
            "id": input_data.get("id", "policy_default"),
            "collection": "policies",
            "status": "processed",
            "details": input_data
        }

        # Save to DB
        await self.db.set(policy_result["collection"], policy_result["id"], policy_result, storage="edge")

        # Emit DB update event
        self.event_bus.publish("db:update", {
            "collection": policy_result["collection"],
            "key": policy_result["id"],
            "value": policy_result,
            "source": self.name
        })

        return policy_result

    async def recover(self, error: Exception):
        """
        Handle errors gracefully.
        """
        print(f"[PolicyEngine] Recovered from error: {error}")
        return {"error": str(error)}

# Optional: for direct testing
if __name__ == "__main__":
    import asyncio
    engine = PolicyEngine()
    result = asyncio.run(engine.run({"id": "policy1", "rule": "example_rule"}))
    print(result)
