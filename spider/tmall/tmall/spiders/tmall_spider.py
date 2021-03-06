#coding:UTF-8
from scrapy.selector import HtmlXPathSelector
from scrapy.spider import BaseSpider
from scrapy.log import err
from scrapy.http import Request,Response
from tmall.items import ProductCommonItem,ProductImgItem,ProductDetailItem,ProductSizeItem
import re
import HTMLParser
import httplib
import json
import os

class TmallSpider(BaseSpider):
    name = "tmall"
    allowed_domain = ["tmall"]
    tmall_url_prefix = "http://detail.tmall.hk/hk/item.htm?id=" 
    tmall_url_suffix = "&cat_id="

    m_product_detail_url_prefix = "http://detail.m.tmall.hk/item.htm?id=" 

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
            #pageId = (response_dic[0]["productId"]-1)*60 
            pc_start_url = self.tmall_url_prefix + str(response_dic[0]["productId"]) + self.tmall_url_suffix + response_dic[0]["keyword"]
            m_start_url = self.m_product_detail_url_prefix + str(response_dic[0]["productId"]) 
            head={}
            head["catId"] = int(response_dic[0]["keyword"])
            head["taskId"] = response_dic[0]["taskId"]
            head["productId"] = long(response_dic[0]["productId"])
            yield Request(pc_start_url,callback=self.parse,meta=head, priority = 5) 
            yield Request(m_start_url, callback=self.parseMobileProductDetail, meta=head) 
             
    def product(self,response):
        hxs = HtmlXPathSelector(response)
        hea = response.meta
        html_parser = HTMLParser.HTMLParser()
        common = ProductCommonItem()
        img = ProductImgItem()
        detail = ProductDetailItem()
        # 爬取产品详情页公共信息
        re_product_url = re.search("id=([0-9]+)",response.url)
        re_cat_url = re.search("cat_id=([0-9]+)",response.url)
        common['productId'] = re_product_url.group(1)
        common['catId'] = re_cat_url.group(1)
        common['taskId'] = hea['taskId']
        common['url'] = response.url
        common_send_address = hxs.select("//input[@name='region']/@value").extract()
        if common_send_address:
            common['send_address'] = common_send_address[0]
        else:
            common['send_address'] = ""
        common_name = hxs.select("//input[@name='title']/@value").extract()
        if common_name:
            common['name'] = html_parser.unescape(common_name[0])
        else:
            common['name'] = ""
        re_brand = re.search("brand\":\"([^,]*)\"",response.body)
        if re_brand:
            common_brand= re_brand.group(1)
            common['brand'] = html_parser.unescape(common_brand)
        else:
            common['brand'] = ""
        common_description = hxs.select("//div[@class='tb-detail-hd']/p/text()").extract()
        if common_description:
            common['description'] = common_description[0].strip()
        else:
            common['description'] = ""
        common_parameter = hxs.select("//ul[@id='J_AttrUL']/li/text()").extract()
        if  common_parameter: 
            common['parameter'] = self.process_data(common_parameter)
        else:
            common['parameter'] = ""
        yield common
        # 爬取产品详情页品牌图片
        img['productId'] = common['productId']
        img['taskId']= common['taskId']
        brand_little_img_list = hxs.select("//ul[@class='tb-thumb tm-clear']/li")
        for letter in brand_little_img_list:
            brand_little_img = letter.select("./a/img/@src").extract()
            if brand_little_img:
                img['brand_little_img'] = brand_little_img[0]
                img['brand_big_img'] = self.process_img(img['brand_little_img'])
            else:
                img['brand_little_img'] = ""
                img['brand_big_img'] = ""
            yield img
        # 爬取产品详情页详情信息
        detail['productId'] = img['productId']
        detail['taskId'] = img['taskId']
        detail_all = re.search("skuMap\":(.*)},\"valLoginIndicator\"",response.body)
        if detail_all:
            detail_data = detail_all.group(1)
            detail_dict = json.loads(detail_data)
            for letter in detail_dict:
                detail_detail = detail_dict[letter]
                detail['skuId'] = long(detail_detail['skuId'])
                detail['origin_price'] = detail_detail['price']
                detail['stock'] = int(detail_detail['stock'])
                letter = letter.replace(";","")
                if hxs.select("//ul[@class='tm-clear J_TSaleProp tb-img  ']/li[@data-value='"+letter+"']/@title").extract():
                    detail_color_name = hxs.select("//ul[@class='tm-clear J_TSaleProp tb-img  ']/li[@data-value='"+letter+"']/@title").extract()
                    detail['color_name'] = detail_color_name[0]
                else:
                    detail['color_name'] = ""
                if hxs.select("//ul[@class='tm-clear J_TSaleProp  ']/li[@data-value='"+letter+"']/a/span/text()").extract():
                    detail_standard = hxs.select("//ul[@class='tm-clear J_TSaleProp  ']/li[@data-value='"+letter+"']/a/span/text()").extract()
                    detail['standard'] = detail_standard[0]
                else:
                    detail['standard'] = ""
                if hxs.select("//ul[@class='tm-clear J_TSaleProp tb-img  ']/li[@data-value='"+letter+"']/a/@style").extract():
                    detail_little_img = hxs.select("//ul[@class='tm-clear J_TSaleProp tb-img  ']/li[@data-value='"+letter+"']/a/@style").extract()
                    re_img = re.search("background:url\(([^)]*)\)",detail_little_img[0])
                    detail['color_little_img'] = re_img.group(1)
                    detail['color_big_img'] = self.process_img(detail['color_little_img'])
                else:
                    detail['color_little_img'] = ""
                    detail['color_big_img'] = ""
                yield detail 
        else:
            detail['skuId'] = 0
            detail_origin_price = re.search('defaultItemPrice\":\"([^"]*)\",',response.body)
            if detail_origin_price:
                detail['origin_price'] = detail_origin_price.group(1)
            else:
                detail['origin_price'] = 0
            detail_stock = re.search('quantity\":([0-9]*),',response.body)
            if detail_stock:
                detail['stock'] = detail_stock.group(1)
            else:
                detail['stock'] = 0
            detail['standard'] = ""
            detail['color_name'] = ""
            detail['color_little_img'] = ""
            detail['color_big_img'] = ""   
            yield detail

    def process_img(self,img):
        if img.find("60x60")!=-1:
            img = img.replace("60x60","430x430")
            return img
        if img.find("40x40")!=-1:
            img = img.replace("40x40","430x430")
            return img
        return img

    def process_data(self,data):
        html_parser = HTMLParser.HTMLParser()
        data = html_parser.unescape(data)
        list_dict = []
        for letter in data:
            letter = letter.replace(":","@@")
            letter = letter.replace(u"：","@@")
            aa = letter.split("@@")
            list_dict.append((aa[0],aa[1]))
        json_data = json.dumps(dict(list_dict), ensure_ascii=False)
        return json_data
    #def list_page(self,response):
    #    hxs = HtmlXPathSelector(response)
    #    url_price = hxs.select("//div[@class='product']/div[@class='product-iWrap']")
    #    for letter in url_price:
    #        url_one = letter.select("./div[@class='productImg-wrap']/a[1]/@href").extract()
    #        price_one = letter.select("./p[@class='productPrice']/em/@title").extract()
    #        head = response.meta
    #        head["price"] = price_one[0]
    #        yield Request("http:"+url_one[0],callback=self.detail_page,meta=head)
 
    def parse(self,response):
        return self.product(response)

    def parseMobileProductDetail(self, response):
        product_size_info = ProductSizeItem()
        size_json = re.search("priceInfo\":(.*?),\"resultCode\":0,\"wanrentuanInfo", response.body)
        if size_json:
            size_json = size_json.group(1)
            size_json = size_json.decode("gbk")
            size_dict = json.loads(size_json)
            for skuid in size_dict:
                sku = size_dict[skuid]
                price = sku['price']['amount']
                promot_price = sku['promPrice']['price']
                #print "skuid[" + str(skuid) + "] price[" + str(price) + "]promPrice[" + str(promot_price) + "]"
                product_size_info['productId'] = response.meta['productId']
                product_size_info['taskId'] = response.meta['taskId']
                product_size_info['skuId'] = skuid
                product_size_info['price'] = price 
                product_size_info['promot_price'] = promot_price 
                yield product_size_info
        return 
