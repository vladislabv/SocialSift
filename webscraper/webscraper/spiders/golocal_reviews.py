import scrapy
from urllib.parse import urlparse, urlencode

from webscraper.items import Review
from webscraper.itemsloaders import ReviewLoader

class GolocalSpider(scrapy.Spider):
    name = "golocal_reviews"
    handle_httpstatus_list = [301]
    allowed_domains = ["www.golocal.de"]
    town = "Berlin"
    place = "Meena Kumari"
    review_page_size = 10


    def start_requests(self):
        url = "https://www.golocal.de/suchen/"
        
        payload = {
            "q": "location",
            "what": self.place,
            "address": '',
        }

        q_string = urlencode(payload)
        url += f"?{q_string}"
  
        yield scrapy.Request(url)
    

    def parse(self, response):
        self.logger.info("A response from %s just arrived!", response.url)
        
        new_url = response.headers.get("Location", b"").decode()

        if new_url:
            parsed_url = urlparse(new_url)

            yield scrapy.Request(url=parsed_url.path + "bewertungen/", callback=self.parse_reviews)


    def parse_reviews(self, response):
        self.logger.info("A response from %s just arrived!", response.url)

        for selector in response.css("section[id=reviewList] > article"):
            l = ReviewLoader(item=Review(), selector=selector)

            l.add_css("date", ".reviewitem__ratinginfo .reviewitem__datewrap meta::attr(content)")
            l.add_css("rating", ".reviewitem__ratinginfo .reviewitem__rating > div[itemprop='ratingValue']::text")
            l.add_css("text", ".reviewitem__reviewbody > p[itemprop='reviewBody']::text")
            l.add_css("platform", ".reviewitem__ratinginfo .reviewitem__datewrap a:not(.reviewitem__date)::text,span:not(span[itemprop='author'])::text")
            l.add_css("author_name", ".reviewitem__usertitle meta::attr(content)")

            yield l.load_item()

