import os

from dotenv import load_dotenv
from telegram import ChatAction, ReplyKeyboardRemove, ParseMode
from telegram.ext import CommandHandler, ConversationHandler, MessageHandler
from telegram.ext.dispatcher import run_async

from .constants import *
from .ilovepdf import (love_addpagenumbers, love_compress, love_imgtopdf,
                       love_merge, love_officetopdf, love_pdfa, love_pdftojpg,
                       love_protect, love_rotate, love_split, love_unlock,
                       love_watermark)
from .utils import (ask_file, bye, del_tmp, file_ok, img_ok, result_file,
                    unzip_file, usr_msg)

load_dotenv()
token = os.getenv('BOT_TOKEN')


# cancel action
def cancel_without_async(update):
    update.effective_message.reply_text(
        "🚫 Action cancelled"
    )
    return ConversationHandler.END


# compress functions
def compress_pdf(update, context):
    """
    Return ConversationHandler.END after answer to the user
    with the compressed PDF file or an error message.
    :param update: (telegram.update.Update) the update object
    :param context: (telegram.ext.callbackcontext.CallbackContext),
    the context object
    :return: (ConversationHandler.END) after send the file or message
    """

    doc = update.message.document
    if file_ok(update=update, usr_file=doc):
        usr_msg(update=update,
                msg="please wait a moment while I compress it for you...",
                error=False)
        file_id = doc.file_id
        usr_file = context.bot.getFile(file_id)
        file_path = f"./tmp/{file_id}"
        usr_file.download(f"{file_path}.pdf")
        # a file_id folder is created to know where the file is
        os.mkdir(file_path)
        # compress the file
        love_compress(file_path)
        # get the path of the compressed file
        compressed_file = result_file(file_path)
        if compressed_file:
            update.effective_message.chat.send_action(
                ChatAction.UPLOAD_DOCUMENT)
            update.effective_message.reply_document(
                document=open(f"{file_path}/{compressed_file}", "rb"),
                caption="✨ Here is your compressed file",
            )
        else:
            usr_msg(update)
        bye(update)
    else:
        compress(update, context)
    del_tmp()
    return ConversationHandler.END


@run_async
def compress(update, context):
    msg = "📄 Send me the PDF file you want to compress, please"
    return ask_file(update, msg, WAIT_FILE_COMPRESS)


def error_compress(update, context):
    msg = "That is not a PDF file 😔, try again."
    usr_msg(update=update, msg=msg, error=False)
    return compress(update, context)


def compress_handler():
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("compress", compress)],
        states={
            WAIT_FILE_COMPRESS: [
                MessageHandler(Filters.document, compress_pdf),
                MessageHandler(not_doc_filter, error_compress)],
        },
        fallbacks=[
            CommandHandler("cancel", cancel_without_async)
        ],
        allow_reentry=True,
    )

    return conv_handler


# imgtopdf functions
@run_async
def imgtopdf(update, context):
    global images
    images = []
    msg = "🖼 Send me an image file you want to convert, please. " \
          "*(I strongly recommend you DO NOT compress it.)*"
    return ask_file(update, msg, WAIT_FILE_IMGTOPDF)


def check_img(update, context):
    """
    Check if the user has sent a valid image file,
    and show a message asking an image file or 'done' word
    :param update: (telegram.update.Update) the update object
    :param context: (telegram.ext.callbackcontext.CallbackContext),
    the context object
    :return: (int) WAIT_MERGE constant according to handler state
    """
    img = img_ok(update=update)
    if img:
        file_id = img.file_id
        file_path = f"./tmp/{file_id}"
        usr_file = context.bot.getFile(file_id)
        usr_file.download(f"{file_path}.png")
        images.append(file_path)

    msg = "Send me the word *'done'* if you want the PDF file, " \
          "or send me more images 🖼"
    if images:
        return ask_file(update, msg, WAIT_IMGTOPDF)
    else:
        return imgtopdf(update, context)


def check_text(update, context):
    """
    Check user text according to:
    'done' -> convert images to pdf
    'cancel' -> end the conversation
    other -> send a message to the user

    :param update: (telegram.update.Update) the update object
    :return: (int) WAIT_MERGE constant according to handler state
    """
    text = update.effective_message.text
    if text:
        if text.lower() == 'done':
            if images:
                usr_msg(update=update,
                        msg=f"I received {len(images)} images, "
                            f"please wait a moment while "
                            f"I convert them for you...",
                        error=False)
                # convert images to PDF
                img_to_pdf(update, images)
            else:
                return ConversationHandler.END
        elif text.lower() == 'cancel':
            return cancel_without_async(update)
        else:
            msg = "I can't understand you 😔, sorry, try again"
            usr_msg(update, msg=msg, error=False)
            msg = "Send me the word *'done'* if you want the PDF file, " \
                  "or send me more images 🖼"
            return ask_file(update, msg, WAIT_IMGTOPDF)


def img_to_pdf(update, images):
    """
    Answer to the user with the PDF file
    or an error message.
    :param update: (telegram.update.Update) the update object
    :param images: (list) of each image paths
    :return: (ConversationHandler.END) after send the file or message
    """
    pdfs = []
    merged_file = ''
    pdf_file = ''
    final_file = None

    # convert each image to PDF
    for file_path in images:
        love_imgtopdf(file_path)
        converted_file = result_file(file_path)
        if converted_file:
            pdfs.append(f"{file_path}/{converted_file}")
    if images:
        last_file_id = images[-1]  # .split('.')[0]
        output_dir = f"{last_file_id}-merge"
        if len(images) == 1:
            pdf_file = pdfs[0]
            if pdf_file:
                final_file = pdf_file
        else:
            # merge all PDF files
            love_merge(files=pdfs, output_dir=output_dir)
            merged_file = result_file(output_dir)

            if merged_file:
                final_file = f"{output_dir}/{merged_file}"

        if final_file:
            update.effective_message.chat.send_action(
                ChatAction.UPLOAD_DOCUMENT)
            update.effective_message.reply_document(
                document=open(final_file, "rb"),
                caption="✨ Here is your PDF file", )
        else:
            usr_msg(update, error=True)
    bye(update)
    del_tmp()
    return ConversationHandler.END


def error_imgtopdf(update, context):
    msg = "That is not an image 😔, try again."
    usr_msg(update=update, msg=msg, error=False)

    return imgtopdf(update, context)


def imgtopdf_handler():
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("imgtopdf", imgtopdf)],
        states={
            WAIT_FILE_IMGTOPDF: [
                MessageHandler(img_filter, check_img),
                MessageHandler(text_filter, check_text)],
            WAIT_IMGTOPDF: [
                MessageHandler(img_filter, check_img),
                MessageHandler(text_filter, check_text),
            ],
        },
        fallbacks=[
            CommandHandler("cancel", cancel_without_async)
        ],
        allow_reentry=True,
    )

    return conv_handler


# office to pdf functions
@run_async
def officetopdf(update, context):
    office_ext = ('odt', 'doc', 'docx',
                  'ods', 'xls', 'xlsx',
                  'odp', 'ppt', 'pptx')
    msg = f"📄 Send me an office file you want to convert, please. " \
          f"Extensions allowed are: {', '.join(office_ext)}",
    return ask_file(update, msg, WAIT_OFFICETOPDF)


def office_to_pdf(update, context):
    """
    Check if the user has sent a valid office doc
    :param update: (telegram.update.Update) the update object
    :param context: (telegram.ext.callbackcontext.CallbackContext),
    the context object
    :return: (int) WAIT_CONVERT constant according to handler state
    """
    doc = update.message.document
    valid_ext = {'opendocument.text': 'docx',
                 'wordprocessingml.document': 'docx',
                 'sheet': 'xls', 'presentation': 'ppt'}

    file_ext = file_ok(update=update, usr_file=doc,
                       ext=tuple(valid_ext.keys()),
                       obj='Office file', send_msg=True)
    if file_ext:
        usr_msg(update=update,
                msg="please wait a moment while I convert it for you...",
                error=False)
        ext = valid_ext[file_ext]
        file_id = doc.file_id
        file_path = f"./tmp/{file_id}"
        usr_file = context.bot.getFile(file_id)
        usr_file.download(f"{file_path}.{ext}")
        # a file_id folder is created to know where the file is
        output_dir = file_path
        os.mkdir(output_dir)
        love_officetopdf(f"{file_path}.{ext}", output_dir)
        converted_file = result_file(output_dir)
        if converted_file:
            update.effective_message.chat.send_action(
                ChatAction.UPLOAD_DOCUMENT)
            update.effective_message.reply_document(
                document=open(f"{file_path}/{converted_file}", "rb"),
                caption="✨ Here is your PDF file",
            )
        else:
            usr_msg(update)
        bye(update)
        del_tmp()
    return ConversationHandler.END


def error_office(update, context):
    msg = "That is not an Office file 😔, try again."
    usr_msg(update=update, msg=msg, error=False)

    return officetopdf(update, context)


def officetopdf_handler():
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("officetopdf", officetopdf)],
        states={
            WAIT_OFFICETOPDF: [
                MessageHandler(Filters.document, office_to_pdf),
                MessageHandler(not_doc_filter, error_office)],
        },
        fallbacks=[
            CommandHandler("cancel", cancel_without_async)
        ],
        allow_reentry=True,
    )

    return conv_handler


# addpagenumbers functions
def add_page_numbers(update, context):
    """
    Return ConversationHandler.END after answer to the user
    with the PDF file with page numbers or an error message.
    :param update: (telegram.update.Update) the update object
    :param context: (telegram.ext.callbackcontext.CallbackContext),
    the context object
    :return: (ConversationHandler.END) after send the file or message
    """
    doc = update.message.document
    if file_ok(update=update, usr_file=doc):
        msg = "please wait a moment while " \
              "I add page numbers to it for you...",
        usr_msg(update=update, msg=msg, error=False)
        file_id = doc.file_id
        usr_file = context.bot.getFile(file_id)
        file_path = f"./tmp/{file_id}"
        usr_file.download(f"{file_path}.pdf")
        # a file_id folder is created to know where the file is
        os.mkdir(file_path)
        # add page numbers to the file
        love_addpagenumbers(file_path)
        # get the path of the result file
        pagenumbers_file = result_file(file_path)
        if pagenumbers_file:
            update.effective_message.chat.send_action(
                ChatAction.UPLOAD_DOCUMENT)
            update.effective_message.reply_document(
                document=open(f"{file_path}/{pagenumbers_file}", "rb"),
                caption="✨ Here is your compressed file",
            )
        else:
            usr_msg(update)
        bye(update)
    else:
        return addpagenumbers(update, context)
    del_tmp()
    return ConversationHandler.END


@run_async
def addpagenumbers(update, context):
    msg = "📄 Send me the PDF file you want to add page numbers, please"
    return ask_file(update, msg, WAIT_ADDNUMBERS)


def error_pagesnumber(update, context):
    msg = "That is not a PDF file 😔, try again."
    usr_msg(update=update, msg=msg, error=False)

    return addpagenumbers(update, context)


def addpagenumbers_handler():
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("addpagenumbers", addpagenumbers)],
        states={
            WAIT_ADDNUMBERS: [
                MessageHandler(Filters.document, add_page_numbers),
                MessageHandler(not_doc_filter, error_pagesnumber)],
        },
        fallbacks=[
            CommandHandler("cancel", cancel_without_async)
        ],
        allow_reentry=True,
    )

    return conv_handler


# pdfa functions
def pdf_to_pdfa(update, context):
    """
    Return ConversationHandler.END after answer to the user
    with the PDF file converted to PDF/A ISO-standardized.
    :param update: (telegram.update.Update) the update object
    :param context: (telegram.ext.callbackcontext.CallbackContext),
    the context object
    :return: (ConversationHandler.END) after send the file or message
    """

    doc = update.message.document
    if file_ok(update=update, usr_file=doc):
        msg = "please wait a moment while " \
              "I convert it to PDF/A ISO standard for you...",
        usr_msg(update=update, msg=msg, error=False)
        file_id = doc.file_id
        usr_file = context.bot.getFile(file_id)
        file_path = f"./tmp/{file_id}"
        usr_file.download(f"{file_path}.pdf")
        # a file_id folder is created to know where the file is
        os.mkdir(file_path)
        # add page numbers to the file
        love_pdfa(file_path)
        # get the path of the compressed file
        pdfa_file = result_file(file_path)
        if pdfa_file:
            update.effective_message.chat.send_action(
                ChatAction.UPLOAD_DOCUMENT)
            update.effective_message.reply_document(
                document=open(f"{file_path}/{pdfa_file}", "rb"),
                caption="✨ Here is your PDF/A file",
            )
        else:
            usr_msg(update)
        bye(update)
    del_tmp()
    return ConversationHandler.END


@run_async
def pdfa(update, context):
    msg = "📄 Send me the PDF file you want to convert to PDF/A, please"
    return ask_file(update, msg, WAIT_PDFTOPDFA)


def error_pdfa(update, context):
    msg = "That is not a PDF file 😔, try again."
    usr_msg(update=update, msg=msg, error=False)

    return pdfa(update, context)


def pdfa_handler():
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("pdfa", pdfa)],
        states={
            WAIT_PDFTOPDFA: [MessageHandler(Filters.document, pdf_to_pdfa),
                             MessageHandler(not_doc_filter, error_pdfa)],
        },
        fallbacks=[
            CommandHandler("cancel", cancel_without_async)
        ],
        allow_reentry=True,
    )

    return conv_handler


# pdftojpg functions
def pdf_to_jpg(update, context):
    """
    Return ConversationHandler.END after answer to the user with the jpg file(s)
    :param update: (telegram.update.Update) the update object
    :param context: (telegram.ext.callbackcontext.CallbackContext),
    the context object
    :return: (ConversationHandler.END) after send the file or message
    """

    doc = update.message.document
    if file_ok(update=update, usr_file=doc):
        msg = "please wait a moment while " \
              "I convert it to jpg for you..."
        usr_msg(update=update, msg=msg, error=False)
        file_id = doc.file_id
        usr_file = context.bot.getFile(file_id)
        file_path = f"./tmp/{file_id}"
        usr_file.download(f"{file_path}.pdf")
        # a file_id folder is created to know where the file is
        os.mkdir(file_path)
        # add page numbers to the file
        love_pdftojpg(file_path)
        # get the path of the compressed file
        jpg_zip_file = result_file(file_path)
        if jpg_zip_file:
            jpg_files = unzip_file(zip_path=f"{file_path}/{jpg_zip_file}",
                                   output_dir=f"{file_path}-unzip")

            for num, file_path in enumerate(jpg_files[::-1]):
                update.effective_message.chat.send_action(
                    ChatAction.UPLOAD_PHOTO)
                update.effective_message.reply_document(
                    document=open(file_path, "rb"),
                    caption=f"🖼 page {num + 1} of your PDF file",
                )
            msg = "✨ Here are your jpg images"
            usr_msg(update=update, msg=msg, error=False)
        else:
            usr_msg(update)
        bye(update)
    del_tmp()
    return ConversationHandler.END


@run_async
def pdftojpg(update, context):
    msg = "📄 Send me the PDF file you want to convert into jpg images, please"
    return ask_file(update, msg, WAIT_PDFTOJPG)


def error_pdftojpg(update, context):
    msg = "That is not a PDF file 😔, try again."
    usr_msg(update=update, msg=msg, error=False)

    return pdftojpg(update, context)


def pdftojpg_handler():
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("pdftojpg", pdftojpg)],
        states={
            WAIT_PDFTOJPG: [MessageHandler(Filters.document, pdf_to_jpg),
                            MessageHandler(not_doc_filter, error_pdftojpg)],
        },
        fallbacks=[
            CommandHandler("cancel", cancel_without_async)
        ],
        allow_reentry=True,
    )

    return conv_handler


# protectpdf functions
global pdf_to_protect
pdf_to_protect = None


@run_async
def protectpdf(update, context):
    msg = "📄 Send me the PDF file you want to protect, please. "
    return ask_file(update, msg, WAIT_PROTECT)


def check_pdf_protect(update, context):
    """
    Check if the user has sent a valid PDF file,
    and show a message asking a password
    :param update: (telegram.update.Update) the update object
    :param context: (telegram.ext.callbackcontext.CallbackContext),
    the context object
    :return: (int) WAIT_CONVERT constant according to handler state
    """
    doc = update.message.document
    if file_ok(update=update, usr_file=doc):
        file_id = doc.file_id
        file_path = f"./tmp/{file_id}"
        os.mkdir(file_path)
        usr_file = context.bot.getFile(file_id)
        usr_file.download(f"{file_path}.pdf")
        global pdf_to_protect
        pdf_to_protect = f"{file_path}.pdf"
        msg = "Send me the password to protect the PDF file, please 🔑"
        return ask_file(update, msg, WAIT_PROTECT)


def check_pass(update, context):
    """
    Check the password

    :param update: (telegram.update.Update) the update object
    :return: (int) WAIT_MERGE constant according to handler state
    """
    text = update.effective_message.text
    if text:
        if text.lower() == 'cancel':
            return ConversationHandler.END
        else:
            msg = "I received the password"
            if pdf_to_protect:
                msg += ", please wait a moment while " \
                       "I protect the file for you..."
                usr_msg(update=update, msg=msg, error=False)
                # protect PDF
                protect_pdf(update, text)
            else:
                msg += ", but I still need the PDF file to protect"
                usr_msg(update=update, msg=msg, error=False)
                protectpdf(update, context)


def protect_pdf(update, password):
    """
    Answer to the user with the protected PDF file
    or an error message.
    :param password: (str) to protect the PDF file
    :param update: (telegram.update.Update) the update object
    :return: (ConversationHandler.END) after send the file or message
    """
    if pdf_to_protect:
        output_dir = pdf_to_protect.split('.pdf')[0]
        love_protect(pdf_to_protect, password, output_dir)
        protected_file = result_file(output_dir)
        if protected_file:
            update.effective_message.chat.send_action(
                ChatAction.UPLOAD_DOCUMENT)
            update.effective_message.reply_document(
                document=open(f"{output_dir}/{protected_file}", "rb"),
                caption="✨ Here is your protected PDF file",
            )
        else:
            usr_msg(update)
        bye(update)
        del_tmp()
        return ConversationHandler.END


def error_protect(update, context):
    msg = "That is not a PDF 😔, try again."
    usr_msg(update=update, msg=msg, error=False)

    return protectpdf(update, context)


def protectpdf_handler():
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("protectpdf", protectpdf)],
        states={
            WAIT_PROTECT: [
                MessageHandler(Filters.document, check_pdf_protect),
                MessageHandler(text_filter, check_pass),
                MessageHandler(not_doc_filter, error_protect)
            ],
        },
        fallbacks=[
            CommandHandler("cancel", cancel_without_async)
        ],
        allow_reentry=True,
    )

    return conv_handler


# splitpdf functions
global pdf_to_split
pdf_to_split = None


@run_async
def splitpdf(update, context):
    msg = "📄 Send me the PDF file you want to split, please. "
    return ask_file(update, msg, WAIT_FILE_SPLIT)


def check_pdf_split(update, context):
    """
    Check if the user has sent a valid PDF file,
    and show a message asking a rotate value
    :param update: (telegram.update.Update) the update object
    :param context: (telegram.ext.callbackcontext.CallbackContext),
    the context object
    :return: (int) WAIT_CONVERT constant according to handler state
    """
    doc = update.message.document
    if file_ok(update=update, usr_file=doc):
        file_id = doc.file_id
        file_path = f"./tmp/{file_id}"
        os.mkdir(file_path)
        usr_file = context.bot.getFile(file_id)
        usr_file.download(f"{file_path}.pdf")
        global pdf_to_split
        pdf_to_split = f"{file_path}.pdf"
        msg = "Send me the range you want to split the file, please ✂️. " \
              "(e.g. 2 for split 2 pages per file)"
        return ask_file(update, msg, WAIT_RANGE)
    else:
        return splitpdf(update, context)


def check_range(update, context):
    """
    Check the range number
    :param update: (telegram.update.Update) the update object
    :return: (int) WAIT_MERGE constant according to handler state
    """
    text = update.effective_message.text
    if text:
        try:
            int(text)
            msg = f"I received the range, please wait a moment while I split " \
                  f"the file {text} pages per file for you..."
            usr_msg(update=update, msg=msg, error=False)
            # split PDF
            split_pdf(update, text)
        except ValueError:
            msg = "This range is not valid 😔, it must be an interger number, " \
                  "try again."
            usr_msg(update=update, msg=msg, error=False)
            return WAIT_RANGE


def split_pdf(update, range):
    """
    Answer to the user with the rotated PDF file
    or an error message.
    :param angle: (str) to rotate the PDF file
    :param update: (telegram.update.Update) the update object
    :return: (ConversationHandler.END) after send the file or message
    """
    if pdf_to_split:
        output_dir = pdf_to_split.split('.pdf')[0]
        love_split(pdf_to_split, output_dir, int(range))
        splitted_file = result_file(output_dir)
        if splitted_file:
            if splitted_file.endswith('.zip'):
                pdf_files = unzip_file(zip_path=f"{output_dir}/{splitted_file}",
                                       output_dir=f"{output_dir}-unzip")
                for num, file_path in enumerate(pdf_files[::-1]):
                    update.effective_message.chat.send_action(
                        ChatAction.UPLOAD_PHOTO)
                    update.effective_message.reply_document(
                        document=open(file_path, "rb"),
                        caption=f"📄 {num + 1} range of your PDF file",
                    )
                msg = "✨ Here are your PDF files"
                usr_msg(update=update, msg=msg, error=False)
            else:
                update.effective_message.chat.send_action(
                    ChatAction.UPLOAD_PHOTO)
                update.effective_message.reply_document(
                    document=open(f"{output_dir}/{splitted_file}", "rb"),
                    caption=f"The range you sent me generated just one PDF file.",
                )
    else:
        usr_msg(update)
    bye(update)
    del_tmp()
    return ConversationHandler.END


def error_split(update, context):
    msg = "That is not a PDF 😔, try again."
    usr_msg(update=update, msg=msg, error=False)

    return splitpdf(update, context)


def error_range_split(update, context):
    msg = "That is not a range 😔, try again."
    usr_msg(update=update, msg=msg, error=False)

    return WAIT_RANGE


def splitpdf_handler():
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("splitpdf", splitpdf)],
        states={
            WAIT_FILE_SPLIT: [MessageHandler(img_filter, check_pdf_split),
                              MessageHandler(not_doc_filter, error_split)],
            WAIT_RANGE: [MessageHandler(text_filter, check_range),
                         MessageHandler(not_text_filter, error_range_split)],
        },
        fallbacks=[
            CommandHandler("cancel", cancel_without_async)
        ],
        allow_reentry=True,
    )

    return conv_handler


# rotatepdf functions

global pdf_to_rotate, allowed_rot
pdf_to_rotate = ''
allowed_rot = ('90', '180')


@run_async
def rotatepdf(update, context):
    msg = "📄 Send me the PDF file you want to rotate, please. "
    return ask_file(update, msg, WAIT_FILE_ROTATE)


def check_pdf_rotate(update, context):
    """
    Check if the user has sent a valid PDF file,
    and show a message asking a rotate value
    :param update: (telegram.update.Update) the update object
    :param context: (telegram.ext.callbackcontext.CallbackContext),
    the context object
    :return: (int) WAIT_CONVERT constant according to handler state
    """
    doc = update.message.document
    if file_ok(update=update, usr_file=doc):
        file_id = doc.file_id
        file_path = f"./tmp/{file_id}"
        os.mkdir(file_path)
        usr_file = context.bot.getFile(file_id)
        usr_file.download(f"{file_path}.pdf")
        global pdf_to_rotate
        pdf_to_rotate = f"{file_path}.pdf"
        msg = "Send me the rotation angle you want, please ↩️. " \
              f"*Allowed angles are: {' ,'.join(allowed_rot)}.*"
        return ask_file(update, msg, WAIT_ANGLE)


def check_angle(update, context):
    """
    Check the rotation angle
    :param update: (telegram.update.Update) the update object
    :return: (int) WAIT_MERGE constant according to handler state
    """
    text = update.effective_message.text
    if text:
        if text in allowed_rot:
            msg = f"I received the angle, please wait a moment while " \
                  f"I rotate a {text} angle the file for you..."
            usr_msg(update=update, msg=msg, error=False)
        else:
            msg = f"This angle is not allowed 😔, *allowed angles are: " \
                  f"{' ,'.join(allowed_rot)}, *try again."
            usr_msg(update=update, msg=msg, error=False)
            return WAIT_ANGLE
        # rotate PDF
        rotate_pdf(update, text)


def rotate_pdf(update, angle):
    """
    Answer to the user with the rotated PDF file
    or an error message.
    :param angle: (str) to rotate the PDF file
    :param update: (telegram.update.Update) the update object
    :return: (ConversationHandler.END) after send the file or message
    """
    if pdf_to_rotate:
        output_dir = pdf_to_rotate.split('.pdf')[0]
        love_rotate(pdf_to_rotate, output_dir, int(angle))
        rotated_file = result_file(output_dir)
        if rotated_file:
            update.effective_message.chat.send_action(
                ChatAction.UPLOAD_DOCUMENT)
            update.effective_message.reply_document(
                document=open(f"{output_dir}/{rotated_file}", "rb"),
                caption=f"✨ Here is your {angle} rotated PDF file",
            )
        else:
            usr_msg(update)
        bye(update)
        del_tmp()
        return ConversationHandler.END


def error_rotate(update, context):
    msg = "That is not a PDF 😔, try again."
    usr_msg(update=update, msg=msg, error=False)

    return rotatepdf(update, context)


def error_angle(update, context):
    msg = "That is not an angle 😔, try again."
    usr_msg(update=update, msg=msg, error=False)

    return ask_file(update, msg, WAIT_ANGLE)


def rotatepdf_handler():
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("rotatepdf", rotatepdf)],
        states={
            WAIT_FILE_ROTATE: [MessageHandler(Filters.document, check_pdf_rotate),
                               MessageHandler(not_doc_filter, error_rotate)],
            WAIT_ANGLE: [MessageHandler(not_text_filter, error_angle),
                         MessageHandler(text_filter, check_angle)],
        },
        fallbacks=[
            CommandHandler("cancel", cancel_without_async)
        ],
        allow_reentry=True,
    )

    return conv_handler


# unlock functions
def unlock_pdf(update, context):
    """
    Return ConversationHandler.END after answer to the user
    with the PDF file unlocked.
    :param update: (telegram.update.Update) the update object
    :param context: (telegram.ext.callbackcontext.CallbackContext),
    the context object
    :return: (ConversationHandler.END) after send the file or message
    """

    doc = update.message.document
    if file_ok(update=update, usr_file=doc):
        msg = "please wait a moment while I unlock it for you..."
        usr_msg(update=update, msg=msg, error=False)
        file_id = doc.file_id
        usr_file = context.bot.getFile(file_id)
        file_path = f"./tmp/{file_id}"
        usr_file.download(f"{file_path}.pdf")
        # a file_id folder is created to know where the file is
        os.mkdir(file_path)
        # unlock the file
        love_unlock(f"{file_path}.pdf", file_path)
        # get the path of the compressed file
        unlocked_file = result_file(file_path)
        if unlocked_file:
            update.effective_message.chat.send_action(
                ChatAction.UPLOAD_DOCUMENT)
            update.effective_message.reply_document(
                document=open(f"{file_path}/{unlocked_file}", "rb"),
                caption="✨ Here is your unlocked file",
            )
        else:
            usr_msg(update)
        bye(update)
    del_tmp()
    return ConversationHandler.END


@run_async
def unlockpdf(update, context):
    msg = "📄 Send me the PDF file you want to unlock, please"
    return ask_file(update, msg, WAIT_UNLOCK)


def error_unlock(update, context):
    msg = "That is not a PDF file 😔, try again."
    usr_msg(update=update, msg=msg, error=False)

    return unlockpdf(update, context)


def unlockpdf_handler():
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("unlockpdf", unlockpdf)],
        states={
            WAIT_UNLOCK: [MessageHandler(Filters.document, unlock_pdf),
                          MessageHandler(not_doc_filter, error_unlock)],
        },
        fallbacks=[
            CommandHandler("cancel", cancel_without_async)
        ],
        allow_reentry=True,
    )

    return conv_handler


# watermark functions
global pdf_to_mark
pdf_to_mark = None


@run_async
def watermarkpdf(update, context):
    msg = "📄 Send me the PDF file you want to apply a watermark, please. "
    return ask_file(update, msg, WAIT_FILE_WATERMARK)


def check_pdf_mark(update, context):
    """
    Check if the user has sent a valid PDF file,
    and show a message asking a rotate value
    :param update: (telegram.update.Update) the update object
    :param context: (telegram.ext.callbackcontext.CallbackContext),
    the context object
    :return: (int) WAIT_CONVERT constant according to handler state
    """
    doc = update.message.document
    if file_ok(update=update, usr_file=doc):
        file_id = doc.file_id
        file_path = f"./tmp/{file_id}"
        os.mkdir(file_path)
        usr_file = context.bot.getFile(file_id)
        usr_file.download(f"{file_path}.pdf")
        global pdf_to_mark
        pdf_to_mark = f"{file_path}.pdf"
        msg = "Send me the text you want to apply in the file, please 💧. "
        return ask_file(update, msg, WAIT_TEXT_MARK)
    else:
        return watermarkpdf(update, context)


def check_text_mark(update, context):
    """
    Check the watermark text
    :param update: (telegram.update.Update) the update object
    :return: (int) WAIT_MERGE constant according to handler state
    """
    text = update.effective_message.text
    if text:
        msg = "I received the text, please wait a moment while I apply " \
              f"'{text}' as a watermark for you..."
        usr_msg(update=update, msg=msg, error=False)
        # apply watermark PDF
        watermark_pdf(update, text)
    else:
        msg = f"You didn't send me a text 😔, try again."
        usr_msg(update=update, msg=msg, error=False)
        return WAIT_WATERMARK


def watermark_pdf(update, text):
    """
    Answer to the user with the PDF file with a watermark
    or an error message.
    :param angle: (str) to rotate the PDF file
    :param update: (telegram.update.Update) the update object
    :return: (ConversationHandler.END) after send the file or message
    """
    if pdf_to_mark:
        output_dir = pdf_to_mark.split('.pdf')[0]
        love_watermark(pdf_to_mark, output_dir, text)
        marked_file = result_file(output_dir)
        if marked_file:
            if marked_file.endswith('.zip'):
                pdf_files = unzip_file(zip_path=f"{output_dir}/{marked_file}",
                                       output_dir=f"{output_dir}-unzip")
                for num, file_path in enumerate(pdf_files[::-1]):
                    update.effective_message.chat.send_action(
                        ChatAction.UPLOAD_PHOTO)
                    update.effective_message.reply_document(
                        document=open(file_path, "rb"),
                        caption=f"📄 {num + 1} range of your PDF file",
                    )
                msg = "✨ Here are your PDF files"
                usr_msg(update=update, msg=msg, error=False)
            else:
                update.effective_message.chat.send_action(
                    ChatAction.UPLOAD_PHOTO)
                update.effective_message.reply_document(
                    document=open(f"{output_dir}/{marked_file}", "rb"),
                    caption="✨ Here is your marked file",
                )
    else:
        usr_msg(update)
    bye(update)
    del_tmp()
    return ConversationHandler.END


def error_file_watermark(update, context):
    msg = "That is not a PDF file 😔, try again."
    usr_msg(update=update, msg=msg, error=False)

    return watermarkpdf(update, context)


def error_text_mark(update, context):
    msg = "That is not a valid text to the watermark 😔, try again."
    usr_msg(update=update, msg=msg, error=False)

    msg = "Send me the text you want to apply in the file, please 💧. "
    return ask_file(update, msg, WAIT_TEXT_MARK)


def watermark_handler():
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("watermark", watermarkpdf)],
        states={
            WAIT_FILE_WATERMARK: [
                MessageHandler(Filters.document, check_pdf_mark),
                MessageHandler(not_doc_filter, error_file_watermark)],
            WAIT_TEXT_MARK: [
                MessageHandler(text_filter, check_text_mark),
                MessageHandler(not_text_filter, error_text_mark)
            ],
        },
        fallbacks=[
            CommandHandler("cancel", cancel_without_async)
        ],
        allow_reentry=True,
    )

    return conv_handler

