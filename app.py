import asyncio
import discord
from discord import client
from discord import message
from discord.colour import Color
from discord.ext import tasks, commands
from discord.ext.commands import CommandNotFound
from discord.ext.commands.core import check
import requests
import json
import os
import pymongo

discord_token = os.environ.get("discord_token")
token = os.environ.get("token")
incidentDatabaseURL = os.environ.get("incidentDatabaseURL")
profileDatabaseURL = os.environ.get("profileDatabaseURL")
incidentDatabaseId = os.environ.get("incidentDatabaseId")
appealsDatabaseURL = os.environ.get("appealsDatabaseURL")
appealsDatabaseId = os.environ.get("appealsDatabaseId")
mongoDBConnSTR = os.environ.get("mongoDBConnSTR")


    
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

def queryAppeals(gamertag):
  header = {"Authorization": token, "Notion-Version": "2021-05-13"}
  r = requests.post(appealsDatabaseURL, json = {
      "filter": {
  "or": [
    {
      "property": "Appealed By",
      "rich_text": {
        "contains": gamertag
      }
    },
    {
      "property": "GamerTag(s) involved",
      "rich_text": {
        "contains": gamertag
      }
    }
  ]
      },
  "sorts": [{ "property": "AP-Case Number", "direction": "ascending" }]}

    , headers=header).text
  

  embed = discord.Embed(title=f"Appeals where {gamertag} was involved", color=16236412)

  b = json.loads(r)
  if (len(b["results"]) == 0):
      embed.add_field(name="Error", value="Gamertag is incorrect, please try again.")
      return embed

  for i in range(len(b["results"])):
      try: 
          caseNumberAndStatus = f'{b["results"][i]["properties"]["AP-Case Number"]["title"][0]["text"]["content"]} - {b["results"][i]["properties"]["Status"]["select"]["name"]}'
      except IndexError:
          caseNumberAndStatus = "Case number hasn't been assigned yet (you cannot get this ticket with the bot until it has a case number)"
      except KeyError:
          caseNumberAndStatus = "The stewards haven't got to the appeal yet, please check back later"
      driversInvolved = (f'{b["results"][i]["properties"]["Appealed By"]["rich_text"][0]["text"]["content"]} vs {b["results"][i]["properties"]["GamerTag(s) involved"]["rich_text"][0]["text"]["content"]}\n')
      embed.add_field(name=caseNumberAndStatus, value=driversInvolved, inline=False)
  
  return embed  

def submitAppeal(caseNumber, evidence, gamertag, gamertagInvolved, reason, additionalInfo):
  url = "https://api.notion.com/v1/pages/"
  header = {"Authorization": token, "Notion-Version": "2021-05-13"}
  r = requests.post(url, headers=header, json={
  "parent": {
    "database_id": appealsDatabaseId
  },
  "properties": {
    "Case Number": {
      "rich_text": [
        {
          "text": {
            "content": caseNumber
          }
        }
      ]
    },
  "Status": {
    "select": {
      "name": "In Progress",
      "color": "pink"
    }
  },
  "Additional Evidence": {
    "rich_text": [
      {
        "text": {
          "content": evidence
        }
      }
    ]
  },
  "Appealed By": {
    "rich_text": [
      {
        "text": {
          "content": gamertag
        }
      }
    ]
  },
  "GamerTag(s) involved": {
    "rich_text": [
      {
        "text": {
          "content": gamertagInvolved
        }
      }
    ]
  },
  "Reason": {
    "rich_text": [
      {
        "text": {
          "content": reason
        }
      }
    ]
  },
  "Additional Info": {
    "rich_text": [
      {
        "text": {
          "content": additionalInfo
        }
      }
    ]
  }
}
}
)
  if(r.status_code == 200):
    return "Your appeal was successfully submitted!"
  else:
    return "There was an error submitting your appeal, please reach out to the admin team"


def GetHelpCommand():
    embed = discord.Embed(title="Help")
    embed.add_field(name=";gettickets <gamertag>", value="This command is useful when you don’t know the number of your ticket. The command lists all tickets you’ve been involved (whether you reported it or someone else reported you) and gives you the number of the ticket.", inline=False)
    embed.add_field(name=";getappeals <gamertag>", value="This command gets you a list of appeals you've been involeved in (whether you appealed or someone appealed against you) and gives you the number of the appeal and it's status.")
    embed.add_field(name=";ticketdetail <number of ticket>", value="This command gets you the details of ticket you provide. It lists the status, penalty that was awarded and who was involved.", inline=False)
    embed.add_field(name=";getprofile <gamertag>", value="This command gets you your profile from our profile database on the website. You can see how many penalty points you have or whether you have a quali or race ban as well as your team and tier. You can also see how many points you have scored in F1 or F2 tiers", inline=False)
    embed.add_field(name=";incidentreport", value="This command allows you to submit an incident from discord. Please read the messages carefully and reply correctly.", inline=False)
    embed.add_field(name=";submitappeal", value="This command allows you to submit an appeal to a decision that has been made by the stewards. Please use ;gettickets before you start submitting it to make sure you know the case number of the incident you want to appeal", inline=False)
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
intents.members = True
bot = commands.Bot(command_prefix=";", help_command=None, intents=intents)
bot.remove_command("help")


@bot.event
async def on_ready():
    print("We have logged in as {0.user}".format(bot))

@bot.command(name="help")
async def HelpCommand(ctx):
    await ctx.send(embed = GetHelpCommand())

@bot.command(name="gettickets")
async def GetTickets(ctx, *, arg):
    await ctx.send(embed=queryTickets(arg))

@bot.command(name="getappeals")
async def GetAppeals(ctx, *, arg):
  await ctx.send(embed = queryAppeals(arg))

@bot.command(name="ticketdetail")
async def TicketDetail(ctx, ticketNum):
    await ctx.send(embed = TicketDetailQuery(ticketNum))

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        await ctx.send("Command not found")
    print(error)

@bot.command(name="getprofile")
async def getprofile(ctx, *, arg):
    await ctx.send(embed = profileQuery(arg))

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
    logEmbed = discord.Embed(title="⚠️New Ticket has been reported!⚠️")
    logEmbed.add_field(name="Tier", value=tierOfIncident, inline=False)
    logEmbed.add_field(name="Drivers involved", value=f"{gamertagOfUser} vs {gamertagOfInvolevedDriver}", inline=False)
    channel = bot.get_channel(861939856481189908)
    await channel.send("<@&774702830816067634>")
    await channel.send(embed = logEmbed)
    await ctx.author.send(response)

@bot.command(name="submitappeal")
async def decisionappeal(ctx):
    def check(m):
        return m.author == ctx.author and m.guild is None
    
    await ctx.send(f"Please follow the bot to your DMs to submit your appeal <@{ctx.author.id}>")
    try:
        await ctx.author.send("What is the case number you want to appeal (use ;querytickets in the bot channel in the server if you need to get it)")
        caseNumber = await bot.wait_for("message", check=check, timeout=60.0)
        caseNumber = caseNumber.content
        await ctx.author.send("What is your gamertag?")
        gamertagOfUser = await bot.wait_for("message", check=check, timeout=60.0)
        gamertagOfUser = gamertagOfUser.content
        await ctx.author.send("Please state the reason for you appeal.")
        reason = await bot.wait_for("message", check=check, timeout=60.0)
        reason = reason.content
        await ctx.author.send("State any additional information to support your appeal (if you don't have any, reply with N/A)")
        additionalInfo = await bot.wait_for("message", check=check, timeout=60.0)
        additionalInfo = additionalInfo.content
        await ctx.author.send("Please provide addition video evidence to support your appeal (Only reply with links to gamerdvr or other services)")
        evidence = await bot.wait_for("message", check=check, timeout=60.0)
        evidence = evidence.content
        await ctx.author.send("What is the gamertag(s) of the driver(s) involved? (For penalties, reply with N/A)")
        gamertagOfInvolevedDriver = await bot.wait_for("message", check=check, timeout=60.0)
        gamertagOfInvolevedDriver = gamertagOfInvolevedDriver.content
    except asyncio.TimeoutError:
        await ctx.author.send("Unfortunately you took too long to reply (Limit is a minute per message). Please start a new incident if you want to proceed.")
    response = submitAppeal(caseNumber, evidence, gamertagOfUser, gamertagOfInvolevedDriver, reason, additionalInfo)
    logEmbed = discord.Embed(title="⚠️New Appeal has been submitted!⚠️")
    logEmbed.add_field(name="Case Number", value=caseNumber, inline=False)
    logEmbed.add_field(name="Drivers involved", value=f"{gamertagOfUser} vs {gamertagOfInvolevedDriver}", inline=False)
    channel = bot.get_channel(861939856481189908)
    await channel.send("<@&774702830816067634>")
    await channel.send(embed = logEmbed)
    await ctx.author.send(response)


@bot.command(name="lobbytier1")
@commands.has_any_role("Admin", "Moderator")
async def lobbyMSGtier1(ctx):
  await ctx.message.delete()
  await ctx.send("<@&795227294766727169>\n**Lobby is now open!**\nPlease join off <@805472151914283079>\nGamertag is - Playzz769\nPlease put a message in this chat if you need an invite.\nIf you have a qualifying ban, make sure to serve it!\nWhile waiting why not check out our website - F1ABEEZ.com")

@bot.command(name="lobbytier2")
@commands.has_any_role("Admin", "Moderator")
async def lobbyMSGtier2(ctx):
  await ctx.message.delete()
  await ctx.send("<@&795227317684928546>\n**Lobby is now open!**\nPlease join off <@434849746830622720>\nGamertag is - Chaviscool\nPlease put a message in this chat if you need an invite.\nIf you have a qualifying ban, make sure to serve it!\nWhile waiting why not check out our website - F1ABEEZ.com")

@bot.command(name="lobbytier3")
@commands.has_any_role("Admin", "Moderator")
async def lobbyMSGtier3(ctx):
  await ctx.message.delete()
  await ctx.send("<@&813703851349245965>\n**Lobby is now open!**\nPlease join off <@401204069890523137>\nGamertag is - OwningLeMoNz\nPlease put a message in this chat if you need an invite.\nIf you have a qualifying ban, make sure to serve it!\nWhile waiting why not check out our website - F1ABEEZ.com")

@bot.command(name="lobbytier4")
@commands.has_any_role("Admin", "Moderator")
async def lobbyMSGtier4(ctx):
  await ctx.message.delete()
  await ctx.send("<@&840694396990521364>\n**Lobby is now open!**\nPlease join off <@637377176517345311>\nGamertag is - qpef\nPlease put a message in this chat if you need an invite.\nIf you have a qualifying ban, make sure to serve it!\nWhile waiting why not check out our website - F1ABEEZ.com")

@bot.command(name="lobbyf2")
@commands.has_any_role("Admin", "Moderator")
async def lobbyMSGf2(ctx):
  await ctx.message.delete()
  await ctx.send("**Lobby is now open!**\nPlease join off <@499568806469959691>\nGamertag is - MrJSmithy\nPlease put a message in this chat if you need an invite.\nIf you have a qualifying ban, make sure to serve it!\nWhile waiting why not check out our website - F1ABEEZ.com")

@bot.command(name="readytier1")
@commands.has_any_role("Admin", "Moderator")
async def readyMSGtier1(ctx):
  await ctx.message.delete()
  await ctx.send("<@&795227294766727169>\n**Ready up**\n\nRemember after qualifying do not ready up until you recieve the message in this chat or you will get a post race 3 place grid penalty.")

@bot.command(name="readytier2")
@commands.has_any_role("Admin", "Moderator")
async def readyMSGtier2(ctx):
  await ctx.message.delete()
  await ctx.send("<@&795227317684928546>\n**Ready up**\n\nRemember after qualifying do not ready up until you recieve the message in this chat or you will get a post race 3 place grid penalty.")

@bot.command(name="readytier3")
@commands.has_any_role("Admin", "Moderator")
async def readyMSGtier3(ctx):
  await ctx.message.delete()
  await ctx.send("<@&813703851349245965>\n**Ready up**\n\nRemember after qualifying do not ready up until you recieve the message in this chat or you will get a post race 3 place grid penalty.")

@bot.command(name="readytier4")
@commands.has_any_role("Admin", "Moderator")
async def readyMSGtier4(ctx):
  await ctx.message.delete()
  await ctx.send("<@&840694396990521364>\n**Ready up**\n\nRemember after qualifying do not ready up until you recieve the message in this chat or you will get a post race 3 place grid penalty.")

@bot.command(name="readyf2")
@commands.has_any_role("Admin", "Moderator")
async def readyMSGf2(ctx):
  await ctx.message.delete()
  await ctx.send("**Ready up**\n\nRemember after qualifying do not ready up until you recieve the message in this chat or you will get a post race 3 place grid penalty.")

@bot.command(name="racetier1")
@commands.has_any_role("Admin", "Moderator")
async def raceMSGtier1(ctx):
  await ctx.message.delete()
  await ctx.send("<@&795227294766727169>\n**Ready up for the race start please!**\n\nGood luck out there everyone, see you after the race")

@bot.command(name="racetier2")
@commands.has_any_role("Admin", "Moderator")
async def raceMSGtier2(ctx):
  await ctx.message.delete()
  await ctx.send("<@&795227317684928546>\n**Ready up for the race start please!**\n\nGood luck out there everyone, see you after the race")

@bot.command(name="racetier3")
@commands.has_any_role("Admin", "Moderator")
async def raceMSGtier3(ctx):
  await ctx.message.delete()
  await ctx.send("<@&813703851349245965>\n**Ready up for the race start please!**\n\nGood luck out there everyone, see you after the race")

@bot.command(name="racetier4")
@commands.has_any_role("Admin", "Moderator")
async def raceMSGtier4(ctx):
  await ctx.message.delete()
  await ctx.send("<@&840694396990521364>\n**Ready up for the race start please!**\n\nGood luck out there everyone, see you after the race")

@bot.command(name="racef2")
@commands.has_any_role("Admin", "Moderator")
async def raceMSGf2(ctx):
  await ctx.message.delete()
  await ctx.send("Ready up for the race start please!**\n\nGood luck out there everyone, see you after the race")

@bot.command(name="academymessage")
@commands.has_any_role("Admin", "Moderator", "Trialist Manager")
async def academyMSG(ctx):
  await ctx.message.delete()
  msg =  await ctx.send("<@&774740889557270539>\n**TRIAL RACE BRIEFING:**\nWelcome to the F1ABEEZ trial race! I would just like to run through what is expected of you from your trial:\n- Please drive clean - we are a clean racing league, show respect to your fellow drivers! dirty driving will not be tolerated\n- Drive fast! It's still a race after all, we would like to see a true reflection of your pace\n- Do not use medium tyres in Qualifying for this trial race, as this lets us compare your quali pace!\n- Have fun! That's what we're all here for\n\nThe format is short qualifying, 25% race\nAfter the race is completed, <@401204069890523137> will DM you individually with our decision\nPlease react with a thumbs up once you have read this, good luck!")
  await msg.add_reaction("👍")

@bot.command(name="warn")
@commands.has_any_role("Admin")
async def warnUser(ctx,user, *, reason=None):
  if (reason is None):
    await ctx.send("The reason for the warning is missing")
    return
  await ctx.message.delete()
  member = ctx.message.mentions[0]
  membername = ctx.message.mentions[0].name
  memberid = ctx.message.mentions[0].id
  embed = discord.Embed(title="A warning has been issued!", color=16236412)
  embed.add_field(name="User", value=membername, inline=False)
  embed.add_field(name="Warned by", value=ctx.author.name, inline=False)
  embed.add_field(name="Reason", value=reason, inline=False)
  client = pymongo.MongoClient(mongoDBConnSTR)
  mydb = client["warningDatabase"]
  mycol = mydb["WarningCollection"]
  insert = {"discordid": memberid, "discordname": membername, "warnedby": ctx.author.name, "reason": reason}
  mycol.insert_one(insert)
  query = {"discordid": memberid}
  warningCount = mycol.count_documents(query)
  if (warningCount == 1):
    embed.add_field(name="Number of Warnings", value=f"This is {membername}'s first and last warning.")
    await ctx.send(embed=embed)
  elif(warningCount == 2):
    embed = discord.Embed(title="A ban has been issued!", color=16236412)
    embed.add_field(name="User", value=membername, inline=False)
    embed.add_field(name="Reason", value=reason, inline=False)
    embed.add_field(name="Warnings", value="The user had two warnings.", inline=False)
    mycol.delete_many(query)
    channel = bot.get_channel(853679513406013460)
    await channel.send(embed = embed)
    await member.ban(reason = reason)
    await ctx.send(embed = embed)

@bot.command(name="warnings")
@commands.has_any_role("Admin")
async def GetWarnings(ctx, user=None):
  if(user is None):
    await ctx.send("The user wasn't mentioned")
  client = pymongo.MongoClient(mongoDBConnSTR)
  mydb = client["warningDatabase"]
  mycol = mydb["WarningCollection"]
  try:
    memberid = ctx.message.mentions[0].id
  except IndexError:
    memberid = int(user)
  query = {"discordid": memberid}
  embed = discord.Embed(title=f"Warnings for user", color=16236412)
  warningCount = mycol.count_documents(query)
  if (warningCount == 0):
    embed.add_field(name="Number of Warnings", value=f"<@{memberid}> has no warnings", inline=False)
  elif (warningCount == 1):
    embed.add_field(name="Number of Warnings", value=f"<@{memberid}> has one warning", inline=False)
  await ctx.send(embed = embed)

@bot.command(name="ban")
@commands.has_any_role("Admin")
async def ban(ctx, user=None, *, reason=None):
  if(user is None):
    await ctx.send("You didn't mention the user")
    return
  if(reason is None):
    await ctx.send("You didn't provide a reason")
    return

  try: 
    member = ctx.message.mentions[0]
    membername = ctx.message.mentions[0].name
  except IndexError:
    print(user)
    member = await ctx.guild.fetch_member(int(user))
    print(member)
    membername = member.name

  embed = discord.Embed(title="A Ban has been issued", color=16236412)
  embed.add_field(name="User", value=membername, inline=False)
  embed.add_field(name="Reason", value=reason, inline=False)
  channel = bot.get_channel(853679513406013460)
  await channel.send(embed = embed)
  await member.ban(reason = reason)
  await ctx.send(embed = embed)   
    
@bot.event
async def on_member_join(member):
  role = discord.utils.get(member.guild.roles, name="Academy Driver")
  await member.add_roles(role)
  channel = bot.get_channel(838841316519313408)
  await channel.send(f"**Welcome <@{member.id}>**\n\nPlease use this chat if you have any questions and someone will be on hand.\n\nAll the information you need is on <#865379267977412618>")

@bot.event
async def on_member_remove(member):
  memberName = member.name
  channel = bot.get_channel(774605933661257729)
  await channel.send(f"**{memberName}** has left the server.")



bot.run(discord_token)