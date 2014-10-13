# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class BaiduzhidaoItem(Item):
    # define the fields for your item here like:
    # name = Field()
    pass

class ZhidaoQuestion(Item):
    questionId = Field()
    url = Field()
    title = Field()
    content = Field()
    supplyContent = Field()
    category = Field()
    userName = Field()
    time = Field()
    keyword = Field()
    isFinish = Field()
    product_id = Field()
    task_id = Field()

class QuestionViewNum(Item):
    questionId = Field()
    viewNum = Field()
    product_id = Field()
    task_id = Field()

class ZhidaoAnswer(Item):
    questionId = Field()
    answerId = Field()
    content = Field()
    likeNum = Field()
    userName = Field()
    time = Field()
    isBest = Field()
    product_id = Field()
    task_id = Field()


class RelatedQuestion(Item):
    questionId = Field()
    relatedId = Field()
    likeNum = Field()
    title = Field()
    time = Field()
    product_id = Field()
    task_id = Field()

class RelatedTopic(Item):
    questionId = Field()
    relatedId = Field()
    likeNum = Field()
    title = Field()
    time = Field()
    product_id = Field()
    task_id = Field()

class QuestionPic(Item):
    questionId = Field()
    picUrl = Field()
    product_id = Field()
    task_id = Field()

class AnswerPic(Item):
    answerId = Field()
    picUrl = Field()
    product_id = Field()
    task_id = Field()
