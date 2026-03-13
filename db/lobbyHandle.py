import asyncio
import random

from db import get_Db
from db.userHandle import addPlayertoDB


async def createLobbyDB(uid: int, name: str):
    db = get_Db()
    col = db.get_collection('lobbys')
    code = await generateLobbyCode()
    await asyncio.gather(
        col.insert_one({
            "host": uid,
            "code": 1234, #TEMP
            "name": name,
            "status": "waiting",
            "players": [uid],
            "pack": "none"
        }),
        addPlayertoDB(uid, name, uid, "host")
    )

async def deleteLobbyDB(uid: int):
    db = get_Db()
    col = db.get_collection('lobbys')

    rmdoc = await col.find_one_and_delete({"host": uid})
    if rmdoc:
        print("MONGO: Removed ", rmdoc)
    else:
        print("MONGO: No lobby deleted, removing user instead")
        coll = db.get_collection('players')
        player = await coll.find_one({"uid": uid})
        if player is not None:
            lobby_id = player.get("lobby_id")
            await col.find_one_and_update({"host": lobby_id}, {"$pull": {"players": uid}})
            print("MONGO: Removed ", uid)


async def joinLobbyDB(lobby_id: int, user_id: int, usname: str):
    db = get_Db()
    col = db.get_collection('lobbys')
    print("Got lobby_id,", type(lobby_id))
    col.find_one_and_update({"host": lobby_id}, {'$push': {"players": user_id}})
    await addPlayertoDB(user_id, usname, lobby_id, "player")
    print("Added ", user_id)

# -------------------------

async def flushDb():
    db = get_Db()
    col = db.get_collection('lobbys')
    col.delete_many({})
    print("MONGO: Deleted All lobbies on start")

async def generateLobbyCode():
    db = get_Db()
    col = db.get_collection('lobbys')
    while True:
        code = random.randint(1000, 9999)
        exist = await col.find_one({"code": code})
        if not exist:
            return code

async def findLobbyByCode(lobby_code: int):
    db = get_Db()
    col = db.get_collection('lobbys')
    lobby = await col.find_one({"code": lobby_code})
    if lobby:
        return lobby
    else:
        return None

async def getLobbyCode(host_id: int):
    db = get_Db()
    col = db.get_collection('lobbys')
    lobby = await col.find_one({"host": host_id})
    return lobby['code']