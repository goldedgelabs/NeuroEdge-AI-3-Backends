# backend-python/utils/logger.py
import time

class Logger:
    def log(self, msg):
        print(f"[LOG {time.strftime('%H:%M:%S')}] {msg}")

    def warn(self, msg):
        print(f"[WARN {time.strftime('%H:%M:%S')}] {msg}")

    def error(self, msg):
        print(f"[ERROR {time.strftime('%H:%M:%S')}] {msg}")

logger = Logger()
