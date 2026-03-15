import asyncio
import random
from datetime import datetime

from db import get_Db
from db.userHandle import addPlayertoDB


async def createLobbyDB(uid: int, name: str):
    db = get_Db()
    col = db.get_collection('lobbys')
    code = await generateLobbyCode()
    await asyncio.gather(
        col.insert_one({
            "creation_date": datetime.now().timestamp(),
            "host": uid,
            "code": code,
            "name": name,
            "status": "waiting",
            "players": [uid],
            "player_names": [name],
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


async def joinLobbyDB(code: int, user_id: int, usname: str):
    db = get_Db()
    col = db.get_collection('lobbys')
    print("MONGO: Got code,", code)
    col.find_one_and_update({"code": code}, {'$push': {"players": user_id}})
    col.find_one_and_update({"code": code}, {'$push': {"player_names": usname}})
    lobby = await col.find_one({"code": code})
    if not lobby:
        return False
    lobby_id = lobby['host']
    print("MONGO: Got lobby_id, ", lobby_id)
    await addPlayertoDB(user_id, usname, lobby_id, "player")
    print("Added ", user_id)
    return True

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