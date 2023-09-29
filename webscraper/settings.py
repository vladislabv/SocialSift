# Scrapy settings for webscraper project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import os
import dotenv

# load environment variables
project_dir = os.path.join(os.path.dirname(__file__), os.pardir)
dotenv_path = os.path.join(os.path.abspath(project_dir), '.env')
dotenv.load_dotenv(dotenv_path)
# ---------------------------------

BOT_NAME = 'webscraper'

SPIDER_MODULES = ['webscraper.spiders']
NEWSPIDER_MODULE = 'webscraper.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 1

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 0.25
DOWNLOAD_TIMEOUT = 15
# Middlewares
DOWNLOADER_MIDDLEWARES = {
    'scrapy_user_agents.middlewares.RandomUserAgentMiddleware': 400,
    #'rotating_proxies.middlewares.RotatingProxyMiddleware': 300,
    #'rotating_proxies.middlewares.BanDetectionMiddleware': 300,
}
# CLOSESPIDER_PAGECOUNT = 500
# TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"

# The download delay setting will honor only one of:
CONCURRENT_REQUESTS_PER_DOMAIN = 1
#CONCURRENT_REQUESTS_PER_IP = 2

# Disable cookies (enabled by default)
COOKIES_ENABLED = True

# Proxy Settings
# ROTATING_PROXY_LIST = [
#     '2.56.119.93:5074',
#     '185.199.229.156:7492',
#     '185.199.228.220:7300',
#     '185.199.231.45:8382',
#     '188.74.210.207:6286',
#     '188.74.183.10:8279',
#     '188.74.210.21:6100',
#     '45.155.68.129:8133',
#     '154.95.36.199:6893',
#     '45.94.47.66:8110',
# ]

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
DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'scrapy_user_agents.middlewares.RandomUserAgentMiddleware': 400,
    #'scrapy_wayback_middleware.WaybackMiddleware': 543,
    # 'webscraper.middlewares.WaybackMachineMiddleware': 543,
    #"https": "scrapy.core.downloader.handlers.http2.H2DownloadHandler",
}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}
MONGO_DATABASE = 'web_scraper'
MONGO_DB_USERNAME = os.getenv('MONGO_DB_USERNAME')
MONGO_DB_PASSWORD = os.getenv('MONGO_DB_PASSWORD')
MONGO_URI = f'mongodb+srv://{MONGO_DB_USERNAME}:{MONGO_DB_PASSWORD}@gastrohub.o9izr0g.mongodb.net'

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    # 'webscraper.pipelines.PlaceToMongoPipeline': 50,
    'webscraper.pipelines.WebFilesPipeline': 1,
    'webscraper.pipelines.MongoDBPipeline': 50,
}

# Pipeline settings
FILES_STORE = "data/webscraper/files/"
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
AUTOTHROTTLE_ENABLED = True
# The initial download delay
AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
HTTPCACHE_ENABLED = False
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

FEEDS = {
    'data/webscraper/%(name)s/%(name)s_%(time)s.csv': {
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
LOG_FILE = "logs/webscraper/live.log"
LOG_LEVEL = "DEBUG"


RETRY_ENABLED = True
AJAXCRAWL_ENABLED = True
REACTOR_THREADPOOL_MAXSIZE = 1
SCHEDULER_PRIORITY_QUEUE = "scrapy.pqueues.DownloaderAwarePriorityQueue"

WAYBACK_MACHINE_TIME_RANGE = (20010101000000, 20210101000000)