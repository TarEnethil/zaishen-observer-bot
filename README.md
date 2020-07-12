# Zaishen Observer Bot

Post all or subscribe to specific daily or weekly bonuses in Guild Wars.

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
0 0 * * 2 cd <path>/zaishen-observer-bot && venv/bin/python bot.py --weekly --alert
```


## Usage

```
usage: bot.py [-h] [-d] [-w] [-a] [-p]

Guild Wars Zaishen Mission Notifier

optional arguments:
  -h, --help    show this help message and exit
  -d, --daily   check daily missions
  -w, --weekly  check weekly missions
  -a, --alert   announce matched missions via telegram
  -p, --post    post all missions via telegram
```

* `--daily` and `--weekly` can be combined.
* `--alert` and `--post` can be combined.