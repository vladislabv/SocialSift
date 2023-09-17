import re
import string
import unicodedata
import dateutil.parser as dparser
from datetime import datetime as dt

import pymongo
from scrapy.linkextractors import IGNORED_EXTENSIONS
import phonenumbers as pn

from webscraper.settings import MONGO_URI, MONGO_DATABASE


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
    
def get_mongo_connection(monog_uri=MONGO_URI, mongo_db=MONGO_DATABASE):
    """get a mongo connection"""
    client = pymongo.MongoClient(monog_uri)
    db = client[mongo_db]
    return db
    
def fetch_documents(collection, query={}, projection={}, limit=10):
    """fetch documents from a mongo collection"""
    if limit:
        return collection.find(query, projection).limit(limit)
    return collection.find(query, projection)

def gen_weekdays_in_between(start = "monday", end = "sunday"):
    """generate a list of weekdays in between two weekdays"""
    weekdays = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    start = weekdays.index(start)
    end = weekdays.index(end)
    if start <= end:
        return weekdays[start:end+1]
    return weekdays[start:] + weekdays[:end+1]
    
# constants
# common file extensions that are not followed if they occur in links
DOWNLOAD_EXTENSIONS = ['pdf', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx', 'odt', 'ods', 'odg', 'odp']
CUSTOM_IGNORED_EXTENSIONS = [i for i in IGNORED_EXTENSIONS if i not in DOWNLOAD_EXTENSIONS]