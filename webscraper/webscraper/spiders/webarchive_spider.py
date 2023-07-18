import os.path as osp
from datetime import datetime
from urllib.parse import urlparse

import scrapy

# import nltk
from bs4 import BeautifulSoup
import pandas as pd

from webscraper.items import Website, FileLoader

CITIES = ["duisburg", "berlin", "dortmund"]

class WebarchiveSpider(scrapy.Spider):
    name = "webarchive"

    custom_settings = {
        "DOWNLOADER_MIDDLEWARES": {
            'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
            'scrapy_user_agents.middlewares.RandomUserAgentMiddleware': 100,
            'webscraper.middlewares.IgnoreRequestsMiddleware': 200,
            'webscraper.middlewares.WaybackMachineMiddleware': 300,
        },
        # be bad but not too bad
        "ROBOTSTXT_OBEY": False,
        "DOWNLOAD_DELAY": 5,
        "FEEDS": {
            'data/%(name)s/website_%(time)s.csv': {
                'format': 'csv',
                'encoding': 'utf-8',
                'store_empty': False,
                'fields': None,
                'item_export_kwargs': {
                    'export_empty_fields': True,
                },
            }
        }
    }
    
    # read urls from db, for developing use csv
    # pd.read_csv("data/data.csv").website.dropna().sample(1).tolist()
    start_urls = ['http://www.mueller-menden.de']

    domains = list({urlparse(url).netloc for url in start_urls})

    def parse(self, response):
        self.logger.info("A response from %s just arrived!", response.url)
        print(response.meta)
        if response.status != 200:
            return
        
        fetched_at_dt = datetime.strptime(response.headers.get("Date").decode("utf-8"), "%a, %d %b %Y %H:%M:%S %Z")
        snapshot_at_dt = response.meta.get("wayback_machine_time", fetched_at_dt)

        yield Website(
            title=response.css("head > title::text").get(),
            full_text=' '.join(BeautifulSoup(response.body, features="lxml").get_text('|>|', strip=True).split()),
            snapshot_at=snapshot_at_dt.strftime("%Y-%m-%dT%H:%M:%S"),
            fetched_at=fetched_at_dt.strftime("%Y-%m-%dT%H:%M:%S"),
            wayback_url=response.meta.get("wayback_machine_url", response.url),
            url=response.url,
        )
        
        next_pages = response.css("a::attr(href)").getall()
        next_pages = {x for x in next_pages if x and osp.splitext(x)[-1]}

        if True:
            yield FileLoader(
                file_urls=response.css("a::attr(href)").getall(),
                wayback_url=response.meta.get("wayback_machine_url", response.url),
                url=response.url,
            )
        
        for next_page in next_pages:
            yield response.follow(next_page, callback=self.parse)
    
process = scrapy.crawler.CrawlerProcess()#get_project_settings())
process.crawl(WebarchiveSpider)
process.start()