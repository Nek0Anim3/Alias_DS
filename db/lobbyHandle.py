from db import get_Db
from motor.motor_asyncio import AsyncIOMotorClient
from aiogram import types

async def createLobbyDB(uid: int, name: str):
    db = get_Db()
    col = db.get_collection('lobbys')
    add = await col.insert_one({
        "host": uid,
        "name": "",
        "status": "waiting", 
        "players": [], 
        "pack": "none"
    })
    print("Lobby DB id: ", add.inserted_id)
    print("Lobby created, host_id: ", uid)



lobbies_list = []
lobbies_id_list = []

async def fetchLobbiesList():
    db = get_Db()
    col = db.get_collection('lobbys')
    lobbys_list = col.find({"status": "waiting"}).limit(10)
    async for lobby in lobbys_list: 
        if lobby["name"] in lobbies_list:
            continue
        else:
            lobbies_list.append(lobby["name"])
        #---------------------------------------
        if lobby["host"] in lobbies_id_list:
            continue
        else:
            lobbies_id_list.append([lobby["host"]])
        
    print("Lobby of players ", lobbies_list)
    print("IDs ", lobbies_id_list)
    return lobbies_list

def getLobbyIdList():
    return lobbies_id_list
