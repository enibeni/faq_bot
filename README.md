# Answer bot

Get help for your support team with the answer bot.  
Train the bot with common Q&A and free your support team time

### How to install

To use this script you should provide certain keys as environment variables in the .env file.
The keys you need to provide:
- GOOGLE_APPLICATION_PROJECT_ID - DialogFlow project id
- GOOGLE_APPLICATION_CREDENTIALS - authentication credentials to your application
- VK_TOKEN_ANSWER_BOT - vk bot api key
- TG_TOKEN_ANSWER_BOT - telegram bot api key
- TG_TOKEN_LOGGER_BOT - telegram bot api key for logging
- TG_CHAT_ID - telegram chat id provided via @userinfobot bot

to get GOOGLE_APPLICATION_PROJECT_ID create DialogFlow project with this manual https://cloud.google.com/dialogflow/es/docs/quick/setup

to get GOOGLE_APPLICATION_CREDENTIALS follow this manual https://cloud.google.com/docs/authentication/getting-started

to create vk bot and get VK_TOKEN_ANSWER_BOT follow this manual https://vk.com/dev/bots_docs

You will need two telegram bots for this script. One for notification about work check status
and another one for logging. Find out how to create them on telegram docs https://core.telegram.org/bots

Python3 should be already installed. 
Then use `pip` (or `pip3`, if there is a conflict with Python2) to install dependencies:
```
pip install -r requirements.txt
```

# Quickstart

to train bot fill questions.json file with your common Q&A and run script:
```bash
$ python3 dialogflow_helper.py
```

run telegram bot:
```bash
$ python3 tg_bot.py
```

![Alt Text](https://media.giphy.com/media/PIaJJgfsJbjwxjG9Hv/giphy.gif)

run vk bot:
```bash
$ python3 vk_bot.py
```

![Alt Text](https://media.giphy.com/media/wvMWJ59vJzjCanB8mk/giphy.gif)

### Project Goals

The code is written for educational purposes on online-course for web-developers [dvmn.org](https://dvmn.org/).