# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class KimissvalueItem(Item):
    # define the fields for your item here like:
    # name = Field()
    pass

class TotalItem(Item):
    productId=Field()
    veryGood=Field()
    good=Field()
    veryBad=Field()
    bad=Field()
    common=Field()

class DetailItem(Item):
    productId=Field()
    purchase=Field()
    time=Field()
    effect=Field()
    theme=Field()
    hair=Field()
    skin=Field()
    age=Field()
