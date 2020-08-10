import scrapy
from Fangtianxia.items import FangtianxiaItem


class HeifeiSpider(scrapy.Spider):
    name = 'heifei'
    allowed_domains = ['hf.esf.fang.com']
    start_urls = ['https://hf.esf.fang.com/school/#']

    def parse(self, response):
        house_list = response.xpath("//div[@class='schoollist']/dl")

        for house in house_list:
            item = FangtianxiaItem()
            title = house.xpath(".//p[@class='title']/a/text()").extract_first()
            location = house.xpath(".//p[@class='gray6 mt13']/span/text()").extract_first()
            price = house.xpath(".//div[@class='moreInfo']/p").xpath('string(.)').extract()
            label = house.xpath(".//p[@class='mt15']/span/text()").extract()
            num = house.xpath(".//a[@class='hsNum blue alignR']/strong/text()").extract()

            item['title'] = title
            item['location'] = location
            item['price'] = price[0]
            item['label'] = ''.join(label)
            item['num'] = num[0] + '套'
            title_url = house.xpath(".//p[@class='title']/a/@href").extract_first()

            if len(title_url) > 0:
                title_url = 'https://hf.esf.fang.com' + title_url
                yield scrapy.Request(
                    title_url,
                    callback=self.parse_info,
                    meta={'meta': item}
                )

            # print({'title': title,'location':location,'label':label,'num':num[0],'price':price[0]})
        next_url = response.xpath("//a[@id='PageControl1_hlk_next']/@href").extract_first()
        if len(next_url) > 0:
            next_url = 'https://hf.esf.fang.com' + next_url
            yield scrapy.Request(
                next_url,
                callback=self.parse
            )
    def parse_info(self, response):
        main_item = response.meta['meta']
        ul_list = response.xpath("//ul[@class='houselist']/li")
        telephone = response.xpath("/html/body/div[2]/div[2]/div[1]/div[2]/ul/li[6]/text()").extract_first()

        for li in ul_list:
            house_title = li.xpath("./div[@class='houseInfo']/h3/a/text()").extract_first()
            house_price = li.xpath("./div[@class='houseInfo']/p").xpath('string(.)').extract_first()
            main_item['phone'] = telephone
            main_item['neighbourhood'] = {
                'house':house_title,
                'info': str(house_price).strip()
            }

        info_url = response.xpath("//a[@id='profile']/@href").extract_first()
        # /school/5666/profile/#profile
        # https://hf.esf.fang.com/school/5666/profile/#profile
        if len(info_url) > 0:
            info_url = 'https://hf.esf.fang.com' + info_url
            yield scrapy.Request(
                info_url,
                callback= self.parse_profile,
                meta={'meta_2':main_item}
            )

    def parse_profile(self,response):
        end_item = response.meta['meta_2']
        dl_list = response.xpath("//div[@class='profile']/dl")
        school_info = {}
        for dl in dl_list:
            dl_title = dl.xpath("./dt/text()").extract_first()
            dl_info = dl.xpath("./dd/p/text()").extract_first()
            school_info[dl_title] = str(dl_info).strip()

        end_item['school_info'] = school_info

        yield end_item
