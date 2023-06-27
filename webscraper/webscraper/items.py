# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import hashlib
import scrapy


class Restaurant(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    about = scrapy.Field()
    phone = scrapy.Field()
    website = scrapy.Field()
    contact = scrapy.Field()


class Website(scrapy.Item):
    # UNIQUE(url, snapshot_at)
    url = scrapy.Field()
    title = scrapy.Field()
    full_text = scrapy.Field()
    snapshot_at = scrapy.Field()
    fetched_at = scrapy.Field()
    wayback_url = scrapy.Field()
    source_item = scrapy.Field()


# class ImageLoader(scrapy.Item):
#     # ... other item fields ...
#     image_urls = scrapy.Field()
#     images = scrapy.Field()

class FileLoader(scrapy.Item):
    # ... other item fields ...
    file_urls = scrapy.Field()
    files = scrapy.Field()
