# -*- coding: utf-8 -*-
"""Database module, including the MondoDB database object and DB-related utilities."""
from typing import Optional, Type, TypeVar
import pymongo
from gih_site.extensions import db
from gih_site.settings import MONGO_URI, MONGO_DATABASE

db = pymongo.MongoClient(MONGO_URI)[MONGO_DATABASE]

