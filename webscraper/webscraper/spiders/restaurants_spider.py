import scrapy
from geopy.geocoders import Nominatim
from webscraper.items import Restaurant

CITIES = ["duisburg", "berlin", "dortmund"]

class RestaurantsSpider(scrapy.Spider):
    name = "restaurant"
    start_urls = [
        f"https://restaurant.info/essen-gehen/{city}"
        for city in CITIES
    ]

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

        # get location from address
        geolocator = Nominatim(user_agent='LocationFinder')
        address = ", ".join(response.css("div#overviewContact > div span::text").getall())
        location = geolocator.geocode(address)

        return Restaurant(
            name=response.url.split("/")[-1],
            about=response.css("div#description > blockquote::text").get(),
            phone=response.css("a.jq-phone-complete::attr(href)").get(),
            website=response.css("a.jq-link-to-website::attr(href)").get(),
            contact=address,
            coordinates=[location.latitude, location.longitude],
        )