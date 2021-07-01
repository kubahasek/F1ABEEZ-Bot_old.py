import asyncio
import discord
from discord import client
from discord import message
from discord.ext import tasks, commands
from discord.ext.commands import CommandNotFound
from discord.ext.commands.core import check
import requests
import json
import os

discord_token = os.environ.get("discord_token")
token = os.environ.get("token")
incidentDatabaseURL = os.environ.get("incidentDatabaseURL")
profileDatabaseURL = os.environ.get("profileDatabaseURL")
incidentDatabaseId = os.environ.get("incidentDatabaseId")


    
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
        try: 
            caseNumber = b["results"][i]["properties"]["Case Number"]["title"][0]["plain_text"]
        except IndexError:
            caseNumber = "Case number hasn't been assigned yet (you cannot get this ticket with the bot until it has a case number)"
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
    embed.add_field(name=";gettickets <gamertag>", value="This command is useful when you don’t know the number of your ticket. The command lists all tickets you’ve been involved (whether you reported it or someone else reported you) and gives you the number of the ticket.", inline=False)
    embed.add_field(name=";ticketdetail <number of ticket>", value="This command gets you the details of ticket you provide. It lists the status, penalty that was awarded and who was involved.", inline=False)
    embed.add_field(name=";getprofile <gamertag>", value="This command gets you your profile from our profile database on the website. You can see how many penalty points you have or whether you have a quali or race ban as well as your team and tier. You can also see how many points you have scored in F1 or F2 tiers", inline=False)
    embed.add_field(name=";incidentreport", value="This command allows you to submit an incident from discord. Please read the messages carefully and reply correctly.", inline=False)
    return embed

def submitAnIncident(gamertag, lap, description, tier, evidence, driverInvolved):
    url = "https://api.notion.com/v1/pages/"
    header = header = {"Authorization": token, "Notion-Version": "2021-05-13"}
    r = requests.post(url, headers=header, json={
  "parent": {
    "database_id": incidentDatabaseId
  },
  "properties": {
    "Description": {
      "rich_text": [
        {
          "text": {
            "content": description
          }
        }
      ]
    },
    "Status": {
      "select": {
        "name": "In Progress",
        "color": "red"
      }
    },
    "Tier/Division": {
      "select": {
        "name": tier
      }
    },
    "Video Evidence (other video sources are allowed)": {
      "rich_text": [
        {
          "text": {
            "content": evidence
          }
        }
      ]
    },
    "Time Reported": {
      "created_time": "2021-06-14T15:30:00.000Z"
    },
    "Lap of incident/penalty": {
      "number": lap
    },
    "Reported By": {
      "rich_text": [
        {
          "text": {
            "content": gamertag
          }
        }
      ]
    },
    "GamerTag(s) of Driver(s) involved incident (N/A for penalties)": {
      "rich_text": [
        {
          "text": {
            "content": driverInvolved
          }
        }
      ]
    }
  }
}
)
    if(r.status_code == 200):
        return "Your ticket was successfully submitted!"
    else:
        return "There was an error submitting your ticket, please reach out to the admin team"

intents = discord.Intents.default()
intents.reactions = True
bot = commands.Bot(command_prefix=";", help_command=None, intents=intents)
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

@bot.command(name="incidentreport")
async def incidentreport(ctx):
    def check(m):
        return m.author == ctx.author and m.guild is None 

    def checkRaw(u):
      return u.user_id == ctx.author.id and u.guild_id is None
    
    await ctx.send(f"Please follow the bot to your DMs to report your incident <@{ctx.author.id}>")
    try:
        await ctx.author.send("What is your gamertag?")
        gamertagOfUser = await bot.wait_for("message", check=check, timeout=60.0)
        gamertagOfUser = gamertagOfUser.content
        await ctx.author.send("Please describe your incident.")
        description = await bot.wait_for("message", check=check, timeout=60.0)
        description = description.content
        tierOfIncidentMSG =  await ctx.author.send("What is the tier or division this incident/penalty occured in? \n1️⃣ = F1 - Tier 1\n2️⃣ = F1 - Tier 2\n3️⃣ = F1 - Tier 3\n4️⃣ = F1 - Tier 4\n5️⃣ = F2\nPlease react with the corresponding tier")
        await tierOfIncidentMSG.add_reaction("1️⃣")
        await tierOfIncidentMSG.add_reaction("2️⃣")
        await tierOfIncidentMSG.add_reaction("3️⃣")
        await tierOfIncidentMSG.add_reaction("4️⃣")
        await tierOfIncidentMSG.add_reaction("5️⃣")
        tierOfIncidentReaction = await bot.wait_for("raw_reaction_add", check=checkRaw, timeout=60.0)
        if(str(tierOfIncidentReaction.emoji) == "1️⃣"):
          tierOfIncident = "F1 - Tier 1"
          await ctx.author.send("You chose "+tierOfIncident)
        elif(str(tierOfIncidentReaction.emoji) == "2️⃣"):
          tierOfIncident = "F1 - Tier 2"
          await ctx.author.send("You chose "+tierOfIncident)
        elif(str(tierOfIncidentReaction.emoji) == "3️⃣"):
          tierOfIncident = "F1 - Tier 3"
          await ctx.author.send("You chose "+tierOfIncident)
        elif(str(tierOfIncidentReaction.emoji) == "4️⃣"):
          tierOfIncident = "F1 - Tier 4"
          await ctx.author.send("You chose "+tierOfIncident)
        elif(str(tierOfIncidentReaction.emoji) == "5️⃣"):
          tierOfIncident = "F2"
          await ctx.author.send("You chose "+tierOfIncident)
        await ctx.author.send("Please provide video evidence (Only reply with links to gamerdvr or other services)")
        evidence = await bot.wait_for("message", check=check, timeout=60.0)
        evidence = evidence.content
        incorrect = True
        while(incorrect == True):
            await ctx.author.send("What lap did this incident/penalty occur on?")
            lapOfIncident = await bot.wait_for("message", check=check, timeout=60.0)
            try:
                lapOfIncident = int(lapOfIncident.content)
                incorrect = False
            except ValueError:
                await ctx.author.send("The content you entered wasn't a number, please enter a number")
                incorrect = True
        await ctx.author.send("What is the gamertag(s) of the driver(s) involved? (For penalties, reply with N/A)")
        gamertagOfInvolevedDriver = await bot.wait_for("message", check=check, timeout=60.0)
        gamertagOfInvolevedDriver = gamertagOfInvolevedDriver.content
    except asyncio.TimeoutError:
        await ctx.author.send("Unfortunately you took too long to reply (Limit is a minute per message). Please start a new incident if you want to proceed.")
    response = submitAnIncident(gamertagOfUser, lapOfIncident, description, tierOfIncident, evidence, gamertagOfInvolevedDriver)
    await ctx.author.send(response)


bot.run(discord_token)