import scrapy
from scrapy_playwright.page import PageMethod
from webscraper.items import Restaurant

BINDADDRESSES = ["8.8.8.8", "8.8.4.4"]

class ClickAndSavePdfSpider(scrapy.Spider):
    name = "pdf"

    def start_requests(self):
        yield scrapy.Request(
            url="https://example.org",
            meta=dict(
                playwright=True,
                playwright_page_methods={
                    "click": PageMethod("click", selector="a"),
                    "pdf": PageMethod("pdf", path="/tmp/file.pdf"),
                },
            ),
        )

    def parse(self, response):
        pdf_bytes = response.meta["playwright_page_methods"]["pdf"].result
        with open("iana.pdf", "wb") as fp:
            fp.write(pdf_bytes)
        yield {"url": response.url}

class RestaurantsCrawler(scrapy.Spider):
    name = 'quotes'

    def start_requests(self):
        url = "https://www.meenakumari.de"
        yield scrapy.Request(
            url,
            meta = dict(
                playwright = True,
                playwright_include_page = True,
                playwright_page_methods = [
                    PageMethod("wait_for_selector", "div.quote"),
                    PageMethod("evaluate", "window.scrollBy(0, document.body.scrollHeight)"),
                    PageMethod("wait_for_selector", "div.quote:nth-child(11)"),  # 10 per page
                ],
                errback = self.errback,
            )
        )

    async def parse(self, response):
        page = response.meta["playwright_page"]
        await page.close()

        next_page = response.css('.next>a ::attr(href)').get()

        if next_page:
            yield response.follow(
                next_page, 
                meta = dict(
                    playwright = True,
                    playwright_include_page = True, 
                    playwright_page_methods = {
                        "click": PageMethod("click", selector="a"),
                        "pdf": PageMethod("pdf", path="/data/test.pdf"),
                    },
                errback=self.errback,
                )
            )
  
    async def errback(self, failure):
        page = failure.request.meta["playwright_page"]
        await page.close()