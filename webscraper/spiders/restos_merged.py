import math
from urllib.parse import urlparse

import scrapy
from scrapy.spiders import SitemapSpider

import parsel

from webscraper.items import (
    Resto,
    Menu,
    Review,
    RestoAddress,
    RestoHours,
    RestoLocation,
)
from webscraper.itemsloaders import (
    RestoLoader,
    MenuLoader,
    ReviewLoader,
    AddressLoader,
    WorkingHoursLoader,
    LocationLoader,
)

from webscraper.utils import gen_weekdays_in_between



class RestosSpider(SitemapSpider):
    name = "restos"
    allowed_domains = ["images.speisekarte.de", "speisekarte.de", "yelp.de", "golocal.de"]
    sitemap_urls  = ["https://images.speisekarte.de/media/docs/sitemaps/staedte1.xml"]
    sitemap_rules = [('https://www.speisekarte.de', 'parse_page')]

    review_page_size = 10

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
        working_hours = []
        l = RestoLoader(item=Resto(), response=response)

        l.add_css('name', "p.css-name::text")
        l.add_css('about', "div#detail-description p[itemprop='description']::text")
        l.add_css('website', "div#detail-contact-info a.css-website::attr(href)")
        l.add_css('kitchen_types', "div#detail-kitchen-types a::text")
        l.add_css('social_media', "div#detail-social a::attr(href)")
        l.add_css('phone', "div#detail-contact-info a.css-phone::text")

        l_location = LocationLoader(item=RestoLocation(), response=response)
        l_location.add_value('type', 'Point')
        l_location.add_css('coordinates', "div#detail-map div[itemprop='geo'] meta::attr(content)")

        l.add_value('location', l_location.load_item())

        for selector in response.css("div.day-name meta[itemprop='openingHours']::attr(content)"):
            # TODO: split value in a selector by whitespace, 1st part - for day, 2nd part - time
            # split each resulting part by '-', in the day part is start day, end day; in the time part
            # open time - close time, load the resulted parts to the mongodb
            openings_string = selector.get()
            days, hours = openings_string.split()
            days_range = gen_weekdays_in_between(days.split('-')[0].lower(), days.split('-')[1].lower())

            for day in days_range:
                l_openings = WorkingHoursLoader(item=RestoHours(), selector=selector)
                l_openings.add_value('day', day)
                try:
                    l_openings.add_value('open_time', hours.split('-')[0])
                    l_openings.add_value('close_time', hours.split('-')[1])
                except IndexError:
                    # if there is no close time, the restaurant is open 24/7
                    l_openings.add_value('open_time', '00:00')
                    l_openings.add_value('close_time', '23:59')
                
                working_hours.append(l_openings.load_item())

        l_sub = AddressLoader(item=RestoAddress(), response=response)

        l_sub.add_css('street', "p span[class='css-address']::text")
        l_sub.add_css('zip', "p span[class='css-zip']::text")
        l_sub.add_css('city', "p span[class='css-city']::text")

        # put all together
        l.add_value('working_hours', working_hours)
        l.add_value('address', l_sub.load_item())
        
        yield scrapy.Request(
            response.url + "/speisekarte",
            callback=self.parse_menu,
            cb_kwargs=dict(loader=l)
        )

    def parse_menu(self, response, loader):
        self.logger.info('Hi, this is a menu page! %s', response.url)
        items = []

        for selector in response.css("section.menu-entry-filter > div.menu-entry-filter"):
            l = MenuLoader(item=Menu(), selector=selector)
            l.add_css('name', "div.grid-dishes b *::text")
            l.add_css('price', "div.price span[itemprop='price']::attr(content)")
            l.add_css('currency', "div.price span[itemprop='priceCurrency']::attr(content)")
            l.add_css('description', "div.grid-dishes > div:not(.price)::text")
            l.add_css('category', "p::text")

            items.append(l.load_item())
        
        loader.add_value('menu_positions', items)

        yield scrapy.Request(
            url=response.url.replace("/speisekarte", "/bewertung"),
            callback=self.parse_reviews,
            cb_kwargs=dict(loader=loader)
        )
        

    def parse_reviews(self, response, loader):
        self.logger.info('Hi, this is a reviews page! %s', response.url)
        items = []
        
        # parse main site
        for selector in response.css("li.user-comment"):
            l = ReviewLoader(item=Review(), selector=selector)
            
            l.add_css('text', "div > p::text")
            l.add_css('author_name', ".comment-info div.username *::text")
            l.add_css('date', ".comment-info div.date > span::text")
            l.add_value('platform', "speisekarte.de")

            rating_stars = selector.css(".comment-info div.stars img.ratingstarfull::attr(id)").getall()
            l.add_value('rating', len(rating_stars))
            
            items.append(l.load_item())

        rest = loader.load_item()
        rest_name = rest['name'].strip()
        rest_city = rest['address'].get('city', '').strip()
        
        # yelp.de
        items.extend(
            scrapy.FormRequest(
                url="https://www.yelp.de/search/snippet", 
                method = 'GET', 
                callback=self.parse_yelp_api_response, 
                formdata= {
                    "find_desc": rest_name,
                    "find_loc": rest_city,
                    "request_origin": "user",
                }
            )
        )

        # golocal.de
        items.extend(
            scrapy.FormRequest(
                url="https://www.golocal.de/suchen/", 
                method='GET', 
                callback=self.parse_golocal_response, 
                formdata={
                    "q": "location",
                    "what": rest_name,
                    "address": "",
                }
            )
        )

        # separate reviews from restaurants later
        loader.add_value('reviews', items)

        yield loader.load_item()


    def parse_yelp_api_response(self, response):
        self.logger.info("A response from %s just arrived!", response.url)
        selector = parsel.Selector(response.text)
        biz = selector.jmespath('searchPageProps.mainContentComponentsListProps[?ranking==1]')

        if not biz:
            self.logger.error(f"Could not find location data for query: {response.url}")
            return
        
        biz_info = biz.get('searchResultBusiness', {})
        no_of_reviews = biz_info.get('reviewCount', 0)
        total_review_pages = int(math.ceil(no_of_reviews / self.review_page_size))

        for i in range(0, total_review_pages + 1):
            yield scrapy.FormRequest(
                url=f"https://www.yelp.de/biz/{biz['bizId']}/review_feed", 
                method='GET', 
                callback=self.parse_yelp_reviews, 
                formdata={
                    "q": "",
                    "sort_by": "relevance_desc",
                    "start": i,
                }
        )
            
    def parse_yelp_reviews(self, response):
        self.logger.info("A response from %s just arrived!", response.url)
        yelp_reviews = []
        for selector in parsel.Selector(response.text).jmespath('reviews'):
            l = ReviewLoader(item=Review(), selector=selector)

            l.add_jmes('date', 'localizedDate')
            l.add_jmes('rating', 'rating')
            l.add_jmes('text', 'comment.text')
            l.add_jmes('language', 'comment.language')
            l.add_jmes('votes', 'comment.feedback')
            l.add_jmes('author_name', 'user.markupDisplayName')
            l.add_value('platform', self.name)

            yelp_reviews.append(l.load_item())
        
        return yelp_reviews
    

    def parse_golocal_response(self, response):
        self.logger.info("A response from %s just arrived!", response.url)
        
        new_url = response.headers.get("Location", b"").decode()

        if new_url:
            parsed_url = urlparse(new_url)

            yield scrapy.Request(
                url=parsed_url.path+"bewertungen/",
                callback=self.parse_golocal_reviews
            )


    def parse_golocal_reviews(self, response):
        self.logger.info("A response from %s just arrived!", response.url)
        golocal_reviews = []
        for selector in response.css("section[id=reviewList] > article"):
            l = ReviewLoader(item=Review(), selector=selector)

            l.add_css("date", ".reviewitem__ratinginfo .reviewitem__datewrap meta::attr(content)")
            l.add_css("rating", ".reviewitem__ratinginfo .reviewitem__rating > div[itemprop='ratingValue']::text")
            l.add_css("text", ".reviewitem__reviewbody > p[itemprop='reviewBody']::text")
            l.add_css("platform", ".reviewitem__ratinginfo .reviewitem__datewrap a:not(.reviewitem__date)::text,span:not(span[itemprop='author'])::text")
            l.add_css("author_name", ".reviewitem__usertitle meta::attr(content)")

            golocal_reviews.append(l.load_item())

        return golocal_reviews