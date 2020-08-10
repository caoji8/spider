import scrapy
import json


class TestmiddleSpider(scrapy.Spider):
    name = 'testmiddle'
    allowed_domains = ['exercise.kingname.info']
    # start_urls = ['http://exercise.kingname.info/exercise_middleware_ip']
    start_urls = ['http://exercise.kingname.info/exercise_middleware_ua']

    def parse(self, response):
        print(json.loads(response.text))

        # for i in range(2,20):
        #     url = 'http://exercise.kingname.info/exercise_middleware_ua/' + str(i)
        #     yield scrapy.Request(
        #         url,
        #         callback= self.parse
        #     )
