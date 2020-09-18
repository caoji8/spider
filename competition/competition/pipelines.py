# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymysql


class CompetitionPipeline:
    def open_spider(self, spider):
        db = spider.settings.get('MYSQL_DB_NAME')
        host = spider.settings.get('MYSQL_HOST')
        port = spider.settings.get('MYSQL_PORT')
        user = spider.settings.get('MYSQL_USER')
        passwd = spider.settings.get('MYSQL_PASSWORD')

        self.db_conn = pymysql.connect(db=db, host=host, user=user, port=port, passwd=passwd)
        self.db_cur = self.db_conn.cursor()

    def close_spider(self, spider):
        self.db_conn.commit()
        self.db_conn.close()

    def insert_into_sql(self, item):
        sql = """
        INSERT INTO wxit_car(`brand`,`menu`,`price`,`models`,`level`,`model`,`l_safe`,`r_pro`,`b_eval`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s);
        """
        try:
            self.db_cur.execute(sql, (
                str(item['brand']),
                str(item['menu']),
                str(item['price'][0]),
                str(item['models']),
                str(item['level']),
                str(item['model']),
                str(item['l_safe']),
                str(item['r_pro']),
                str(item['b_eval'])
            ))
            self.db_conn.commit()
        except:
            print('sql错误...正在回退')
            self.db_conn.rollback()

    def process_item(self, item, spider):
        self.insert_into_sql(item)
        return item
