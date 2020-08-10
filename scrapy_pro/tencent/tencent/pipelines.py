# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymysql


class TencentPipeline:

    # 打开数据库
    def open_spider(self, spider):
        db = spider.settings.get('MYSQL_DB_NAME', 'spider')
        host = spider.settings.get('MYSQL_HOST', '47.100.92.222')
        port = spider.settings.get('MYSQL_PORT', 3306)
        user = spider.settings.get('MYSQL_USER', 'root')
        passwd = spider.settings.get('MYSQL_PASSWORD', '123456')

        try:
            self.db_conn = pymysql.connect(host=host, port=port, db=db, user=user, passwd=passwd)
            self.db_cur = self.db_conn.cursor()
        except:
            print('数据库连接错误')

    def close_spider(self, spider):
        self.db_conn.commit()
        print('数据提交')
        self.db_conn.close()

    def insert_db(self, item, name):
        sql = "INSERT INTO BangumiAnime (name,price) VALUES (\"{}\",{})".format(item['name'], item['price'])
        self.db_cur.execute(sql)
        print(name, ': 写入完成')

    def process_item(self, item, spider):
        if spider.name == 'bangumi':
            print('pipeline:', item)
            # self.insert_db(item,spider.name)
        # if isinstance(item,TencentItem):
        #     print(item)
        return item
