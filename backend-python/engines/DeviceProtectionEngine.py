from core.EngineBase import EngineBase
from db.db_manager import db
from event_bus import event_bus
from utils.logger import logger

class DeviceProtectionEngine(EngineBase):
    """
    Manages device security, malware scanning, encryption, and threat detection.
    """

    async def scan_device(self, device_id: str):
        """
        Scan a device for threats.
        """
        # Placeholder scan logic
        threats_found = ["malware.exe"] if device_id.endswith("1") else []
        result = {
            "id": device_id,
            "collection": "device_protection",
            "threats": threats_found,
            "status": "clean" if not threats_found else "infected"
        }

        # Write to DB and trigger replication
        await db.set("device_protection", device_id, result, "edge")
        await event_bus.publish("db:update", {
            "collection": "device_protection",
            "key": device_id,
            "value": result,
            "source": "DeviceProtectionEngine"
        })

        logger.log(f"[DeviceProtectionEngine] Scanned device {device_id}: {result['status']}")
        return result

    async def encrypt_data(self, device_id: str, data: str):
        """
        Encrypt data for a given device.
        """
        encrypted = f"encrypted({data})"
        result = {
            "id": f"{device_id}_data",
            "collection": "device_protection",
            "encrypted_data": encrypted
        }

        # Write to DB and trigger replication
        await db.set("device_protection", result["id"], result, "edge")
        await event_bus.publish("db:update", {
            "collection": "device_protection",
            "key": result["id"],
            "value": result,
            "source": "DeviceProtectionEngine"
        })

        logger.log(f"[DeviceProtectionEngine] Data encrypted for device {device_id}")
        return result

    async def run(self, input_data: dict):
        """
        Main entry point:
        {
            "action": "scan" | "encrypt",
            "device_id": str,
            "data": str (optional)
        }
        """
        action = input_data.get("action")
        device_id = input_data.get("device_id")

        if action == "scan":
            return await self.scan_device(device_id)
        elif action == "encrypt":
            data = input_data.get("data", "")
            return await self.encrypt_data(device_id, data)
        else:
            return {"error": f"Unknown action: {action}"}
