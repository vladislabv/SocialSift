# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import hashlib
import os.path as osp
from urllib.parse import urlparse

import scrapy
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
from scrapy.utils.python import to_bytes
from scrapy.pipelines.files import FilesPipeline

import pymongo
from itemadapter import ItemAdapter

from webscraper.items import FileLoader, Website

class WebsiteSaveToMongoPipeline:
    collection_name = "websites_raw_data"

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get("MONGO_URI"),
            mongo_db=crawler.settings.get("MONGO_DATABASE", "items"),
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        if isinstance(item, Website):
            d = ItemAdapter(item).asdict()
            # do not store duplicated text, instead refer to the first appearance
            d["source_item"] = self.add_source_pointer(d) or None
            self.db[self.collection_name].insert_one(d)
        return item
    
    def add_source_pointer(self, item):
        return self.db[self.collection_name].find_one(
            {"full_text": item["full_text"]},
            {"_id": 1}
        )

class WebFilesPipeline(FilesPipeline):

    RELEVANT_EXTENSIONS = [
        '.pdf', 
        '.doc', 
        '.docx', 
        '.xls', 
        '.xlsx', 
        '.ppt', 
        '.pptx',
        '.jpg',
        '.jpeg',
        '.png',
        '.gif',
        '.svg',
        '.webp',
    ]

    def process_item(self, item, spider):
        if isinstance(item, FileLoader):
            super().process_item(item, spider)
        
        return item

    def file_path(self, request, response=None, info=None, *, item=None):
        uri_parsed = urlparse(request.url)
        file_name = osp.basename(uri_parsed.path)
        file_ext = osp.splitext(file_name)[-1]
        url_hash = hashlib.sha1(to_bytes(request.url)).hexdigest()

        if file_ext in self.RELEVANT_EXTENSIONS:
            return f"{uri_parsed.netloc}_{url_hash}.{file_ext}"
        
        raise DropItem('Not a valid file type in %s' % item)
    
    def get_media_requests(self, item, info):
        urls = item.get('file_urls', [])
        for url in urls:
            yield scrapy.Request(url)