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
from lefeng_product.items import LeFengProduct

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

class LeFengProductPipeline(object):
    def __init__(self): 
        return

    def process_item(self, item, spider):
        result_sql = ""
        if not item : return None
        if isinstance(item, LeFengProduct):
            result_sql = self._product_insert(item)
        elif isinstance(item, LeFengProductPic):
            result_sql = self._product_pic_insert(item)

        #dump to files
        timestamp = time.strftime('%Y-%m-%d',time.localtime(time.time()))
        result_file_name = str(spider.result_filename_prefix) + str(item.get('task_id')) + "_" + str(timestamp) + "_" + str(spider.result_filenname_suffix)
        result_file = open(result_file_name, 'a')
        result_sql = result_sql.encode("utf-8")
        result_sql = result_sql.replace("None", "null")
        result_sql = result_sql + "\n"
        result_file.write(result_sql)
        result_file.flush()
        result_file.close()
        return item 


    def _product_insert(self, item):
        if item.get('product_id'):
            return "insert into lefeng_product(product_id, product_name, market_price, pic_url, comment_num, like_num) values(%s, '%s', '%s', '%s', '%s', '%s');" % (item['product_id'], TransformSQLString(item['product_name']), item['market_price'], TransformSQLString(item['product_pics']), item['comment_count'], item['favor_count'])

    def handle_error(self, e):
        log.err(e)  

