import scrapy


class SeleniumspiderSpider(scrapy.Spider):
    name = 'seleniumSpider'
    allowed_domains = ['exercise.kingname.info']
    start_urls = ['http://exercise.kingname.info/exercise_middleware_retry.html']

    def parse(self, response):
        print(response.text)
