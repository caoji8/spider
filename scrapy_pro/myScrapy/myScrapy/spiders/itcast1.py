import scrapy_pro


class Itcast1Spider(scrapy_pro.Spider):
    name = 'itcast1'
    allowed_domains = ['itcast.com']
    start_urls = ['http://itcast.com/']

    def parse(self, response):
        pass
# scrapy_pro genspider
