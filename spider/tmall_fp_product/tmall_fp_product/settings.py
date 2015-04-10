# -*- coding: utf-8 -*-

# Scrapy settings for tmall_fp_product project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'tmall_fp_product'

SPIDER_MODULES = ['tmall_fp_product.spiders']
NEWSPIDER_MODULE = 'tmall_fp_product.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'tmall_fp_product (+http://www.yourdomain.com)'

CONCURRENT_ITEMS = 100
CONCURRENT_REQUESTS = 5
CONCURRENT_REQUESTS_PER_DOMAIN = 1
CONCURRENT_REQUESTS_PER_IP = 0
DOWNLOAD_TIMEOUT = 180
DOWNLOADER_DEBUG = True
DOWNLOAD_DELAY=2
TELNETCONSOLE_ENABLED = 0
WEBSERVICE_ENABLED = 0
ITEM_PIPELINES = { 
    'tmall_fp_product.pipelines.TmallFpProductPipeline': 300, 
}

LOG_LEVEL = "WARNING"
LOG_FILE = "tmall_fp_product.log"

