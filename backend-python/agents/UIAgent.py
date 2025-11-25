# UIAgent.py
# Agent responsible for handling user interface interactions and updates

class UIAgent:
    def __init__(self):
        self.name = "UIAgent"
        self.active_sessions = {}
        print("[UIAgent] Initialized")

    def open_session(self, user_id: str):
        self.active_sessions[user_id] = {"status": "active"}
        print(f"[UIAgent] Session opened for user: {user_id}")
        return self.active_sessions[user_id]

    def close_session(self, user_id: str):
        if user_id in self.active_sessions:
            self.active_sessions[user_id]["status"] = "closed"
            print(f"[UIAgent] Session closed for user: {user_id}")
            return self.active_sessions[user_id]
        return {"error": "Session not found"}

    def update_ui(self, user_id: str, data: dict):
        if user_id not in self.active_sessions:
            return {"error": "Session not found"}
        print(f"[UIAgent] UI updated for {user_id} with data: {data}")
        return {"status": "updated"}

    async def handle_request(self, request: dict):
        action = request.get("action")
        user_id = request.get("user_id")
        data = request.get("data", {})
        if action == "open_session":
            return self.open_session(user_id)
        elif action == "close_session":
            return self.close_session(user_id)
        elif action == "update_ui":
            return self.update_ui(user_id, data)
        else:
            return {"error": "Invalid action"}

    async def recover(self, error):
        print(f"[UIAgent] Recovered from error: {error}")
