import json

with open("config5.json", "r") as conf:
    data = json.load(conf)
with open("raw.json", "r") as raw:
    raw_schedules = json.load(raw)


def isUser(team):
    for player in data["players"]:
        if team == player["team"]:
            return True
    return False

def clear_data():
    for player in data['players']:
        player["schedule"] = []
        player["is_user"] = []
        player["results"] = []


def update_schedules():
    for player in data["players"]:
        name = player["name"]
        player["schedule"] = raw_schedules[name]
        
def update_opps():
    for player in data["players"]:
        opps = []
        for opp in player["schedule"]:
            oppTeam = str(opp)
            if isUser(oppTeam) == True:
                opps.append(True)
            else:
                opps.append(False)
        player["is_user"] = opps

def write_data():
    with open('config5.json', 'w') as conf:
        json.dump(data, conf)


loop = True
while loop == True:
    val = input("Enter your command: ")
    if val == "quit":
        loop = False
    elif val == "write":
        write_data()
        print("DATA WRITTEN TO FILE")
    elif val == "clear data":
        clear_data()
        print("DATA CLEARED")
    elif val == "update schedules":
        update_schedules()
        print("SCHEDULES UPDATED")
    elif val == "update opps":
        update_opps()
        print("OPPS UPDATED")
    elif val == "troubleshoot":
        week = input("Enter a week: ")
        for player in data["players"]:
            print("Name: " + player["name"] + ", Opp: " + "'" + player["schedule"][int(week)] + "'" + ", " + str(player["is_user"][int(week)]))
    elif val == "teams":
        for player in data["players"]:
            print("'" + player["team"] + "'")
    else:
        print("INVALID COMMAND")

    


