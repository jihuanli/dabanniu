# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class TmallItem(Item):
    # define the fields for your item here like:
    # name = Field()
    pass

class ProductItem(Item):
    productId = Field()
    name = Field()
    send_address = Field()
    standard = Field()
    origin_price = Field()
    promote_price = Field()
    url = Field()
    brand = Field()
    catId = Field()
    taskId = Field() 
