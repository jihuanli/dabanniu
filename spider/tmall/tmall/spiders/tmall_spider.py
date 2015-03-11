#coding:UTF-8
from scrapy.selector import HtmlXPathSelector
from scrapy.spider import BaseSpider
from scrapy.log import err
from scrapy.http import Request,Response
from tmall.items import ProductItem
import re
import HTMLParser
import httplib
import json
import os

class TmallSpider(BaseSpider):
    name = "tmall"
    allowed_domain = ["tmall"]
    tmall_url_prefix = "http://list.tmall.com/search_product.htm?cat=" 
    tmall_url_suffix = "&s="

    conf_path=os.path.expanduser("~/app-root/data/")
    result_filename_prefix=os.path.expanduser("~/app-root/data/"+name+"/")
    if not os.path.isdir(result_filename_prefix):
        os.mkdir(result_filename_prefix)
    result_filename_suffix=name+".sql"
 
    # spider conf
    spider_conf_filename=conf_path+"spider.conf"
    spider_name=""
    if os.path.isfile(spider_conf_filename):
        spider_file=open(spider_conf_filename)
        spider_name=spider_file.readline()
        spider_name=spider_name.replace(" ","")
        spider_name=spider_name.replace("\n","")
        spider_file.close()
 
    def start_requests(self):
        while True:
            conn=httplib.HTTPConnection("182.92.67.121","8888")
            task_url="/gettask?spider_name="+self.spider_name+"&spider_type="+self.name
            conn.request('GET',task_url)
            response_result = conn.getresponse().read()
            if response_result.find("taskId")==-1:
                continue
            if response_result.find("productId")==-1:
                continue                
            if response_result.find("keyword")==-1:
                continue
            conn.close()      
            response_dic = json.loads(response_result)
            pageId = (response_dic[0]["productId"]-1)*60 
            start_url = self.tmall_url_prefix+response_dic[0]["keyword"]+self.tmall_url_suffix+str(pageId)
            head={}
            head["catId"] = int(response_dic[0]["keyword"])
            head["taskId"] = response_dic[0]["taskId"]
            yield Request(start_url,callback=self.parse,meta=head) 
             
    def detail_page(self,response):
        hxs = HtmlXPathSelector(response)
        hea = response.meta
        html_parser = HTMLParser.HTMLParser()
        product = ProductItem()
        re_url = re.search("id=([0-9]+)&skuId",response.url)
        product['productId'] = re_url.group(1)
        product['url'] = response.url
        product['promote_price'] = hea["price"]
        origin_price_re = re.search('defaultItemPrice\":\"([^"]*)\",',response.body)
        product['origin_price'] = origin_price_re.group(1)
        product_send_address = hxs.select("//input[@name='region']/@value").extract()
        if product_send_address:
            product['send_address'] = product_send_address[0]
        else:
            product['send_address'] = ""
        product_standard = hxs.select("//ul[@class='tm-clear J_TSaleProp  ']/li/a/span/text()").extract()
        if product_standard:
            product['standard'] = product_standard[0]
        else:
            product['standard'] = ""
        product_name = hxs.select("//input[@name='title']/@value").extract()
        product['name'] = html_parser.unescape(product_name[0])
        re_brand = re.search("brand\":\"([^,]*)\"",response.body)
        if re_brand:
            product_brand = re_brand.group(1)
            product['brand'] = html_parser.unescape(product_brand)
        else:
            product['brand'] = ""
        product['catId'] = int(hea["catId"])
        product['taskId'] = hea["taskId"]
        yield product

    def list_page(self,response):
        hxs = HtmlXPathSelector(response)
        url_price = hxs.select("//div[@class='product']/div[@class='product-iWrap']")
        for letter in url_price:
            url_one = letter.select("./div[@class='productImg-wrap']/a[1]/@href").extract()
            price_one = letter.select("./p[@class='productPrice']/em/@title").extract()
            head = response.meta
            head["price"] = price_one[0]
            yield Request("http:"+url_one[0],callback=self.detail_page,meta=head)
 
    def parse(self,response):
        return self.list_page(response)
    














