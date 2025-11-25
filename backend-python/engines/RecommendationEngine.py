from core.EngineBase import EngineBase
from db.db_manager import db
from event_bus import event_bus
import datetime

class RecommendationEngine(EngineBase):
    async def run(self, input_data):
        """
        Generates recommendations based on user input or data analytics.
        """
        user_id = input_data.get("user_id", "anonymous")
        context = input_data.get("context", {})
        recommendation_id = f"rec_{user_id}_{int(datetime.datetime.utcnow().timestamp())}"

        # Example: generate dummy recommendations
        recommendations = context.get("items", ["item1", "item2", "item3"])

        recommendation_record = {
            "collection": "recommendations",
            "id": recommendation_id,
            "user_id": user_id,
            "recommendations": recommendations,
            "created_at": datetime.datetime.utcnow().isoformat()
        }

        # Save to DB
        await db.set(recommendation_record["collection"], recommendation_record["id"], recommendation_record, "edge")

        # Publish event for subscribers
        await event_bus.publish("db:update", recommendation_record)

        return recommendation_record

    async def get_user_recommendations(self, user_id):
        """
        Retrieve recommendations for a specific user
        """
        all_recs = await db.getAll("recommendations", "edge")
        return [r for r in all_recs if r["user_id"] == user_id]
