from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

app = FastAPI()

# CORS-Konfiguration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],  # POST hinzugefügt für Reservierungen
    allow_headers=["*"],
)

class Room(BaseModel):
    id: int
    name: str
    capacity: int

class Reservation(BaseModel):
    room_id: int
    user: str

# Testdaten für die Räume der HTL-Weiz
rooms = [
    Room(id=1, name="EDV 1", capacity=30),
    Room(id=2, name="EDV 2", capacity=25),
    Room(id=3, name="EDV 3", capacity=20),
]

reservations = []

@app.get("/rooms", response_model=List[Room])
async def get_rooms():
    return rooms

@app.get("/rooms/{room_id}/reservations", response_model=List[Reservation])
async def get_reservations(room_id: int):
    return [r for r in reservations if r.room_id == room_id]

@app.post("/rooms/{room_id}/reserve", response_model=Reservation)
async def reserve_room(room_id: int, user: str):
    # Check if the room exists
    room = next((r for r in rooms if r.id == room_id), None)
    if room is None:
        raise HTTPException(status_code=404, detail="Room not found")

    # Check if the room is full
    if len([r for r in reservations if r.room_id == room_id]) >= room.capacity:
        raise HTTPException(status_code=400, detail="Room is full")

    # Create and append the reservation
    reservation = Reservation(room_id=room_id, user=user)
    reservations.append(reservation)
    return reservation

