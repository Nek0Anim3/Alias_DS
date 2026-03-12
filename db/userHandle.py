import asyncio

from aiogram.types import CallbackQuery

from db import get_Db

async def addPlayertoDB(uid: int, usname: str, lobby_id: int, role: str):
    db = get_Db()
    col = db.get_collection("players")
    if await col.find_one({"uid": uid}):
        await asyncio.gather(
            col.update_one({"uid": uid}, {"$set": {"lobby_id": lobby_id}}),
            col.update_one({"uid": uid}, {"$set": {"role": role}}),
        )
    else:
        await col.insert_one({
            "uid": uid,
            "name": usname,
            "lobby_id": lobby_id,
            "role": role
        })
    print("USER DB: Player added", uid)

async def removePlayerfromDB(uid: int):
    db = get_Db()
    col = db.get_collection("players")
    await asyncio.gather(
        col.find_one_and_update({"uid": uid}, {"$set": {"lobby_id": ""}}),
        col.find_one_and_update({"uid": uid}, {"$set": {"role": ""}})
    )
    print("USER DB: Player flushed, ", uid)

async def flushPlayersDB():
    db = get_Db()
    col = db.get_collection("players")
    await asyncio.gather(
        col.update_many({}, {"$set": {"lobby_id": ""}}),
        col.update_many({}, {"$set": {"role": ""}}),
        )
    print("USER DB: Player's lobbys and roles flushed")