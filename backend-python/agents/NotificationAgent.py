# backend-python/agents/NotificationAgent.py

from ..core.dbManager import db
from ..core.eventBus import eventBus
from ..utils.logger import logger
import time

class NotificationAgent:
    name = "NotificationAgent"

    def __init__(self):
        # Subscribe to DB events
        eventBus.subscribe("db:update", self.handle_db_update)
        eventBus.subscribe("db:delete", self.handle_db_delete)

    async def send_notification(self, user_id: str, message: str, meta: dict = None):
        """
        Sends a notification to a user and logs it to the database.
        """
        notification = {
            "user_id": user_id,
            "message": message,
            "meta": meta or {},
            "timestamp": time.time()
        }

        notif_id = f"notif_{int(time.time()*1000)}"
        await db.set("notifications", notif_id, notification, target="edge")
        eventBus.publish("db:update", {"collection": "notifications", "key": notif_id, "value": notification, "source": self.name})

        logger.log(f"[NotificationAgent] Notification sent to {user_id}: {message}")
        return notification

    async def handle_db_update(self, event: dict):
        logger.log(f"[NotificationAgent] DB update received: {event.get('collection')}:{event.get('key')}")

    async def handle_db_delete(self, event: dict):
        logger.log(f"[NotificationAgent] DB delete received: {event.get('collection')}:{event.get('key')}")

    async def recover(self, error: Exception):
        logger.error(f"[NotificationAgent] Recovering from error: {error}")
