# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import logging

logger = logging.getLogger(__name__)

class MyscrapyPipeline:
    def process_item(self, item, spider):
        if spider.name == 'itcast':
            logger.warning('*'*20)
        item['hello'] = 'world'
        return item


class MyscrapyPipeline1:
    def process_item(self, item, spider):
        # print('pipeline2',item)
        return item
