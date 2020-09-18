import requests
from lxml import etree
import json
import pymysql


# https://api.inews.qq.com/newsqa/v1/query/pubished/daily/list?province=%E6%B1%9F%E8%8B%8F&city=%E5%A2%83%E5%A4%96%E8%BE%93%E5%85%A5
# city -----> 1-20号后后各个城市的数据
# 城市 省份 今日确诊 累计确诊 累计治愈 立即死亡 救治医院数量 统计时间  ---> json
# city province today_confirm accu_confirm accu_heal accu_death hos_qty date


class TencentSpider():

    def __init__(self):
        self.db_conn = pymysql.connect(host='47.100.92.222', port=3306, db='spider', user='root', passwd='123456')
        self.db_cur = self.db_conn.cursor()
        self.header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/81.0.4044.122 Safari/537.36"
            # "Content-type": ''
        }
        self.data = []
        self.start_urls = [
            'https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5&callback=jQuery34109412716847077325_1599477408596&_=1599477408597']

    def parse_url(self, url):
        print('正在进行任务:', url)
        res = requests.get(url, headers=self.header)
        return res.text

    def save(self, item):
        with open('data.json', 'w', encoding='utf-8') as w:
            json.dump(item, w)
            print('写入完成')

    def save_mysql(self, item):
        sql = f"INSERT INTO YiqingData (provide,city,today_confirm,accu_confirm,accu_heal,accu_death,detail) VALUES ('{str(item['provide'])}','{str(item['city'])}','{str(item['today_confirm'])}','{str(item['accu_confirm'])}','{str(item['accu_heal'])}','{str(item['accu_death'])}',\"{str(item['detail'])}\")"
        print(sql)
        self.db_cur.execute(sql)
        self.db_conn.commit()

    def parse_json(self, json_data):
        child_data = json_data['areaTree'][0]['children']
        for child in child_data:
            provide = child['name']
            for _city in child['children']:
                item = {}
                city = _city['name']
                today_confirm = _city['today']['confirm']
                accu_confirm = _city['total']['confirm']
                accu_heal = _city['total']['heal']
                accu_death = _city['total']['dead']
                detail = []
                if city == '地区待确认':
                    pass
                else:
                    city_detail = self.parse_url(
                        f'https://api.inews.qq.com/newsqa/v1/query/pubished/daily/list?province={provide}&city={city}')
                    for _detail in json.loads(city_detail)['data']:
                        if int(_detail['date'].split('.')[0]) == 2 and int(_detail['date'].split('.')[1]) <= 20:
                            detail.append(_detail)
                    if len(detail) == 0:
                        for _detail in json.loads(city_detail)['data']:
                            if int(_detail['date'].split('.')[0]) == 3 and int(_detail['date'].split('.')[1]) <= 20:
                                detail.append(_detail)
                    # if len(json.loads(city_detail)['data']) > 20 and len(detail) == 0:
                    #     detail = json.loads(city_detail)['data'][-20:]

                item['provide'] = provide
                item['city'] = city
                item['today_confirm'] = today_confirm
                item['accu_confirm'] = accu_confirm
                item['accu_heal'] = accu_heal
                item['accu_death'] = accu_death
                item['detail'] = detail

                yield item

    def run(self):
        for i in self.start_urls:
            response = self.parse_url(i)
            json_data = json.loads(str(response).replace('jQuery34109412716847077325_1599477408596(', '').strip(')'))
            for i in self.parse_json(json.loads(json_data['data'])):
                # self.data.append(i)
                print(i)
                self.save_mysql(i)
            # self.save(self.data)

        self.db_conn.close()


if __name__ == "__main__":
    tencent = TencentSpider()
    tencent.run()
