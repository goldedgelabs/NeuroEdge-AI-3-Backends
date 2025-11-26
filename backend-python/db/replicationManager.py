# backend-python/db/replicationManager.py

from ..core.dbManager import db
from ..core.eventBus import eventBus
from ..utils.logger import logger
import asyncio

async def replicate_edge_to_shared(collection: str = None):
    """
    Replicates data from edge storage to shared storage.
    If 'collection' is None, replicate all collections.
    """
    logger.log(f"[ReplicationManager] Starting replication for: {collection or 'all collections'}")

    collections_to_replicate = [collection] if collection else list(db.store['edge'].keys())

    for coll in collections_to_replicate:
        edge_data = await db.get_all(coll, target="edge") or []
        for record in edge_data:
            record_id = record.get("id")
            if not record_id:
                continue

            await db.set(coll, record_id, record, target="shared")
            logger.log(f"[ReplicationManager] Replicated {coll}:{record_id} → shared")

            # Emit DB update event for shared store
            eventBus.publish("db:update", {
                "collection": coll,
                "key": record_id,
                "value": record,
                "source": "replicationManager"
            })

    logger.log(f"[ReplicationManager] Replication complete for: {collection or 'all collections'}")

# -----------------------------
# Event subscription for automatic replication
# -----------------------------
def subscribe_to_db_updates():
    """
    Subscribe to edge DB updates and replicate them to shared automatically.
    """
    async def on_update(event):
        if event.get("source") != "replicationManager":
            collection = event.get("collection")
            await replicate_edge_to_shared(collection)

    eventBus.subscribe("db:update", lambda event: asyncio.create_task(on_update(event)))
    logger.log("[ReplicationManager] Subscribed to DB updates for automatic replication")
