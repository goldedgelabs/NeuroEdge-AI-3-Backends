from core.EngineBase import EngineBase
from db.db_manager import db
from event_bus import event_bus
import datetime

class SchedulingEngine(EngineBase):
    async def run(self, input_data):
        """
        Schedules tasks or events based on input instructions.
        """
        task_id = input_data.get("id", f"task_{datetime.datetime.utcnow().timestamp()}")
        task_name = input_data.get("name", "Unnamed Task")
        schedule_time = input_data.get("schedule_time", datetime.datetime.utcnow().isoformat())

        task_record = {
            "collection": "tasks",
            "id": task_id,
            "name": task_name,
            "schedule_time": schedule_time,
            "created_at": datetime.datetime.utcnow().isoformat()
        }

        # Save task to DB
        await db.set(task_record["collection"], task_record["id"], task_record, "edge")

        # Publish update to event bus
        await event_bus.publish("db:update", task_record)

        return task_record

    async def get_tasks(self, date: str = None):
        """
        Retrieve all tasks, optionally filtered by date (YYYY-MM-DD)
        """
        all_tasks = await db.getAll("tasks", "edge")
        if date:
            filtered_tasks = [t for t in all_tasks if t["schedule_time"].startswith(date)]
            return filtered_tasks
        return all_tasks
