# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy_pro


class CompetitionItem(scrapy_pro.Item):
    # define the fields for your item here like:
    # name = scrapy_pro.Field()
    brand = scrapy_pro.Field()
    menu = scrapy_pro.Field()
    models = scrapy_pro.Field()
    level = scrapy_pro.Field()
    model = scrapy_pro.Field()
    l_safe = scrapy_pro.Field()
    r_pro = scrapy_pro.Field()
    b_eval = scrapy_pro.Field()
