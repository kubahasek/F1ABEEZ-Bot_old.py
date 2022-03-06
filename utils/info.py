import os
from dotenv import load_dotenv
import json

load_dotenv()

discord_token = os.environ.get("discord_token")
token = os.environ.get("token")
incidentDatabaseURL = os.environ.get("incidentDatabaseURL")
profileDatabaseURL = os.environ.get("profileDatabaseURL")
incidentDatabaseId = os.environ.get("incidentDatabaseId")
appealsDatabaseURL = os.environ.get("appealsDatabaseURL")
appealsDatabaseId = os.environ.get("appealsDatabaseId")
mongoDBConnSTR = os.environ.get("mongoDBConnSTR")
figmaToken = os.environ.get("figma_token")
f1abeezID = os.environ.get("f1abeezID")
f1abeezEsportsID = os.environ.get("f1abeezEsportsID")
f2abeezID = os.environ.get("f2abeezID")
testServerID = os.environ.get("testServerID")
highlightsDatabaseId = os.environ.get("highlightsDatabaseId")

IDList = json.load(open('IDList.json'))

def get_channelID(serverID, channelName):
    return IDList[str(serverID)]["channels"][channelName] 

def get_roleID(serverID, roleName):
    return IDList[str(serverID)]["roles"][roleName]

color = 16236412