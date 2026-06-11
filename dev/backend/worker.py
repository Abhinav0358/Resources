import asyncio
import json
import random
from datetime import datetime

from .database import mongo_db, redis_client


async def simulate_vision_pipeline():
    """
    Simulates an AI camera system:
    1. Generates a random detection.
    2. Saves the event to MongoDB (Persistence).
    3. Publishes the event to Redis (Real-time).
    """
    labels = ["person", "car", "dog", "bicycle"]

    while True:
        # 1. Create fake detection
        event = {
            "camera_id": random.randint(1, 10),
            "timestamp": datetime.utcnow().isoformat(),
            "label": random.choice(labels),
            "confidence": round(random.uniform(0.7, 0.99), 2),
            "bounding_box": [
                random.randint(0, 100),
                random.randint(0, 100),
                random.randint(100, 500),
                random.randint(100, 500),
            ],
        }

        # 2. Persist to MongoDB
        await mongo_db.events.insert_one(event.copy())

        # 3. Publish to Redis for WebSockets
        # Convert _id if present because it's not JSON serializable
        if "_id" in event:
            event["_id"] = str(event["_id"])

        await redis_client.publish("vision_events", json.dumps(event))

        print(
            f"Worker: Processed event for Camera {event['camera_id']} - {event['label']}"
        )

        # Wait before next event
        await asyncio.sleep(random.uniform(1.0, 5.0))


if __name__ == "__main__":
    asyncio.run(simulate_vision_pipeline())
