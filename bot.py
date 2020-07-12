#!venv/bin/python3

import json
import telebot
import requests
import argparse
from bs4 import BeautifulSoup

def get_daily_activities():
    html = requests.get("https://wiki.guildwars.com/wiki/Daily_activities").text
    soup = BeautifulSoup(html, 'html.parser')

    tr = soup.find('tr', attrs = {'style' : "font-weight: bold;"})

    activities = {}

    activities["mission"] = { "type": "Zaishen Mission", "name" : tr.contents[3].find("a").string }
    activities["bounty"] = { "type": "Zaishen Bounty", "name" : tr.contents[5].find("a").string }
    activities["combat"] = { "type": "Zaishen Combat", "name" : tr.contents[7].find("a").string }
    activities["vanquish"] = { "type": "Zaishen Vanquish", "name" : tr.contents[9].find("a").string }
    activities["blade"] = { "type": "Shining Blade", "name" : tr.contents[11].find("a").string }
    activities["vanguard"] = { "type": "Vanguard Quest", "name" : tr.contents[13].find("a").string }
    activities["nicholas"] = { "type": "Nicholas Sandford", "name" : tr.contents[15].find("a").string }

    return activities

def get_weekly_activities():
    html = requests.get("https://wiki.guildwars.com/wiki/Weekly_activities").text
    soup = BeautifulSoup(html, 'html.parser')

    tr = soup.find('tr', attrs = {'style' : "font-weight: bold;"})

    activities = {}

    activities["pve"] = { "type": "PvE bonus", "name" : tr.contents[3].find("a").string }
    activities["pvp"] = { "type": "PvP bonus", "name" : tr.contents[5].find("a").string }
    activities["nicholas"] = { "type": "Nicholas item", "name" : tr.contents[7].find("a").string }


    return activities

def get_monthly_activities():
    html = requests.get("https://wiki.guildwars.com/wiki/Flux").text
    soup = BeautifulSoup(html, 'html.parser')

    tr = soup.find('tr', attrs = {'style' : "font-weight:bold"})

    activities = {}

    activities["flux"] = { "type": "Flux", "name" : tr.contents[3].find("a").string }

    return activities

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Guild Wars Zaishen Mission Notifier")
    parser.add_argument("-d", "--daily", action="store_true", help="check daily missions", dest="daily")
    parser.add_argument("-w", "--weekly", action="store_true", help="check weekly bonuses", dest="weekly")
    parser.add_argument("-m", "--monthly", action="store_true", help="check monthly effects", dest="monthly")
    parser.add_argument("-a", "--alert", action="store_true", help="announce matched missions via telegram", dest="alert")
    parser.add_argument("-p", "--post", action="store_true", help="post all missions via telegram", dest="post")
    parser.add_argument("--debug", action="store_true", help="don't send via telegram, print to stdout instead", dest="debug")

    args = parser.parse_args()

    if not (args.daily or args.weekly or args.monthly):
        print("specify at least one of --daily, --weekly or --monthly")
        parser.print_help()
        exit(1)

    if not (args.alert or args.post):
        print("specify at least one of --alert or --post")
        parser.print_help()
        exit(1)

    config_file = open("config.json", "r")
    config = json.load(config_file)

    message = ""

    if args.daily:
        dailies = get_daily_activities()

        if args.post:
            message += "Today's Missions:\n"
            for d in dailies.values():
                message += "{}: {}\n".format(d["type"], d["name"])

        if args.alert:
            matches = ""

            if "daily" in config.keys():
                for mission_type in dailies.keys():
                    if dailies[mission_type]["name"] in config["daily"][mission_type]:
                        matches += "{}: {}\n".format(dailies[mission_type]["type"], dailies[mission_type]["name"])

            if matches != "":
                matches = "Your matched missions for today:\n{}".format(matches)

                if message != "":
                    matches = "\n" + matches

                message += matches

    if args.weekly:
        weeklies = get_weekly_activities()

        if args.post:
            if message != "":
                message += "\n"

            message += "This Week's Bonuses:\n"

            for w in weeklies.values():
                message += "{}: {}\n".format(w["type"], w["name"])

        if args.alert:
            matches = ""

            if "weekly" in config.keys():
                for bonus_type in weeklies.keys():
                    if weeklies[bonus_type]["name"] in config["weekly"][bonus_type]:
                        matches += "{}: {}\n".format(weeklies[bonus_type]["type"], weeklies[bonus_type]["name"])

            if matches != "":
                matches = "Your matched bonuses for this week:\n{}".format(matches)

                if message != "":
                    matches = "\n" + matches

                message += matches

    if args.monthly:
        monthlies = get_monthly_activities()

        if args.post:
            if message != "":
                message += "\n"

            message += "This Month's Effects:\n"

            for m in monthlies.values():
                message += "{}: {}\n".format(m["type"], m["name"])

        if args.alert:
            matches = ""

            if "monthly" in config.keys():
                for effect in monthlies.keys():
                    if monthlies[effect]["name"] in config["monthly"][effect]:
                        matches += "{}: {}\n".format(monthlies[effect]["type"], monthlies[effect]["name"])

            if matches != "":
                matches = "Your matched effects for this month:\n{}".format(matches)

                if message != "":
                    matches = "\n" + matches

                message += matches

    if message != "":
        if args.debug:
            print(message)
        else:
            bot = telebot.TeleBot(config["token"])
            bot.send_message(config["chat_id"], message)