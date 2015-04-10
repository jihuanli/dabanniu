# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import time
import codecs
import os
import md5
from twisted.enterprise import adbapi 
from scrapy import log
from baiduzhidao.items import ZhidaoQuestion,ZhidaoAnswer,RelatedQuestion,QuestionPic,AnswerPic, QuestionViewNum,RelatedTopic
import httplib
from urllib import quote

#get md5 of a input string 
def GetStringMD5(to_md5_str):
    m = md5.new()
    m.update(to_md5_str)
    return m.hexdigest()

def TransformSQLString(sql_str):
    if sql_str == None:
        return ""
    sql_str = sql_str.replace("\n", "\\n");
    sql_str = sql_str.replace("'", "\'")  
    return sql_str

class BaiduzhidaoPipeline(object):
    def __init__(self): 
        return

    def process_item(self, item, spider):
        result_sql = ""
        if not item :
            return None
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
        if item.get('task_type') != None and item.get('task_type') == 1:
            conn = httplib.HTTPConnection('182.92.67.121',8888) 
            dest_url = str("/insertTemp?sql=") + quote(result_sql.encode("utf-8"))
            print "dest_url" + dest_url
            conn.request('GET', dest_url)
        timestamp = time.strftime('%Y-%m-%d',time.localtime(time.time()))
        result_file_name = str(spider.result_filename_prefix) + str(item.get('product_id')) + "_" + str(item.get('task_id')) + "_" + str(timestamp) + "_" + str(spider.result_filenname_suffix)
        result_file = open(result_file_name, 'a')
        result_sql = result_sql.encode("utf-8")
        result_sql = result_sql.replace("None", "null")
        result_sql = result_sql + "\n"
        result_file.write(result_sql)
        result_file.flush()
        result_file.close()
        return item 


    def _question_insert(self, item):
        if item.get('questionId'):
            md5_str = GetStringMD5(str(item['questionId']) + str(item['product_id']))
            sql = "insert into question(productId, questionId, url, title, content, supplyContent, category, userName, time,keyword, isFinish, md5) values(%s, %s, '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', %s, '%s');" % (item['product_id'], item['questionId'], TransformSQLString(item['url']), TransformSQLString(item['title']), TransformSQLString(item['content']), TransformSQLString(item['supplyContent']), TransformSQLString(item['category']), TransformSQLString(item['userName']), TransformSQLString(item['time']), TransformSQLString(item['keyword']), item['isFinish'], md5_str)
            return sql

    def _answer_insert(self, item):
        if item.get('questionId'):
            md5_str = GetStringMD5(str(item['questionId']) + str(item['answerId']))
            sql = "insert into answer (answerId, questionId, likeNum, content, userName, time, isBest, md5) values(%s, %s, %s, '%s', '%s', '%s', %s, '%s');" % (item['answerId'], item['questionId'], item['likeNum'], TransformSQLString(item['content']), TransformSQLString(item['userName']), TransformSQLString(item['time']), item['isBest'], md5_str)
            return sql

    def _related_question_insert(self, item):
        if item.get('questionId'):
            md5_str = GetStringMD5(str(item['questionId']) + str(item['relatedId']))
            sql = "insert into relatedQuestion (relatedId, questionId, likeNum, title, time, md5) values(%s, %s, %s, '%s', '%s', '%s');" % (item['relatedId'], item['questionId'], item['likeNum'], TransformSQLString(item['title']), TransformSQLString(item['time']), md5_str)
            return sql

    def _related_topic_insert(self, item):
        if item.get('questionId'):
            md5_str = GetStringMD5(str(item['questionId']) + str(item['relatedId']))
            sql = "insert into relatedTopic (relatedId, questionId, likeNum, title, time, md5) values(%s, %s, %s, '%s', '%s', '%s');" % (item['relatedId'], item['questionId'], item['likeNum'], TransformSQLString(item['title']), TransformSQLString(item['time']), md5_str)
            return sql

    def _question_pic_insert(self, item):
        if item.get('questionId'):
            md5_str = GetStringMD5(str(item['questionId']) + str(item['picUrl']))
            sql = "insert into questionPic (questionId, picUrl, md5) values(%s, '%s', '%s');" % (item['questionId'], TransformSQLString(item['picUrl']), md5_str)
            return sql

    def _answer_pic_insert(self, item):
        if item.get('answerId'):
            md5_str = GetStringMD5(str(item['answerId']) + str(item['picUrl']))
            sql = "insert into answerPic (answerId, picUrl, md5) values(%s, '%s', '%s');" % (item['answerId'], TransformSQLString(item['picUrl']), md5_str)
            return sql

    def _question_view_update(self, item):
        if item.get('questionId'):
            sql = "update question set viewNum = %s where questionId = %s;" % (item['viewNum'],item['questionId'])
            return sql

    def handle_error(self, e):
        log.err(e)  

