#coding:UTF-8
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
import re
from scrapy.log import err
from scrapy.spider import BaseSpider
from kimissValue.items import TotalItem,DetailItem
class KimissValueSpider(BaseSpider):
    name="kimissValue"
    allowed_domain=["kimiss.com"]
    start_urls=["http://product.kimiss.com/product/5711/1/"]
    def parse(self,response):
        total=TotalItem()
        detail=DetailItem()
        hxs=HtmlXPathSelector(response)
        total_veryGood=hxs.select("//div[@class='user_content']/div/table/tr/td/table/tr[1]/td/div[4]/text()").extract()
        total['veryGood']=total_veryGood[0].replace(u"条","")
        total_good=hxs.select("//div[@class='user_content']/div/table/tr/td/table/tr[2]/td/div[4]/text()").extract()
        total['good']=total_good[0].replace(u"条","")
        total_common=hxs.select("//div[@class='user_content']/div/table/tr/td/table/tr[3]/td/div[4]/text()").extract()
        total['common']=total_common[0].replace(u"条","")
        total_bad=hxs.select("//div[@class='user_content']/div/table/tr/td/table/tr[4]/td/div[4]/text()").extract()
        total['bad']=total_bad[0].replace(u"条","")
        total_veryBad=hxs.select("//div[@class='user_content']/div/table/tr/td/table/tr[5]/td/div[4]/text()").extract()
        total['veryBad']=total_veryBad[0].replace(u"条","")
        yield total               
        detail_detail=hxs.select("//div[@class='user_box']")
        for letter in detail_detail:
            detail_body=letter.select("./div[@class='userm']").extract()
            detail_hair=re.search(u"<br([^<]+发质)",detail_body[0])
            detail['hair']=detail_hair.group(1)
            detail_skin=re.search(u"<br([^<]+皮肤)",detail_body[0])
            detail['skin']=detail_skin.group(1)
            detail_age=re.search(u"<br[^<]+年龄：(.+)</div>",detail_body[0])
            if detail_age:
                detail['age']=detail_age.group(1)
            else:
                detail['age']=""
            detail_theme=letter.select("./div[@class='comment_area']/div[@class='iwom']/span[1]/a/text()").extract()
            detail['theme']=detail_theme[0]
            detail_time=letter.select("./div[@class='comment_area']/div[@class='iwom']/span[2]/text()").extract()
            detail['time']=detail_time[0]
            detail_purchase=letter.select("./div[@class='comment_area']/div[@class='buying'][1]/span[2]/text()").extract()
            detail['purchase']=detail_purchase[0]
            detail_effect=letter.select("./div[@class='comment_area']/div[@class='buying'][2]/span/text()").extract()
            detail_effectA=re.sub("<[^>]+>","",detail_effect[0])
            detail['effect']=detail_effectA
            yield detail
            




        
     
