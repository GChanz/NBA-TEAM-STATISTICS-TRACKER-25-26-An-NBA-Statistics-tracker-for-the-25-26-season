from curl_cffi import requests as cr
from nba_api.stats.library.http import NBAStatsHTTP
session = cr.Session(impersonate="chrome120")
session.get("https://www.nba.com/stats/", timeout=20)  # warmup
NBAStatsHTTP.get_session = lambda self: session
from nba_api.stats.static import teams
from nba_api.stats.endpoints import leaguedashteamstats
from flask import Flask,jsonify,request,render_template
from flask_cors import CORS
import re
app = Flask(__name__)
CORS(app, origins=["http://127.0.0.1:5500"])


def getTeamBaseStats(id):  
   finalstring =""
   data = leaguedashteamstats.LeagueDashTeamStats(
                          team_id_nullable=id,
                          measure_type_detailed_defense="Base",
                          per_mode_detailed="PerGame",
                          season="2025-26",
                          season_type_all_star="Regular Season")
   
   data = data.get_data_frames()[0]
   teamName = str(data["TEAM_NAME"].values[0])
   gamesPlayed = int(data["GP"].values[0])
   wins = int(data["W"].values[0])
   losses = int(data["L"].values[0])
   turnovers = float(data["TOV"].values[0])
   points = int(data["PTS"].values[0])
   fieldGoalsMade = int(data["FGM"].values[0])
   fieldGoalsAttempted = int(data["FGA"].values[0])
   

   
    
   finalstring = teamName + '\n' \
    + 'Games Played: ' + str(gamesPlayed) + '\n' \
    + 'Wins: ' + str(wins) + '\n' \
    + 'Losses: ' + str(losses) + '\n' \
    + 'Average Points Per Game: ' + str(points) + '\n' \
    + 'Average Field Goal Percentage: ' + str(round((fieldGoalsMade/fieldGoalsAttempted) * 100)) + '%' '\n' \
    + 'Turnovers Per Game: ' + str(turnovers)
  
   return finalstring
                

def getTeamData(TeamName):
    team =  teams.find_teams_by_full_name(TeamName)
    print(team)
    team = team[0]

    name = str(team["full_name"])
    state = str(team["state"])
    yearfounded = str(team["year_founded"])
    id = int(team["id"])
    
    stats = (getTeamBaseStats(id))
    print (stats)

    return  name + '\n' \
          + state + '\n' \
          + yearfounded + '\n' \
          + stats


@app.route("/api/TeamData")
def getdata():
    Tname = request.args.get("tag")
    
    TeamData = getTeamData(Tname)
    return jsonify({
        "value" : TeamData
    })

@app.route("/api/StatComparison")
def getComparisonData():
    Teamlist = request.args.get("teams")
    Filter = request.args.get("Filter")
    TeamData = generateStatsByFilter(Teamlist,Filter)
    
    
    return jsonify({
      "value" : TeamData
    })


def generateStatsByFilter(teamlist,filter):
   # teamlist will come as a string first so they need to be split
    #teamlist = 
    #filter = ""
   # print(filter)
    #print(teamlist)
    
    teamlist = teamlist.split(",")
    Namelist = teamlist
    
    sFilter = str(filter) + ":"
    
    reg = sFilter + r'(\s{1}\d+)'
    regex = re.compile(reg)
    
    
    
    for x in range (0, len(teamlist)):
        print ("1")
        print(teamlist[x])
        data = getTeamData(teamlist[x])
        print(data)
        
        result = regex.search(data)
        print (result)
        teamlist[x] = Namelist[x] +":"+ result.group(1)

    
    return str(teamlist)
        # Get teamdata
        # Remove data that doesn't match the filter



               



if __name__ == "__main__":
   app.run(host="127.0.0.1", port=5000, debug=True)

 



