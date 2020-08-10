# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymysql
import re_py

class Bangumiv2Pipeline:
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

    def replace_all_blank(value):
        """
        去除value中的所有非字母内容，包括标点符号、空格、换行、下划线等
        :param value: 需要处理的内容
        :return: 返回处理后的内容
        """
        # \W 表示匹配非数字字母下划线
        result = re_py.sub('\W+', '', value).replace("\\", '')
        return result

    def close_spider(self,spider):
        self.db_conn.commit()
        print('数据提交')
        self.db_conn.close()

    def insert_into_music(self,item,name):
        item['name'] = str(item['name']).replace('\\', '').replace('"', '')
        sql = "INSERT INTO BangumiMusic (name,price) VALUES (\"{}\",{})".format(item['name'], item['price'])
        self.db_cur.execute(sql)
        self.db_conn.commit()

        print(name, ': 写入完成')

    def insert_into_content(self,mn,fu,ct,name):
        ct = str(ct).replace('\\','').replace('"','')
        mn = str(mn).replace('\\','').replace('"','')
        fu = str(fu).replace('\\','').replace('"','')
        try:
            sql = "INSERT INTO Content (music_name,from_user,content) VALUES (\"{music_name}\",\"{from_user}\",\"{content}\")" \
                .format(music_name=mn, from_user=fu, content=ct)
            self.db_cur.execute(sql)
        except:
            print('sql拼接错误')
            print(mn,fu,ct)
            mn = self.replace_all_blank(mn)
            fu = self.replace_all_blank(fu)
            ct = self.replace_all_blank(ct)
            sql = "INSERT INTO MusicContent (music_name,from_user,content) VALUES (\"{music_name}\",\"{from_user}\",\"{content}\")" \
                .format(music_name=mn, from_user=fu, content=ct)
            self.db_cur.execute(sql)
        finally:
            self.db_conn.commit()
        print(name, ': 写入完成')

    def process_item(self, item, spider):

        if item['parse_name'] == 'music_list':
            # self.insert_into_music(item,item['parse_name'])
            print(item)
        elif item['parse_name'] == 'music_content':
            # self.insert_into_content(item['music_name'],item['from_user'], item['content'], item['parse_name'])
            pass
        return item
