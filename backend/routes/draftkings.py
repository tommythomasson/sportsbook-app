from bs4 import BeautifulSoup
from util import Util

from pydantic import BaseModel
from typing import List
from pathlib import Path

import json
#import pandas as pd
import re

#from datetime import date
import time

from fastapi import APIRouter


class SportsRequest(BaseModel):
    sports: List[str]

router = APIRouter(prefix="/draftkings")

class Draftkings:

    extensions = {'NHL': '42133',
                  'NFL': '88808',
                  'MLB': '84240',
                  'NBA': '42648',
                  'UFC': '9034'}

    def getSourceMainPage(driver, extension: str) -> dict:

        # The URL you want to scrape
        url = 'https://sportsbook-nash.draftkings.com/api/sportscontent/dkusnj/v1/leagues/' + Draftkings.extensions[extension]
        #urlAlternate = 'https://sportsbook.draftkings.com/sites/US-SB/api/v5/eventgroups/' + extension

        if extension not in Draftkings.extensions.keys():
            raise KeyError(f"{extension} not in sports list: {Draftkings.extensions.keys()}")

        driver.get(url)  # Navigate to the page

        # Allow some time for the page to load and make network requests
        time.sleep(1)  # Adjust as necessary based on page load time

        soup = BeautifulSoup(driver.page_source, 'lxml') # alternate 'html.parser'
        print(soup)
        page_source = json.loads(soup.find('pre').text)

        return page_source
    
    def getSourceEventPage(driver, extension: str) -> dict:
        # The URL you want to scrape
        url = 'https://sportsbook.draftkings.com/event/' + extension

        driver.get(url)  # Navigate to the page

        time.sleep(1)
        # no time.sleep needed as this is part of webpage html

        src = driver.page_source

        soup = BeautifulSoup(src, 'lxml') # alternate 'html.parser'
        page_source = re.search(r'"stadiumEventData":(.*?),"stadiumLeagueData"', str(soup), re.DOTALL).group(1)
        #print(page_source)
        
        page_json = json.loads(page_source)

        return page_json
    

    '''
    events {    idNUMBER : { 'game' : _____
                            'markets' : { marketID : [(type, odds)] }
                            }
            }
    '''
    def getDict(page_source: dict, events: dict = None, markets_to_events: dict = None) -> tuple:
        if events is None:
            events = {}
        if markets_to_events is None:
            markets_to_events = {}

        for event in page_source['events']:
            events[event['id']] = { 'game' : event['name'] }

        for market in page_source['markets']:
            events[market['eventId']][market['id']] = { 'type' : market['name'], 'odds': []}
            markets_to_events[market['id']] = market['eventId']

        for selection in page_source['selections']:
            element = events[markets_to_events[selection['marketId']]][selection['marketId']]

            element['odds'].append([selection['label'], int(selection['displayOdds']['american'].replace('\u2212', '-'))])     # change to digital (or add to dict) for return on bet
            try:
                element['odds'][-1].append(selection['points'])
            except:
                continue

        return events, markets_to_events
    
    @router.post("/sport_odds")
    def parseSports(req: SportsRequest):
        print("Received JSON:", req.model_dump())
        sports = req.sports
        driver = Util.connectDriver()

        for sport in sports:
            print(f"Parsing {sport}")
            sourceMain = Draftkings.getSourceMainPage(driver, sport)
            events, markets_to_events = Draftkings.getDict(sourceMain)

            for event in events.keys():
                print(f"\t- {events[event]['game']}")
                sourceEvent = Draftkings.getSourceEventPage(driver, event)
                events, markets_to_events = Draftkings.getDict(sourceEvent, events, markets_to_events)

            # dont have to save these off since they are stored on the webpage 
            #with open(f"./odds_data/DK_{sport}.json", "w") as f:
            #    json.dump(events, f)
        
        driver.quit()

        return markets_to_events #events

    # will pull things that arent player names, but these will just fail the get stats
    def getEventPlayers(event: dict):
        names = set()
        for item in event.keys():
            if item != 'game':
                name = event[item]['type']

                split = name.split(' ')
                if len(split) > 2:
                    names.add(' '.join(split[0:2]))
        return names
    

    #def getEventTeamStats(driver, sport: str, event: dict):
    #    players = Draftkings.getEventPlayers(event)
    #    teams = [team.strip() for team in event['game'].split('@')]
    #    ESPN.getGameStats(driver, sport, teams, players)
        

        

# # SAMPLE RUN::
# driver = Draftkings.connectDriver()

# sourceMain = Draftkings.getSourceMainPage(driver, Draftkings.NHL)
# events, markets = Draftkings.getDict(sourceMain)

# # relationship between each type bet and game
# Draftkings.print_dict(markets)

# # full json of scraped odds
# Draftkings.print_dict(events)

# sampleEvent = '32154725'

# print(Draftkings.getSourceEventPage(driver, sampleEvent))

# driver.quit()

# Draftkings.parseSports(['MLB'])

# with open('./odds/DK_MLB.json', 'r') as f:
#    odds_json = json.load(f)

# for event in odds_json:
#     Draftkings.getEventTeamStats(Util.connectDriver(), 'MLB', odds_json[event])
#     break

#with open('./stats/MLB.json', 'r') as f:
#    stats_json = json.load(f)

# make plot
#player_stats = stats_json['mia']['Agustin Ramirez']
#dates = [row[ESPN.glossary['MLB']['B']['Date']] for row in player_stats]
#hits = [row[ESPN.glossary['MLB']['B']['Hits']] for row in player_stats]

#stats = list(zip(dates, hits))
#Util.createPlot(odds_json['32314635']['250952266']['odds'], stats)