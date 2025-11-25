from core.EngineBase import EngineBase
from db.db_manager import db
from event_bus import event_bus

class AnalyticsEngine(EngineBase):
    async def run(self, input_data):
        """
        Performs analytics on datasets, generates summaries, insights,
        or metrics. Works on edge or shared database data.
        """
        collection = input_data.get("collection")
        try:
            # Fetch all relevant records from the edge DB
            records = await db.get_all(collection, "edge")
            
            # Example analytics: count records, sum numeric fields
            total_records = len(records)
            summary = {"total_records": total_records}

            # Optional: compute numeric field aggregates if present
            numeric_fields = input_data.get("numeric_fields", [])
            for field in numeric_fields:
                summary[field + "_sum"] = sum(r.get(field, 0) for r in records)

        except Exception as e:
            summary = {"error": str(e)}

        result = {
            "collection": "analytics",
            "id": input_data.get("id", "analytics_default"),
            "summary": summary
        }

        # Save to DB and notify subscribers
        await db.set(result["collection"], result["id"], result, "edge")
        await event_bus.publish("db:update", result)

        return result
