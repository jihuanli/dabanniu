#coding=utf-8
import sys,re,os
from scrapy.selector import Selector
from scrapy.spider import Spider
from scrapy.http import Response, Request
from baiduzhidao.items import ZhidaoQuestion,ZhidaoAnswer,RelatedQuestion,QuestionPic,AnswerPic,QuestionViewNum,RelatedTopic
from datetime import datetime
from .spider_common import *
import json as json_mod
from scrapy import signals,log
from urllib import quote
import urllib
import json
import httplib 

#reload(sys) 
#sys.setdefaultencoding("utf-8")

class ZhidaoSpider(Spider):
    name = "zhidao"
    allowed_domains = ["zhidao.baidu.com"]
    zhidao_url_prefix = "http://zhidao.baidu.com/search?word=";
    #url match pattern
    detail_page_pattern = re.compile(r'zhidao.baidu.com/question/([0-9]+).html')
    view_num_url_pattern = re.compile(r'cp.zhidao.baidu.com/v.php\?q=([0-9]+)')

    #result filename format: "prefix + product_id + task_id + .sql"
    conf_path = os.path.expanduser("~/app-root/data/")
    result_filename_prefix = os.path.expanduser("~/app-root/data/" + name + "/");
    if not os.path.isdir(result_filename_prefix):
        os.makedirs(result_filename_prefix)
    result_filenname_suffix = name + ".sql"
    html_tag_pattern = re.compile(r'<[^>]+>')
    have_fetch_set = set()
    
    # spider conf
    spider_conf_filename = conf_path + "spider.conf"
    if os.path.isfile(spider_conf_filename):
        spider_file = open(spider_conf_filename)
        spider_name = spider_file.readline()
        spider_file.close();

    #construct the request from the start utls
    def start_requests(self):
        # task init
        while True:
            conn=httplib.HTTPConnection('182.92.67.121',8888)
            dest_url = str("/gettask?spider_name=") + str(self.spider_name) + "&spider_type=" + self.name
            conn.request('GET', dest_url)
            task_data = conn.getresponse().read()
            if task_data.find("taskId") == -1:
                continue
            if task_data.find("productId") == -1:
                continue
            if task_data.find("keyword") == -1:
                continue
            conn.close()
            task_json_data = json.loads(task_data)
            meta = {}
            meta["task_id"] = task_json_data[0]['taskId']
            meta["product_id"] = task_json_data[0]['productId']
            meta["keyword"] = task_json_data[0]["keyword"]
            start_url = self.zhidao_url_prefix + quote(task_json_data[0]['keyword'].encode("gbk"))
            yield Request(start_url, meta = meta, callback = self.parse, priority = 5)

    def parse_list_page(self, response):
        hxs = Selector(response)
        for url in hxs.xpath('.//a[@class="ti"]/@href').extract():
            yield Request(url, meta = response.meta, callback = self.parse_detail_page, priority = 5)
        for url in hxs.xpath('.//div[@class="pager"]/a/@href').extract():
            newUrl="http://zhidao.baidu.com" + url
            if not (newUrl in self.have_fetch_set):
                self.have_fetch_set.add(newUrl)
                yield Request(newUrl, meta = response.meta, callback = self.parse_list_page, priority = 5)

    def parse_viewnum_page(self, response):
        questionId = self.view_num_url_pattern.search(response.url).group(1)
        viewNumInfo = QuestionViewNum()
        viewNumInfo['product_id'] = response.meta["product_id"]
        viewNumInfo['task_id'] = response.meta["task_id"]
        viewNumInfo['questionId'] = questionId
        viewNumInfo['viewNum'] = response.body
        yield viewNumInfo

    def parse_detail_page(self,response):
        hxs = Selector(response)
        questionId = self.detail_page_pattern.search(response.url).group(1)
        guide = ZhidaoQuestion()
        title = first_item(hxs.xpath('.//span[contains(@class,"ask-title")]/text()').extract())
        if not title:
            log.err("no title")
            print "no title"
            return
        guide['title'] =  title.strip()
        guide['isFinish'] = 1
        # hack----zhidao  wordreplace
        wordReplace = first_item(hxs.xpath('.//pre[@class="line mt-10 q-content"]/img').extract())
        if wordReplace:
            guide['isFinish'] = 0
        wordReplace = first_item(hxs.xpath('.//div[@class="line mt-10 q-content"]/p/img').extract())
        if wordReplace:
            guide['isFinish'] = 0

        guide['content'] = "\n".join(hxs.xpath('.//pre[@class="line mt-10 q-content"]/text()').extract())

        if not guide['content']:
            guide['content'] =  "\n".join(hxs.xpath('.//div[@class="line mt-10 q-content"]/p/text()').extract())
        
        guide['supplyContent'] =  first_item(hxs.xpath('.//pre[@class="line mt-10 q-supply-content"]/text()').extract())
        if not guide['supplyContent']:
            guide['supplyContent'] = "\n".join(hxs.xpath('.//div[@class="line mt-10 q-supply-content"]/p/text()').extract())

        guide['category'] =  first_item(hxs.xpath('.//div[@id="ask-info"]/span/a[@class="f-aid"]/text()').extract())
        guide['userName'] =  first_item(hxs.xpath('.//div[@id="ask-info"]/a[@class="user-name"]/text()').extract())
        guide['time'] = first_item(hxs.xpath('.//span[@class="grid-r ask-time"]/text()').extract())
        guide['questionId'] = questionId
        guide['url'] = response.url
        guide['keyword']=response.meta["keyword"]
        guide['product_id'] = response.meta["product_id"]
        guide['task_id'] = response.meta["task_id"]
        yield guide

        for picUrl in hxs.xpath('//div[@id="wgt-ask"]/div/p/a/@href').extract():
            qp = QuestionPic()
            qp['questionId'] = questionId
            qp['picUrl'] = picUrl

            qp['product_id'] = response.meta["product_id"]
            qp['task_id'] = response.meta["task_id"]
            yield qp

        if guide['isFinish']==0:
            log.err("not finish======> %s" % response.url)
            return
        newUrl="http://cp.zhidao.baidu.com/v.php?q=" + questionId
        yield Request(newUrl, meta = response.meta, callback = self.parse_viewnum_page, priority = 8)

        ba = hxs.xpath('.//div[@class="wgt-best "]')
        if ba:
            ba=ba[0]
            best=ZhidaoAnswer()
            best['questionId'] = questionId
            best['isBest'] = 1
            best['product_id'] = response.meta["product_id"]
            best['task_id'] = response.meta["task_id"]

            wordReplace = first_item(ba.xpath('.//div[@class="bd answer"]/div[@class="line content"]/pre/img').extract())
            if wordReplace:
                log.err("================================================")
                log.err(response.url)
                return
            wordReplace = first_item(ba.xpath('.//div[@class="bd answer"]/div/div[@class="best-text mb-10"]/p/img').extract())
            if wordReplace:
                log.err("================================================")
                log.err(response.url)
                return
            best['content'] = "\n".join(ba.xpath('.//div[@class="bd answer"]/div[@class="line content"]/pre/text()').extract())
            if not best['content']:
                best['content'] =  "\n".join(ba.xpath('.//div[@class="bd answer"]/div/div[@class="best-text mb-10"]/p/text()').extract())

            best['userName'] =  first_item(ba.xpath('..//div[@class="bd answer"]/div/div/p/a[@class="user-name"]/text()').extract())
            if not best['userName']:
                best['userName'] =  u"热心网友"
            best['time'] =  ba.xpath('..//div[@class="hd line mb-10"]/span[@class="grid-r f-aid pos-time mt-20"]/text()').extract()[1].strip()
            best['likeNum'] =  first_item(ba.xpath('.//div[@class="bd answer"]/div/div/span[@class="evaluate evaluate-32"]/@data-evaluate').extract())
            best['answerId'] = first_item(ba.xpath('.//div[@class="bd answer"]/div/div/span[@class="evaluate evaluate-32"]/@id').re('evaluate-([0-9]+)'))
            yield best
            for picUrl in ba.xpath('.//div[@class="bd answer"]/div/div[@class="best-text mb-10"]/p/a/@href').extract():
                bap = AnswerPic()
                bap['product_id'] = response.meta["product_id"]
                bap['task_id'] = response.meta["task_id"]
                bap['answerId'] = best['answerId']
                bap['picUrl'] = picUrl
                yield bap
    
        ra = hxs.xpath('.//div[@class="wgt-recommend "]')
        if ra:
            ra=ra[0]
            best=ZhidaoAnswer()
            best['questionId'] = questionId
            best['isBest'] = 2
            best['product_id'] = response.meta["product_id"]
            best['task_id'] = response.meta["task_id"]

            wordReplace = first_item(ra.xpath('.//div[@class="bd answer"]/div[@class="line content"]/pre/img').extract())
            if wordReplace:
                og.err("================================================")
                log.err(response.url)
                eturn
            wordReplace = first_item(ra.xpath('.//div[@class="bd answer"]/div/div[@class="recommend-text mb-10"]/p/img').extract())
            if wordReplace:
                log.err("================================================")
                log.err(response.url)
                return
            best['content'] = "\n".join(ra.xpath('.//div[@class="bd answer"]/div[@class="line content"]/pre/text()').extract())
            if not best['content']:
                best['content'] =  "\n".join(ra.xpath('.//div[@class="bd answer"]/div/div[@class="recommend-text mb-10"]/p/text()').extract())

            best['userName'] =  first_item(ra.xpath('..//div[@class="bd answer"]/div/div/p/a[@class="user-name"]/text()').extract())
            if not best['userName']:
                best['userName'] =  u"热心网友"
            best['time'] =  ra.xpath('..//div[@class="hd line mb-10"]/span[@class="grid-r f-aid pos-time mt-20"]/text()').extract()[1].strip()
            best['likeNum'] =  first_item(ra.xpath('.//div[@class="bd answer"]/div/div/span[@class="evaluate evaluate-32"]/@data-evaluate').extract())
            best['answerId'] = first_item(ra.xpath('.//div[@class="bd answer"]/div/div/span[@class="evaluate evaluate-32"]/@id').re('evaluate-([0-9]+)'))
            yield best
            for picUrl in ra.xpath('.//div[@class="bd answer"]/div/div[@class="best-text mb-10"]/p/a/@href').extract():
                bap = AnswerPic()
                bap['product_id'] = response.meta["product_id"]
                bap['task_id'] = response.meta["task_id"]
                bap['answerId'] = best['answerId']
                bap['picUrl'] = picUrl
                yield bap
    
        for node in hxs.xpath('//div[@id="wgt-answers"]/div/div[@class="line"]/div[contains(@class,"content")]'):
            answer = ZhidaoAnswer()
            answer['product_id'] = response.meta["product_id"]
            answer['task_id'] = response.meta["task_id"]
            answer['questionId'] = questionId
            wordReplace = first_item(node.xpath('.//pre/img').extract())
            if wordReplace:
                log.err("================================================")
                log.err(response.url)
                return
            wordReplace = first_item(node.xpath('.//div[@class="answer-text mb-10"]/p/img').extract())
            if wordReplace:
                log.err("================================================")
                log.err(response.url)
                return
            answer['content']= "\n".join(node.xpath('.//pre/text()').extract())
            if not answer['content']:
                answer['content'] =  "\n".join(node.xpath('.//div[@class="answer-text mb-10"]/p/text()').extract())
            answer['userName'] =  first_item(node.xpath('..//div/a[@class="user-name"]/text()').extract())
            if not answer['userName']:
                answer['userName'] =  u"热心网友"
            answer['time'] =  node.xpath('..//div/span[@class="grid-r pos-time"]/text()').extract()[1].strip()
            answer['likeNum'] =  first_item(node.xpath('.//div/span[@class="evaluate"]/@data-evaluate').extract())
            answer['answerId'] =  first_item(node.xpath('.//div/span[@class="evaluate"]/@id').re('evaluate-([0-9]+)'))
            answer['isBest'] = 0 
            yield answer
            for picUrl in node.xpath('.//div[@class="answer-text mb-10"]/p/a/@href').extract():
                ap = AnswerPic()
                ap['product_id'] = response.meta["product_id"]
                ap['task_id'] = response.meta["task_id"]
                ap['answerId'] = answer['answerId']
                ap['picUrl'] = picUrl
                yield ap

        for node in hxs.xpath('//div[@id="wgt-related"]/div/ul/li'):
             rq = RelatedQuestion()
             rq['product_id'] = response.meta["product_id"]
             rq['task_id'] = response.meta["task_id"]
             rq['questionId'] = questionId
             rq['relatedId'] = first_item(node.xpath('.//a/@data-qid').extract())
             rq['time'] =  first_item(node.xpath('.//span/text()').extract())
             rq['title'] =  self.html_tag_pattern.sub("",first_item(node.xpath('.//a').extract()))
             rq['likeNum'] = first_item(node.xpath('.//em/span/text()').extract())
             if not rq['likeNum']:
                 rq['likeNum'] = 0
             yield rq

        for node in hxs.xpath('//div[@id="wgt-topic"]/ul/li'):
            rq = RelatedTopic()
            rq['product_id'] = response.meta["product_id"]
            rq['task_id'] = response.meta["task_id"]
            rq['questionId'] = questionId
            rq['relatedId'] = first_item(node.xpath('.//a/@href').re('([0-9]+).html'))
            rq['time'] =  first_item(node.xpath('.//span[@class="grid-r f-aid"]/text()').extract())
            rq['title'] =  first_item(node.xpath('.//a/text()').extract()).strip()
            rq['likeNum'] = first_item(node.xpath('.//span[@class="ml-5 f-red"]/text()').extract())
            if not rq['likeNum']:
                rq['likeNum'] = 0
            yield rq
    def parse(self, response):
        self.have_fetch_set.clear()
        meta=response.meta
        if not meta.get("product_id"):
            log.err("===================Error... missing product_id")
        return self.parse_list_page(response)
