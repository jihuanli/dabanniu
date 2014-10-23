# Scrapy settings for kimissValue project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'kimissValue'

SPIDER_MODULES = ['kimissValue.spiders']
NEWSPIDER_MODULE = 'kimissValue.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'kimissValue (+http://www.yourdomain.com)'

CONCURRENT_ITEMS = 100
CONCURRENT_REQUESTS = 5
CONCURRENT_REQUESTS_PER_DOMAIN = 5
CONCURRENT_REQUESTS_PER_IP = 0
DOWNLOAD_TIMEOUT = 180
DOWNLOADER_DEBUG = True
DOWNLOAD_DELAY=0
ITEM_PIPELINES=['kimissValue.pipelines.KimissvaluePipeline']
LOG_LEVEL="WARNING"
LOG_FILE="kimissValue.log"


DEPTH_PRIORITY=0
COOKIES_ENABLED=False
COOKIES_DEBUG=False

RETRY_ENABLED = True                                                                                        
RETRY_TIMES = 2 
RETRY_HTTP_CODES = [500, 503, 504, 400, 408]
RETRY_PRIORITY_ADJUST = -1

SCHEDULER_DISK_QUEUE = 'scrapy.squeue.PickleFifoDiskQueue'
SCHEDULER_MEMORY_QUEUE = 'scrapy.squeue.FifoMemoryQueue'
DEFAULT_REQUEST_HEADERS = {
	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
	'Accept-Language': 'en',
}

WNLOADER_MIDDLEWARES = {
	'kimissValue.random_useragent.RandomUserAgentMiddleware': 400,
	'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware': None,
#	'scrapy.contrib.downloadermiddleware.httpproxy.HttpProxyMiddleware': 110, 
#	'baiduzhidao.random_proxy.RandomProxyMiddleware': 100, 
}




