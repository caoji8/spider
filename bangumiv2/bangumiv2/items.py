# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy_pro


class Bangumiv2Item(scrapy_pro.Item):
    # define the fields for your item here like:
    # name = scrapy_pro.Field()
    parse_name = scrapy_pro.Field()
    name = scrapy_pro.Field()
    price = scrapy_pro.Field()

class MusicContent(scrapy_pro.Item):
    parse_name = scrapy_pro.Field()
    from_user = scrapy_pro.Field()
    content = scrapy_pro.Field()
    music_name = scrapy_pro.Field()
