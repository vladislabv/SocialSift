from urllib.parse import urlparse

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from webscraper.items import RestoHistory, WebFile
from webscraper.itemsloaders import WebsiteLoader, WebFileLoader
from webscraper.utils import CUSTOM_IGNORED_EXTENSIONS, DOWNLOAD_EXTENSIONS


class WebarchiveSpider(CrawlSpider):
    name = "webarchive"
    allowed_domains = ["web.archive.org", "www.costa-azzurra.de"]
    start_urls = [ 'http://www.costa-azzurra.de']
    # read urls from db
    # domains = list({urlparse(url).netloc for url in start_urls})
    # TBD: filter out Routes and Extensions
    rules = (
        Rule(
            LinkExtractor(
                deny_extensions=CUSTOM_IGNORED_EXTENSIONS,
                allow=[r'.*/kueche.*', r'.*/(speise|saison|wochen|mittags|monats|fruehstueck|jahres)karte.*', r'.*/gerichte.*', r'.*/.*menu.*', r'.*/card.*']
            ), 
            callback='parse_site',
            follow=True
        ),
    )

    def parse_site(self, response):
        self.logger.info("A response from %s just arrived!", response.url)

        ext = response.url.split('.')[-1]
        if ext in DOWNLOAD_EXTENSIONS:
            l = WebFileLoader(item=WebFile(), response=response)
            l.add_value('file_urls', response.url)
        else:
            l = WebsiteLoader(item=RestoHistory(), response=response)
            l.add_value('url', response.url)
            l.add_value('snapshot_at', response.meta.get("wayback_machine_time"))
            l.add_css('title', 'head > title::text')
            l.add_xpath('text', '//text()')
            # worked
            # ' '.join(BeautifulSoup(response.body, features="lxml").get_text('|>|', strip=True).split())

        yield l.load_item()
        
        
        