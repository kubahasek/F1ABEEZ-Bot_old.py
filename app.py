import discord
from discord import client
from discord.ext import tasks, commands
from discord.ext.commands import CommandNotFound
import requests
import json
import os

discord_token = os.environ.get("discord_token")
token = os.environ.get("token")
incidentDatabaseURL = os.environ.get("incidentDatabaseURL")
profileDatabaseURL = os.environ.get("profileDatabaseURL")


    
def queryTickets(gamertag):
    zprava = ""
    header = {"Authorization": token, "Notion-Version": "2021-05-13"}
    r = requests.post(incidentDatabaseURL, json = {
      "filter": {
  "or": [
    {
      "property": "Reported By",
      "rich_text": {
        "contains": gamertag
      }
    },
    {
      "property": "GamerTag(s) of Driver(s) involved incident (N/A for penalties)",
      "rich_text": {
        "contains": gamertag
      }
    }
  ]
      },
  "sorts": [{ "property": "Case Number", "direction": "ascending" }]}

    , headers=header).text

    embed = discord.Embed(title=f"Tickets where {gamertag} was involved", color=16236412)

    b = json.loads(r)

    if (len(b["results"]) == 0):
        embed.add_field(name="Error", value="Gamertag is incorrect, please try again.")
        return embed

    for i in range(len(b["results"])):
        caseNumber = b["results"][i]["properties"]["Case Number"]["title"][0]["plain_text"]
        driversInvolved = (f'{b["results"][i]["properties"]["Reported By"]["rich_text"][0]["text"]["content"]} vs {b["results"][i]["properties"]["GamerTag(s) of Driver(s) involved incident (N/A for penalties)"]["rich_text"][0]["text"]["content"]}\n')
        embed.add_field(name=caseNumber, value=driversInvolved, inline=False)

    return embed





def TicketDetailQuery(ticketNumber):
    header = {"Authorization": token,  "Notion-Version": "2021-05-13"}
    req = requests.post(incidentDatabaseURL, json = {
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
    try:
        ticketNumber = c["results"][0]["properties"]["Case Number"]["title"][0]["text"]["content"]
    except IndexError:
        embed.add_field(name="Error", value="This ticket does not exist in our database.")
        return embed
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

def profileQuery(gamertag):
    gamertag = str(gamertag)
    header = {"Authorization": token,  "Notion-Version": "2021-05-13"}
    req2 = requests.post(profileDatabaseURL, headers=header, json={
      "filter": {
      "property": "GamerTag",
      "title": {
          "contains": gamertag
      }
      }
    }).text

    d = json.loads(req2)

    embed=discord.Embed(title=str(gamertag), color=16236412)

    try: 
        gamertagQuery = d["results"][0]["properties"]["GamerTag"]["title"][0]["text"]["content"]
    except IndexError:
        embed.add_field(name="Error", value="The profile for this gamertag doesn't exist in our database, please contact the admins if think that is a mistake.", inline=False)
        return embed

    if(gamertagQuery != gamertag):
        embed.add_field(name="Error", value="The profile for this gamertag doesn't exist in our database, please contact the admins if think that is a mistake.", inline=False)
        return embed

    try:
        tier = d["results"][0]["properties"]["S3 Tier"]["rollup"]["array"][0]["select"]["name"]
    except IndexError:
        embed.add_field(name="Tier", value="You don't have a tier assigned, please contact the admins if you think that is a mistake", inline=False)
    embed.add_field(name="Tier", value=str(tier))

    try: 
        team = d["results"][0]["properties"]["Team"]["rollup"]["array"][0]["select"]["name"]
    except IndexError:
        team = ""
        embed.add_field(name="Team", value="You don't have a team assigned, please contact the admins if you think that is a mistake", inline=False)

    if (team != ""):
        embed.add_field(name="Team", value=str(team), inline=False)

    try:
        numberOfF1Points = d["results"][0]["properties"]["Total F1 Points"]["rollup"]["number"]
    except KeyError:
        numberOfF1Points = 0
    embed.add_field(name="Points", value=str(numberOfF1Points), inline=False) 

    try:
        numberOfPenPoints = d["results"][0]["properties"]["Penalty Points"]["rollup"]["number"]
    except KeyError:
        numberOfPenPoints = 0
    embed.add_field(name="Penalty Points", value=str(numberOfPenPoints), inline=False)

    f2Participant = d["results"][0]["properties"]["F2 Participant"]["rollup"]["array"][0]["checkbox"]
    if(f2Participant == True):
        try:
            f2Points = d["results"][0]["properties"]["Total F2 Points"]["rollup"]["number"]
        except KeyError:
            f2Points = 0
        embed.add_field(name="F2 Points", value=str(f2Points))

    return embed


def GetHelpCommand():
    embed = discord.Embed(title="Help")
    embed.add_field(name=";gettickets <gamertag>", value="This command is useful when you don’t know the number of your ticket. The command lists all tickets you’ve been involved (whether you reported it or someone else reported you) and gives you the number of the ticket.")
    embed.add_field(name=";ticketdetail <number of ticket>", value="This command gets you the details of ticket you provide. It lists the status, penalty that was awarded and who was involved.")
    embed.add_field(name=";getprofile <gamertag>", value="This command gets you your profile from our profile database on the website. You can see how many penalty points you have or whether you have a quali or race ban as well as your team and tier. You can also see how many points you have scored in F1 or F2 tiers")
    return embed

bot = commands.Bot(command_prefix=";", help_command=None)
bot.remove_command("help")

@bot.event
async def on_ready():
    print("We have logged in as {0.user}".format(bot))

@bot.command(name="help")
async def HelpCommand(ctx):
    await ctx.send(embed = GetHelpCommand())

@bot.command(name="gettickets")
async def GetTickets(ctx, gamertag):
    await ctx.send(embed=queryTickets(gamertag))

@bot.command(name="ticketdetail")
async def TicketDetail(ctx, ticketNum):
    await ctx.send(embed = TicketDetailQuery(ticketNum))

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        await ctx.send("Command not found")
    print(error)

@bot.command(name="getprofile")
async def getprofile(ctx, gamertag):
    await ctx.send(embed = profileQuery(gamertag))

bot.run(discord_token)