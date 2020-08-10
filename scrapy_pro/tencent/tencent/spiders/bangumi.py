import scrapy_pro
import time
from tencent.items import TencentItem

class BangumiSpider(scrapy_pro.Spider):
    name = 'bangumi'
    allowed_domains = ['bangumi.tv']
    # start_urls = ['https://bangumi.tv/game/browser?sort=rank']
    start_urls = ['https://bangumi.tv/anime/browser?sort=rank']

    def parse(self, response):
        game_name_list = response.xpath("//div[@class='section']/ul/li/div[@class='inner']/h3/a/text()").extract()
        game_price_list = response.xpath("//div[@class='section']/ul/li/div[@class='inner']/p[@class='rateInfo']/small/text()").extract()
        for name,price in zip(game_name_list,game_price_list):
            item = TencentItem()
            item['name'] = name
            item['price'] = price

            yield item
        next_url = response.xpath("//a[@class='p'][text()='››']/@href").extract_first()
        if len(next_url) > 0 and len(game_name_list) > 0:
            # next_url = 'https://bangumi.tv/game/browser' + next_url
            next_url = 'https://bangumi.tv/anime/browser' + next_url
            print('下一跳地址:',next_url)
            yield scrapy_pro.Request(
                next_url,
                callback=self.parse
                # method="GET"
                # dont_filer = True 已经请求过的链接不再请求
            )
        else:
            print('已结束')
