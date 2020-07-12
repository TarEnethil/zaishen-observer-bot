# Zaishen Observer Bot

Post all or subscribe to specific daily, weekly or monthly events in Guild Wars via your own Telegram Bot.

## Setup Telegram Bot
* Create Telegram bot (@BotFather) to get API Key ("token")
* Write one message to your bot and get your "chat_id" from `https://api.telegram.org/bot<TOKEN>/getUpdates`

## Setup Python Bot
```bash
git clone https://github.com/TarEnethil/zaishen-observer-bot.git
cd zaishen-observer-bot
python3 -m venv venv
venv/bin/activate
pip install -r requirements.txt
cp config.json.template config.json
```

* Add "token" and "api_key" to `config.json`
* (optional) configure which missions you want to be alerted for (exact matches only, currently)

## Setup cronjob
`crontab -e`

Examples:
```
# alert for daily missions at 20:00
0 20 * * * cd <path>/zaishen-observer-bot && venv/bin/python bot.py --daily --alert

# post all missions at midnight
0 0 * * * cd <path>/zaishen-observer-bot && venv/bin/python bot.py --daily --post

# alert for weekly bonuses every monday at 17:00
0 17 * * 1 cd <path>/zaishen-observer-bot && venv/bin/python bot.py --weekly --alert

# post all weekly bonuses at midnight every tuesday
0 0 * * 2 cd <path>/zaishen-observer-bot && venv/bin/python bot.py --weekly --post

# post monthly effects at the second day of each month at 07:00
0 7 2 * * cd <path>/zaishen-observer-bot && venv/bin/python bot.py --monthly --post

# send a silent monthly ping to show that bot is still working
0 10 1 * * cd <path>/zaishen-observer-bot && venv/bin/python bot.py --ping --silent
```


## Usage

```
usage: bot.py [-h] [-d] [-w] [-m] [-a] [-p] [-s] [--debug] [--ping]

Guild Wars Zaishen Mission Notifier

optional arguments:
  -h, --help     show this help message and exit
  -d, --daily    check daily missions
  -w, --weekly   check weekly boni
  -m, --monthly  check monthly effects
  -a, --alert    announce matched missions via telegram
  -p, --post     post all missions via telegram
  -s, --silent   send a silent notification (no sound)
  --debug        don't send via telegram, print to stdout instead
  --ping         send a simple message to show that the bot is working
```

* `--daily`, `--weekly` and `--monthly` can be combined.
* `--alert` and `--post` can be combined.
