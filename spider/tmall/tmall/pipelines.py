# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import MySQLdb
from tmall.items import ProductCommonItem,ProductImgItem,ProductDetailItem
from scrapy.log import err
import time
import md5
def GetStringMD5(to_md5_str):
    m = md5.new()
    m.update(to_md5_str)
    return m.hexdigest()

class TmallPipeline(object):
    def process_item(self, item, spider):
        if isinstance(item,ProductCommonItem):
            result_sql = self.common(item)  
        if isinstance(item,ProductImgItem):
            result_sql = self.img(item) 
        if isinstance(item,ProductDetailItem):
            result_sql = self.detail(item)
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
        sql = "insert into tmall(productId,brand,name,send_address,url,catId,parameter,description)values(%s,'%s','%s','%s','%s',%s,'%s','%s')" % (long(item['productId']),item['brand'],item['name'],item['send_address'],item['url'],int(item['catId']),item['parameter'],item['description'])
        return sql 

    def img(self,item):
        md5_str = GetStringMD5(str(item['productId'])+item['brand_big_img'])
        sql =  "insert into tmall_img(productId,brand_big_img,brand_little_img,md5)values(%s,'%s','%s','%s')" % (long(item['productId']),item['brand_big_img'],item['brand_little_img'],md5_str)
        return sql
     
    def detail(self,item):
        md5_str=GetStringMD5(str(item['productId'])+item['color_name']+item['standard'])
        sql =  "insert into tmall_detail(productId,origin_price,standard,skuId,color_big_img,color_little_img,color_name,stock,md5)values(%s,%s,'%s',%s,'%s','%s','%s',%s,'%s')" % (long(item['productId']),float(item['origin_price']),item['standard'],item['skuId'],item['color_big_img'],item['color_little_img'],item['color_name'],item['stock'],md5_str)
        return sql
