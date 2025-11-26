# backend-python/core/engineManager.py
from ..db.dbManager import db
from ..core.eventBus import eventBus
from ..utils.logger import logger

engineManager = {}

def register_engine(name: str, engine_instance):
    engineManager[name] = engine_instance
