# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import hashlib

import scrapy
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
from scrapy.utils.python import to_bytes
from scrapy.pipelines.files import FilesPipeline

import pymongo

from webscraper.items import WebFile, RestoHistory
from webscraper.processors import ProcessMongoEntries


class MongoDBPipeline:

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get("MONGO_URI"),
            mongo_db=crawler.settings.get("MONGO_DATABASE", "webscraper"),
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        proccessor = getattr(ProcessMongoEntries, item.collection)
        if not proccessor:
            return item
        return proccessor(item, spider, self.db, item.collection)


class WebFilesPipeline(FilesPipeline):

    def process_item(self, item, spider):
        if isinstance(item, WebFile):
            super().process_item(item, spider)
        
        return item

    def file_path(self, request, response=None, info=None, *, item=None):
        file_url_hash = hashlib.shake_256(request.url.encode()).hexdigest(5)
        file_perspective = request.url.split("/")[-1]
        filename = f"{file_url_hash}_{file_perspective}"

        return filename
    
    def get_media_requests(self, item, info):
        urls = item.get('file_urls', [])
        for url in urls:
            yield scrapy.Request(url)