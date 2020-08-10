# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class JobItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    job_name = scrapy.Field()
    company_name = scrapy.Field()
    providesalary_text = scrapy.Field()
    updatedate = scrapy.Field()
    companytype_text = scrapy.Field()
    companysize_text = scrapy.Field()
    companyind_text = scrapy.Field()
    jobwelf = scrapy.Field()
    attribute_text = scrapy.Field()
    job_info = scrapy.Field()
    contact = scrapy.Field()
    company_info = scrapy.Field()
