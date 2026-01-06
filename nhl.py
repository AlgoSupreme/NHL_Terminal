from nhlpy import NHLClient
import nhl_team_list as TCL
import nhl_r_team_list as RTCL
import os

class NHL_Term():

    def __init__(self):

        # Let the user know that something is happening
        # Goddamn does the client take a while
        print("LOADING NHL TERM...")

        self.season = "20252026"

        self.command = 0

        # Create client which takes forever to load
        self.client = NHLClient()

        # Placeholder for later usage
        self.teams = {}
        self.teams_goalie = {}

        # Get current standings
        #self.standings = self.client.standings.league_standings()

        # Get today's games
        self.games = self.client.schedule.daily_schedule()

        for team in TCL.TeamThreeCodes:
            # Get all teams and their stats
            self.teams[(TCL.TeamThreeCodes[team][1])] = (
                self.client.edge.team_detail(team_id=(TCL.TeamThreeCodes[team][1]), season=self.season)
                )
            

        #Get goalie information
        self.teams_goalie = self.client.stats.goalie_stats_summary(
                start_season=self.season,
                end_season=self.season,
                limit=90
                )

        

        while not self.command == "99":
            os.system('cls' if os.name == 'nt' else 'clear')
            print("-----Welcome to the NHL TERM-----")
            print("\n\n")
            print("Please type in the choice you would like to access:")
            print("\n")
            print("1. Today's Games    2. Team Stats")
            print("3. Player Stats     4. Other")
            print("99. EXIT")
            self.command = input("Enter a choice: ")
            os.system('cls' if os.name == 'nt' else 'clear')
            match self.command:
                case "1":
                    self.daily_games(self.teams, self.games)
                case "2":
                    self.team_stats(self.teams)
                case "3":
                    self.player_stats(self.teams)
                case "4":
                    pass
                case "99":
                    quit()
                case _:           
                    print("Incorrect choice")

    def daily_games(self, teams, games):
        count = 0
        for team in range(0, len(games)-1):
            
            print(f"GAME {team+1} OF {len(games)-1}\n") 
            print("--------------------------------------------------------")
            print("--------------------------------------------------------")

            #Away Team Calcs
            away_team_code = games["games"][count]["awayTeam"]["abbrev"]
            awaySOG=teams[TCL.TeamThreeCodes[away_team_code][1]]["sogSummary"][0]["shots"]
            awayGoals=teams[TCL.TeamThreeCodes[away_team_code][1]]["sogSummary"][0]["goals"]
            awayWins=teams[TCL.TeamThreeCodes[away_team_code][1]]["team"]["wins"]
            awayLoss=teams[TCL.TeamThreeCodes[away_team_code][1]]["team"]["losses"]
            awayOtLosses=teams[TCL.TeamThreeCodes[away_team_code][1]]["team"]["otLosses"]
            awayGamesPlayed=teams[TCL.TeamThreeCodes[away_team_code][1]]["team"]["gamesPlayed"]
            awayPoints=teams[TCL.TeamThreeCodes[away_team_code][1]]["team"]["points"]
            awaySavePctg = 0

            #Home Team Calcs
            home_team_code = games["games"][count]["homeTeam"]["abbrev"]
            homeSOG=teams[TCL.TeamThreeCodes[home_team_code][1]]["sogSummary"][0]["shots"]
            homeGoals=teams[TCL.TeamThreeCodes[home_team_code][1]]["sogSummary"][0]["goals"]
            homeWins=teams[TCL.TeamThreeCodes[home_team_code][1]]["team"]["wins"]
            homeLoss=teams[TCL.TeamThreeCodes[home_team_code][1]]["team"]["losses"]
            homeOtLosses=teams[TCL.TeamThreeCodes[home_team_code][1]]["team"]["otLosses"]
            homeGamesPlayed=teams[TCL.TeamThreeCodes[home_team_code][1]]["team"]["gamesPlayed"]
            homePoints=teams[TCL.TeamThreeCodes[home_team_code][1]]["team"]["points"]
            homeSavePctg = 0

            homeCounter = 0
            awayCounter = 0

            print("GOALIES NOT INCLUDED:")
            for i in range(0, len(self.teams_goalie)):
                
                if self.teams_goalie[i]["teamAbbrevs"] == home_team_code:
                    if self.teams_goalie[i]["saves"] > 100:    
                        homeSavePctg += self.teams_goalie[i]["savePct"]
                        homeCounter += 1
                    else:
                        print(self.teams_goalie[i]["goalieFullName"])
                        print(f"Not included because saves are: {self.teams_goalie[i]["saves"]}")
                elif self.teams_goalie[i]["teamAbbrevs"] == away_team_code:
                    if self.teams_goalie[i]["saves"] > 100:    
                        awaySavePctg += self.teams_goalie[i]["savePct"]
                        awayCounter += 1
                    else:
                        print(self.teams_goalie[i]["goalieFullName"])
                        print(f"Not included because saves are: {self.teams_goalie[i]["saves"]}")
                
            print("--------------------------------------------------------")    
            homeSavePctg = homeSavePctg/homeCounter
            awaySavePctg = awaySavePctg/awayCounter
            

            if homeSavePctg == 0 or awaySavePctg == 0:
                print(f"ERROR NO SAVE FOUND FOR TEAM {home_team_code if homeSavePctg == 0 else away_team_code}")

            #Begin of fancy math magic
            sogDenom = homeSOG**2.15 + awaySOG**2.15
            goalDenom = homeGoals**2.15 + awayGoals**2.15

            # Get the calculations with the magic sauce
            # Probability is weighted with a double Pythagorean
            # Combines Corsi with a General goal average
            home_prob = ((homeSOG**2.15)/(sogDenom) * ( homeGoals**2.15 / (goalDenom)))
            away_prob = ((awaySOG**2.15)/(sogDenom) * ( awayGoals**2.15 / (goalDenom)))

            #Probability Denominator for out of 100% proprotion
            prob_denom = (home_prob+away_prob)

            print(f"AWAY TEAM                          : {away_team_code}")
            print(f"Current Status                     : {awayWins}-{awayLoss}-{awayOtLosses}")
            print(f"Standing Points                    : {awayPoints}")
            print(f"Season win rate                    : {awayWins/awayGamesPlayed*100:.2f}%")
            print(f"Goals per Game                     : {awayGoals/awayGamesPlayed:.2f}")

            ## Sauced Corsi is my own algorithm for determining winner. YMMV
            print(f"Odds of winning (Sauced Corsi)(ML) : {(away_prob/prob_denom)*100:.2f}%")

            print("\n")

            print(f"HOME TEAM                          : {home_team_code}")
            print(f"Current Status                     : {homeWins}-{homeLoss}-{homeOtLosses}")
            print(f"Standing Points                    : {homePoints}")
            print(f"Season win rate                    : {homeWins/homeGamesPlayed*100:.2f}%")
            print(f"Odds of winning (Sauced Corsi)(ML) : {(home_prob/prob_denom)*100:.2f}%")
            print(f"Goals per Game                     : {homeGoals/homeGamesPlayed:.2f}")

            print("\n")

            print("Scoring expectations:")
            print(f"Home Save Pctg: {homeSavePctg*100:.2f}%")
            print(f"Away Save Perc: {awaySavePctg*100:.2f}%")

            #Calculate the goalie adjusted expected goal rate 
            #GAR = Goalie Adjusted Rate
            homeGoalsGAR = (homeSOG/homeGamesPlayed)*(1-awaySavePctg)
            awayGoalsGAR = (awaySOG/awayGamesPlayed)*(1-homeSavePctg)

            print(f"Expected Combined Goals Floor   (O): {(awayGoals/awayGamesPlayed + homeGoals/homeGamesPlayed) * (0.66):.2f}")
            print(f"Expected Combined Goal Average  (A): {awayGoals/awayGamesPlayed + homeGoals/homeGamesPlayed:.2f}")
            print(f"Expected Combined Goals Ceiling (U): {(awayGoals/awayGamesPlayed + homeGoals/homeGamesPlayed) * (1.33):.2f}")
            print()
            print(f"Adj. expected home goals: {homeGoalsGAR:.2f}")
            print(f"Adj. expected away goals: {awayGoalsGAR:.2f}")
            print(f"Adj. expected Combined Goals Floor   (O): {(homeGoalsGAR + awayGoalsGAR) * (0.66):.2f}")
            print(f"Adj. expected Combined Goal Average  (A): {homeGoalsGAR + awayGoalsGAR:.2f}")
            print(f"Adj. expected Combined Goals Ceiling (U): {(homeGoalsGAR + awayGoalsGAR) * (1.33):.2f}")
            
            print("--------------------------------------------------------")
            print("--------------------------------------------------------")
            count +=1
            input("Press enter to see the next game:")
            os.system('cls' if os.name == 'nt' else 'clear')
        input("Press enter to return to the previous screen...")
        os.system('cls' if os.name == 'nt' else 'clear')

    def team_stats(self, teams):
        command = ""
        count = 0
        team_code = ""
        while not command == "99":
            print("Selected a team code to show their statistics and ratings: \n")

            ## Yes the codes make no sense
            ## They're the exact codes the NHL uses in their API
            ## Any issues feel free to scrum with the NHL execs over it
            print("1. New Jersey Devils    2. New York Islanders    3. New York Rangers       4. Philadelphia Flyers")
            print("5. Pittsburg Penguins   6. Boston Bruins         7. Buffalo Sabres         8. Montreal Canadiens")
            print("9. Ottawa Senators      10. Toronto Maple Leafs  12. Carolina Hurricanes   13. Florida Panthers")
            print("14. Tampa Bay Lightning 15. Washington Capitals  16. Chicago Blackhawks    17. Detroit Red Wings")
            print("18. Nashville Predators 19. St. Louis Blues      20. Calgary Flames        21. Colorado Avalanche")
            print("22. Edmonton Oilers     23. Vancouver Canucks    24. Anaheim Ducks         25. Dallas Stars")
            print("26. Los Angeles Kings   28. San Jose Sharks      29. Columbus Blue Jackets 30. Minnesota Wilds")
            print("52. Winnipeg Jets       54. Vegas Golden Knights 55.Seattle Kraken         68.Utah Mammoth")
            print("99. EXIT")

            # Get the code from the goofy
            command = input("Please input a team code: ")

            os.system('cls' if os.name == 'nt' else 'clear')
            if not command == "99":
                try:

                    #Convert the input from string to int for dictionary access
                    team_code = int(command)

                    #Gets Values for Display
                    SOG=teams[team_code]["sogSummary"][0]["shots"]
                    Goals=teams[team_code]["sogSummary"][0]["goals"]
                    Wins=teams[team_code]["team"]["wins"]
                    Loss=teams[team_code]["team"]["losses"]
                    OtLosses=teams[team_code]["team"]["otLosses"]
                    GamesPlayed=teams[team_code]["team"]["gamesPlayed"]
                    Points=teams[team_code]["team"]["points"]

                    roster = self.client.teams.team_roster(team_abbr=RTCL.TeamThreeCodes[team_code], season=self.season)

                    #Output all of the important deets
                    print(f"Team Name            : {teams[team_code]["team"]["placeNameWithPreposition"]["default"] + " " + teams[team_code]["team"]["commonName"]["default"]}")
                    print(f"Win-Loss Record      : {Wins}-{Loss}-{OtLosses}")
                    print(f"Games Played         : {GamesPlayed}")
                    print(f"Win Percentage       : {Wins/GamesPlayed*100:.2f}%")
                    print(f"Current Season Points: {Points}")
                    print(f"Season Goals         : {Goals}")
                    print(f"Avg. Goals per Game  : {Goals/GamesPlayed*100:.2f}")
                    print()
                    print("Current Roster: ")
                    for position in roster:
                        count = 0 
                        for player in range(0, (len(roster[position])-1)):
                            print(f"#{roster[position][count]["sweaterNumber"]} {roster[position][count]["firstName"]["default"]} {roster[position][count]["lastName"]["default"]}")
                            count += 1
                        count = 0 

                #Throw error if not found 
                #This will only happen if the user input isn't a team code
                except:
                    print("INVALID TEAM CODE")

                input("Press enter to return to the previous screen...")
            os.system('cls' if os.name == 'nt' else 'clear')

    def player_stats(self, teams):
        player_count = 0
        count = 0
        command = ""
        sOG = 0
        goals = 0
        assists = 0

        ## Currently dreading setting this up
        ## Gonna need a lot of vodka to code this one

        while not command == "99":
            command = ""
            count = 0
            player_count = 0
            players = {}
            team_code = ""
            roster = {}
            
            os.system('cls' if os.name == 'nt' else 'clear')

            print("Selected a team code to show their statistics and ratings: \n")

            ## Yes the codes make no sense
            ## They're the exact codes the NHL uses in their API
            ## Any issues feel free to scrum with the NHL execs over it
            print("1. New Jersey Devils    2. New York Islanders    3. New York Rangers       4. Philadelphia Flyers")
            print("5. Pittsburg Penguins   6. Boston Bruins         7. Buffalo Sabres         8. Montreal Canadiens")
            print("9. Ottawa Senators      10. Toronto Maple Leafs  12. Carolina Hurricanes   13. Florida Panthers")
            print("14. Tampa Bay Lightning 15. Washington Capitals  16. Chicago Blackhawks    17. Detroit Red Wings")
            print("18. Nashville Predators 19. St. Louis Blues      20. Calgary Flames        21. Colorado Avalanche")
            print("22. Edmonton Oilers     23. Vancouver Canucks    24. Anaheim Ducks         25. Dallas Stars")
            print("26. Los Angeles Kings   28. San Jose Sharks      29. Columbus Blue Jackets 30. Minnesota Wilds")
            print("52. Winnipeg Jets       54. Vegas Golden Knights 55.Seattle Kraken         68.Utah Mammoth")
            print("99. EXIT")

            # Get the code from the goofy
            command = input("Please input a team code: ")

            os.system('cls' if os.name == 'nt' else 'clear')
            if not command == "99":
                try:
                    
                    team_code = int(command)

                    roster = self.client.teams.team_roster(team_abbr=RTCL.TeamThreeCodes[team_code], season=self.season)

                    #Convert the input from string to int for dictionary access
                    team_code = int(command)
                    print("Choose a player to see their stats:\n")
                    
                    players = {}
                    player_roster=0

                    for position in roster:
                        count = 0 
                        for player in range(0, (len(roster[position]))):
                            
                            print(
                                f"Player ID.  {player_roster} | #{roster[position][count]["sweaterNumber"]} {roster[position][count]["firstName"]["default"]}"\
                                f" {roster[position][count]["lastName"]["default"]}"
                                )
                            
                            players[player_roster] = (
                                roster[position][count]["id"], 
                                f"#{roster[position][count]["sweaterNumber"]} {roster[position][count]["firstName"]["default"]} {roster[position][count]["lastName"]["default"]}", 
                                roster[position][count]["positionCode"]
                            )

                            count += 1
                            player_roster+=1
                    print("98. See all players\n99.EXIT")
                    command = input(":")     
                    os.system('cls' if os.name == 'nt' else 'clear')
                    if not command=="98" and not command=="99":
                        player_stats = {
                            "games":self.client.stats.player_game_log(players[int(command)][0],self.season,"2"),
                            "pos":players[int(command)][2]
                            }
                        
                        #Reset Variables
                        count=0
                        goals=0
                        assists=0
                        shotsAgainst=0
                        goalsAgainst=0
                        grossSavePctg=0
                        for game in player_stats["games"]:
                            if not player_stats["pos"] == 'G':
                                #Gets Values for Display
                                sOG+=player_stats["games"][count]["shots"]
                                goals+=player_stats["games"][count]["goals"]
                                assists+=player_stats["games"][count]["assists"]
                                gamesPlayed=teams[team_code]["team"]["gamesPlayed"]
                                count += 1
                            
                                teamGoals=teams[team_code]["sogSummary"][0]["goals"]    
                            else:
                                goals+=player_stats["games"][count]["goals"]
                                assists+=player_stats["games"][count]["assists"]
                                shotsAgainst+=player_stats["games"][count]["shotsAgainst"]
                                goalsAgainst+=player_stats["games"][count]["goalsAgainst"]
                                grossSavePctg+=player_stats["games"][count]["savePctg"]
                                count += 1
                            
                                teamGoals=teams[team_code]["sogSummary"][0]["goals"]
                                pass

                        if not player_stats["pos"] == "G":
                            #Output all of the important deets
                            print("PLAYER DATA:\n")
                            print("-----------------------\n")
                            print(f"Player Name         : {players[int(command)][1]}")
                            print(f"Shots               : {sOG}")
                            print(f"Shots per Game      : {sOG/gamesPlayed:2f}")
                            print(f"Goals               : {goals}")
                            print(f"Goals per Shot      : {goals/sOG:.2f}")
                            print(f"Team Goal Pctg.     : {goals/teamGoals*100:.2f}%")
                            print(f"Goals/Game Pctg.    : {goals/gamesPlayed*100:.2f}%")
                            print(f"Assists             : {assists}")
                            print(f"Assists per shot    : {assists/sOG:.2f}")
                            print(f"Assists/Game Pctg.  : {assists/gamesPlayed*100:.2f}%")
                            print(f"")
                        else:
                            #Output all of the important deets
                            print("PLAYER DATA:\n")
                            print("-----------------------\n")
                            print(f"Player Name             : {players[int(command)][1]}")
                            print(f"Shots Against           : {shotsAgainst}")
                            print(f"Goals Against           : {goalsAgainst}")
                            print(f"Seasonal Save Percentage: {grossSavePctg/count*100:.2f}%")
                            print(f"Goals                   : {goals}")
                            print(f"Assists                 : {assists}")
                            print(f"")
                        input("Press any key to continue...")
                    else:
                        roster_count=0
                        #Generate full team roster with stats
                        print(f"Player Name               | SoG | S/P/G | TG | G/P/S |  TG%  | G/G% | Assists | Assist Per Shot | Assists/Game Pctg.")
                        for player in range(0, (len(roster["forwards"])+len(roster["defensemen"])+len(roster["goalies"]))):
                            if not players[roster_count][2] == "G":
                                player_id=players[roster_count][0]
                                player_stats = {
                                "games":self.client.stats.player_game_log(player_id,self.season,"2")
                                }
                            
                                #Reset Variables
                                count=0
                                goals=0
                                sOG=0
                                assists=0
                                shotsAgainst=0
                                goalsAgainst=0
                                grossSavePctg=0
                                for game in player_stats["games"]:
                                    #Gets Values for Display
                                    sOG+=player_stats["games"][count]["shots"]
                                    goals+=player_stats["games"][count]["goals"]
                                    assists+=player_stats["games"][count]["assists"]
                                    gamesPlayed=teams[team_code]["team"]["gamesPlayed"]
                                    count += 1
                                
                                    teamGoals=teams[team_code]["sogSummary"][0]["goals"]
                                if len(players[roster_count][1]) < 25:
                                    space = (25-len(players[roster_count][1])) * " "
                                    playerName = players[roster_count][1] + space

                                # Here because if player never got any shots the code breaks
                                if sOG > 0:
                                    goalsPerShot = goals/sOG 
                                    assistsPerShot = assists/sOG
                                else:
                                    goalsPerShot = 0
                                    assistsPerShot = 0
                                if len(str(sOG)) < 3:
                                    shots = str(sOG) + ((3-len(str(sOG))) * " ")
                                print(
                                    f"{playerName} | {shots} | {sOG/gamesPlayed:.3f} | {goals} | {goalsPerShot:.3f} |"\
                                    f" {goals/teamGoals*100:.2f}% | {goals/gamesPlayed*100:.2f}% | {assists} |"\
                                    f" {assistsPerShot:.2f} | {assists/gamesPlayed*100:.2f}%"
                                    )
                                roster_count+=1
                            else:
                                roster_count+=1
                        roster_count=0
                        input("Press any key to continue...")
                        

                #Throw error if not found 
                #This will only happen if the user input isn't a team code
                except:
                    print("INVALID TEAM CODE")

                    input("Press enter to return to the previous screen...")
            
        


### For Debug Use
### DO NOT RUN THIS FILE DIRECTLY
### I mean you can but it won't be as nice as having everything together
### Unless you downloaded it from Github as NHL_Terminal
#NHL_Term()