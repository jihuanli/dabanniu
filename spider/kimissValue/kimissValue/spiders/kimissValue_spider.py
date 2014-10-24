#coding:UTF-8
from scrapy.selector import Selector
from scrapy.http import Request
import re
from scrapy.log import err
from scrapy.spider import BaseSpider
from kimissValue.items import TotalItem,DetailItem,ContentItem
import httplib
import json
import os
class KimissValueSpider(BaseSpider):
    name="kimissValue"
    allowed_domain=["kimiss.com"]
    #start_urls=["http://product.kimiss.com/product/5711/1/"]
    urlAll=[]
    
    kimiss_url_prefix="http://product.kimiss.com/product/"
    #result filename format: "prefix+product_id+task_id+.sql"
    conf_path=os.path.expanduser("~/app-root/data/")
    result_filename_prefix=os.path.expanduser("~/app-root/data/"+name+"/")
    if not os.path.isdir(result_filename_prefix):
        os.makedirs(result_filename_prefix)
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
    #construct the request from the start urls
    def start_requests(self):
        while True:
            self.urlAll=[]
            conn=httplib.HTTPConnection("182.92.67.121","8888") 
            dest_url="/gettask?spider_name="+self.spider_name+"&spider_type="+self.name
            print dest_url
            conn.request('GET',dest_url)
            task_data=conn.getresponse().read()   
            if task_data.find("taskId")==-1:
                continue
            if task_data.find("productId")==-1:
                continue
            conn.close()
            task_json_data=json.loads(task_data)
            head={}
            head["task_id"]=task_json_data[0]['taskId']
            head["product_id"]=task_json_data[0]['productId']
            start_url=self.kimiss_url_prefix+str(task_json_data[0]['productId'])+"/1/"
            yield Request(start_url,meta=head,callback=self.parse)
    def kaka(self,response):
        total=TotalItem()
        detail=DetailItem()
        content=ContentItem()
        hxs=Selector(response)
        hea=response.meta
        number=0
        total['productId']=hea['product_id']
        total_veryGood=hxs.xpath("//div[@class='user_content']/div/table/tr/td/table/tr[1]/td/div[4]/text()").extract()
        total['veryGood']=total_veryGood[0].replace(u"条","")
        total_good=hxs.xpath("//div[@class='user_content']/div/table/tr/td/table/tr[2]/td/div[4]/text()").extract()
        total['good']=total_good[0].replace(u"条","")
        total_common=hxs.xpath("//div[@class='user_content']/div/table/tr/td/table/tr[3]/td/div[4]/text()").extract()
        total['common']=total_common[0].replace(u"条","")
        total_bad=hxs.xpath("//div[@class='user_content']/div/table/tr/td/table/tr[4]/td/div[4]/text()").extract()
        total['bad']=total_bad[0].replace(u"条","")
        total_veryBad=hxs.xpath("//div[@class='user_content']/div/table/tr/td/table/tr[5]/td/div[4]/text()").extract()
        total['veryBad']=total_veryBad[0].replace(u"条","")
        total['taskId']=hea['task_id']
        yield total               
        err("=======================================")
        content_element=hxs.xpath("//div[@class='comment_area']")
        if content_element:       
            for letter in content_element:
                content['productId']=hea['product_id']
                content_title=letter.xpath("./div[@class='iwom']/span[1]/a/text()").extract()
                if content_title:
                    content['title']=content_title[0]
                else:
                    content['title']=""
                content_comment_time=letter.xpath("./div[@class='iwom']/span[2]/text()").extract()
                if content_comment_time:
                    content['comment_time']=content_comment_time[0]  
                else:
                    content['comment_time']=""
                content_buying=letter.xpath("./div[@class='buying'][1]/span[@class='comment_content']/text()").extract()
                if content_buying:
                    content_buying_join=" ".join(content_buying)
                    content['buying']=content_buying_join
                else:
                    content['buying']=""
                content_content=letter.xpath("./div[@class='buying'][2]/span/text()").extract()
                if content_content:
                    content_effectA=re.sub("<[^>]+>","",content_content[0])
                    content['content']=content_effectA
                else:
                    content['content']=""
                content_commentId=letter.xpath("./div[@class='iwom']/span[@class='comment_title']/@id").extract()
                content['commentId']=content_commentId[0].replace("title_","")
                content['taskId']=hea['task_id']
                yield content
     
                detail_element=hxs.xpath("//div[@class='userm']").extract()
                letterA=detail_element[number]
                detail['productId']=hea['product_id']
                detail_hair=re.search(u"<br[ ]*>([^<]+)发质",letterA)
                if detail_hair:
                    detail['hair']=detail_hair.group(1)
                else:
                    detail['hair']=""
                detail_skin=re.search(u"<br[^<]*>([^<]+)皮肤",letterA)
                if detail_skin:
                    detail['skin']=detail_skin.group(1)
                else:
                    detail['skin']=""
                detail_age=re.search(u"<br[^<]+年龄:(.+)</div>",letterA)
                if detail_age:
                    detail['age']=detail_age.group(1)
                else:
                    detail['age']=""
                detail_commentId=letter.xpath("./div[@class='iwom']/span[@class='comment_title']/@id").extract()
                detail['commentId']=detail_commentId[0].replace("title_","")
                detail['taskId']=hea['task_id']
                yield detail

                number+=1
        other_page=hxs.xpath("//div[@align='right']/div[@align='right']").extract()
        if other_page:
            other_page_a=other_page[0]
            other_page_b=other_page_a.strip()
            if "\n" in other_page_b:
                other_page_b=other_page_b.replace("\n","")
            result=re.search(u"当前页：[0-9]+/([0-9]+) 第",other_page_b)
            if result:
                page=result.group(1)
                list_page=range(2,int(page)+1)
                for letter in list_page:
                    url_url_url="http://product.kimiss.com/product/"+str(hea['product_id'])+"/"+str(letter)+"/"
                    if url_url_url not in self.urlAll:
                        (self.urlAll).append(url_url_url)
                        yield Request(url_url_url,callback=self.kaka,meta=hea)
    def parse(self,response):
        return self.kaka(response)



        
     
