# MORE HELP = python packmanager.py --help or -h
# THIS SCRIPT MUST BE EXECUTED FROM TERMINAL
# USE IT !ONLY! IF YOU WANT AS DEVELOPER QUICKLY ADD LARGE PACKS
#
# HOW TO USE IT:
#
# IF YOU HAVE A JSON FILE OF PACK: packmanager.py -i "example.json"
#
# IF YOU DONT HAVE: JUST EXECUTE AND FOLLOW STEPS
#
# STEP 1: SPECIFY NAME OF PACK
# STEP 2: SPECIFY AUTHOR
# STEP 3: WRITE DOWN NAME OF .TXT FILE WITH WORDS
# STEP 4 (OPTIONAL): WRITE A COPY .JSON ? (Y/n)
#
# FORMATTING TXT:
# VARIANT 1 [example.txt]: apple, banana, rice, vinegar , salt, pineapple
# VARIANT 2 [example.txt] (Every word from new line):
# apple
# banana
# pineapple
# vinegar
# salt
# ...

# FORMATTING JSON (I dunno why you need to struggle with JSON, if you just import existing, you dont need to edit it):
# {
#   "name": "MyCoolPack",
#   "author": "NekoAnime"
#   "words": ["apple", "banana", "pineapple"]
# }

import argparse
import asyncio
import json
import os

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from mypy.join import update_callable_ids

_db = None
def connect_db():
    global _db
    client = AsyncIOMotorClient(os.getenv("MONGO_URI"))
    _db = client.get_database("alias")

async def pushToDB(data: dict):
    global _db
    collection = _db.get_collection("packs")
    doc = await collection.find_one({"name": data["name"]})
    if doc is not None:
        print(f"Pack {data['name']} already exists")
        return
    collection.insert_one({
        "uid": data["uid"],
        "name": data["name"],
        "words": data["words"],
    })
    print(f"Pack {data['name']} added to DB")

def cmd_json(args):
    try:
        with open(args.file, 'r', encoding='utf-8') as f:
            data_dict = json.load(f)
    except FileNotFoundError:
        print(f"File {args.file} not found")
        return
    print(f"Loaded JSON")
    try:
        data_dict['name']
        data_dict['words']
        data_dict["uid"]
    except KeyError:
        print(f"Error: CHECK YOUR JSON DATA (name, words, uid)")
        return
    asyncio.run(pushToDB(data_dict))



def cmd_convert(args):
    print(f"Конвертирую {args.file} → формат {args.format}")

def packmanager():
    connect_db()
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='command', required=True)

    # Import JAY SON
    p_read = subparsers.add_parser('import', help='Imports JSON and pushes to DB | packmanager.py import awesomepack.json')
    p_read.add_argument('file', help='Specify JSON file')  # позиционный аргумент
    p_read.set_defaults(func=cmd_json)


    # TODO: CREATE PACK FROM SCRATCH
    p_conv = subparsers.add_parser('create', help='Create a new pack | packmanager.py create MyNewAwesomePack')
    p_conv.add_argument('name', help='Name of pack')

    p_conv.set_defaults(func=cmd_convert)

    args = parser.parse_args()
    args.func(args)  # вызываем нужную функцию автоматически


if __name__ == '__main__':
    packmanager()
