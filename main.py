from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pymongo.mongo_client import MongoClient
from typing import List

uri = "mongodb+srv://iriscciou:supermon@selfuse.wvpvqks.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri)
try:
    client.admin.command('ping')
    db = client["Selfuse"]
    col = db["poll"]
except Exception as e:
    print(e)


# App initailization
app = FastAPI()

#templates
templates = Jinja2Templates(directory="templates")
app.mount("/templates", StaticFiles(directory="templates", html=True), name="templates")

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_json(message)




manager = ConnectionManager()



@app.get("/")
async def get(request: Request):
    votes = get_vote()
    vote_cnt = vote_cal(votes)
    print(vote_cnt)
    return templates.TemplateResponse("Index.html", {'request': request, 'votes': vote_cnt})


# recieve js value
@app.websocket("/sendVote")
async def user_vote(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive()
            if data['type'] != 'websocket.disconnect':
                if data['text'] != 'Reset':
                    doc = {"vote": data, "num": 1}
                    add_vote(doc)
                else:
                    reset_vote()

                votes_now = get_vote()
                vote_now = vote_cal(votes_now)
                await manager.broadcast(vote_now)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as ex:
        print(ex)


def get_vote():
    group = { "$group": {"_id": "$vote", "cnt": {"$sum": "$num"}}}
    pipeline = [group]
    results = col.aggregate(pipeline)
    result_list = list(results)

    return result_list

def vote_cal(vote_result):
    vote_count = [0, 0, 0, 0, 0, 0]
    options = ["Red", "Blue", "Yellow", "Green", "Purple", "Orange"]
    for v in vote_result:
        if type(v['_id']) is dict:
            if 'text' in v['_id']:
                vote_count[options.index(v['_id']['text'])] += v['cnt']

    return vote_count

def add_vote(vote):
    col.insert_one(vote)

def reset_vote():
    col.delete_many({"num": 1})

def connect_db():
# connect to DB
    uri = "mongodb+srv://iriscciou:supermon@selfuse.wvpvqks.mongodb.net/?retryWrites=true&w=majority"
    client = MongoClient(uri)
    try:
        client.admin.command('ping')
        db = client["Selfuse"]
        col = db["poll"]
        return col
    except Exception as e:
        print(e)

    
    
    