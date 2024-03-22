from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

with open("index.html", "r") as file:
    index_html_content = file.read()

class Room(BaseModel):
    id: int
    name: str
    capacity: int

class Reservation(BaseModel):
    room_id: int
    user: str

rooms = [
    Room(id=1, name="Room A", capacity=30),
    Room(id=2, name="Room B", capacity=25),
    Room(id=3, name="Room C", capacity=20),
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
    room_exists = False
    for room in rooms:
        if room.id == room_id:
            room_exists = True
            if len([r for r in reservations if r.room_id == room_id]) >= room.capacity:
                raise HTTPException(status_code=400, detail="Room is full")
            else:
                reservation = Reservation(room_id=room_id, user=user)
                reservations.append(reservation)
                return reservation
    if not room_exists:
        raise HTTPException(status_code=404, detail="Room not found")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
