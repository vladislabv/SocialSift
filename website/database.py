# -*- coding: utf-8 -*-
"""Database module, including the MondoDB database object and DB-related utilities."""
from typing import Optional, Type, TypeVar

import pymongo
import mongoengine as me

from website.settings import MONGO_URI, MONGO_DB_SITE, MONGO_DB_SCRAPER

db = pymongo.MongoClient(MONGO_URI)[MONGO_DB_SITE]
db_scraper = pymongo.MongoClient(MONGO_URI)[MONGO_DB_SCRAPER]

me.register_connection(alias='default', name=MONGO_DB_SITE, host=MONGO_URI)

T = TypeVar("T", bound="PkDocument")

# class CRUDMixin(object):
#     """Mixin that adds convenience methods for CRUD (create, read, update, delete) operations."""

#     def update(self, commit=True, **kwargs):
#         """Update specific fields of a record."""
#         for attr, value in kwargs.items():
#             setattr(self, attr, value)
#         if commit:
#             return self.save()
#         return self

#     def save(self, commit=True):
#         """Save the record."""
#         self.save()
#         return self

#     def delete(self, commit: bool = True) -> None:
#         """Remove the record from the database."""
#         self.delete()
#         return


# class Model(CRUDMixin, me.Document):
#     """Base model class that includes CRUD convenience methods."""

#     meta = {
#         "abstract": True
#     }

class PkDocument(me.Document):
    """Base model class that includes CRUD convenience methods, plus adds a 'primary key' field named 'id'."""
    meta = {
        "allow_inheritance": True,
        "abstract": True,
    }
    @classmethod
    def create(cls: Type[T], **kwargs) -> T:
        """Create a new record and save it to the database."""
        instance = cls(**kwargs)
        return instance.save()

    @classmethod
    def get_by_id(cls: Type[T], record_id) -> Optional[T]:
        """Get record by ID."""
        return cls.objects(pk=record_id).first()