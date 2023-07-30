from itemloaders.processors import TakeFirst, MapCompose
from scrapy.loader import ItemLoader
from itemadapter import ItemAdapter

class ProcessMongoEntries:
    item = None
    spider = None
    
    @classmethod
    def websites(cls, item, spider, collection):
        d = ItemAdapter(item).asdict()
        # do not store duplicated text, instead refer to the first appearance
        d["source_item"] = collection.find_one({"full_text": item["full_text"]}, {"_id": 1}) or None
        collection.insert_one(d)
        return
    
    @classmethod
    def restaurants(cls, item, spider, collection):
        d = ItemAdapter(item).asdict()
        collection.insert_one(d)
        return

