from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import mysql.connector
import asyncio

app = FastAPI()

# --------------------------
# CORS
# --------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------------------------
# DATABASE
# --------------------------
def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Yasmeen2004.",
        database="parking_system"
    )

# --------------------------
# MODELS
# --------------------------
class UserRegister(BaseModel):
    full_name: str
    phone_number: str
    password: str

class UserLogin(BaseModel):
    phone_number: str
    password: str

class Vehicle(BaseModel):
    user_id: int
    plate_number: str
    vehicle_type: str
    color: str

# --------------------------
# AUTH
# --------------------------
@app.post("/register")
def register(user: UserRegister):

    db = get_db()
    cursor = db.cursor()

    cursor.execute("SELECT * FROM Users WHERE phone_number=%s", (user.phone_number,))
    existing = cursor.fetchone()

    if existing:
        db.close()
        return {"message": "Phone already exists"}

    cursor.execute("""
        INSERT INTO Users (full_name, phone_number, password, role)
        VALUES (%s, %s, %s, %s)
    """, (user.full_name, user.phone_number, user.password, "user"))

    db.commit()
    user_id = cursor.lastrowid
    db.close()

    return {
        "message": "success",
        "user_id": user_id
    }


@app.post("/login")
def login(user: UserLogin):

    db = get_db()
    cursor = db.cursor()

    cursor.execute("""
        SELECT user_id, full_name
        FROM Users
        WHERE phone_number=%s AND password=%s
    """, (user.phone_number, user.password))

    result = cursor.fetchone()
    db.close()

    if result:
        return {
            "message": "success",
            "user_id": result[0],
            "name": result[1]
        }

    return {"message": "invalid"}


# --------------------------
# VEHICLE
# --------------------------
@app.post("/add-vehicle")
def add_vehicle(v: Vehicle):

    db = get_db()
    cursor = db.cursor()

    # check manually (like phone number)
    cursor.execute("SELECT * FROM Vehicles WHERE plate_number=%s", (v.plate_number,))
    existing = cursor.fetchone()

    if existing:
        db.close()
        return {"message": "Plate already exists"}

    cursor.execute("""
        INSERT INTO Vehicles (user_id, plate_number, vehicle_type, color)
        VALUES (%s, %s, %s, %s)
    """, (v.user_id, v.plate_number, v.vehicle_type, v.color))

    db.commit()
    db.close()

    return {"message": "success"}


# --------------------------
# PARKING
# --------------------------
@app.get("/spots")
def get_spots():

    db = get_db()
    cursor = db.cursor()

    cursor.execute("SELECT spot_number, status FROM Parking_Spots")
    rows = cursor.fetchall()

    db.close()

    return [
        {"spot_number": r[0], "status": r[1]}
        for r in rows
    ]


@app.get("/find-car/{plate}")
def find_car(plate: str):

    db = get_db()
    cursor = db.cursor()

    cursor.execute("""
        SELECT spot_number
        FROM Parking_Spots
        WHERE plate_number = %s
    """, (plate,))

    result = cursor.fetchone()
    db.close()

    if result:
        return {
            "plate": plate,
            "spot": result[0],
            "source": "hardware_sync"
        }

    return {"message": "car not found"}


@app.get("/find-owner/{plate}")
def find_owner(plate: str):

    db = get_db()
    cursor = db.cursor()

    cursor.execute("""
        SELECT u.full_name, u.phone_number, v.plate_number
        FROM Users u
        JOIN Vehicles v ON u.user_id = v.user_id
        WHERE v.plate_number = %s
    """, (plate,))

    result = cursor.fetchone()
    db.close()

    if result:
        return {
            "name": result[0],
            "phone": result[1],
            "plate": result[2],
            "source": "hardware_sync"
        }

    return {"message": "not found"}


@app.get("/suggest-spot")
def suggest_spot():

    db = get_db()
    cursor = db.cursor()

    cursor.execute("""
        SELECT spot_number
        FROM Parking_Spots
        WHERE status = 'available'
        ORDER BY spot_number ASC
        LIMIT 1
    """)

    spot = cursor.fetchone()
    db.close()

    if spot:
        return {
            "suggested_spot": spot[0],
            "source": "hardware_live"
        }

    return {"message": "no available spots"}


@app.put("/spot/{spot_number}")
async def update_spot(spot_number: int, status: str):

    db = get_db()
    cursor = db.cursor()

    cursor.execute("""
        UPDATE Parking_Spots
        SET status = %s
        WHERE spot_number = %s
    """, (status, spot_number))

    db.commit()
    db.close()

    await broadcast_spots()

    return {"message": "updated"}

@app.post("/hardware/update-spot")
def hardware_update(data: dict):

    spot_number = data["spot_number"]
    status = data["status"]  # "occupied" or "available"

    db = get_db()
    cursor = db.cursor()

    cursor.execute("""
        UPDATE Parking_Spots
        SET status = %s
        WHERE spot_number = %s
    """, (status, spot_number))

    db.commit()
    db.close()

    return {"message": "updated", "spot": spot_number, "status": status}

#bind-spot-----------------------------------
@app.post("/bind-spot")
def bind_spot(data: dict):

    print("📦 RECEIVED:", data)

    plate = data["plate"]
    spot = data["spot"]

    db = get_db()
    cursor = db.cursor()

    cursor.execute("""
        UPDATE Parking_Spots
        SET plate_number = %s,
            status = 'occupied'
        WHERE spot_number = %s
    """, (plate, spot))

    db.commit()
    db.close()

    return {"message": "bound"}
# --------------------------
# WEBSOCKET
# --------------------------
clients = []

@app.websocket("/ws/spots")
async def websocket_endpoint(websocket: WebSocket):

    await websocket.accept()
    clients.append(websocket)

    await broadcast_spots()

    try:
        while True:
            await asyncio.sleep(1)
    except WebSocketDisconnect:
        clients.remove(websocket)


# --------------------------
# BROADCAST
# --------------------------
async def broadcast_spots():

    db = get_db()
    cursor = db.cursor()

    cursor.execute("SELECT spot_number, status FROM Parking_Spots")
    rows = cursor.fetchall()
    db.close()

    data = [{"spot_number": r[0], "status": r[1]} for r in rows]

    for client in clients:
        try:
            await client.send_json(data)
        except:
            clients.remove(client)
