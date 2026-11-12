from app.db.redis_client import redis_client

redis_client.set("test_key", "SmartBank AI", ex=60)

value = redis_client.get("test_key")

print(value)