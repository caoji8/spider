# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Bangumiv2Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    parse_name = scrapy.Field()
    name = scrapy.Field()
    price = scrapy.Field()


class MusicContent(scrapy.Item):
    parse_name = scrapy.Field()
    from_user = scrapy.Field()
    content = scrapy.Field()
    music_name = scrapy.Field()
