import os
from typing import List

from dotenv import load_dotenv
from pylovepdf.ilovepdf import ILovePdf
from pylovepdf.tools.imagetopdf import ImageToPdf
from pylovepdf.tools.merge import Merge
from pylovepdf.tools.officepdf import OfficeToPdf
from pylovepdf.tools.pagenumber import Pagenumber
from pylovepdf.tools.pdfa import ToPdfA
from pylovepdf.tools.pdftojpg import PdfToJpg
from pylovepdf.tools.protect import Protect
from pylovepdf.tools.rotate import Rotate
from pylovepdf.tools.split import Split
from pylovepdf.tools.unlock import Unlock
from pylovepdf.tools.watermark import Watermark

load_dotenv()
public_key = os.getenv('PUBLIC_KEY')
ilovepdf = ILovePdf(public_key, verify_ssl=True)


def love_execute_task(task, file_path: str) -> None:
    """
    Execute common lines of ilovepdf tasks
    """
    task.set_output_folder(file_path)
    task.execute()
    task.download()
    task.delete_current_task()


def love_compress(file_path: str) -> None:
    """
    Compress a PDF file and save the result in file_path folder
    :param file_path: (str) without extension
    (e.g. ./tmp/file_id for ./tmp/file_id.pdf)
    """
    task = ilovepdf.new_task('compress')
    task.add_file(f"{file_path}.pdf")
    # file_path folder should exist
    love_execute_task(task, file_path)


def love_imgtopdf(file_path: str) -> None:
    """
    Convert an image to a PDF file and save the result in file_id folder
    :param file_path: (str) without extension
    (e.g. ./tmp/file_id for ./tmp/file_id.pdf)
    """
    task = ImageToPdf(public_key, verify_ssl=True, proxies='')
    task.add_file(f"{file_path}.png")
    task.debug = False
    task.orientation = 'portrait'
    task.margin = 0
    task.pagesize = 'fit'
    # file_id folder should exist
    love_execute_task(task, file_path)


Files = List[str]


def love_merge(files: Files, output_dir: str) -> None:
    """
    Merge two or more PDF files and save the result in output_dir folder
    :param files: (list) of each PDF file paths.
    :param output_dir: (str) path of output dir (it should exist)
    """
    task = Merge(public_key, verify_ssl=True, proxies='')
    # two or more files needed
    for file_name in files:
        task.add_file(file_name)
    task.debug = False
    # output_dir folder should exist
    love_execute_task(task, output_dir)


def love_officetopdf(file_path: str, output_dir: str) -> None:
    """
    Convert one or more Office files and save the result in output_dir folder
    (if more than one office file is converted, the result will be a zip file)
    :param file_path: (str)
    :param output_dir: (str) to save the converted file
    """
    task = OfficeToPdf(public_key, verify_ssl=True, proxies='')
    task.debug = False
    task.add_file(file_path)
    love_execute_task(task, output_dir)


def love_addpagenumbers(file_path: str) -> None:
    """
    Add page numbers to a PDF file and save the result in file_path folder
    :param file_path: (str) without extension
    (e.g. ./tmp/file_id for ./tmp/file_id.pdf)
    """
    task = Pagenumber(public_key, verify_ssl=True, proxies='')
    task.debug = False
    task.add_file(f"{file_path}.pdf")
    love_execute_task(task, file_path)


def love_pdfa(file_path: str) -> None:
    """
    Convert a PDF file to PDF/A (the ISO-standardized version)
    and save the result in file_path folder
    :param file_path: (str) without extension
    (e.g. ./tmp/file_id for ./tmp/file_id.pdf)
    """
    task = ToPdfA(public_key, verify_ssl=True, proxies='')
    task.debug = False
    task.add_file(f"{file_path}.pdf")
    love_execute_task(task, file_path)


def love_pdftojpg(file_path: str) -> None:
    """
    Convert a PDF file to PDF/A (the ISO-standardized version)
    and save the result in file_path folder
    :param file_path: (str) without extension
    (e.g. ./tmp/file_id for ./tmp/file_id.pdf)
    """
    task = PdfToJpg(public_key, verify_ssl=True, proxies='')
    task.debug = False
    task.add_file(f"{file_path}.pdf")
    task.pdfjpg_mode = 'pages'
    love_execute_task(task, file_path)


def love_protect(file_path: str, password: str, output_dir: str) -> None:
    """
    Protect a PDF file with a password
    and save the result in output_dir folder
    :param output_dir: (str) to save the protected PDF file
    :param password: (str) to protect the PDF file
    :param file_path: (str) of the PDF to protect
    """
    task = Protect(public_key, verify_ssl=True, proxies='')
    task.debug = False
    task.add_file(file_path)
    task.file_encryption_key = 'ilovepdfbot'
    task.file.password = password
    love_execute_task(task, output_dir)


def love_rotate(file_path: str, output_dir: str, rot: int = 90) -> None:
    """
    Rotate a PDF file and save the result in output_dir folder
    :param rot: (int) angle to rotate the PDF file
    :param file_path: (str) without extension
    :param output_dir: (str) to save the protected PDF file
    (e.g. ./tmp/file_id for ./tmp/file_id.pdf)
    """
    task = Rotate(public_key, verify_ssl=True, proxies='')
    task.debug = False
    task.add_file(file_path)
    task.file.rotate = rot
    love_execute_task(task, output_dir)


def love_split(file_path: str, output_dir: str, range=1):
    """
    Rotate a PDF file and save the result in output_dir folder
    :param range: (int) of split the PDF file
    :param file_path: (str) without extension
    :param output_dir: (str) to save the protected PDF file
    (e.g. ./tmp/file_id for ./tmp/file_id.pdf)
    """
    task = Split(public_key, verify_ssl=True, proxies='')
    task.debug = False
    task.add_file(file_path)
    task.split_mode = 'fixed_range'
    task.fixed_range = range
    love_execute_task(task, output_dir)


def love_unlock(file_path: str, output_dir: str) -> None:
    """
    Rotate a PDF file and save the result in output_dir folder
    :param file_path: (str) without extension
    :param output_dir: (str) to save the protected PDF file
    (e.g. ./tmp/file_id for ./tmp/file_id.pdf)
    """
    task = Unlock(public_key, verify_ssl=True, proxies='')
    task.debug = False
    task.add_file(file_path)
    love_execute_task(task, output_dir)


def love_watermark(file_path: str, output_dir: str, text: str) -> None:
    """
    Embed a watermark to a PDF file and save the result in output_dir folder
    :param text: (str) of watermark
    :param file_path: (str) without extension
    :param output_dir: (str) to save the protected PDF file
    (e.g. ./tmp/file_id for ./tmp/file_id.pdf)
    """
    task = Watermark(public_key, verify_ssl=True, proxies='')
    task.debug = False
    task.add_file(file_path)
    task.mode = 'text'
    task.text = text
    task.rotation = 30
    task.fontsize = 150
    task.transparency = 40
    love_execute_task(task, output_dir)
