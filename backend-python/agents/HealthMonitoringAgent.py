# HealthMonitoringAgent.py
# Agent responsible for monitoring system and service health

class HealthMonitoringAgent:
    def __init__(self):
        self.name = "HealthMonitoringAgent"
        self.services_status = {}

    def register_service(self, service_name: str):
        if service_name not in self.services_status:
            self.services_status[service_name] = "unknown"
            print(f"[HealthMonitoringAgent] Service registered: {service_name}")

    def unregister_service(self, service_name: str):
        if service_name in self.services_status:
            del self.services_status[service_name]
            print(f"[HealthMonitoringAgent] Service unregistered: {service_name}")

    async def update_status(self, service_name: str, status: str):
        if service_name in self.services_status:
            self.services_status[service_name] = status
            print(f"[HealthMonitoringAgent] Service {service_name} status updated to: {status}")

    async def get_status(self, service_name: str):
        return self.services_status.get(service_name, "unknown")

    async def recover(self, error):
        print(f"[HealthMonitoringAgent] Recovered from error: {error}")
