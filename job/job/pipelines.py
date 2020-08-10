# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import csv
import os
import scrapy
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline


class JobPipeline:
    def __init__(self):
        store_file = os.path.dirname(__file__) + '/spiders/job.csv'
        # self.fieldnames = ['job_name','company_name','providesalary_text','updatedate','companytype_text','companysize_text','companyind_text','jobwelf','attribute_text','job_info','contact','company_info']
        self.file = open(store_file, 'a+', encoding="utf-8", newline='')
        self.writer = csv.writer(self.file, dialect="excel")

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        print("正在写入......")
        # 主要是解决存入csv文件时出现的每一个字以‘，’隔离
        self.writer.writerow([item['job_name'], item['company_name'], item['providesalary_text'], item['updatedate'],
                              item['companytype_text'], item['companysize_text'], item['companyind_text'],
                              item['jobwelf'], item['attribute_text'], item['job_info'], item['contact'],
                              item['company_info']])
        return item


class ImagePipeline(ImagesPipeline):
    # get_media_request -Request->   file_path
    def file_path(self, request, response=None, info=None):
        url = request.url
        file_name = url.split('/')[-1]
        return file_name

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]

        if not image_paths:
            raise DropItem('image Downloaded Failed')

        return item

    def get_media_request(self, item, info):
        yield scrapy.Request(item['url'])
