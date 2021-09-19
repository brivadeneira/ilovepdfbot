import logging
import os

from telegram.ext import CommandHandler, Updater

from ilovepdf_bot.commands import (addpagenumbers_handler, compress_handler,
                                   imgtopdf_handler, officetopdf_handler,
                                   pdfa_handler, pdftojpg_handler,
                                   protectpdf_handler, rotatepdf_handler,
                                   splitpdf_handler, unlockpdf_handler,
                                   watermark_handler)

token = os.getenv('BOT_TOKEN')

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

commands = ("🗄 /compress to compress a PDF file",
            "🖼 -> 📄 /imgtopdf to convert one or more images to a PDF file",
            "📝 -> 📄 /officetopdf to convert an office file to a PDF file",
            "1️⃣2️⃣3️⃣ /addpagenumbers to add numbers to the pages of a PDF file",
            "📐 /pdfa to convert a PDF file to PDF/A standard",
            "📄 -> 🖼/pdftojpg to convert each page of a PDF file to jpg images",
            "🔑 /protectpdf to protect a PDF file using a password",
            "↩️ /rotatepdf to rotate (90, 180 degrees) a PDF file",
            "✂️ /splitpdf to split a PDF file according to a range",
            "🔑 /unlockpdf to unlock a protected PDF file",
            "💧 /watermark to apply a watermark to a PDF file",
            "❤️ /donate")


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="I ♥ pdf, and you?")
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Please, use /help to know what can I do for you")


def help(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Please feel free to use my commands:")
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text='\n'.join(commands))


def donate(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Is ilovepdfbot useful you?")
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Would you like to donate my mother a coffe? ♥")
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Please go to: https://www.paypal.com/donate?hosted_button_id=N374LBS72AAMA")


start_handler = CommandHandler('start', start)
help_handler = CommandHandler('help', help)
donate_handler = CommandHandler('donate', donate)

updater = Updater(token=token, use_context=True)
dispatcher = updater.dispatcher

# basic handlers
dispatcher.add_handler(start_handler)
dispatcher.add_handler(help_handler)
dispatcher.add_handler(donate_handler)

# command handlers
dispatcher.add_handler(compress_handler())
dispatcher.add_handler(imgtopdf_handler())
dispatcher.add_handler(officetopdf_handler())
dispatcher.add_handler(addpagenumbers_handler())
dispatcher.add_handler(pdfa_handler())
dispatcher.add_handler(pdftojpg_handler())
dispatcher.add_handler(protectpdf_handler())
dispatcher.add_handler(rotatepdf_handler())
dispatcher.add_handler(splitpdf_handler())
dispatcher.add_handler(unlockpdf_handler())
dispatcher.add_handler(watermark_handler())

updater.start_polling()
