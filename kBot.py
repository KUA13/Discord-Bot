import discord
from discord.ext import commands
import json


def run_bot():
    with open('config.json', 'r') as conf:
        data = json.load(conf)
        token = data["TOKEN"]
        global players
        players = data["players"]
        global week
        week = data["week"]


    client = discord.Client(intents=discord.Intents.default())
    intents = discord.Intents.default()
    intents.message_content = True
    bot = commands.Bot(command_prefix="!", intents=intents)

    @bot.event
    async def on_ready():
        print(f'{bot.user} is online')

    #Displays the author's entire weekly schedule for the regular season
    @bot.command()
    async def myschedule(msg):
        author = str(msg.message.author)
        for player in players:
            if author == player["discord_id"]:
                name = player["name"]
                await msg.send(name + "'s schedule")
                schedule = ""
                for i in range(0, len(player["schedule"])):
                    schedule += "Week " + str(i) + ": " + player["schedule"][i] + "\n"
                await msg.send(schedule)
                return
        await msg.send("User not found")
    
    #Displays this week's matchup for the author
    @bot.command()
    async def matchup(msg):
        author = str(msg.message.author)
        for player in players:
            if author == player["discord_id"]:
                author_name = str(player["name"])
                opponent = str(player["schedule"][week])
                if opponent == "Bye":
                    await msg.send(author_name + " you have a bye this week")
                    return
                await msg.send(author_name + " your matchup for this week is: " + opponent)
                if player["is_user"][week] == True:
                    for opp in players:
                        if opp["team"] == opponent:
                            await msg.send("Your opponent is: " + opp["name"])
                            psn = str(opp["psn"])
                            await msg.send("Their PSN ID is: " + psn)
                else:
                    await msg.send("You are playing a CPU")
                return
        await msg.send("User not found")

    #Advances the week
    # @bot.command()
    # async def advance(msg):
    #     author = str(msg.message.author)
    #     global week
    #     await msg.send(week)
    #     if author == "kua13":
    #         global week
    #         week += 1
    #         await msg.send("The week has been adavanced")
    #         await msg.send("We are now on week " + week)

    #Displays the author's discord ID
    @bot.command()
    async def whoAmI(ctx):
        await ctx.send(f'You are {ctx.message.author}')
        

    bot.run(token)



