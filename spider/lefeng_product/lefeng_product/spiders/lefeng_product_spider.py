#coding=utf-8
import sys,re,os
from scrapy.selector import Selector
from scrapy.spider import Spider
from scrapy.http import Response,Request
from lefeng_product.items import LeFengProduct
from datetime import datetime
from .spider_common import *
import json as json_mod
from scrapy import signals,log
from urllib import quote
import urllib
import json
import httplib 

class LeFengProductSpider(Spider):
    name = "lefeng_product"
    allowed_domains = ["lefeng.com"]
    lefeng_product_url_prefix = "http://s.lefeng.com/directory/26000_0_0_0_0_0_0_0_";
    max_page_no = 170 
    #url match pattern
    detail_page_pattern = re.compile(r'http://product.lefeng.com/product/([0-9]+).html')

    #result filename format: "prefix + product_id + task_id + .sql"
    conf_path = os.path.expanduser("~/app-root/data/")
    result_filename_prefix = os.path.expanduser("~/app-root/data/" + name + "/");
    result_filenname_suffix = name + ".sql"

    html_tag_pattern = re.compile(r'<[^>]+>')
    spider_name = ""
    
    def load_conf(self):
        spider_conf_filename = self.conf_path + "spider.conf"
        if os.path.isfile(spider_conf_filename):
            spider_file = open(spider_conf_filename)
            self.spider_name = spider_file.readline()
            spider_file.close();

    def init(self):
        # create data dir
        if not os.path.isdir(self.result_filename_prefix):
            os.makedirs(self.result_filename_prefix)
        self.load_conf()

    #construct the request from the start utls
    def start_requests(self):
        self.init()
        while True:
            if self.spider_name == None or self.spider_name == "" :
                self.load_conf();
            conn=httplib.HTTPConnection('182.92.67.121',8888)
            dest_url = str("/gettask?spider_name=") + str(self.spider_name) + "&spider_type=" + self.name
            conn.request('GET', dest_url)
            task_data = conn.getresponse().read()
            if task_data.find("taskId") == -1:
                log.err("Task error:missing task id")
                continue
            if task_data.find("productId") == -1:
                log.err("Task error:missing product id")
                continue
            if task_data.find("keyword") == -1:
                log.err("Task error:missing keyword")
                continue
            conn.close()
            task_json_data = json.loads(task_data)
            meta = {}
            meta["task_id"] = task_json_data[0]['taskId']
            for page_no in range(1, self.max_page_no):
                start_url = self.lefeng_product_url_prefix + str(page_no) + ".html"  
                yield Request(start_url, meta = meta, callback = self.parse, priority = 5)

    def parse_list_page(self, response):
        hxs = Selector(response)
        for url in hxs.xpath('.//dd[@class="nam"]/a/@href').extract():
            product_id = self.detail_page_pattern.search(url).group(1)
            response.meta['product_id'] = product_id
            yield Request(url, meta = response.meta, callback = self.parse_detail_page, priority = 5)

    def parse_detail_page(self, response):
        hxs = Selector(response)
        lefeng_product = LeFengProduct()
        lefeng_product['product_id'] = response.meta['product_id']
        lefeng_product['task_id'] = response.meta['task_id']

        # product_name
        product_name = first_item(hxs.xpath('.//span[@class="pname"]/text()').extract())
        if not product_name:
            return
        lefeng_product['product_name'] = product_name.strip()
       
        # market_price       
        market_price = first_item(hxs.xpath('.//p[@class="specials"]/del/text()').extract()) 
        tmp_str = "市场价："
        market_price = market_price.replace(tmp_str.decode("utf-8"),"")
        lefeng_product['market_price'] = market_price
       
        # product_pics
        pic_url = first_item(hxs.xpath('.//img[@class="jqzoom"]/@src').extract()) 
        if not pic_url:
            pic_url = first_item(hxs.xpath('//div[@class="pic"]/img/@src').extract())
        lefeng_product['product_pics'] = pic_url

        # comment_count 
        comment_count = first_item(hxs.xpath('.//table[@class="hpl"]/tbody/tr/td/i/em/text()').extract())
        if not comment_count:
            comment_count = 0
        lefeng_product['comment_count'] = comment_count
        
        # favor_count
        favor_count = first_item(hxs.xpath('.//a[@class="save"]/@fc').extract())
        if not favor_count:
            favor_count = first_item(hxs.xpath('.//a[@class="save"]/span/text()').extract())
        lefeng_product['favor_count'] = favor_count

        yield lefeng_product

    def parse(self, response):
        meta=response.meta
        if not meta.get("task_id"):
            log.err("===================Error... missing task_id=======================")
        return self.parse_list_page(response)
