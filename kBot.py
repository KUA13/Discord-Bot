import discord
from discord.ext import commands
import json


def run_bot():
    with open('config5.json', 'r') as conf:
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
    async def matchup(cmd, msg=None):
        if msg == None:
            target = str(cmd.message.author)
        else:
            target = msg
            target = find(target)
            target = target["discord_id"]
        for player in players:
            if target == player["discord_id"]:
                target_name = str(player["name"])
                opponent = str(player["schedule"][wk])
                if opponent == "Bye" or opponent == "Open":
                    await cmd.send(target_name + " has a bye this week")
                    return
                await cmd.send(target_name + "'s matchup for this week is: " + opponent)
                if player["is_user"][wk] == True:
                    for opp in players:
                        if opp["team"] == opponent:
                            await cmd.send(target_name + "'s opponent is: " + opp["name"])
                            psn = str(opp["psn"])
                            await cmd.send(opp["name"] + "'s PSN ID is: " + psn)
                else:
                    await cmd.send(target_name + " is playing a CPU")
                return
        await cmd.send("User not found")

    #Displays a given user's schedule. No specified user returns the author's schedule
    @bot.command()
    async def schedule(cmd, msg=None):
        target = ""
        if msg == None:
            author = cmd.message.author
            player = findID(str(author))
            if player == "user not found":
                await cmd.send(player)
                return player
            target = str(player["name"])
        else:
            target = msg
        player = find(target)
        if player == "user not found":
            await cmd.send(player)
            return
        schedule = target + "'s Schedule:" + "\n"
        for i in range(0, len(player["schedule"])):
            schedule += "Week " + str(i) + ": " + player["schedule"][i]
            if isUser(player["schedule"][i]):
                opp = findTeam(player["schedule"][i])
                schedule += " (" + opp["name"] + ")"
            schedule += "\n"
        await cmd.send(schedule)

    
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

    #Displays the isUser[] list for all users
    @bot.command()
    async def getAllUserLists(cmd):
        author = str(cmd.message.author)
        if author != "kua13":
            cmd.send("You cannot use this command")
            return
        output = ""
        counter = 0
        for player in players:
            output += player["name"] + ": "
            for opp in player["schedule"]:
                oppTeam = str(opp)
                if isUser(oppTeam) == True:
                    output += "true, "
                else:
                    output += "false, "
            output += "\n" + "\n"
            counter += 1
            if counter == 7:
                await cmd.send(output)
                output = ""
                counter = 0
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
    async def user_matches(cmd, msg=None):
        targetWK = wk
        if msg != None:
            targetWK = int(msg)
        users = []
        for player in players:
            if player["is_user"][targetWK] == True:
                users.append(player)
        output = "The user matches for week " + str(targetWK) +  " are:" + "\n" + "\n"
        # for user in users:
        #     print(user["name"] + ", " + str(type(user)))
        #     print(user)
        print()
        while len(users) > 0:
            user = users[0]
            output += user["name"] + " (" + user["team"] + ")" + " vs. "
            oppTeam = user["schedule"][targetWK] 
            opp = findTeam(oppTeam)
            output += opp["name"] + " (" + opp["team"] + ")" + "\n"
            users.remove(user)
            users.remove(opp)
        await cmd.send(output)

    #Displays all remaining user matches for the season
    @bot.command()
    async def rem_user_matches(cmd):
        author = str(cmd.author)
        if author != "kua13" and author != "aadegun":
            await cmd.send("You are not authorized to use this command")
            return
        wk_count = wk
        output = ""
        users = []
        sendCount = 0
        while(wk_count < 15):
            if sendCount == 5:
                output += "\n"
                await cmd.send(output)
                output = ""
                sendCount = 0
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
            sendCount += 1
            users.clear()
        await cmd.send(output)
            
    #Outputs the current week
    @bot.command()
    async def week(cmd):
        await cmd.send("It is currently week: " + str(wk))
                

    #Returns the player who plays as the given team
    def findTeam(team):
        for player in players:
            if player["team"] == team:
                return player
        return "team not found"

    #Returns the player with the given given name
    def find(user_name):
        for player in players:
            if player["name"].lower() == user_name.lower():
                return player
        return "user not found"
    
    #Returns the player with the given discord ID
    def findID(ID):
        for player in players:
            if player["discord_id"] == ID:
                return player
        return "user not found"
    
    #Returns true if the entered team is controlled by a user, false otherwise
    def isUser(team):
        for player in players:
            if team == player["team"]:
                return True
        return False

    def findTeam(team):
        for player in players:
            if team == player["team"]:
                return player
        return "Player not found"

    bot.run(token)



