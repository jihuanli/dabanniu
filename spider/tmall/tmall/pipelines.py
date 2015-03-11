# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import MySQLdb
from tmall.items import ProductItem
from scrapy.log import err
import time
class TmallPipeline(object):
    def process_item(self, item, spider):
        if isinstance(item,ProductItem):
            result_sql = self.product(item)   
            err("+++++++++++++++++++++++++++++++++")
            err(result_sql) 
            err("+++++++++++++++++++++++++++++++++")
        timestamp=time.strftime('%Y-%m-%d',time.localtime(time.time()))
        result_file_name=str(spider.result_filename_prefix)+str(item['catId'])+"_"+str(item['taskId'])+"_"+str(timestamp)+"_"+str(spider.result_filename_suffix)
        result_file=open(result_file_name,'a')
        result_sql=result_sql.encode("utf-8")
        result_sql=result_sql.replace("None","null")
        result_sql=result_sql+"\n"
        result_file.write(result_sql)
        result_file.close()
        return item
         
    def product(self,item):
        sql = "insert into tmall(productId,brand,name,promote_price,origin_price,standard,send_address,url,catId)values(%s,'%s','%s',%s,'%s','%s','%s','%s',%s)" % (long(item['productId']),item['brand'],item['name'],float(item['promote_price']),item['origin_price'],item['standard'],item['send_address'],item['url'],item['catId'])
        return sql 
