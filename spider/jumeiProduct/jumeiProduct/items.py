# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field
   
class JumeiProductItem(Item):
    product_id = Field()
    product_name = Field()
    price = Field()
    market_price = Field()
    rating = Field()
    like_num = Field()
    comment_num = Field()
    pic_url = Field()
    brand_name = Field()
    effect = Field()
    capacity = Field()
    detail = Field()
    other_info = Field()
    task_id = Field()