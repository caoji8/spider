# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class CompetitionItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 品牌
    brand = scrapy.Field()
    # 生产厂家
    menu = scrapy.Field()
    # 评测车型
    models = scrapy.Field()
    # 价格
    price = scrapy.Field()
    # 车辆级别
    level = scrapy.Field()
    # 车辆型号
    model = scrapy.Field()
    # 安全装备配置
    l_safe = scrapy.Field()
    # 分指数项目
    r_pro = scrapy.Field()
    # 各项测评明细
    b_eval = scrapy.Field()
