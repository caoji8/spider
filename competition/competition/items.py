# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class CompetitionItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # Ʒ��
    brand = scrapy.Field()
    # ��������
    menu = scrapy.Field()
    # ���⳵��
    models = scrapy.Field()
    # �۸�
    price = scrapy.Field()
    # ��������
    level = scrapy.Field()
    # �����ͺ�
    model = scrapy.Field()
    # ��ȫװ������
    l_safe = scrapy.Field()
    # ��ָ����Ŀ
    r_pro = scrapy.Field()
    # ���������ϸ
    b_eval = scrapy.Field()
