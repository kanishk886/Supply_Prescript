import json
from datetime import datetime

class DummyRedisCache:
    def __init__(self):
        self.store = {}

    def get(self, key):
        if key in self.store:
            # Simple expiry check (hardcoded to 5 mins for demo)
            data, timestamp = self.store[key]
            if (datetime.now() - timestamp).total_seconds() < 300:
                return json.dumps(data)
            else:
                del self.store[key]
        return None

    def set(self, key, value, ex=300):
        self.store[key] = (json.loads(value), datetime.now())
        return True

# Initialize a dummy Redis client fallback for local development
redis_client = DummyRedisCache()
