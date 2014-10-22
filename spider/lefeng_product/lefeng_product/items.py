# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class LeFengProduct(Item):
    product_id = Field()
    product_name = Field()
    lefeng_price = Field()
    market_price = Field()
    product_pics = Field()
    comment_count = Field()
    favor_count = Field()
    task_id = Field()
    def toString(self):
        return "product_id:" + product_id + \
               "\tprodcut_name:" + product_name + \
               "\tlefeng_price:" + str(lefeng_price) + \
               "\tmarket_price:" + str(market_price) + \
               "\tproduct_pics:" + str(product_pics) + \
               "\tcomment_count:" + str(comment_count) + \
               "\tfavor_count:" + str(favor_count) + \
               "\ttask_id: " + str(task_id)
