import asyncio
import math
import random
from datetime import datetime

from db import get_Db
from db.userHandle import addPlayertoDB
from debug.DebugLogger import DebugLogger
from game.game_manager import GameManager


async def createLobbyDB(uid: int, name: str):
    db = get_Db()
    col = db.get_collection('lobbys')
    code = await generateLobbyCode()
    await asyncio.gather(
        col.insert_one({
            "creation_date": math.floor(datetime.now().timestamp()),
            "host": uid,
            "code": code,
            "name": name,
            "status": "waiting",
            "players": [uid],
            "player_names": [name],
            "pack": "Не обрано",
            "timer": 10
        }),
        addPlayertoDB(uid, name, uid, "host")
    )
    lobby: dict = await col.find_one({"host": uid})
    return lobby

async def deleteLobbyDB(uid: int):
    db = get_Db()
    col = db.get_collection('lobbys')

    rmdoc = await col.find_one_and_delete({"host": uid})
    if rmdoc:
        DebugLogger.Console("MONGO: Removed ", rmdoc)
    else:
        DebugLogger.Console("MONGO: No lobby deleted, removing user instead")
        coll = db.get_collection('players')
        player = await coll.find_one({"uid": uid})
        if player is not None:
            lobby_id = player.get("lobby_id")
            await col.find_one_and_update({"host": lobby_id}, {"$pull": {"players": uid}})
            DebugLogger.Console("MONGO: Removed ", uid)


async def joinLobbyDB(code: int, user_id: int, usname: str):
    db = get_Db()
    col = db.get_collection('lobbys')
    DebugLogger.Console("MONGO: Got code,", code)
    col.find_one_and_update({"code": code}, {'$push': {"players": user_id}})
    col.find_one_and_update({"code": code}, {'$push': {"player_names": usname}})
    lobby = await col.find_one({"code": code})
    if not lobby:
        return False
    lobby_id = lobby['host']
    DebugLogger.Console("MONGO: Got lobby_id, ", lobby_id)
    await addPlayertoDB(user_id, usname, lobby_id, "player")
    DebugLogger.Console("Added ", user_id)
    return True

async def leaveLobbyDB(code: int, user_id: int, usname: str):
    db = get_Db()
    col = db.get_collection('lobbys')
    DebugLogger.Console("MONGO: Got code,", code)
    await col.find_one_and_update({"code": code}, {'$pull': {"players": user_id}})
    await col.find_one_and_update({"code": code}, {'$pull': {"player_names": usname}})
    DebugLogger.Console("MONGO: Removed from lobby,", user_id)

# -------------------------

async def flushDb():
    db = get_Db()
    col = db.get_collection('lobbys')
    col.delete_many({})
    DebugLogger.Console("MONGO: Deleted All lobbies on start")

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

async def getLobbyByID(host_id: int):
    db = get_Db()
    col = db.get_collection('lobbys')
    lobby = await col.find_one({"host": host_id})
    return lobby

async def getLobbyCode(host_id: int):
    db = get_Db()
    col = db.get_collection('lobbys')
    lobby = await col.find_one({"host": host_id})
    return lobby['code']

async def update_status_lobby(lobby_id: int, status: str):
    db = get_Db()
    col = db.get_collection('lobbys')
    await col.update_one({"host": lobby_id}, {"$set": {"status": status}})
    DebugLogger.Console(f"MONGO: Updated status to {status}", lobby_id)

async def updatePackInLobby(uid: int, pack_name: str):
    db = get_Db()
    col = db.get_collection('lobbys')
    await col.update_one({"host": uid}, {"$set": {'pack': pack_name}})

async def updateTeamInLobby(lobby_id: int, uid: int, team_name: str):
    db = get_Db()
    col = db.get_collection('lobbys')
    await col.update_one({"host": lobby_id}, {"$push": {uid: team_name}})

#scores down 'ere
async def push_scores_db(game_manager: GameManager):
    DebugLogger.Console("MONGO: Starting pushing scores to DB...")

    db = get_Db()
    col = db.get_collection('players')

    scores_dict = game_manager.game_session.team_scores
    score_players = scores_dict.keys()

    for player in score_players:
        document = await col.find_one({"name": player})
        await col.update_one({"name": player}, {"$set": {"score": document['score']+scores_dict[player]}})

        DebugLogger.Console(f"MONGO: Updated score to {player}: {document['score']+scores_dict[player]}")
    DebugLogger.Console("MONGO: Pushed scores to DB")

async def fetch_leaderboard_db():
    db = get_Db()
    col = db.get_collection('players')
    cursor = col.find({})
    doc_list = []
    async for document in cursor:
        doc_list.append(document)
    return doc_list
    DebugLogger.Console(f"MONGO: Fetched leaderboard data: {doc_list}")

