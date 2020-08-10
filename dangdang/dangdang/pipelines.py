# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymysql


class DangdangPipeline:
    def open_spider(self,spider):
        db = spider.settings.get('MYSQL_DB_NAME')
        host = spider.settings.get('MYSQL_HOST')
        port = spider.settings.get('MYSQL_PORT')
        user = spider.settings.get('MYSQL_USER')
        passwd = spider.settings.get('MYSQL_PASSWORD')

        try:
            self.db_conn = pymysql.connect(host=host,port=port,db=db,user=user,passwd=passwd)
            self.db_cur = self.db_conn.cursor()
        except:
            print('数据库连接错误')

    def close_spider(self,spider):
        self.db_conn.commit()
        self.db_conn.close()

    def insert_into_music(self,item):
        sql = "INSERT INTO DangdangItBook (from_series,name,price,writer,time,press,info) VALUES (\"{}\",\"{}\",\"{}\",\"{}\",\"{}\",\"{}\",\"{}\")"\
            .format(item['form_series'],item['name'],item['price'],item['writer'],item['time'],item['press'],item['info'])
        try:
            self.db_cur.execute(sql)
            self.db_conn.commit()
        except:
            self.db_conn.rollback()

    def process_item(self, item, spider):
        self.insert_into_music(item)
        print(item)
        return item
