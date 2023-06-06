# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Restaurant(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    about = scrapy.Field()
    phone = scrapy.Field()
    website = scrapy.Field()
    contact = scrapy.Field()


class RestaurantDetails(scrapy.Item):
    menu = scrapy.Field()
    about = scrapy.Field()
    ext_pages = scrapy.Field()
    images = scrapy.Field()
    reviews = scrapy.Field()
    opening_hours = scrapy.Field()
