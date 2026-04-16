import asyncio

import bot.connectBot as connectBot
import db
from db.lobbyHandle import flushDb
from db.userHandle import flushPlayersDB


async def main():
    await asyncio.gather(
        db.connect_Db(),
        flushDb(),
        flushPlayersDB(),
        connectBot.start_bot())

    
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Stopped")
    

