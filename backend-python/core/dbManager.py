# backend-python/core/dbManager.py

import asyncio
import time
from typing import Any

class DBManager:
    def __init__(self):
        self.store = {"edge": {}, "shared": {}}

    async def set(self, collection: str, key: str, value: Any, target: str = "edge"):
        if target not in self.store:
            self.store[target] = {}
        if collection not in self.store[target]:
            self.store[target][collection] = {}
        self.store[target][collection][key] = value

    async def get(self, collection: str, key: str, target: str = "edge"):
        return self.store.get(target, {}).get(collection, {}).get(key)

    async def get_all(self, collection: str, target: str = "edge"):
        return list(self.store.get(target, {}).get(collection, {}).values())

db = DBManager()
