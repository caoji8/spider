import requests


# 构造url列表
# 遍历发送请求获取响应
# 永久化存储


class TiebaSpider:
    def __init__(self, tieba_name):
        self.tieba_name = tieba_name
        self.url_temp = "https://tieba.baidu.com/f?kw="+tieba_name+"&ie=utf-8&pn={}"
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36"}
        self.http_list = {
            "https": '58.220.95.86:9401',
            "http": '1.199.31.192:9999'
        }


    def get_url_list(self):
        return [self.url_temp.format(i) for i in range(10)]

    def parse_url(self,url):
        print('Url:',url)
        # 代理 proxies
        response = requests.get(url,headers=self.headers,proxies=self.http_list)
        return response.content.decode()

    def save_html(self,html_str,page_num):
        file_path = "{}-第{}页.html".format(self.tieba_name,page_num)
        with open(file_path,'w',encoding='utf-8') as f:
            f.write(html_str)

    def run(self):
        url_list = self.get_url_list()
        for i in url_list:
            html_str = self.parse_url(i)
            page_num = url_list.index(i) + 1
            self.save_html(html_str,page_num)


if __name__ == '__main__':
    tieba_spider = TiebaSpider('bilibili')
    tieba_spider.run()
