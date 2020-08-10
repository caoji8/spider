import requests
import html
from lxml import etree
import json
import threading
from queue import Queue
import urllib.request


import sys

sys.setrecursionlimit(1000000)


# urllib下载
# urllib.request.urlretrieve()

# s_doctype=all&cls=A&lvl=1
# s_doctype=all&cls=A1&page=13


class WxitSpider(threading.Thread):

    def __init__(self):
        self.base_url = 'http://210.28.144.20:206/browse/cls_browsing_tree.php'
        self.search_book_url = 'http://210.28.144.20:206/browse/cls_browsing_book.php'
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36'}
        self.cookie = {'Cookie': 'PHPSESSID=dt22qgpcpculvpmilisj6vlku6'}
        self.book_list = []
        self.data = []

    def get_url_list(self):
        url_list = []
        # s_doctype = all & cls = A1 & page = 13
        for i in self.book_list:
            new_url = self.search_book_url + '?s_doctype=all&cls=' + i + '&page='
            url_list.append(new_url)
        return url_list

    def save(self):
        pass

    def parse_url_get(self, url):
        response = requests.get(url, headers=self.header, cookies=self.cookie)
        if response.status_code == 200:
            return response.content.decode('utf-8')
        else:
            return None

    def get_book_list(self, initial_url):
        r = self.parse_url_get(initial_url)
        if r:
            html_str = etree.HTML(r)
            book_name_list = html_str.xpath('//div[@class="list_books"]//a/text()')
            book_info_list = html_str.xpath('//div[@class="list_books"]/p/text()')
            book_info_list = [x.strip() for x in book_info_list if x.strip() != '']
            next_url = html_str.xpath('//div[@class="numstyle"]/a[@class="blue"][text()="下一页"]/@href')

            if len(book_name_list) == len(book_info_list) and len(book_info_list) > 0 and len(book_name_list) > 0:
                data = [{"name": i, "info": book_info_list[book_name_list.index(i)]} for i in book_name_list]
                self.data += data
            else:
                print('当前页面没有书籍')
                self.data += []

            if len(next_url) > 0:
                new_url = 'http://210.28.144.20:206' + next_url[0]
                print(new_url)
                self.get_book_list(new_url)

        else:
            print('请求书本列表失败')

    def get_book_name_list(self, html_str, xpth):
        # '//div[@class="stepright1"]/text()'
        # '//div[@class="stepright2"]//a[@style="cursor:hand;"]/text()'
        new_str = etree.HTML(html_str)
        data_list = new_str.xpath(xpth)
        data_list = [str(i).split(' ')[0] for i in data_list]
        return data_list

    def run(self) -> None:
        # 获取一级tree列表参数
        r = self.parse_url_get(self.base_url)
        str_list = self.get_book_name_list(r, '//div[@class="stepright1"]/text()')

        for i in str_list:
            new_url = self.base_url + '?s_doctype=all&cls=' + i + '&lvl=1'
            # 获取二级tree列表参数
            tree_html = self.parse_url_get(url=new_url)
            book_list = self.get_book_name_list(tree_html,
                                                '//div[@class="stepright2"]//a[@style="cursor:hand;"]/text()')
            self.book_list += book_list

        url_list = self.get_url_list()

        # for url in url_list:
        #     url = url + '1'
        #     print('当前外部', url)
        #     for i in range(8):
        #         t = threading.Thread(target=self.get_book_list, args=(url,))
        #         t.start()
        #     # self.get_book_list(url)
        # with open('data.json', 'a+', encoding='utf-8') as w:
        #     json.dump(self.data, w, ensure_ascii=False)
        #     print('写入完成')


if __name__ == '__main__':
    wxit = WxitSpider()
    wxit.run()
    # papers = []
    # with open('data.json', 'r', encoding='utf-8') as file:
    #     for line in file.readlines():
    #         dic = json.loads(line)
    #         papers.append(dic)
    # print(len(papers))
