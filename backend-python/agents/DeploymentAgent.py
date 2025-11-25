# DeploymentAgent.py
# Agent responsible for deploying applications, services, or models

class DeploymentAgent:
    def __init__(self):
        self.name = "DeploymentAgent"
        self.deployment_log = []
        print("[DeploymentAgent] Initialized")

    def deploy_service(self, service_name: str, version: str, environment: str):
        deployment_entry = {
            "service": service_name,
            "version": version,
            "environment": environment,
            "status": "deployed"
        }
        self.deployment_log.append(deployment_entry)
        print(f"[DeploymentAgent] Deployed {service_name} v{version} to {environment}")
        return deployment_entry

    def rollback_service(self, service_name: str, environment: str):
        rollback_entry = {
            "service": service_name,
            "environment": environment,
            "status": "rolled back"
        }
        self.deployment_log.append(rollback_entry)
        print(f"[DeploymentAgent] Rolled back {service_name} in {environment}")
        return rollback_entry

    def get_deployment_history(self):
        print(f"[DeploymentAgent] Deployment history: {self.deployment_log}")
        return self.deployment_log

    async def handle_deployment_request(self, request: dict):
        action = request.get("action")
        if action == "deploy":
            return self.deploy_service(request.get("service_name"), request.get("version"), request.get("environment"))
        elif action == "rollback":
            return self.rollback_service(request.get("service_name"), request.get("environment"))
        elif action == "history":
            return self.get_deployment_history()
        else:
            return {"error": "Invalid action"}

    async def recover(self, error):
        print(f"[DeploymentAgent] Recovered from error: {error}")
