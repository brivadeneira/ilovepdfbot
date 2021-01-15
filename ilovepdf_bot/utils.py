import os
import shutil
import zipfile
from typing import List, Union

from telegram import ParseMode, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.constants import MAX_FILESIZE_DOWNLOAD


def ask_file(update: str, msg: str, const_state: int) -> int:
    """
    Show a message asking a file or cancel button

    :param const_state: (int) constant state according to the handler
    :param update: (telegram.update.Update) the update object
    :param msg: (str) to show the user
    :return: (int) WAIT constant according to handler state
    """
    reply_markup = ReplyKeyboardMarkup(
        [["Cancel"]], resize_keyboard=True,
        one_time_keyboard=True
    )
    update.effective_message.reply_text(
        msg,
        reply_markup=reply_markup,
        parse_mode=ParseMode.MARKDOWN,
    )
    return const_state


def is_too_large(usr_file: str) -> bool:
    """
    Return True is the file is higher than the max allowed,
    False otherwise.
    :param usr_file: (str) path of user file
    :return: (bool)
    """
    if usr_file.file_size >= MAX_FILESIZE_DOWNLOAD:
        return True
    else:
        return False


def usr_msg(update, msg: str = '', error: bool = True) -> None:
    """
    Send an (undefined) error message to the user
    :param msg: (str) to show to the user
    :param error: (bool) If True, send a generic error message to the user
    :param update: (telegram.update.Update) the update object
    :return: None
    """
    if error:
        update.effective_message.reply_text(
            "An error occured 😔, sorry.",
            reply_markup=ReplyKeyboardRemove(),
            parse_mode=ParseMode.MARKDOWN,
        )
    if msg:
        update.effective_message.reply_text(
            msg,
            reply_markup=ReplyKeyboardRemove(),
            parse_mode=ParseMode.MARKDOWN,
        )


def status_usr_msg(update, status='ok', obj='PDF file') -> None:
    """
    Send a message to the user according to the status and obj
    :param update: (telegram.update.Update) the update object
    :param status: (str) 'ok', 'too large', 'invalid' or other
    :param obj: (str) type of object, e.g. 'PDF file' or 'image'
    :return: None
    """
    if status == 'ok':
        update.effective_message.reply_text(
            f"I received your {obj} correctly 😄",
            reply_markup=ReplyKeyboardRemove()
        )
    elif status == 'too large':
        update.effective_message.reply_text(
            f"The {obj} you sent is {status} 😔, try again",
            reply_markup=ReplyKeyboardRemove()
        )
    elif status == 'invalid':
        update.effective_message.reply_text(
            f"What you sent is not a valid {obj} 😔, try again",
            reply_markup=ReplyKeyboardRemove()
        )
    else:
        update.effective_message.reply_text(
            f"Something went wrong with the {obj} you sent me 😔: {status}",
            reply_markup=ReplyKeyboardRemove()
        )


def bye(update) -> None:
    """
    Remove files an directories created during process,
    and send a bye message to the user.
    :param update: (telegram.update.Update) the update object
    :return: None
    """
    update.effective_message.reply_text(
        "Thank you, see you soon! 👋",
        reply_markup=ReplyKeyboardRemove()
    )


def del_tmp() -> None:
    """
    Remove tmp file content
    :return: None
    """
    for elem in os.listdir('./tmp'):
        path = f"./tmp/{elem}"
        if os.path.isfile(path):
            os.remove(path)
        else:
            shutil.rmtree(path)


def file_ok(update, usr_file, ext=('pdf',), obj='PDF file', send_msg=True) -> str:
    """
    Check a usr file, send ok, too_large or invalid message
    :param obj: (str) type of object, e.g. 'PDF file' or 'image'
    :param update: (telegram.update.Update) the update object
    :param usr_file: (telegram.update.message.document) or
    (telegram.update.message.photo) the user file object
    :param ext: (tuple) with valid extensions, e.g. ('png', 'jpg')
    :param send_msg: (bool) if True, send a message
    :return: (str) With the extension if file is ok
    """
    if not usr_file:
        status_usr_msg(update=update, status='invalid', obj=obj)
        return None

    if is_too_large(usr_file):
        if send_msg:
            status_usr_msg(update=update, status='too large', obj=obj)
            return None

    file_ext = ''
    for extension in ext:
        if usr_file.mime_type.lower().endswith(ext):
            file_ext = extension
            break

    if file_ext:
        if send_msg:
            status_usr_msg(update=update, status='ok', obj=obj)
    else:
        if send_msg:
            status_usr_msg(update=update, status='invalid', obj=obj)

    return file_ext


def img_ok(update, send_msg=True):
    """
    Return True if the user has sent a valid image (photo or file),
    False otherwise.
    :param update: (telegram.update.Update) the update object
    :param send_msg: (bool) if True, send a message
    :return: (telegram.files.photosize.PhotoSize
    or telegram.files.document.Document)
    if user document/foto is valid, None otherwise
    """
    if update.message.document:
        if not update.message.document.mime_type.startswith("image"):
            if send_msg:
                status_usr_msg(update=update, status='invalid', obj='image')
            img = None
        else:
            img = update.message.document
    else:
        img = update.message.photo[-1]
        if img:
            if img.file_size > MAX_FILESIZE_DOWNLOAD:
                if send_msg:
                    status_usr_msg(update, 'too large', 'image')
                img = None
    if img and send_msg:
        status_usr_msg(update, 'ok', 'image')
    return img


def result_file(file_path: str) -> Union[str, None]:
    """
    Return a file path if it and the file_path directory exist
    :param file_path: (str) where should be the file (e.g. ./tmp/file_id)
    :return: (str) the file path in the directory if it exists,
    None otherwise
    """
    if not os.path.isdir(file_path):
        return None
    else:
        file_list = list()
        for file in os.listdir(file_path):
            file_list.append(file)
        if not file_list or len(file_list) > 1:
            # it should be just one file per file_id directory
            return None
        else:
            return file_list[0]


UnzipFiles = List[str]


def unzip_file(zip_path: str, output_dir: str) -> UnzipFiles:
    """
    Return a list of each file paths after unzip
    :param output_dir: (str) where files will be saved
    :param zip_path: (str) path of zip file
    :return files: (list) of each file paths
    """
    files = []
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(output_dir)
    for file_path in os.listdir(output_dir):
        files.append(f"{output_dir}/{file_path}")
    return files
