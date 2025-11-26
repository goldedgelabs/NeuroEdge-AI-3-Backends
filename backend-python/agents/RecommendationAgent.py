# backend-python/agents/RecommendationAgent.py

from ..core.dbManager import db
from ..core.eventBus import eventBus
from ..utils.logger import logger
import time

class RecommendationAgent:
    name = "RecommendationAgent"

    def __init__(self):
        # Subscribe to DB events
        eventBus.subscribe("db:update", self.handle_db_update)
        eventBus.subscribe("db:delete", self.handle_db_delete)

    async def recommend(self, collection: str, user_data: dict) -> dict:
        """
        Generate recommendations based on user data.
        """
        # Example: simple recommendation logic
        recommendations = [f"item_{i}" for i in range(1, 6)]

        result = {
            "timestamp": time.time(),
            "user": user_data,
            "recommendations": recommendations
        }

        # Save recommendations to DB
        record_id = f"recommend_{int(time.time()*1000)}"
        await db.set(collection, record_id, result, target="edge")
        eventBus.publish("db:update", {
            "collection": collection,
            "key": record_id,
            "value": result,
            "source": self.name
        })

        logger.log(f"[RecommendationAgent] Recommendations saved: {collection}:{record_id}")
        return result

    async def handle_db_update(self, event: dict):
        logger.log(f"[RecommendationAgent] DB update received: {event.get('collection')}:{event.get('key')}")

    async def handle_db_delete(self, event: dict):
        logger.log(f"[RecommendationAgent] DB delete received: {event.get('collection')}:{event.get('key')}")

    async def recover(self, error: Exception):
        logger.error(f"[RecommendationAgent] Recovering from error: {error}")
