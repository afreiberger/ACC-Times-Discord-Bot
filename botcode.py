#!/usr/bin/env python3
import json
import os

from time import sleep
from enum import Enum

import aiohttp
import asyncio

#import discord
#from discord.ext import commands, tasks

from dotenv import load_dotenv

#intents = discord.Intents.default()

load_dotenv()

#guild_id = os.getenv("GUILD_ID")


class Tracks(Enum):
    barcelona = "Barcelona"
    brands_hatch = "Brands Hatch"
    cota = "Circuit of the Americas"
    donington = "Donington"
    hungaroring = "Hungaroring"
    imola = "Imola"
    indianapolis = "Indianapolis"
    kyalami = "Kyalami"
    laguna_seca = "Laguna Seca"
    misano = "Misano"
    monza = "Monza"
    mount_panorama = "Mount Panorama"
    nurburgring = "Nurburgring"
    nurburgring_24h = "Nordschleife"
    oulton_park = "Oulton Park"
    paul_ricard = "Paul Ricard"
    red_bull_ring = "Red Bull Ring"
    silverstone = "Silverstone"
    snetterton = "Snetterton"
    spa = "Spa"
    suzuka = "Suzuka"
    valencia = "Valencia"
    watkins_glen = "Watkins Glen"
    zandvoort = "Zandvoort"
    zolder = "Zolder"


car_types = [
    "Porsche 991 GT3 R (2018)",
    "Mercedes-AMG GT3 (2015)",
    "Ferrari 488 GT3 (2018)",
    "Audi R8 LMS (2015)",
    "Lamborghini Huracán GT3 (2015)",
    "McLaren 650S GT3 (2015)",
    "Nissan GT-R Nismo GT3 (2018)",
    "BMW M6 GT3 (2017)",
    "Bentley Continental GT3 (2018)",
    "Porsche 991 II GT3 Cup (2017)",
    "Nissan GT-R Nismo GT3 (2015)",
    "Bentley Continental GT3 (2015)",
    "AMR V12 Vantage GT3 (2013)",
    "Reiter Engineering R-EX GT3 (2017)",
    "Emil Frey Jaguar G3 (2012)",
    "Lexus RC F GT3 (2016)",
    "Lamborghini Huracan GT3 Evo (2019)",
    "Honda NSX GT3 (2017)",
    "Lamborghini Huracan SuperTrofeo (2015)",
    "Audi R8 LMS Evo (2019)",
    "AMR V8 Vantage (2019)",
    "Honda NSX GT3 Evo (2019)",
    "McLaren 720S GT3 (2019)",
    "Porsche 991 II GT3 R (2019)",
    "Ferrari 488 GT3 Evo (2020)",
    "Mercedes-AMG GT3 (2020)",
    "Ferrari 488 Challenge Evo (2020)",
    "BMW M2 Club Sport Racing (2020)",
    "Porsche 992 GT3 Cup (2021)",
    "Lamborghini Huracán SuperTrofeo EVO2 (2021)",
    "BMW M4 GT3 (2022)",
    "Audi R8 LMS GT3 Evo 2 (2022)",
    "Ferrari 296 GT3 (2023)",
    "Lamborghini Huracan GT3 Evo 2 (2023)",
    "Porsche 992 GT3 R (2023)",
    "McLaren 720S GT3 Evo (2023)",
    "Ford Mustang GT3 (2024)",
    "Alpine A110 GT4 (2018)",
    "Aston Martin Vantage GT4 (2018)",
    "Audi R8 LMS GT4 (2018)",
    "BMW M4 GT4 (2018)",
    "Chevrolet Camaro GT4 (2017)",
    "Ginetta G55 GT4 (2012)",
    "KTM X-Bow GT4 (2016)",
    "Maserati MC GT4 (2016)",
    "McLaren 570S GT4 (2016)",
    "Mercedes AMG GT4 (2016)",
    "Porsche 718 Cayman GT4 Clubsport (2019)",
    "Audi R8 LMS GT2 (2021)",
    "KTM XBOW GT2 (2021)",
    "Maserati MC20 GT2 (2023)",
    "Mercedes AMG GT2 (2023)",
    "Porsche 911 GT2 RS CS Evo (2023)",
    "Porsche 935 (2019)",
]


#class DiscordBot(commands.Bot):
#    def __init__(self) -> None:
#        #super().__init__(
#        #    intents=intents, help_command=None, command_prefix=commands.when_mentioned
#        #)
#
#        self.database = None
#
#        #self.database = json.load(open("db.json", "r+"))


async def get_latest_results() -> dict:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{os.getenv('BASE_URL')}/api/results/list.json"
            ) as sessionlist:
                logged_sessions = await sessionlist.json()

                async with session.get(
                    f"{os.getenv('BASE_URL')}{logged_sessions['results'][0]['results_json_url']}"
                ) as latest_session_results:
                    return await latest_session_results.json()

def get_track_cache_list(track_name, db):
    sessions = []
    for session in db.get(track_name, []):
        sessions.append(session['SessionFile'])
    return sessions

async def seed_track_results(track_name, db) -> dict:
        all_results={}
        all_results[track_name] = db.get(track_name, [])

        cached_files = get_track_cache_list(track_name, db)

        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{os.getenv('BASE_URL')}/api/results/list.json?q={track_name}"
            ) as sessionlist:
                pageresult = await sessionlist.json()

        # get list of result files from all pages minus those in the db already
        new_logs = []
        async with aiohttp.ClientSession() as session:
            for page in range(pageresult["num_pages"]):
                    sleep(4)
                    async with session.get(
                        f"{os.getenv('BASE_URL')}/api/results/list.json?q={track_name}&page={page}"
                    ) as paged_result:
                        trackfiles = await paged_result.json()

                        # in each page, pull each track results file if we don't already have it
                        for file in trackfiles.get('results'):
                            if file['results_json_url'].split('/')[3].split('.')[0] not in cached_files::
                                new_logs.append(file['results_json_url'])

        async with aiohttp.ClientSession() as session:
            for file in new_logs:
                sleep(6)
                async with session.get(f"{os.getenv('BASE_URL')}{file}") as track_log:
                    log = await track_log.json()
                    #log = json.loads(log)
                    all_results[track_name].append(log)

        return all_results

def find_fastest_times(track_name, db):
    


if __name__ == '__main__':
    db = json.load(open("db.json","r+"))
    db = asyncio.run(seed_track_results('kyalami', db))
    json.dump(db, open("db.json", "w+"), indent=4)
    find_fastest_times('kyalami', db)
