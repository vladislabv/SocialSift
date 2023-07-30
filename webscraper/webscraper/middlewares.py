# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

import json
import os.path as osp
from datetime import datetime as dt
from urllib.parse import urlparse

from scrapy import signals
from scrapy import FormRequest
from scrapy.exceptions import IgnoreRequest

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter


class UnhandledIgnoreRequest(IgnoreRequest):
    pass


class WaybackMachineMiddleware:
    DOMAIN = 'web.archive.org'

    @classmethod
    def from_crawler(cls, crawler):
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        # read the settings
        s.time_range = crawler.settings.get('WAYBACK_MACHINE_TIME_RANGE')
        return s
    
    def process_request(self, request, spider):
        # let any web.archive.org requests pass through
        if request.url.startswith(f'http://{self.DOMAIN}/') or spider.name != "webarchive":
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
            # schedule all of the snapshots
            for snapshot_request in snapshot_requests[:3]:
                spider.crawler.engine.crawl(snapshot_request)

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
        for snapshot in snapshots[:3]:
            # ignore snapshots outside of the time range
            if not (self.time_range[0] < int(snapshot['timestamp']) < self.time_range[1]):
                continue

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
