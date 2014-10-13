# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import time
import codecs
import os
from twisted.enterprise import adbapi 
from scrapy import log
from baiduzhidao.items import ZhidaoQuestion,ZhidaoAnswer,RelatedQuestion,QuestionPic,AnswerPic, QuestionViewNum,RelatedTopic

class BaiduzhidaoPipeline(object):
    def __init__(self): 
        return

    def process_item(self, item, spider):
        result_sql = ""
        if not item : return None
        if isinstance(item,ZhidaoQuestion):
            result_sql = self._question_insert(item)
        elif isinstance(item,ZhidaoAnswer):
            result_sql = self._answer_insert(item)
        elif isinstance(item,RelatedQuestion):
            result_sql = self._related_question_insert(item)
        elif isinstance(item,RelatedTopic):
            result_sql = self._related_topic_insert(item)
        elif isinstance(item,QuestionPic):
            result_sql = self._question_pic_insert(item)
        elif isinstance(item,AnswerPic):
            result_sql = self._answer_pic_insert(item)
        elif isinstance(item,QuestionViewNum):
            result_sql = self._question_view_update(item)

        #dump to files
        timestamp = time.strftime('%Y-%m-%d',time.localtime(time.time()))
        result_file_name = spider.result_filename_prefix + item.get('product_id') + "_" + item.get('task_id') + "_" + timestamp + "_" + spider.result_filenname_suffix
        print result_file_name
        result_file = open(result_file_name, 'a')
        result_sql = result_sql.encode("utf-8")
        result_file.write(result_sql)
        result_file.flush()
        result_file.close()
        return item 


    def _question_insert(self, item):
        if item.get('questionId'):
            return "insert into product_question(product_id,question_id) values (%s, %s);\ninsert into question(questionId, url, title, content, supplyContent, category, userName, time,keyword, isFinish) values(%s, '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', %s);\n" % (item['product_id'],item['questionId'],item['questionId'],item['url'],item['title'],item['content'],item['supplyContent'],item['category'],item['userName'],item['time'],item['keyword'],item['isFinish'])

    def _answer_insert(self, item):
        if item.get('questionId'):
            return "insert into answer (answerId,questionId,likeNum,content,userName,time,isBest) values(%s, %s, %s, '%s', '%s', '%s', %s);\n" % (item['answerId'],item['questionId'],item['likeNum'],item['content'],item['userName'],item['time'],item['isBest'])

    def _related_question_insert(self, item):
        if item.get('questionId'):
            return "insert into relatedQuestion ( relatedId, questionId, likeNum, title, time) values(%s, %s, %s, '%s', '%s');\n" % (item['relatedId'],item['questionId'],item['likeNum'],item['title'],item['time'])

    def _related_topic_insert(self, item):
        if item.get('questionId'):
            return "insert into relatedTopic (relatedId, questionId, likeNum, title, time) values(%s, %s, %s, '%s', '%s');\n" % (item['relatedId'],item['questionId'],item['likeNum'],item['title'],item['time'])

    def _question_pic_insert(self, item):
        if item.get('questionId'):
            return "insert into questionPic ( questionId, picUrl) values(%s, '%s');\n" % (item['questionId'],item['picUrl'])

    def _answer_pic_insert(self, item):
        if item.get('answerId'):
            return "insert into answerPic ( answerId, picUrl) values(%s, '%s');\n" % (item['answerId'],item['picUrl'])

    def _question_view_update(self, item):
        if item.get('questionId'):
            return "update question set viewNum = %s where questionId = %s;\n" % (item['viewNum'],item['questionId'])

    def handle_error(self, e):
        log.err(e)  

