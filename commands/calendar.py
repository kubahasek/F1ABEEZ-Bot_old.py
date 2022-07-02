from nextcord.ext import commands
import nextcord
from nextcord import Interaction, Member, SlashOption
import utils.info as info
import requests

class Calendar(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name="calendar", description="Shows the current calendar", guild_ids=[int(info.testServerID), int(info.f1abeezID), int(info.f2abeezID)])
    async def getCalendar(self, interaction):
        await interaction.response.defer()
        if(int(info.f1abeezID) == interaction.guild.id):
            try:
                r = requests.get("https://api.figma.com/v1/images/8mL0mwOKyIUcoLG3goL7wk/?ids=102%3A367&format=png", headers={"X-Figma-Token": info.figmaToken})
                r = r.json()
                img = r["images"]["102:367"]
                embed1 = nextcord.Embed(color=info.color) 
                embed1.set_image(url=img) 
                await interaction.send(embed=embed1)
            except Exception as e:
                await interaction.send(f"There was an error getting the calendar, please report this issue to the admins.")
                print("calendar:")
                print(e)
        elif(int(info.f2abeezID) == interaction.guild.id):
            try:
                r = requests.get("https://api.figma.com/v1/images/8mL0mwOKyIUcoLG3goL7wk/?ids=125%3A2&format=png", headers={"X-Figma-Token": info.figmaToken})
                r = r.json()
                img = r["images"]["125:2"]
                embed2 = nextcord.Embed(color=info.color) 
                embed2.set_image(url=img) 
                await interaction.send(embed=embed2)
            except Exception as e:
                await interaction.send(f"There was an error getting the calendar, please report this issue to the admins.")
                print("calendar:")
                print(e)

def setup(bot):
    bot.add_cog(Calendar(bot))