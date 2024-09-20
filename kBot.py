import discord
from discord.ext import commands
import json


def run_bot():
    with open('config.json', 'r') as conf:
        data = json.load(conf)
        token = data["TOKEN"]
        global players
        players = data["players"]
        global wk
        wk = data["week"]

    # client = discord.Client(intents=discord.Intents.default())
    intents = discord.Intents.default()
    intents.message_content = True
    bot = commands.Bot(command_prefix="!", intents=intents)

    @bot.event
    async def on_ready():
        print(f'{bot.user} is online')
        print("The current week is: " + str(wk))

    #Displays the author's entire weekly schedule for the regular season
    @bot.command()
    async def myschedule(msg):
        author = str(msg.message.author)
        for player in players:
            if author == player["discord_id"]:
                name = player["name"]
                await msg.send(name + "'s Schedule:")
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
                opponent = str(player["schedule"][wk])
                if opponent == "Bye":
                    await msg.send(author_name + " you have a bye this week")
                    return
                await msg.send(author_name + " your matchup for this week is: " + opponent)
                if opponent == "Georgia":
                    await msg.send("This team's coach, Yoseph The Shameful, has resigned from the league. You will be playing against a CPU instead.")
                    return
                if player["is_user"][wk] == True:
                    for opp in players:
                        if opp["team"] == opponent:
                            await msg.send("Your opponent is: " + opp["name"])
                            psn = str(opp["psn"])
                            await msg.send("Their PSN ID is: " + psn)
                else:
                    await msg.send("You are playing a CPU")
                return
        await msg.send("User not found")

    #Displays a given user's schedule. No specified user returns the author's schedule
    @bot.command()
    async def schedule(cmd, msg=None):
        target = ""
        if msg == None:
            author = cmd.message.author
            player = findID(str(author))
            target = str(player["name"])
        else:
            target = msg
        player = find(target)
        if player == "user not found":
            await cmd.send(player)
            return
        schedule = target + "'s Schedule:" + "\n"
        for i in range(0, len(player["schedule"])):
            schedule += "Week " + str(i) + ": " + player["schedule"][i] + "\n"
        await cmd.send(schedule)


    #Displays the author's discord ID
    @bot.command()
    async def whoAmI(ctx):
        await ctx.send(f'You are {ctx.message.author}')

    
    #Displays the isUser[] for the given user
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

    #Displays the users who have user matches this week
    @bot.command()
    async def users(cmd):
        output = "The players who have user games this week are:" + "\n"
        for player in players:
            if player["is_user"][wk] == True:
                output += player["name"] + "\n"
        await cmd.send(output)

    #Displays the user matches for the current week
    @bot.command()
    async def user_matches(cmd):
        users = []
        for player in players:
            if player["is_user"][wk] == True:
                users.append(player)
        output = "The user matches for this week are:" + "\n" + "\n"
        while len(users) > 0:
            user = users[0]
            output += user["name"] + " (" + user["team"] + ")" + " vs. "
            oppTeam = user["schedule"][wk] 
            opp = findTeam(oppTeam)
            output += opp["name"] + " (" + opp["team"] + ")" + "\n"
            users.remove(user)
            users.remove(opp)
        await cmd.send(output)

    #Displays all remaining user matches for the season
    @bot.command()
    async def rem_user_matches(cmd):
        wk_count = wk
        output = ""
        users = []
        while(wk_count < 15):
            print(wk_count)
            output += "The user matches for week " + str(wk_count) + " are: " + "\n"
            for player in players:
                if player["is_user"][wk_count] == True:
                    users.append(player)
            while len(users) > 0:
                user = users[0]
                output += user["name"] + " (" + user["team"] + ")" + " vs. "
                oppTeam = user["schedule"][wk_count] 
                opp = findTeam(oppTeam)
                output += opp["name"] + " (" + opp["team"] + ")" + "\n"
                users.remove(user)
                users.remove(opp)
            output += "\n"
            wk_count += 1
            users.clear()
        await cmd.send(output)
            


    @bot.command()
    async def week(cmd):
        await cmd.send("It is currently week: " + str(wk))
                
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
    
    def findID(ID):
        for player in players:
            if player["discord_id"] == ID:
                return player
        return "user not found"
    
    def isUser(team):
        for player in players:
            if team == player["team"]:
                return True
        return False

    bot.run(token)



