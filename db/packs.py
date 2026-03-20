from db import get_Db


async def addPack(packname: str, words: list, uid: int):
    db = get_Db()
    col = db.get_collection('packs')
    add = await col.insert_one({
        "uid": uid,
        "name": packname,
        "words": words,
    })
    print("PACKS: Створений набір слів ", packname)

async def removePack(packname: str, uid: int):
    db = get_Db()
    col = db.get_collection('packs')
    doc = await col.find_one({"name": packname})
    if doc["uid"] == uid:
        await col.delete_one({"name": packname})
        print("PACKS: Removed pack ", packname)
        return


async def getPackById(packname: str):
    docName = None
    db = get_Db()
    col = db.get_collection('packs')
    document = await col.find_one({"name": packname})
    if document:
        docName = document.get("name")
    return docName

async def fetchOwnPacks(uid: int):
    db = get_Db()
    col = db.get_collection('packs')
    docs = col.find({"uid": uid})
    packs = []
    async for doc in docs:
        packs.append(doc)
    return packs

async def fetchAllPacks():
    db = get_Db()
    col = db.get_collection('packs')
    docs = col.find({})
    packs = []
    async for doc in docs:
        packs.append(doc)
    return packs
