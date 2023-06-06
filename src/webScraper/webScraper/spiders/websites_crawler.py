import scrapy
import random
from webScraper.items import Restaurant

BINDADDRESSES = ["8.8.8.8", "8.8.4.4"]
CITIES = ["duisburg", "berlin", "dortmund"]


class RestaurantsSpider(scrapy.Spider):
    name = "RestaurantsAllData"
    bindaddress = random.choice(BINDADDRESSES)
    allowed_domains = ["restaurant.info"]
    start_urls = [
        f"https://restaurant.info/essen-gehen/{city}"
        for city in CITIES
    ]

    def parse(self, response):
        self.logger.info("A response from %s just arrived!", response.url)
        links = response.css("a::attr(href)").getall()

        for next_link in links:
            yield scrapy.Request(next_link, callback=self.parse)

        # go to next page
        next_page = response.css("li.page-next a::attr(href)").extract_first()
        if next_page:
            yield response.follow(next_page, callback=self.parse)


    def parse_item(self, response):
        self.logger.info("A response from %s just arrived!", response.url)
        return Restaurant(
            name=response.url.split("/")[-1],
            about=response.css("div#description > blockquote::text").get(),
            phone=response.css("a.jq-phone-complete::attr(href)").get(),
            website=response.css("a.jq-link-to-website::attr(href)").get(),
            contact=", ".join(response.css("div#overviewContact > div span::text").getall()),
        )