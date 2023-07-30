# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
from datetime import datetime as dt
import scrapy


class Resto(scrapy.Item):
    # meta field
    collection = 'restos'
    # define the fields for your item here like:
    id = scrapy.Field()
    name = scrapy.Field()
    about = scrapy.Field()
    website = scrapy.Field()
    kitchen_type = scrapy.Field()  # list of strings
    opening_hours = scrapy.Field()  # list of strings
    social_media = scrapy.Field()  # list of strings
    # location data fields
    address = scrapy.Field()
    zip = scrapy.Field()
    city = scrapy.Field()
    country = scrapy.Field()
    phone = scrapy.Field()
    location = scrapy.Field()

class RestoHours(scrapy.Item):
    # meta field
    collection = 'resto_hours'
    # define the fields for your item here like:
    day = scrapy.Field()
    open_time = scrapy.Field()
    close_time = scrapy.Field()
    resto_id = scrapy.Field()


class Menu(scrapy.Item):
    # meta field
    collection = 'menus'
    # define the fields for your item here like:
    name = scrapy.Field()
    price = scrapy.Field()
    currency = scrapy.Field()
    description = scrapy.Field()
    category = scrapy.Field()
    resto_id = scrapy.Field()


class Review(scrapy.Item):
    # meta field
    collection = 'reviews'
    """storage type hint for review data"""
    date = scrapy.Field()
    rating = scrapy.Field()
    title = scrapy.Field()
    text = scrapy.Field()
    votes = scrapy.Field()
    language = scrapy.Field()
    platform = scrapy.Field()
    author_name = scrapy.Field()
    resto_id = scrapy.Field()


class RestoHistory(scrapy.Item):
    # meta field
    collection = 'snapshots'
    # UNIQUE(url, snapshot_at)
    # url points to resto item
    url = scrapy.Field()
    title = scrapy.Field()
    text = scrapy.Field()
    snapshot_at = scrapy.Field(default=dt.now())
    fetched_at = scrapy.Field(default=dt.now())


class WebFile(scrapy.Item):
    # ... other item fields ...
    file_urls = scrapy.Field()
