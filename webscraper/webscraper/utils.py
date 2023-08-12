import re
import string
import unicodedata
import dateutil.parser as dparser
from datetime import datetime as dt

from scrapy.linkextractors import IGNORED_EXTENSIONS
import phonenumbers as pn


def format_number(x):
    try:
        return pn.format_number(pn.parse(x), pn.PhoneNumberFormat.E164)
    except Exception:
        return x

def fix_whitespaces(x):
    return ' '.join(x.split())

def filter_empty(x):
    if isinstance(x, list):
        l = [i for i in x if ''.join(i.split())]
        return l or None
    return ''.join(x.split()) or None

def normalize_str(x):
    return unicodedata.normalize('NFC', x)

def to_datetime(x):
    try:
        return dparser.parse(x)
    except ValueError:
        return x
    
def swap_coordinates(x):
    if isinstance(x, list) and len(x) == 2:
        return [x[1], x[0]]
    
    raise ValueError('Invalid coordinates format')
# constants
# common file extensions that are not followed if they occur in links
DOWNLOAD_EXTENSIONS = ['pdf', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx', 'odt', 'ods', 'odg', 'odp']
CUSTOM_IGNORED_EXTENSIONS = [i for i in IGNORED_EXTENSIONS if i not in DOWNLOAD_EXTENSIONS]