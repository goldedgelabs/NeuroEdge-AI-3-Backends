from core.EngineBase import EngineBase
from db.db_manager import db
from event_bus import event_bus

class OrchestrationEngine(EngineBase):
    """
    Coordinates and orchestrates workflows across multiple engines and agents.
    """

    async def orchestrate_chain(self, chain: list):
        """
        Runs a sequence of engine tasks in order.
        Each step is a dict: {engine_name: str, input: dict}
        """
        results = []
        for step in chain:
            engine_name = step.get("engine")
            input_data = step.get("input", {})
            
            # Retrieve engine instance from global registry
            engine = self.get_engine_instance(engine_name)
            if not engine:
                results.append({"error": f"Engine not found: {engine_name}"})
                continue
            
            if hasattr(engine, "run"):
                result = await engine.run(input_data)
                results.append({engine_name: result})
                # Optional: save orchestration step result
                record = {
                    "collection": "orchestration_logs",
                    "id": f"{engine_name}_{hash(str(input_data))}",
                    "engine": engine_name,
                    "input": input_data,
                    "output": result
                }
                await db.set(record["collection"], record["id"], record, "edge")
                await event_bus.publish("db:update", record)
        return results

    def get_engine_instance(self, name: str):
        """
        Access engine instance from global registry.
        """
        from core.engine_manager import engine_manager
        return engine_manager.get(name)
