from nextcord.ext import commands
import nextcord
from nextcord import Interaction, SlashOption
from nextcord.ext import commands
import requests
import utils.info as info

class Standings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name="standings", description="Shows the current standings", guild_ids=[int(info.testServerID), int(info.f1abeezID)])
    async def getStandings(self, interaction: Interaction, tier: str = SlashOption(name="tier", description="The tier to get the standings for", choices={"Tier 1": "1", "Tier 2": "2", "Tier 3": "3", "Tier 4": "4", "Tier M": "M", "Tier H": "H", "Team Standings": "team", "F2 - Tier 1": "f21", "F2 - Tier 2": "f22"})):
        await interaction.response.defer()
        try:
            if(tier == "1"):
                r = requests.get("https://api.figma.com/v1/images/d4sDj6FfYxdOszlQbdOhqu/?ids=2%3A16&format=png", headers={"X-Figma-Token": info.figmaToken})
                r = r.json()
                url = r["images"]["2:16"]
                e = nextcord.Embed(color=info.color) 
                e.set_image(url=url) 
                await interaction.send(embed=e)
            elif(tier == "2"):
                r = requests.get("https://api.figma.com/v1/images/d4sDj6FfYxdOszlQbdOhqu/?ids=406%3A667&format=png", headers={"X-Figma-Token": info.figmaToken})
                r = r.json()
                url = r["images"]["406:667"]
                e = nextcord.Embed(color=info.color) 
                e.set_image(url=url) 
                await interaction.send(embed=e)
            elif(tier == "3"):
                r = requests.get("https://api.figma.com/v1/images/d4sDj6FfYxdOszlQbdOhqu/?ids=4%3A265&format=png", headers={"X-Figma-Token": info.figmaToken})
                r = r.json()
                url = r["images"]["4:265"]
                e = nextcord.Embed(color=info.color) 
                e.set_image(url=url) 
                await interaction.send(embed=e)
            elif(tier == "4"):
                r = requests.get("https://api.figma.com/v1/images/d4sDj6FfYxdOszlQbdOhqu/?ids=406%3A999&format=png", headers={"X-Figma-Token": info.figmaToken})
                r = r.json()
                url = r["images"]["406:999"]
                e = nextcord.Embed(color=info.color) 
                e.set_image(url=url) 
                await interaction.send(embed=e)
            elif(tier == "M"):
                r = requests.get("https://api.figma.com/v1/images/d4sDj6FfYxdOszlQbdOhqu/?ids=406%3A1251&format=png", headers={"X-Figma-Token": info.figmaToken})
                r = r.json()
                url = r["images"]["406:1251"]
                e = nextcord.Embed(color=info.color) 
                e.set_image(url=url) 
                await interaction.send(embed=e)
            elif(tier == "H"):
                r = requests.get("https://api.figma.com/v1/images/d4sDj6FfYxdOszlQbdOhqu/?ids=436%3A2&format=png", headers={"X-Figma-Token": info.figmaToken})
                r = r.json()
                url = r["images"]["436:2"]
                e = nextcord.Embed(color=info.color) 
                e.set_image(url=url) 
                await interaction.send(embed=e)
            elif(tier == "team"):
                r = requests.get("https://api.figma.com/v1/images/d4sDj6FfYxdOszlQbdOhqu/?ids=16%3A1142&format=png", headers={"X-Figma-Token": info.figmaToken})
                r = r.json()
                url = r["images"]["16:1142"]
                e = nextcord.Embed(color=info.color) 
                e.set_image(url=url) 
                await interaction.send(embed=e)
            elif(tier == "f21"):
                r = requests.get("https://api.figma.com/v1/images/d4sDj6FfYxdOszlQbdOhqu/?ids=421%3A168&format=png", headers={"X-Figma-Token": info.figmaToken})
                r = r.json()
                url = r["images"]["421:168"]
                e = nextcord.Embed(color=info.color) 
                e.set_image(url=url) 
                await interaction.send(embed=e)
            elif(tier == "f22"):
                r = requests.get("https://api.figma.com/v1/images/d4sDj6FfYxdOszlQbdOhqu/?ids=2%3A16&format=png", headers={"X-Figma-Token": info.figmaToken})
                r = r.json()
                url = r["images"]["2:16"]
                e = nextcord.Embed(color=info.color) 
                e.set_image(url=url) 
                await interaction.send(embed=e)
        except KeyError:
            await interaction.send("There was an error while getting the standings. Please report this issue to the admins")
            print(KeyError)
        except Exception as e:
            print("standings:")
            print(e)

def setup(bot):
    bot.add_cog(Standings(bot))