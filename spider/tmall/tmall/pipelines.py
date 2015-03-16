# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import MySQLdb
from tmall.items import ProductCommonItem,ProductImgItem,ProductDetailItem,ProductSizeItem
from scrapy.log import err
import time
import md5
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

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


class TmallPipeline(object):
    def process_item(self, item, spider):
        if isinstance(item,ProductCommonItem):
            result_sql = self.common(item)  
        if isinstance(item,ProductImgItem):
            result_sql = self.img(item) 
        if isinstance(item,ProductDetailItem):
            result_sql = self.detail(item)
        if isinstance(item,ProductSizeItem):
            result_sql = self.size(item)
        timestamp=time.strftime('%Y-%m-%d',time.localtime(time.time()))
        result_file_name=str(spider.result_filename_prefix)+str(item['productId'])+"_"+str(item['taskId'])+"_"+str(timestamp)+"_"+str(spider.result_filename_suffix)
        result_file=open(result_file_name,'a')
        result_sql=result_sql.encode("utf-8")
        result_sql=result_sql.replace("None","null")
        result_sql=result_sql+"\n"
        result_file.write(result_sql)
        result_file.close()
        return item
         
    def common(self,item):
        sql = "insert into tmall(productId,brand,name,send_address,url,catId,parameter,description)values(%s,'%s','%s','%s','%s',%s,'%s','%s');" % (long(item['productId']),TransformSQLString(str(item['brand'])),TransformSQLString(str(item['name'])),TransformSQLString(str(item['send_address'])),TransformSQLString(str(item['url'])),int(item['catId']),TransformSQLString(str(item['parameter'])),TransformSQLString(str(item['description'])))
        return sql 

    def img(self,item):
        md5_str = GetStringMD5(str(item['productId'])+item['brand_big_img'])
        sql =  "insert into tmall_img(productId,brand_big_img,brand_little_img,md5)values(%s,'%s','%s','%s');" % (long(item['productId']),TransformSQLString(str(item['brand_big_img'])),TransformSQLString(str(item['brand_little_img'])),md5_str)
        return sql
     
    def detail(self,item):
        md5_str=GetStringMD5(str(item['productId'])+str(item['color_name'])+str(item['standard']))
        sql =  "insert into tmall_detail(productId,origin_price,standard,skuId,color_big_img,color_little_img,color_name,stock,md5)values(%s,%s,'%s',%s,'%s','%s','%s',%s,'%s');" % (long(item['productId']),float(item['origin_price']),TransformSQLString(str(item['standard'])),item['skuId'],TransformSQLString(str(item['color_big_img'])),TransformSQLString(str(item['color_little_img'])),TransformSQLString(str(item['color_name'])),item['stock'],md5_str)
        return sql

    def size(self,item):
        sql = "update tmall_detail set origin_price = '%s' and promot_price ='%s' where productId=%s and skuId=%s;" % (TransformSQLString(str(item['price'])),TransformSQLString(str(item['promot_price'])),str(item['productId']),str(item['skuId']))
        return sql
