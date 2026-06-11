from typing import List, Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI()


# 1. The Model (Data Validation)
class Item(BaseModel):
    name: str
    price: float
    is_offer: Optional[bool] = None
    tags: List[str] = []


# 2. In-memory storage
items = {}


@app.post("/items/{item_id}")
def create_item(item_id: int, item: Item):
    items[item_id] = item
    return {"item_id": item_id, **item.dict()}


@app.get("/items/{item_id}")
def read_item(item_id: int):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    return items[item_id]


# Run with: uvicorn 01_fastapi_basics:app --reload
