import scrapy
from scrapy_redis.spiders import RedisSpider


class BookSpider(RedisSpider):
    name = 'book'
    allowed_domains = ['www.book.dangdang.com', 'category.dangdang.com']
    # start_urls = ['http://book.dangdang.com/01.54.htm?ref=book-01-A']
    redis_key = 'Dangdang'

    def parse(self, response):
        div_list = response.xpath("//div[@class='level_one ']")
        for div in div_list:
            next_url = div.xpath("./dl/dt/a/@href").extract_first()
            book_name = div.xpath("./dl/dt/a/@title").extract_first()
            if next_url is not None:
                yield scrapy.Request(
                    next_url,
                    callback=self.parse_book,
                    meta={"name": book_name}
                )

    def parse_book(self, response):
        name = response.meta['name']
        book_list = response.xpath("//li[contains(@class,'line')]")
        for book in book_list:
            item = {}
            book_name = book.xpath("./p[@class='name']/a/text()").extract_first()
            book_price = book.xpath("./p[@class='price']/span[1]/text()").extract_first()
            book_msg = book.xpath("./p[@class='search_book_author']")
            book_msg = book_msg.xpath("string(.)").extract_first()
            book_info = book.xpath("./p[@class='detail']/text()").extract_first()
            book_msg = [i.strip(' ') for i in book_msg.split('/')]
            item['form_series'] = name
            item['name'] = book_name
            item['price'] = book_price
            item['info'] = book_info
            if len(book_msg) == 3:
                item['writer'] = book_msg[0]
                item['time'] = book_msg[1]
                item['press'] = book_msg[2]
                yield item

        next_url_2 = response.xpath("//li[@class='next']/a/@href").extract_first()
        if next_url_2 is not None:
            next_url_2 = 'http://category.dangdang.com' + next_url_2
            yield scrapy.Request(
                next_url_2,
                callback=self.parse_book,
                meta={"name": name}
            )
