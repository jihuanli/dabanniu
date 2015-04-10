# Scrapy settings for baiduzhidao project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'baiduzhidao'

SPIDER_MODULES = ['baiduzhidao.spiders']
NEWSPIDER_MODULE = 'baiduzhidao.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'baiduzhidao (+http://www.yourdomain.com)'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'taobaoReview (+http://www.yourdomain.com)'
#the download middlewares
DOWNLOADER_MIDDLEWARES = {
	'baiduzhidao.random_useragent.RandomUserAgentMiddleware': 400,
	'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware': None,
#	'scrapy.contrib.downloadermiddleware.httpproxy.HttpProxyMiddleware': 110, 
#	'baiduzhidao.random_proxy.RandomProxyMiddleware': 100, 
}


#the item pipes place here
ITEM_PIPELINES = [
	'baiduzhidao.pipelines.BaiduzhidaoPipeline',
]

DEPTH_PRIORITY = 0

SCHEDULER_DISK_QUEUE = 'scrapy.squeue.PickleFifoDiskQueue'
SCHEDULER_MEMORY_QUEUE = 'scrapy.squeue.FifoMemoryQueue'

#============================================================
#use baidu spider UA,now user random useragent 
#USER_AGENT = 'baiduspider+(+http //www.baidu.com/search/spider.htm)'

#============================================================
# concurrent configures
#Maximum number of concurrent items (per response) to process in parallel in the Pipeline
CONCURRENT_ITEMS = 100
#The maximum number of concurrent (ie. simultaneous) requests that will be performed by the Scrapy downloader
CONCURRENT_REQUESTS = 5 
#The maximum number of concurrent (ie. simultaneous) requests that will be performed to any single domain.
CONCURRENT_REQUESTS_PER_DOMAIN = 1
#The maximum number of concurrent (ie. simultaneous) requests that will be performed to any single IP. 
#If non-zero, the CONCURRENT_REQUESTS_PER_DOMAIN setting is ignored
CONCURRENT_REQUESTS_PER_IP = 0
#the spider size to run concurrent
#CONCURRENT_SPIDERS = 20

#============================================================
#http related configure
DEFAULT_REQUEST_HEADERS = {
	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
	'Accept-Language': 'en',
}
#cookie used and debug
COOKIES_ENABLED = False
COOKIES_DEBUG = False

#download timeout and download debug
DOWNLOAD_TIMEOUT = 180
DOWNLOADER_DEBUG = True
DOWNLOAD_DELAY = 3 

#retry configure
RETRY_ENABLED = True                                                                                        
RETRY_TIMES = 2 # initial response + 2 retries = 3 requests 
RETRY_HTTP_CODES = [500, 503, 504, 400, 408]
RETRY_PRIORITY_ADJUST = -1

#log  CRITICAL, ERROR, WARNING, INFO, DEBUG
LOG_LEVEL = "INFO"
LOG_FILE = "zhidao.log"

