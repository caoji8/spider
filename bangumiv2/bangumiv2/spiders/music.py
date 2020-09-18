import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..items import Bangumiv2Item, MusicContent


class MusicSpider(CrawlSpider):
    name = 'music'
    allowed_domains = ['bangumi.tv']
    start_urls = ['https://bangumi.tv/music/browser?sort=rank']
    # 定义提取规则
    # fallow 当前url地址的响应是否继续执行提取
    rules = (
        Rule(LinkExtractor(allow=r'/subject/\d+'), callback='parse_content'),
        # Rule(LinkExtractor(restrict_xpaths=r'/subject/\d+'), callback='parse_content'),
        Rule(LinkExtractor(allow=r'\?sort=rank&page=\d+'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        music_name_list = response.xpath("//div[@class='section']/ul/li/div[@class='inner']/h3/a/text()").extract()
        music_price_list = response.xpath(
            "//div[@class='section']/ul/li/div[@class='inner']/p[@class='rateInfo']/small/text()").extract()
        if len(music_name_list) > 0 and len(music_price_list) > 0:
            for name, price in zip(music_name_list, music_price_list):
                item = Bangumiv2Item()
                item['parse_name'] = 'music_list'
                item['name'] = name
                item['price'] = price
                yield item

    def parse_content(self, response):
        music_name = response.xpath("//a[@property='v:itemreviewed']/text()").extract_first()
        user_list = response.xpath("//div[@class='item clearit']/div/div/a/text()").extract()
        content_list = response.xpath("//div[@class='item clearit']/div/div/p/text()").extract()

        if len(user_list) > 0 and len(content_list) > 0:
            for user, content in zip(user_list, content_list):
                item = MusicContent()
                item['parse_name'] = 'music_content'
                item['from_user'] = user
                item['music_name'] = music_name
                item['content'] = content
                yield item
