import scrapy
import pandas as pd
from webscraper.items import Restaurant

INPUT_FILE = "data/data.csv"

class WebsitesCrawler(scrapy.Spider):
    name = "website"
    
    def start_requests(self):
        start_url = pd.read_csv("data/data.csv").website.dropna().sample(5).tolist()

    def parse(self, response):
        self.logger.info("A response from %s just arrived!", response.url)
        restaurants_on_page = response.css("ul.jq-result-list > li.jq-result-list-item > div > a::attr(href)").getall()

        for item in restaurants_on_page:
            yield scrapy.Request(item, callback=self.parse_item)

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