[![Telegram Bot](https://img.shields.io/badge/Telegram-Bot-blue.svg)](https://t.me/i_love_pdf_bot)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) [![Open Source Love svg1](https://badges.frapsoft.com/os/v1/open-source.svg?v=103)](https://github.com/ellerbrock/open-source-badges/)
  
[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)
[![ForTheBadge built-with-love](http://ForTheBadge.com/images/badges/built-with-love.svg)](https://GitHub.com/brivadeneira/)

# ilovepdfbot

A telegram bot which offers you all features of [ilovepdf](https://www.ilovepdf.com/)!  
[![](https://github.com/python-telegram-bot/logos/raw/master/logo-text/png/ptb-logo-text_768.png?raw=true)](https://github.com/python-telegram-bot/python-telegram-bot)
[![](https://www.ilovepdf.com/img/ilovepdf.svg)](https://www.ilovepdf.com)

![](https://media.giphy.com/media/cEgtvpYoEdPfqEYJs9/giphy.gif)

# Table of contents

* [Features](#features)  
* [Installation](#installation)  
* [Usage](#usage)
* [TODO](#todo)
* [License](#license)
* [Credits](#credits)

## Features

* `/compress` to compress a PDF file  
* `/imgtopdf` to convert one or more images to a PDF file  
* `/officetopdf` to convert an office file to a PDF file  
* `/addpagenumbers` to add numbers to the pages of a PDF file  
* `/pdfa` to convert a PDF file to PDF/A standard  
* `/pdftojpg` to convert each page of a PDF file to jpg images  
* `/protectpdf` to protect a PDF file using a password  
* `/rotatepdf` to rotate (90, 180 degrees) a PDF file  
* `/splitpdf` to split a PDF file according to a range  
* `/unlockpdf` to unlock a protected PDF file  
* `/watermark` to apply a watermark to a PDF file

## Installation

### 1. Clone the repository 
``` bash
$ git clone https://github.com/brivadeneira/ilovepdfbot
$ cd ilovepdfbot
```
### 2. Install the requirements using `pip`
``` bash
pip install -r requirements.txt
```
### 3. Copy and edit the `.env` file:
``` bash
$ cp .env.example .env
```
#### 3.1 Get the Telegram bot token
- Talk to [BotFather](https://t.me/BotFather),
- use `/newbot` command
> Alright, a new bot. How are we going to call it? Please choose a name for your bot.

- Enter your bot name

> Done! Congratulations on your new bot. You will find it at t.me/<your_bot_name>. You can now add a description, about section and profile picture for your bot, see /help for a list of commands. By the way, when you've finished creating your cool bot, ping our Bot Support if you want a better username for it. Just make sure the bot is fully operational before you do this.

> **Use this token to access the HTTP API:
1234567890:ABCDeFGhij1k2lMNoPpQ3rstUVWwxYZ4ABB**
Keep your token secure and store it safely, it can be used by anyone to control your bot.

> For a description of the Bot API, see this page: https://core.telegram.org/bots/api

- Copy the bot API into the `.env` file 

#### 3.2 Get the ilovepdf API key

- Go to [ilovepdf.com](https://www.ilovepdf.com/) and **sing up**.
- Go to [developer.ilovepdf.com](https://developer.ilovepdf.com/) *(in the rigth pannel click in `products` and click in `API Rest`)*
- Go to [developer.ilovepdf.com/user/projects](https://developer.ilovepdf.com/user/projects) *(or click in `get started`, click in `Projects - My projects`)*
- Create a new project
- Copy the API key
    - `project_public_1a234567b890c12ab3c4de56f7g8h9i0_-Jkl-
12m34no5678p9q01rs23t45u678v9wx0`

* Edit .env file and add the keys

`$ nano .env`

```bash 
BOT_TOKEN=1234567890:ABCDeFGhij1k2lMNoPpQ3rstUVWwxYZ4ABB
PUBLIC_KEY=project_public_1a234567b890c12ab3c4de56f7g8h9i0_-Jkl-
12m34no5678p9q01rs23t45u678v9wx0
```
### 4. Create a tmp directory

To temporary storage user files    
`$ mkdir tmp`

## Usage
```bash
$ python bot.py

2021-01-15 12:12:28,184 - apscheduler.scheduler - INFO - Scheduler started
```

## TODO

* [ ] Add a spanish version.
* [ ] Fix unlock feature.
* [ ] Add sign feature *(probably inside watermark feature)*

## License 
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Credits

ilovepdfbot is alive thanks to:
- [@AndyCyberSec](https://github.com/AndyCyberSec)
- [@tgrandje](https://github.com/tgrandje)
- [@MarkHaakman](https://github.com/MarkHaakman)
- [@oscar6echo](https://github.com/oscar6echo)

Who has made [pylovepdf](https://github.com/AndyCyberSec/pylovepdf)