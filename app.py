import discord
from discord import client
from discord.ext import tasks, commands
import requests
import json
import os

discord_token = os.environ.get("discord_token")
token = os.environ.get("token")
incidentDatabseURL = os.environ.get("incidentDatabaseURL")


    
def queryTickets(gamertag):
    zprava = ""
    header = {"Authorization": token, "Notion-Version": "2021-05-13"}
    r = requests.post(incidentDatabseURL, json = {
      "filter": {
      "property": "Reported By",
      "rich_text": {
          "contains": gamertag
      }
      },
      "sorts": [{ "property": "title", "direction": "ascending" }]
    }
    , headers=header).text

    b = json.loads(r)

    if (len(b["results"]) == 0):
        zprava = "Gamertag is incorrect, please try again."
        return zprava

    for i in range(len(b["results"])):
        zprava += (f'{i +1}. {b["results"][i]["properties"]["Case Number"]["title"][0]["plain_text"]} - {b["results"][i]["properties"]["Reported By"]["rich_text"][0]["text"]["content"]} vs {b["results"][i]["properties"]["GamerTag(s) of Driver(s) involved incident (N/A for penalties)"]["rich_text"][0]["text"]["content"]}\n')

    return zprava





def TicketDetailQuery(ticketNumber):
    header = {"Authorization": token,  "Notion-Version": "2021-05-13"}
    req = requests.post(incidentDatabseURL, json = {
        "filter": {
        "property": "Case Number",
        "title": {
            "contains": ticketNumber
        }
        }
        }
        , headers=header).text

    c = json.loads(req)
    embed=discord.Embed(title="Incident Detail", color=16236412)

    ticketNumber = c["results"][0]["properties"]["Case Number"]["title"][0]["text"]["content"]
    driversInvolved = f'{c["results"][0]["properties"]["Reported By"]["rich_text"][0]["text"]["content"]} vs {c["results"][0]["properties"]["GamerTag(s) of Driver(s) involved incident (N/A for penalties)"]["rich_text"][0]["text"]["content"]}'
    status = c["results"][0]["properties"]["Status"]["select"]["name"]

    description = c["results"][0]["properties"]["Description"]["rich_text"][0]["text"]["content"]

    embed.add_field(name="Status", value=str(status), inline=False)
    embed.add_field(name="Ticket Number", value=str(ticketNumber), inline=True)
    embed.add_field(name="Drivers Involved", value=str(driversInvolved), inline=True)
    embed.add_field(name="Description", value=str(description), inline=False)

    ## Time Penalty
    try:
        timePenalty = c["results"][0]["properties"]["Time Penalty Given"]["rich_text"][0]["text"]["content"]
    except KeyError:
        timePenalty = "N/A"
    except IndexError:
        timePenalty = "N/A"

    if(timePenalty != "N/A"):
        embed.add_field(name="Time Penalty", value=str(timePenalty), inline=False)

    ##Penalty Points    

    try:
        penaltyPoints = c["results"][0]["properties"]["Penalty Points Given"]["number"]
    except KeyError:
        penaltyPoints = "N/A"
    except IndexError:
        penaltyPoints = "N/A"

    if(penaltyPoints != "N/A"):
        embed.add_field(name="Penalty Points", value=str(penaltyPoints), inline=False)

    ## Grid Penalty

    try:
        gridPenalty = c["results"][0]["properties"]["Grid Penalty"]["rich_text"][0]["text"]["content"]
    except IndexError:
        gridPenalty = "N/A"
    except KeyError:
        gridPenalty = "N/A"

    if(gridPenalty != "N/A"):
        embed.add_field(name="Grid Penalty", value=str(gridPenalty), inline=False)

    ## Penalty awarded to

    try:
        penaltyAwardedTo = c["results"][0]["properties"]["Penalty to"]["rich_text"][0]["text"]["content"]
    except IndexError:
        penaltyAwardedTo = "Not specified"
    except KeyError:
        penaltyAwardedTo = "Not specified"

    if(penaltyAwardedTo != "N/A"):
        embed.add_field(name="Penalty Awarded To", value=str(penaltyAwardedTo), inline=False)

    ## Warning awarded

    try:
        warningAwarded = c["results"][0]["properties"]["Warning given"]["number"]
    except KeyError:
        warningAwarded = "N/A"  
    except IndexError:
        warningAwarded = "N/A"    

    if(warningAwarded != "N/A"):
        embed.add_field(name="Warning awarded to", value=str(warningAwarded), inline=False)

    return embed    


bot = commands.Bot(command_prefix=";")

@bot.event
async def on_ready():
    print("We have logged in as {0.user}".format(bot))

@bot.command(name="gettickets")
async def GetTickets(ctx, gamertag):
    await ctx.send(queryTickets(gamertag))

@bot.command(name="ticketdetail")
async def TicketDetail(ctx, ticketNum):
    await ctx.send(embed = TicketDetailQuery(ticketNum))

bot.run(discord_token)