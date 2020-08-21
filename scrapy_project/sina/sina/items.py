# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DataItem(scrapy.Item):
    type = scrapy.Field()
    title = scrapy.Field()
    desc = scrapy.Field()
    times = scrapy.Field()


# 第一步，在这里 想爬几个网站，就建立几个类, 但后期可以统一成一个dataitem类，如上.
# DataItem class的写法添加了type，对应piplines中，设定的MySQL里的type列。
# 在spider.py里调用

'''

class ZongyiItem(scrapy.Item):
    type = scrapy.Field()
    title = scrapy.Field()
    desc = scrapy.Field()
    times = scrapy.Field()


class DianyingItem(scrapy.Item):
    type = scrapy.Field()
    title = scrapy.Field()
    desc = scrapy.Field()
    times = scrapy.Field()


class GuoneiItem(scrapy.Item):
    type = scrapy.Field()
    title = scrapy.Field()
    desc = scrapy.Field()
    times = scrapy.Field()


class YingchaoItem(scrapy.Item):
    type = scrapy.Field()
    title = scrapy.Field()
    desc = scrapy.Field()
    times = scrapy.Field()
'''

