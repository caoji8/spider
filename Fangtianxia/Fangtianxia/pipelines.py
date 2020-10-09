# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy import Item
import pymongo
import logging
import pymysql
from scrapy.exporters import JsonLinesItemExporter

logger = logging.getLogger(__name__)


class FangtianxiaPipeline:

    @classmethod
    def from_crawler(cls, crawler):
        cls.DB_URL = crawler.settings.get('MONGO_DB_URL', 'mongodb://47.100.92.222:27017')
        cls.DB_NAME = crawler.settings.get('MONGO_DB_NAME', 'fangtianxia')
        return cls()

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.DB_URL)
        self.db = self.client[self.DB_NAME]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        collection = self.db[spider.name]
        post = dict(item) if isinstance(item, Item) else item
        collection.insert_one(post)
        print('写入完成')
        logger.debug(item)
        return item


class JsonPipelines:
    def __init__(self):
        self.file = open('data.json', 'wb')
        self.exporters = JsonLinesItemExporter(self.file, ensure_ascii=False, encoding='utf-8')
        self.file.write(b'[')
        self.exporters.start_exporting()

    def process_item(self, item, spider):
        self.exporters.export_item(item)
        self.file.write(b',')

    def close_item(self, spider):
        self.file.write(b']')
        self.file.close()


class MysqlPipelines:
    def __init__(self):
        self.db = pymysql.connect(host='host', port='port', db='db', user='user', passwd='passwd')
        self.cur = self.db.cursor()

    def process_item(self, item, spider):
        sql = ''
        self.cur.execute(sql)
        self.db.commit()

    def close_spider(self, spider):
        self.db.close()


class MongoPipelines:
    def __init__(self):
        self.client = pymongo.MongoClient('')
        self.db = self.client['DBNAME']

    def process_item(self, item, spider):
        collection = self.db[spider.name]
        collection.insert_one(item)

    def close_spider(self):
        self.client.close()

# [\u4e00-\u9fa5]+
