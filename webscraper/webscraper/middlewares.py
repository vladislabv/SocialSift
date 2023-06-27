# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

import json
import os.path as osp
from datetime import datetime as dt
from urllib.parse import urlparse

from scrapy import signals
from scrapy import Request
from scrapy import FormRequest
from scrapy.http import Response
from scrapy.exceptions import IgnoreRequest

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter


class UnhandledIgnoreRequest(IgnoreRequest):
    pass

class WaybackMachineMiddleware:
    DOMAIN = 'web.archive.org'

    # def __init__(self, crawler):
        # self.crawler = crawler
        
        # read the settings
        # self.time_range = crawler.settings.get('WAYBACK_MACHINE_TIME_RANGE')

    @classmethod
    def from_crawler(cls, crawler):
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s
        # return cls(crawler)
    
    def process_request(self, request, spider):
        # let any web.archive.org requests pass through
        if request.url.startswith(f'http://{self.DOMAIN}/'):
            return None
            
        # if the request is within the allowed domains, check if it has a snapshot
        return self.build_cdx_request(request)

    def build_cdx_request(self, request):
        # build the CDX request
        return FormRequest(
            method = 'GET',
            url = f'http://{self.DOMAIN}/cdx/search/cdx',
            formdata = {
                'url': request.url,
                'output': 'json',
                'fl': 'timestamp,original,statuscode,digest'
            },
            meta = {
                'original_request': request,
                'wayback_machine_cdx_request': True,
            },
        )

    def process_response(self, request, response, spider):
        meta = request.meta

        # parse CDX requests and schedule future snapshot requests
        if meta.get('wayback_machine_cdx_request'):
            snapshot_requests = self.build_snapshot_requests(response, meta)
            # provide the original request (i.e. from now) to the queue
            snapshot_requests.append(meta['original_request'])
            # schedule all of the snapshots
            for snapshot_request in snapshot_requests[:1]:
                spider.crawler.engine.crawl(snapshot_request)
                # self.crawler.engine.crawl()

            # abort this request
            raise UnhandledIgnoreRequest

        # clean up snapshot responses
        if meta.get('original_request'):
            return response.replace(url=meta['original_request'].url)

        return response
    
    def build_snapshot_requests(self, response, meta):
        # parse the CDX snapshot data
        data = json.loads(response.text)

        if len(data) < 1:
            return []
        
        keys, rows = data[0], data[1:]
        snapshots = [dict(zip(keys, row)) for row in rows]

        # construct the requests
        snapshot_requests = []
        for snapshot in snapshots:
            # DISABLED - ignore snapshots outside of the time range
            # if not (self.time_range[0] < int(snapshot['timestamp']) < self.time_range[1]):
            #    continue

            # update the url to point to the snapshot
            url = 'http://{DOMAIN}/web/{timestamp}id_/{original}'.format(DOMAIN=self.DOMAIN, **snapshot)
            original_request = meta['original_request']
            snapshot_request = original_request.replace(url=url)

            # attach extension specify metadata to the request
            snapshot_request.meta.update({
                'original_request': original_request,
                'wayback_machine_url': snapshot_request.url,
                'wayback_machine_time': dt.strptime(snapshot['timestamp'], '%Y%m%d%H%M%S'),
            })

            snapshot_requests.append(snapshot_request)

        return snapshot_requests

    def spider_opened(self, spider):
        spider.logger.info('Accessing WaybackMachineMiddleware...')


class IgnoreRequestsMiddleware:
    EXTENSIONS = [
        '.swf',
        '.css',
        '.js',
    ]

    ROUTES = [
        'cookie', 
        'datenschutz', 
        'impressum'
    ]

    @classmethod
    def from_crawler(cls, crawler):
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        parsed_url = urlparse(request.url)
        ext = osp.splitext(parsed_url.path)[-1]

        if len(parsed_url.path) < 2:
            raise UnhandledIgnoreRequest
        
        if not parsed_url.scheme.startswith('http'):
            raise UnhandledIgnoreRequest
        
        if ext in self.EXTENSIONS:
            raise UnhandledIgnoreRequest
        
        if (not parsed_url.netloc in spider.domains):
            # bypass the "file" request if it is not in the extension black list
            # and obviously not the html file
            if ext == '.html':
                raise UnhandledIgnoreRequest
            
            return None
        
        routes_matched = [i for i in self.ROUTES if i in parsed_url.path.lower()]
        if len(routes_matched) > 0:
            raise UnhandledIgnoreRequest
        
        return None
        

    def spider_opened(self, spider):
        spider.logger.info('Accessing IgnoreRequestsMiddleware...')


class RestaurantsSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class RestaurantsDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
