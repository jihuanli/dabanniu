#coding=utf-8
import sys,re,os
from scrapy.selector import Selector
from scrapy.spider import Spider
from scrapy.http import Response, Request
from jumeiProduct.items import JumeiProductItem
from datetime import datetime
from .spider_common import *
import json as json_mod
from scrapy import signals,log
from urllib import quote
import urllib
import json
import httplib

class JumeiProductSpider(Spider):
    name = "jumeiProduct"
    allowed_domains = ["jumei.com"]
    jumei_search_url_prefix = "http://search.jumei.com/?filter=0-11-"
    jumei_product_url_prefix = "http://mall.jumei.com/product_"
    max_page_no = 400
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
            dest_url = str("/gettask?spider_name=") + str(self.spider_name).strip() + "&spider_type=" + self.name
            print dest_url
            conn.request('GET', dest_url)
            task_data = conn.getresponse().read()
            if task_data.find("taskId") == -1:
                log.err("Task error:missing task id")
                continue
            conn.close()
            task_json_data = json.loads(task_data)
            meta = {}
            meta["task_id"] = task_json_data[0]['taskId']
            for page_no in range(1, self.max_page_no):
                start_url = self.jumei_search_url_prefix + str(page_no) 
                yield Request(start_url, meta = meta, callback = self.parse, priority = 5)

    def parse_list_page(self, response):
        hxs = Selector(response)
        for pid in hxs.xpath('.//div[@class="products_wrap"]/ul/li/@pid').extract():
            url = self.jumei_product_url_prefix + pid + ".html"
            response.meta['product_id'] = pid
            yield Request(url, meta = response.meta, callback = self.parse_detail_page, priority = 5)

    def parse_detail_page(self, response):
        hxs = Selector(response)
        jumeiProduct = JumeiProductItem()
        jumeiProduct['product_id'] = response.meta['product_id']
        
        # product_name
        product_name = first_item(hxs.xpath('.//div[@id="detail_top"]/h1/span/text()').extract())
        if not product_name:
            return
        jumeiProduct['product_name'] = product_name.strip()
        
        # price       
        price = first_item(hxs.xpath('.//span[@id="mall_price"]/text()').extract())
        if not price:
            price = '0'
        jumeiProduct['price'] = price.strip()
    
        market_price = first_item(hxs.xpath('.//span[@id="info_market_price"]/text()').extract())
        if not market_price:
            market_price = '0'
        jumeiProduct['market_price'] = market_price.strip()
        
        # pic_url
        jumeiProduct['pic_url'] ="\n".join(hxs.xpath('.//div[@class="ac_container"]/ul/li/img/@jqimg').extract()).replace(u' ','')
        
        #rating
        rating = first_item(hxs.xpath('.//div[@class="koubei"]/span/label/text()').extract())
        if not rating:
            rating = '0'
        jumeiProduct['rating'] = rating.strip()
        
        #like_num
        like_num = first_item(hxs.xpath('.//div[@class="koubei"]/span/a[1]/text()').extract())
        if not like_num:
            like_num = '0'
        jumeiProduct['like_num'] = like_num.strip()
        
        # comment_num 
        comment_num = first_item(hxs.xpath('.//div[@class="koubei"]/span/a[2]/text()').extract())
        if not comment_num:
            comment_num = 0
        jumeiProduct['comment_num'] = comment_num
        
        detail = "\n".join(hxs.xpath('.//div[@id="product_parameter"]/text()').extract())
        if not detail:
            detail = ''
        jumeiProduct['detail'] = detail.strip()
        
        jumeiProduct['task_id'] = response.meta.get("task_id")
        
        all_parameter_info_key = hxs.xpath('.//div[@id="product_parameter"]/table/tr/td/b/text()').extract()
        all_parameter_info_value = hxs.xpath('.//div[@id="product_parameter"]/table/tr/td/span/text()').extract()
        brand_name = ''
        effect = ''
        capacity = ''
        other_info = ''
        product_name = None
        if all_parameter_info_key:
            index = 0 
            for key in all_parameter_info_key:
                key = key.replace(u'\xa0','')
                key = key.replace(u'：','')
                if key == u'商品名称':
                    product_name = all_parameter_info_value[ index ]
                elif key == u'品牌':
                    brand_name = all_parameter_info_value[ index ]
                elif key == u'功效':
                    effect = all_parameter_info_value[ index ]
                elif key == u'产品容量':
                    capacity = all_parameter_info_value[ index ]
                else:
                    other_info = other_info + key + '\n' + all_parameter_info_value[ index ] + '\n'
                index = index + 1
        if product_name:
            jumeiProduct['product_name'] = product_name.strip()
        jumeiProduct['brand_name'] = brand_name.strip()
        jumeiProduct['effect'] = effect.strip()
        jumeiProduct['capacity'] = capacity.strip()
        jumeiProduct['other_info'] = other_info.strip()
        yield jumeiProduct
    def parse(self, response):
        meta=response.meta
        if not meta.get("task_id"):
            log.error("===================Error... missing task_id")
        return self.parse_list_page(response)