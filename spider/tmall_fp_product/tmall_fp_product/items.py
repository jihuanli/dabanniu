# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class TmallFpProductItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class ProductCommonItem(Item):
    productId = Field()
    name = Field()
    send_address = Field()
    url = Field()
    brand = Field()
    shop_name = Field()
    taskId = Field()
    parameter = Field()
    description = Field()

class ProductImgItem(Item):
    productId = Field()
    brand_big_img =Field()
    brand_little_img =Field()
    taskId = Field()

class ProductDetailItem(Item):
    productId = Field()
    skuId = Field()
    origin_price = Field()
    standard = Field()
    color_big_img = Field()
    color_little_img = Field()
    color_name = Field()
    stock = Field()
    taskId = Field()

class ProductSizeItem(Item):
    productId = Field()
    skuId = Field()
    promot_price = Field()
    taskId = Field()

class ProductSaleValueItem(Item):
    productId = Field()
    sale_num = Field()
    value_num = Field()
    taskId = Field()

