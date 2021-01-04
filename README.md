# ilovepdfbot

[![Telegram Bot](https://img.shields.io/badge/Telegram-Bot-blue.svg)](https://t.me/pdfbot)

A telegram bot which offers you all features of [ilovepdf](https://www.ilovepdf.com/)!

`/compress` to compress a PDF file  
`/imgtopdf` to convert one or more images to a PDF file  
`/officetopdf` to convert an office file to a PDF file  
`/addpagenumbers` to add numbers to the pages of a PDF file  
`/pdfa` to convert a PDF file to PDF/A standard  
`/pdftojpg` to convert each page of a PDF file to jpg images  
`/protectpdf` to protect a PDF file using a password  
`/rotatepdf` to rotate (90, 180 degrees) a PDF file  
`/splitpdf` to split a PDF file according to a range  
`/unlockpdf` to unlock a protected PDF file  
`/watermark` to apply a watermark to a PDF file

## Run the bot

```
git clone https://github.com/brivadeneira/ilovepdfbot
cd ilovepdfbot
pip install -r requirements.txt
cp .env.example .env
# edit .env file and add the telegram bot token
# and ilovepdf api key
python bot.py
```