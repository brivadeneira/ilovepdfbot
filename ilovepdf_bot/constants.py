from telegram.ext import Filters

WAIT_FILE_COMPRESS = 0
WAIT_COMPRESS = 1
WAIT_FILE_IMGTOPDF = 0
WAIT_IMGTOPDF = 1
WAIT_FILE_OFFICE = 0
WAIT_OFFICETOPDF = 1
WAIT_FILE_NUMBERS = 0
WAIT_ADDNUMBERS = 1
WAIT_FILE_PDFA = 0
WAIT_PDFTOPDFA = 1
WAIT_FILE_PDFTOJPG = 0
WAIT_PDFTOJPG = 1
WAIT_FILE_PROTECT = 0
WAIT_PASS = 1
WAIT_PROTECT = 2
WAIT_FILE_ROTATE = 0
WAIT_ANGLE = 1
WAIT_ROTATE = 2
WAIT_FILE_SPLIT = 0
WAIT_RANGE = 1
WAIT_SPLIT = 2
WAIT_FILE_UNLOCK = 0
WAIT_UNLOCK = 1
WAIT_FILE_WATERMARK = 0
WAIT_TEXT_MARK = 1
WAIT_WATERMARK = 2

img_filter = Filters.photo | Filters.document
text_filter = Filters.text & ~Filters.command
cancel_filter = Filters.regex(r'cancel') | Filters.regex(r'Cancel')
not_doc_filter = ~Filters.document & ~Filters.command & ~cancel_filter
not_text_filter = ~Filters.text & ~Filters.command