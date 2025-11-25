# backend-python/agents/SelfImprovementAgent.py
from core.AgentBase import AgentBase
from db.dbManager import db
from utils.logger import logger
import time

class SelfImprovementAgent(AgentBase):
    name = "SelfImprovementAgent"

    async def handle(self, task: dict):
        """
        Handles self-optimization:
        - Tracks agent performance
        - Records slow tasks & errors
        - Suggests internal improvements
        - Stores self-evaluation data in DB
        """
        try:
            action = task.get("action")

            if action == "record_performance":
                return await self.record_performance(task.get("data"))

            elif action == "suggest_improvements":
                return await self.suggest_improvements()

            elif action == "get_metrics":
                return await self.get_metrics()

            else:
                return {"error": "Unknown action for SelfImprovementAgent"}

        except Exception as e:
            logger.error(f"[SelfImprovementAgent] ERROR: {e}")
            return {"error": str(e)}

    async def record_performance(self, data: dict):
        """
        Saves performance metrics:
        - execution_time
        - success/failure
        - complexity
        """
        if not data:
            return {"error": "Missing performance data"}

        entry = {
            "timestamp": time.time(),
            "execution_time": data.get("execution_time"),
            "success": data.get("success"),
            "complexity": data.get("complexity"),
        }

        record_id = f"perf_{int(time.time()*1000)}"
        await db.set("agent_performance", record_id, entry)

        return {"status": "saved", "id": record_id}

    async def suggest_improvements(self):
        """
        Based on collected metrics, produce improvement hints.
        """
        metrics = await db.get_all("agent_performance") or []
        if not metrics:
            return {"suggestions": ["Not enough data collected yet."]}

        slow_tasks = [m for m in metrics if m.get("execution_time", 0) > 2.0]
        failed = [m for m in metrics if not m.get("success")]

        suggestions = []

        if slow_tasks:
            suggestions.append("Optimize heavy tasks; reduce execution time.")

        if failed:
            suggestions.append("Improve reliability; reduce error rates.")

        if not suggestions:
            suggestions.append("System running optimally.")

        return {"suggestions": suggestions}

    async def get_metrics(self):
        """
        Retrieve stored metrics.
        """
        metrics = await db.get_all("agent_performance")
        return {
            "count": len(metrics) if metrics else 0,
            "data": metrics
      }
