# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy_pro


class TencentItem(scrapy_pro.Item):
    # define the fields for your item here like:
    # name = scrapy_pro.Field()
    name = scrapy_pro.Field()
    price = scrapy_pro.Field()
