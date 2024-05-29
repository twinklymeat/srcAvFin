import srcomapi, srcomapi.datatypes as dt
import os
import math

api = srcomapi.SpeedrunCom()
api.debug = 0



api.api_key = os.getenv("APIKEY")
motoID = api.get("games/moto_x3m")["id"]
motoGame = api.get_game(motoID)

# print(motoGame.levels[0].data)

masterList = []

for level in motoGame.levels[0:25]:
    levelList = []
    runs = []
    hasNext = True

    RunList = dt.Leaderboard(api, data=api.get(f"leaderboards/{motoID}/level/{level.id}/wdmxwq5k?embed=players"))
        
    masterList.append(RunList)

empty_times = []

for level in masterList:
    level:dt.Leaderboard
    _counter = 0
    for run in level.data["runs"]:
        _counter += 1 
        if _counter == len(level.data["runs"]):
            empty_times.append(run["run"]["times"]["primary_t"])
        
bigDict = {}

playerList = []
nameList = []
for level in masterList:
    level:dt.Leaderboard
    for run in level.data["runs"]:
        player = run["run"]["players"][0]["id"]
        if not player in playerList:
            playerList.append(player)
            for data in level.data["players"]["data"]:
                if player == data["id"]:
                    try:
                        name = data["names"]["international"]
                    except:
                        name = data["name"]
                    
                    nameList.append(name)
                    break

nameDict = {}
_counter = 0
for id in playerList:
    nameDict[id] = nameList[_counter]
    _counter += 1
# print(len(playerList))

playerList = set(playerList)

for player in playerList:
    bigDict[player] = []



_counter = 0
for level in masterList:
    level:dt.Leaderboard
    dupPlayerList = playerList.copy()
    for run in level.data["runs"]:
        player = run["run"]["players"][0]["id"]
        dupPlayerList.remove(player)
        # print(len(playerList))
        bigDict[player].append(run["place"])
    for id in dupPlayerList:
        # print(id)
        bigDict[id].append(len(level.data["runs"]))
    _counter += 1

# print(bigDict)

averageDict = {}
for id in bigDict:
    averageDict[nameDict[id]] = sum(bigDict[id])/len(bigDict[id])

res = {key: val for key, val in sorted(averageDict.items(), key = lambda ele: ele[1])}

for name in res:
    print(res[name], name)