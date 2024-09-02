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
        print("The current week is: " + str(week))

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

    #Displays the author's discord ID
    @bot.command()
    async def whoAmI(ctx):
        await ctx.send(f'You are {ctx.message.author}')

    @bot.command()
    async def testMsg(cmd, msg):
        await cmd.send(msg)
    
    @bot.command()
    async def getUserList(cmd, msg):
        author = str(cmd.message.author)
        if author != "kua13":
            cmd.send("You cannot use this command")
            return
        target = msg
        player = find(str(target))
        output = ""
        for opp in player["schedule"]:
            oppTeam = str(opp)
            if isUser(oppTeam) == True:
                output += "true, "
            else:
                output += "false, "
        await cmd.send(output)

    @bot.command()
    async def users(cmd):
        output = "The players who have user games this week are:" + "\n"
        for player in players:
            if player["is_user"][week] == True:
                output += player["name"] + "\n"
        await cmd.send(output)

    @bot.command()
    async def user_matches(cmd):
        users = []
        for player in players:
            if player["is_user"][week] == True:
                users.append(player)
        output = "The user matches for this week are:" + "\n" + "\n"
        while len(users) > 0:
            user = users[0]
            output += user["name"] + " (" + user["team"] + ")" + " vs. "
            oppTeam = user["schedule"][week] 
            opp = findTeam(oppTeam)
            output += opp["name"] + " (" + opp["team"] + ")" + "\n"
            users.remove(user)
            users.remove(opp)
        await cmd.send(output)
                
    def findTeam(team):
        for player in players:
            if player["team"] == team:
                return player
        return "team not found"

    def find(user_name):
        for player in players:
            if player["name"] == user_name:
                return player
        return "user not found"
    
    def isUser(team):
        for player in players:
            if team == player["team"]:
                return True
        return False

    bot.run(token)



