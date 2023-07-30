import uuid
from urllib.parse import urlparse

import scrapy
from scrapy.spiders import SitemapSpider

from webscraper.items import (
    Resto,
    Menu,
    Review,
)
from webscraper.itemsloaders import (
    RestoLoader,
    MenuLoader,
    ReviewLoader,
)


class RestosSpider(SitemapSpider):
    name = "restos"
    allowed_domains = ["images.speisekarte.de", "speisekarte.de"]
    sitemap_urls  = ["https://images.speisekarte.de/media/docs/sitemaps/staedte1.xml"]
    sitemap_rules = [('https://www.speisekarte.de', 'parse_page')]

    def parse_page(self, response):
        self.logger.info('Hi, this is a resto page! %s', response.url)

        resto_urls = response.css("h2 a[href*='/restaurant/']::attr(href)").getall()
        for url in resto_urls:
            yield scrapy.Request(url, callback=self.parse_item)

        # go to next page (pagination)
        next_page = response.css("nav[aria-label='Seitennummerierung'] .page-item:not(.disabled) a[href*='page=']::attr(href)").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse_page)

    def parse_item(self, response):
        self.logger.info('Hi, this is a resto item page! %s', response.url)

        resto_id = str(uuid.uuid4())

        l = RestoLoader(item=Resto(), response=response)
        l.add_value('id', resto_id)
        l.add_css('name', "p.css-name::text")
        l.add_css('about', "div#detail-description p[itemprop='description']::text")
        l.add_css('address', "p span[class='css-address']::text")
        l.add_css('website', "div#detail-contact-info a.css-website::attr(href)")
        l.add_css('kitchen_type', "div#detail-kitchen-types a::text")
        l.add_css('opening_hours', "div.day-name meta[itemprop='openingHours']::attr(content)")
        l.add_css('social_media', "div#detail-social a::attr(href)")
        l.add_css('zip', "p span[class='css-zip']::text")
        l.add_css('city', "p span[class='css-city']::text")
        l.add_css('phone', "div#detail-contact-info a.css-phone::text")
        l.add_css('location', "div#detail-map div[itemprop='geo'] meta::attr(content)")

        yield l.load_item()
        
        yield scrapy.Request(
            url=response.url + "/speisekarte",
            callback=self.parse_menu,
            cb_kwargs=dict(resto_id=resto_id)
        )

        yield scrapy.Request(
            url=response.url + "/bewertung",
            callback=self.parse_reviews,
            cb_kwargs=dict(resto_id=resto_id)
        )

    def parse_menu(self, response, resto_id):
        self.logger.info('Hi, this is a menu page! %s', response.url)

        for selector in response.css("div.menu-entry-filter"):
            l = MenuLoader(item=Menu(), selector=selector)
            l.add_css('name', "div.grid-dishes b *::text")
            l.add_css('price', "div.price span[itemprop='price']::attr(content)")
            l.add_css('currency', "div.price span[itemprop='priceCurrency']::attr(content)")
            l.add_css('description', "div.grid-dishes > div:not(.price)::text")
            l.add_css('category', "p::text")
            l.add_value('resto_id', resto_id)

            yield l.load_item()

    def parse_reviews(self, response, resto_id):
        self.logger.info('Hi, this is a reviews page! %s', response.url)

        for selector in response.css("li.user-comment"):
            l = ReviewLoader(item=Review(), selector=selector)
            
            l.add_css("text", "div > p::text")
            l.add_css("author_name", ".comment-info div.username *::text")
            l.add_css("date", ".comment-info div.date > span::text")
            l.add_value("platform", "speisekarte.de")
            l.add_value("resto_id", resto_id)

            rating_stars = selector.css(".comment-info div.stars img.ratingstarfull::attr(id)").getall()
            l.add_value('rating', len(rating_stars))
            
            yield l.load_item()
        
