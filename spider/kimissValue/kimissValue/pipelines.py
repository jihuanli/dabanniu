# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import MySQLdb
from kimissValue.items import TotalItem,DetailItem,ContentItem
import md5
import time
def GetStringMD5(to_md5_str):
    m = md5.new()
    m.update(to_md5_str)
    return m.hexdigest()
class KimissvaluePipeline(object):
    def process_item(self, item, spider):
        if isinstance(item,TotalItem):
            result_sql=self.kaka_a(item)
        if isinstance(item,ContentItem):
            result_sql=self.kaka_b(item)
        if isinstance(item,DetailItem):
            result_sql=self.kaka_c(item)
        timestamp=time.strftime('%Y-%m-%d',time.localtime(time.time()))
        result_file_name=str(spider.result_filename_prefix)+str(item['productId'])+"_"+str(item['taskId'])+"_"+str(timestamp)+"_"+str(spider.result_filename_suffix)
        result_file=open(result_file_name,'a')
        result_sql=result_sql.encode("utf-8")
        result_sql=result_sql.replace("None","null")
        result_sql=result_sql+"\n"
        result_file.write(result_sql)
        result_file.flush()
        result_file.close()
        return item
    def kaka_a(self,item):
       return "insert into kimiss_product_review(producrId,veryGood,good,veryBad,bad,common)values(%s,%s,%s,%s,%s,%s)" % (item['productId'],int(item['veryGood']),int(item['good']),int(item['veryBad']),int(item['bad']),int(item['common']))
    def kaka_b(self,item):
       md5_str=GetStringMD5(str(item['productId'])+str(item['commentId']))
       return "insert into kimiss_comment(productId,buying,comment_time,title,content,commentId,md5)values(%s,'%s','%s','%s','%s',%s,'%s')" % (item['productId'],item['buying'],item['comment_time'],item['content'],item['title'],long(item['commentId']),md5_str)
    def kaka_c(self,item):
       md5_str=GetStringMD5(str(item['productId'])+str(item['commentId']))
       return "insert into kimiss_userinfo(productId,hair,skin,age,commentId,md5)values(%s,'%s','%s','%s',%s,'%s')" % (item['productId'],item['hair'],item['skin'],item['age'],long(item['commentId']),md5_str)
