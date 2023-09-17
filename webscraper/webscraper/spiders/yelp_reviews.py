import math
import scrapy
from urllib.parse import urlencode

from parsel import Selector

from webscraper.items import Review
from webscraper.itemsloaders import ReviewLoader
from webscraper.utils import fetch_documents, get_mongo_connection

class YelpReviewsSpider(scrapy.Spider):
    name = "yelp_reviews"
    allowed_domains = ["yelp.de"]
    town = "Berlin"
    place = "Meena Kumari"
    review_page_size = 10

    def start_requests(self):
        url = "https://www.yelp.de/search/snippet"
        db = get_mongo_connection()
        for doc in fetch_documents(db["new_restos"], query={}, projection={"_id": 1, "name": 1, "address.city": 1}):
            payload = {
                "find_desc": doc["name"],
                "find_loc": doc["address"]["city"],
                "request_origin": "user",
            }

            q_string = urlencode(payload)
            url += f"?{q_string}"
  
            yield scrapy.Request(url, self.parse, cb_kwargs=dict(resto_id=doc["_id"]))


    def parse(self, response, resto_id):
        self.logger.info("A response from %s just arrived!", response.url)
        biz = self.parse_api_response(response)

        if not biz:
            return
        
        biz_info = biz.get('searchResultBusiness', {})
        no_of_reviews = biz_info.get('reviewCount', 0)
        total_review_pages = int(math.ceil(no_of_reviews / self.review_page_size))

        for i in range(0, total_review_pages + 1):
            payload = {
                "q": "",
                "sort_by": "relevance_desc",
                "start": i,
            }
            q_string = urlencode(payload)
            url = f"https://www.yelp.de/biz/{biz['bizId']}/review_feed?{q_string}"

            yield scrapy.Request(url, callback=self.parse_reviews, cb_kwargs=dict(resto_id=resto_id))


    def parse_api_response(self, response):
        jmess = Selector(response.text)
        result = jmess.jmespath('searchPageProps.mainContentComponentsListProps[?ranking==1]')
        if not result:
            self.logger.error(f"Could not find location data for query: {response.url}")
            return
        return result
    
            
    def parse_reviews(self, response, resto_id):
        self.logger.info("A response from %s just arrived!", response.url)

        for selector in Selector(response.text).jmespath('reviews'):
            l = ReviewLoader(item=Review(), selector=selector)

            l.add_jmes('date', 'localizedDate')
            l.add_jmes('rating', 'rating')
            l.add_jmes('text', 'comment.text')
            l.add_jmes('language', 'comment.language')
            l.add_jmes('votes', 'comment.feedback')
            l.add_jmes('author_name', 'user.markupDisplayName')
            l.add_value('platform', self.name)
            l.add_value('resto_id', resto_id)

            yield l.load_item()

    