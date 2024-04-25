from fastapi import APIRouter, Depends, HTTPException, WebSocket, Request
from sqlalchemy import or_
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from starlette.websockets import WebSocketDisconnect

from app.database import get_db
from app.models import User, Room, Message
from app.schemas import RoomOutput, RoomCreate
from app.services.oauth2 import get_current_user, verify_access_token

router = APIRouter(prefix='/chat', tags=['chat'])


@router.post('/room-create-public', status_code=201, response_model=RoomOutput)
def create_room(room: RoomCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    new_room = Room(name=room.name)
    db.add(new_room)
    db.commit()
    db.refresh(new_room)
    return new_room


@router.post('/room-create-private/{user_id}', status_code=201, response_model=RoomOutput)
def create_private_room(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    room = db.query(Room).filter(or_(Room.name == f"{user_id}_{current_user.id}",
                                     Room.name == f"{current_user.id}_{user_id}")).first()
    if room:
        return room
    new_room = Room(name=f"{user_id}_{current_user.id}")
    db.add(new_room)
    db.commit()
    db.refresh(new_room)
    return new_room


@router.get('/room-list', status_code=200, response_model=list[RoomOutput])
def get_rooms(db: Session = Depends(get_db)):
    return db.query(Room).all()


class ConnectionManager:
    """Class defining socket events"""

    def __init__(self):
        """init method, keeping track of connections"""
        self.active_connections = []

    async def connect(self, websocket: WebSocket):
        """connect event"""
        await websocket.accept()
        self.active_connections.append(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        """Direct Message"""
        await websocket.send_text(message)

    def disconnect(self, websocket: WebSocket):
        """disconnect event"""
        self.active_connections.remove(websocket)


manager = ConnectionManager()
templates = Jinja2Templates(directory="app/routers")


@router.get("/", response_class=HTMLResponse)
def read_index(request: Request):
    # Render the HTML template
    return templates.TemplateResponse("index.html", {"request": request})


@router.websocket("/room/{room_id}")
async def create_message(room_id: int, websocket: WebSocket,
                         db=Depends(get_db)):
    await websocket.accept()
    token = websocket.headers['Authorization'].split(' ')[1]
    user_id = verify_access_token(token)
    room = db.query(Room).filter(Room.id == room_id).first()
    if not room:
        await websocket.close()
        return HTTPException(status_code=404, detail="Room not Found")
    try:
        while True:
            data = await websocket.receive_text()
            message = Message(room_id=room_id, owner_id=user_id, content=data)
            db.add(message)
            db.commit()
            db.refresh(message)
            await websocket.send_text(f"Message received: {data}")
    except:
        await websocket.close()

    # await manager.connect(websocket)
    # try:
    #     while True:
    #         data = await websocket.receive_text()
    #         await manager.send_personal_message(f"Received:{data}", websocket)
    # except WebSocketDisconnect:
    #     manager.disconnect(websocket)
    #     await manager.send_personal_message("Bye!!!", websocket)
