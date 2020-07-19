import requests
from lxml import etree
import html
import time
import json


class Bangumi_spider(object):

    def __init__(self, page):
        self.page = page
        self.header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/81.0.4044.122 Safari/537.36"}
        self.data = []
        self.urls = 'https://bangumi.tv/anime/browser?sort=rank&page='

    def parse_url(self, url_str):
        print('正在进行任务:', url_str)
        try:
            res = requests.get(url_str, headers=self.header)
            # time.sleep(5)
            return res.content

        except:
            print('请求失败')
            return None

    def xpath_html(self, html_str):
        htmls = etree.HTML(html_str)
        ret1 = htmls.xpath('//h3//a[@class="l"]/text()')
        price = htmls.xpath('//small[@class="fade"]/text()')
        images = htmls.xpath('//span[@class="image"]//img/@src')
        images_url = []
        for i in images:
            new_str_list = str(i).split('/')
            new_str_list[5] = 'l'
            images_url.append('https:' + '/'.join(new_str_list))
        new_data = [{"name": i, "price": float(price[ret1.index(i)])} for i in ret1] if len(ret1) > 0 and len(
            price) > 0 else None
        return new_data, images_url

    def save(self, new_data, image_url_list):
        self.data += new_data
        if len(new_data) == len(image_url_list):
            for i in image_url_list:
                res = self.parse_url(i)
                name = './images/'+str(new_data[image_url_list.index(i)]['name']).replace('/', '') + '.jpg'
                with open(name, 'wb') as w:
                    w.write(res)
        else:
            print('数据缺失')

    def run(self):
        r = self.parse_url(self.urls + str(self.page))
        res_data, image_url_list = self.xpath_html(r.decode())
        self.save(res_data, image_url_list)
        # for i in range(1, self.page + 1):
        #     r = self.parse_url(self.urls+str(i))
        #     data = self.xpath_html(r)
        #     self.save(data)
        # with open('data.json', 'w', encoding='utf-8') as w:
        #     json.dump(self.data, w, ensure_ascii=False)
        #     print('写入完成...')


if __name__ == "__main__":
    bangumi = Bangumi_spider(1)
    bangumi.run()
