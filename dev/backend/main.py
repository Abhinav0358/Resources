import asyncio
import json
from typing import List

from fastapi import Depends, FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession

from . import crud, database, models, schemas

app = FastAPI(title="Pro Vision API")

# --- CORS Middleware ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict this
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- Connection Manager for WebSockets ---
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


manager = ConnectionManager()


# --- Startup Event: Listen to Redis and Create Tables ---
@app.on_event("startup")
async def startup_event():
    # Create Postgres tables (equivalent to 'migrations' for this lab)
    async with database.engine.begin() as conn:
        await conn.run_sync(database.Base.metadata.create_all)

    # Run redis listener in background
    asyncio.create_task(redis_listener())


async def redis_listener():
    pubsub = database.redis_client.pubsub()
    await pubsub.subscribe("vision_events")
    async for message in pubsub.listen():
        if message["type"] == "message":
            await manager.broadcast(message["data"])


# --- API Routes ---
@app.get("/cameras", response_model=List[schemas.CameraResponse])
async def read_cameras(
    skip: int = 0, limit: int = 100, db: AsyncSession = Depends(database.get_db)
):
    return await crud.get_cameras(db, skip=skip, limit=limit)


@app.post("/cameras", response_model=schemas.CameraResponse)
async def create_camera(
    camera: schemas.CameraCreate, db: AsyncSession = Depends(database.get_db)
):
    return await crud.create_camera(db, camera)


@app.get("/events")
async def get_recent_events(limit: int = 50):
    # Fetch from MongoDB (NoSQL)
    cursor = database.mongo_db.events.find().sort("timestamp", -1).limit(limit)
    events = []
    async for doc in cursor:
        doc["_id"] = str(doc["_id"])  # Convert ObjectId to string
        events.append(doc)
    return events


# --- WebSocket Endpoint ---
@app.websocket("/ws/events")
async def websocket_events(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()  # Keep connection alive
    except WebSocketDisconnect:
        manager.disconnect(websocket)
