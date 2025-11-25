# RoutingAgent.py
# Agent responsible for routing tasks, messages, or data between engines and agents

class RoutingAgent:
    def __init__(self):
        self.name = "RoutingAgent"
        self.routes = {}

    def add_route(self, source: str, destination: str):
        if source not in self.routes:
            self.routes[source] = []
        self.routes[source].append(destination)
        print(f"[RoutingAgent] Route added: {source} → {destination}")

    def remove_route(self, source: str, destination: str):
        if source in self.routes and destination in self.routes[source]:
            self.routes[source].remove(destination)
            print(f"[RoutingAgent] Route removed: {source} → {destination}")

    async def route(self, source: str, payload):
        if source not in self.routes:
            return {"error": f"No routes found for source {source}"}
        for destination in self.routes[source]:
            try:
                # Here we assume destination has a `process` method
                await destination.process(payload)
                print(f"[RoutingAgent] Routed payload from {source} to {destination}")
            except Exception as e:
                await self.recover(e)
        return {"status": "routed"}

    async def recover(self, error):
        print(f"[RoutingAgent] Recovered from error: {error}")
