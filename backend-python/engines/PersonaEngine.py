from core.EngineBase import EngineBase
from db.db_manager import db
from event_bus import event_bus

class PersonaEngine(EngineBase):
    """
    Handles user persona creation, updates, and retrieval.
    """
    async def create_persona(self, input_data):
        persona_id = input_data.get("id")
        if not persona_id:
            raise ValueError("Persona ID is required")

        persona_data = {
            "collection": "personas",
            "id": persona_id,
            "name": input_data.get("name"),
            "preferences": input_data.get("preferences", {}),
            "history": input_data.get("history", [])
        }

        # Save to DB
        await db.set(persona_data["collection"], persona_data["id"], persona_data, "edge")

        # Publish DB update event
        await event_bus.publish("db:update", persona_data)

        return persona_data

    async def get_persona(self, persona_id: str):
        return await db.get("personas", persona_id, "edge")

    async def update_preferences(self, persona_id: str, preferences: dict):
        persona = await self.get_persona(persona_id)
        if not persona:
            raise ValueError(f"Persona not found: {persona_id}")

        persona["preferences"].update(preferences)
        await db.set(persona["collection"], persona_id, persona, "edge")
        await event_bus.publish("db:update", persona)
        return persona
