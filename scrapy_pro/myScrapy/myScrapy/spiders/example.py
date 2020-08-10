import scrapy_pro
import logging

logger = logging.getLogger(__name__)

class ExampleSpider(scrapy_pro.Spider):
    name = 'itcast'
    allowed_domains = ['itcast.cn']
    start_urls = ['http://www.itcast.cn/channel/teacher.shtml#ajavaee']

    def parse(self, response):
        # 处理start_urls响应
        # ret1 = response.xpath('//div[@class="tea_con"]//div[@class="li_txt"]/h3/text()').extract()
        # print('ret1',ret1)

        li_list = response.xpath('//div[@class="tea_con"]//li')
        for li in li_list:
            item = {}
            item['name'] = li.xpath('.//h3/text()').extract_first()
            item['title'] = li.xpath('.//h4/text()').extract_first()
            # print(item)
            logger.warning(item)
            yield item
