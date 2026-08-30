from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from database.database import (
    create_message,
    delete_message,
    get_messages,
    update_message,
)

app = FastAPI(
    title="Docker Learning App API",
    description="Small CRUD API for learning Docker architecture",
    version="1.0.0",
)


class MessageCreate(BaseModel):
    message: str


class MessageUpdate(BaseModel):
    message: str


@app.get("/")
def home():
    return {"message": "Docker Learning App backend is running!"}


@app.get("/messages")
def read_messages():
    messages = get_messages()
    return [{"id": message_id, "message": message} for message_id, message in messages]


@app.post("/messages")
def add_message(data: MessageCreate):
    message = data.message.strip()
    if not message:
        raise HTTPException(status_code=400, detail="Message cannot be empty.")
    message_id = create_message(message)
    return {"id": message_id, "message": message}


@app.put("/messages/{message_id}")
def edit_message(
    message_id: int,
    data: MessageUpdate,
):
    message = data.message.strip()
    if not message:
        raise HTTPException(status_code=400, detail="Message cannot be empty.")
    updated = update_message(message_id, message)
    if not updated:
        raise HTTPException(status_code=404, detail="Message not found.")
    return {"id": message_id, "message": message}


@app.delete("/messages/{message_id}")
def remove_message(message_id: int):
    deleted = delete_message(message_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Message not found.")
    return {"id": message_id, "message": "Message deleted successfully."}
