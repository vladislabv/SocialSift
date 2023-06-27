# Scrapy settings for webscraper project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'webscraper'

SPIDER_MODULES = ['webscraper.spiders']
NEWSPIDER_MODULE = 'webscraper.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'restaurants (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 3

# Middlewares
DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'scrapy_user_agents.middlewares.RandomUserAgentMiddleware': 400,
    'rotating_proxies.middlewares.RotatingProxyMiddleware': 800,
    'rotating_proxies.middlewares.BanDetectionMiddleware': 800,
}

## Playwright Settings
DOWNLOAD_HANDLERS = {
    "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
    "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
}
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
PLAYWRIGHT_BROWSER_TYPE = "firefox"
PLAYWRIGHT_LAUNCH_OPTIONS = {
    "headless": True,
    "timeout": 30 * 1000,  # 30 seconds
}
# Maximum amount of allowed concurrent Playwright contexts
PLAYWRIGHT_MAX_CONTEXTS = 32
# Timeout to be used when requesting pages by Playwright, in milliseconds
PLAYWRIGHT_DEFAULT_NAVIGATION_TIMEOUT = 10 * 1000  # 10 seconds

# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Proxy Settings
ROTATING_PROXY_LIST = [
    '2.56.119.93:5074',
    '185.199.229.156:7492',
    '185.199.228.220:7300',
    '185.199.231.45:8382',
    '188.74.210.207:6286',
    '188.74.183.10:8279',
    '188.74.210.21:6100',
    '45.155.68.129:8133',
    '154.95.36.199:6893',
    '45.94.47.66:8110',
]

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'restaurants.middlewares.RestaurantsSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'restaurants.middlewares.RestaurantsDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'webscraper.pipelines.WebsiteSaveToMongoPipeline': 100,
    'webscraper.pipelines.WebFilesPipeline': 200,
}

# Pipeline settings
FILES_STORE = "data/files/"
#IMAGES_STORE = "data/images/"

# 90 days of delay for files expiration
FILES_EXPIRES = 90
# 90 days of delay for images expiration
#IMAGES_EXPIRES = 90

#IMAGES_THUMBS = {
#    "small": (50, 50),
#    "big": (270, 270),
#}

#IMAGES_MIN_HEIGHT = 110
#IMAGES_MIN_WIDTH = 110

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

FEEDS = {
    'data/%(name)s/%(name)s_%(time)s.csv': {
        'format': 'csv',
        'encoding': 'utf-8',
        'store_empty': False,
        'fields': None,
        'item_export_kwargs': {
           'export_empty_fields': True,
        },
    }
}

# Crawlers configuration
LOG_ENABLE = True
LOG_ENCODING = 'UTF-8'
LOG_FILE = "logs/live.log"
LOG_LEVEL = "INFO"


RETRY_ENABLED = False
DOWNLOAD_TIMEOUT = 15
AJAXCRAWL_ENABLED = True
REACTOR_THREADPOOL_MAXSIZE = 20
SCHEDULER_PRIORITY_QUEUE = "scrapy.pqueues.DownloaderAwarePriorityQueue"