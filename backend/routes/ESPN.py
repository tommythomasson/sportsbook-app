from bs4 import BeautifulSoup
from backend.util import Util

import json
import re

#from datetime import date
import time

from fastapi import APIRouter
router = APIRouter(prefix="/espn")

class ESPN:

    teams_dict = {'NHL': ['ana', 'bos', 'buf', 'cgy', 'car', 'chi', 'col', 'cbj', 'dal', 'det', 'edm', 'fla', 'la', 'min', 'mtl', 'nsh',
                    'nj', 'nyi', 'nyr', 'ott', 'phi', 'pit', 'sj', 'sea', 'stl', 'tb', 'tor', 'utah', 'van', 'vgk', 'wsh', 'wpg'],
                'MLB': {'ARI Diamondbacks': 'ari', 'Athletics':'ath', 'ATL Braves': 'atl', 'BAL Orioles': 'bal', 'BOS Red Sox': 'bos', 'CHI Cubs': 'chc',
                        'CHI White Sox': 'chw', 'CIN Reds': 'cin', 'CLE Guardians': 'cle', 'COL Rockies': 'col', 'DET Tigers': 'det', 'HOU Astros': 'hou',
                        'KC Royals': 'kc', 'LA Angels': 'laa', 'LA Dodgers': 'lad', 'MIA Marlins': 'mia', 'MIL Brewers': 'mil', 'MIN Twins': 'min',
                        'NY Mets': 'nym', 'NY Yankees': 'nyy', 'PHI Phillies': 'phi', 'PIT Pirates': 'pit', 'SD Padres': 'sd', 'SF Giants': 'sf',
                        'SEA Mariners': 'sea', 'STL Cardinals': 'stl', 'TB Rays': 'tb', 'TEX Rangers': 'tex', 'TOR Blue Jays': 'tor', 'WAS Nationals': 'wsh'}}

    glossary = { 'MLB': {'P': {'Innings Pitched': 0, 'Hits': 1, 'Runs': 2, 'Earned Runs': 3, 'Home Runs': 4, 'Walks': 5, 'Strikeouts': 6, 'Ground Balls': 7, 'Fly Balls': 8, 
                               'Pitches': 9, 'Batters Faced': 10, 'Game Score': 11, 'Decision': 12, 'Saves-Blown Saves-Holds': 13, 'Earned Run Average': 14, 'Position': 15, 'Home/Away': 16, 'Date': 17},
                        'B': {'At Bats': 0, 'Runs': 1, 'Hits': 2, 'Doubles': 3, 'Triples': 4, 'Home Runs': 5, 'Runs Batted In': 6, 'Walks': 7, 'Hit By Pitch': 8, 
                               'Strikeouts': 9, 'Stolen Bases': 10, 'Caught Stealing': 11, 'Batting Average': 12, 'On Base Percentage': 13, 'Slugging Percentage': 14, 'OBP Pct + SLG Pct': 15, 'Position': 16, 'Home/Away': 17, 'Date': 18}}}

    # API Endpoints

    # these are only going to pull the relavant rosters and stats from
    # teams who are playing in games posted to Draftkings
    # ^ big lack of pulling in data, but big time saver since other 
    #   teams and games are not available yet anyway

    @router.post("/mlb_player_stats")
    def postMLBRosters():
        # probably want a way to start the driver once and not end it until the page is closing
        # for now this is okay
        driver = Util.connectDriver()
        teams = ESPN.getTeamsPlayingToday(driver, 'MLB')
        roster = ESPN.getRosters(driver, 'MLB', teams)
        rosters_and_stats = ESPN.getStats(driver, roster, 'MLB')
        driver.quit()
        return rosters_and_stats
    
    @router.post("/nhl_player_stats")
    def postNHLRosters():
        # same driver concern
        driver = Util.connectDriver()
        teams = ESPN.getTeamsPlayingToday(driver, 'NHL')
        roster = ESPN.getRosters(driver, 'NHL', teams)
        rosters_and_stats = ESPN.getStats(driver, roster, 'NHL')
        driver.quit()
        return rosters_and_stats






    # Helper functions
    def getRosters(driver, sport: str, teams: list):
        roster = {} 
        roster_url = f"https://www.espn.com/{sport.lower()}/team/roster/_/name/"
        
        print(f"Pulling {sport.upper()} Rosters for teams:")

        # pull rosters of all teams from given the sport
        teams = list(ESPN.teams_dict[sport].values())

        for team in teams:
            try:
                driver.get(roster_url + team)  # Navigate to the page
            except:
                print(f"Could not get roster for '{team}'")
                continue
            print(f"\t- {team}")

            soup = BeautifulSoup(driver.page_source, 'lxml') # alternate 'html.parser'
            page_source = re.search(r'"streampicker":{},"roster":(.*?)},"subType"', str(soup), re.DOTALL).group(1)
            team_json = json.loads(page_source)

            for group in team_json["groups"]:
                # set player positions
                position = None
                if sport == 'MLB':
                    position = 'B'
                    if group['key'] == 'Pitchers':
                        position = 'P'
                elif sport == 'NHL':
                    position = 'S'
                    if group['key'] == 'Goalies':
                        position = 'G'

                for athlete in group["athletes"]:
                    try:
                        roster[team][athlete["name"]] = [athlete["id"], position]
                    except:
                        roster[team] = {}
                        roster[team][athlete["name"]] = [athlete["id"], position]
        # post roster to api
        return roster


    def getStats(driver, rosters_and_stats: dict, sport: str):
        url = f"https://www.espn.com/{sport.lower()}/player/gamelog/_/id/"
        #player_url = url + roster[team][player]

        for team_name, players in rosters_and_stats.items():
            print(f"Getting {team_name} stats")
            for player_name in players:
                player_id = players[player_name][0]
                position = players[player_name][1]
                player_url = url + player_id
                try:
                    driver.get(player_url)
                    print(f"\t- {player_name}")
                except:
                    print(f"Could not reach stats for '{player_name}', id: {player_id}")
                    continue

                soup = BeautifulSoup(driver.page_source, 'lxml') # alternate 'html.parser'
                page_source = re.search(r',"gmlog":(.*?),"sbpg":', str(soup), re.DOTALL).group(1)
                gamelog_json = json.loads(page_source)

                rosters_and_stats[team_name][player_name] = [] # list of lists of stats

                # hold last stored date here
                # scraping all games for each player
                for group in gamelog_json["groups"]:
                    for table in group["tbls"]:
                        if "events" in table: #last table is stat definitions
                            for event in table["events"]:
                                date = event["dt"].split("T")[0] # can change date to est first
                                loc = 'A'
                                if (event["opp"]["atVs"] == 'vs'):
                                    loc = 'H'
                                game_stats = event["stats"]
                                game_stats.extend([position, loc, date])
                                rosters_and_stats[team_name][player_name].append(game_stats)
                rosters_and_stats[team_name][player_name].sort(key=lambda x: x[-1]) # this would put the most recent games at the end of the list

        # instead of specifying a date, check stats list for most recent date, 
        # then pull since that time (should be a specific index since this will be a sorted list)
        return rosters_and_stats
    
    # specifying 'today' because of espn scoreboard of most sports being daily
    # nfl will show all games for the given week, with the week updating on tuesdays/wednesdays
    def getTeamsPlayingToday(driver, league: str):
        league_to_sport = {
            "NHL": "hockey", # only known link for now
        }
        if league not in league_to_sport.keys():
            raise KeyError(f"{league} not in supported leagues list: {league_to_sport.keys()}")
        
        scoreboardURL = f"https://site.web.api.espn.com/apis/personalized/v2/scoreboard/header?sport={league_to_sport[league]}&league={league}"

        driver.get(scoreboardURL)
        soup = BeautifulSoup(driver.page_source, 'lxml') # alternate 'html.parser'
        page_source = json.loads(soup.find('pre').text)

        teams_playing = []
        for event in page_source['events']:
            teams_playing.append(team.strip() for team in event['shortName'].split('@'))

        return teams_playing






# make function for odds ask for a player whos stats are not given: update specific team roster, update specific team and player stats


# ESPN.updateRoster(Util.connectDriver(), 'MLB')

# ESPN.updateStats(Util.connectDriver(), 'NHL', 'edm')

# sample
# ESPN.getGameStats(Util.connectDriver(), 'MLB', ['ARI Diamondbacks', 'Athletics'], ["Jalen Beeks", "Corbin Burnes", "Zac Gallen", "Kevin Ginkel", "Tyler Ferguson", "Hogan Harris", "Gunnar Hoglund"])

#find easy way to tell if player is fully up to date... maybe reading the espn gamelog will always read most recent first. then its an easy check