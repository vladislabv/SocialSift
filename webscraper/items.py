"""
This module defines the Scrapy items used for web scraping restaurant data.

Define here the models for your scraped items
See documentation in: https://docs.scrapy.org/en/latest/topics/items.html
"""

from datetime import datetime as dt
import scrapy

class Resto(scrapy.Item):
    """
    Represents a restaurant item.
    """
    collection = 'restos'  # Meta field
    name = scrapy.Field()
    about = scrapy.Field()
    website = scrapy.Field()
    kitchen_types = scrapy.Field()  # List of strings
    social_media = scrapy.Field()  # List of strings
    phone = scrapy.Field()  # Location data fields
    location = scrapy.Field()
    address = scrapy.Field()  # Embedded documents
    menu_positions = scrapy.Field()  # List of Menu items
    working_hours = scrapy.Field()  # List of RestoHours items
    reviews = scrapy.Field()  # Referenced documents

class RestoAddress(scrapy.Item):
    """
    Represents the address of a restaurant.
    """
    street = scrapy.Field()
    zip = scrapy.Field()
    city = scrapy.Field()

class RestoLocation(scrapy.Item):
    """
    Represents the location of a restaurant.
    """
    type = scrapy.Field()
    coordinates = scrapy.Field()

class RestoHours(scrapy.Item):
    """
    Represents the opening hours of a restaurant.
    """
    day = scrapy.Field()
    open_time = scrapy.Field()
    close_time = scrapy.Field()

class Menu(scrapy.Item):
    """
    Represents a menu item.
    """
    collection = 'menus'  # Meta field
    name = scrapy.Field()
    price = scrapy.Field()
    currency = scrapy.Field()
    description = scrapy.Field()
    category = scrapy.Field()

class Review(scrapy.Item):
    """
    Represents a review for a restaurant.
    """
    collection = 'reviews'  # Meta field
    date = scrapy.Field()
    rating = scrapy.Field()
    title = scrapy.Field()
    text = scrapy.Field()
    votes = scrapy.Field()
    language = scrapy.Field()
    platform = scrapy.Field()
    author_name = scrapy.Field()
    resto_name = scrapy.Field()
    resto_city = scrapy.Field()

class RestoHistory(scrapy.Item):
    """
    Represents a historical snapshot of a restaurant's data.
    """
    collection = 'snapshots'  # Meta field
    url = scrapy.Field()  # UNIQUE(url, snapshot_at)
    title = scrapy.Field()
    text = scrapy.Field()
    snapshot_at = scrapy.Field(default=dt.now())
    fetched_at = scrapy.Field(default=dt.now())

class WebFile(scrapy.Item):
    """
    Represents a web file item.
    """
    file_urls = scrapy.Field()
