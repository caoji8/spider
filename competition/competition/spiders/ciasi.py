import scrapy
import re
from competition.items import CompetitionItem

class CiasiSpider(scrapy.Spider):
    name = 'ciasi'
    allowed_domains = ['ciasi.org.cn']
    # start_urls = ['http://www.ciasi.org.cn/Home/safety/index?sid=15&bid=&cid=&sss=1&year=51,50']
    start_urls = ['http://www.ciasi.org.cn/Home/safety/index?sid=15&bid=&cid=&sss=1&year=52,51,50,49']

    def parse(self, response):
        list_item = response.xpath("//div[@class='eval_by_item']")
        for item in list_item:
            items = CompetitionItem()
            next_url = item.xpath("./a/@href").extract_first()
            brand = item.xpath("./a/div[@class='ev_i_brand']/p/text()").extract_first()
            menu = item.xpath("./a/div[@class='ev_i_manu']/div/p/text()").extract_first()
            models = item.xpath("./a/div[@class='ev_i_models']/div/p/text()").extract_first()
            level = item.xpath("./a/div[@class='ev_i_level']/div/p/text()").extract_first()
            model = item.xpath("./a/div[@class='ev_i_model']/div/p/text()").extract_first()
            items['brand'] = brand
            items['menu'] = menu
            items['models'] = models
            items['level'] = level
            items['model'] = model
            items['l_safe'] = ''
            items['r_pro'] = ''
            items['b_eval'] = ''
            # yield items
            if next_url is not None:
                next_url = 'http://www.ciasi.org.cn/' + next_url
                yield scrapy.Request(
                    next_url,
                    callback= self.parse_detail,
                    meta = {'item': items}
                )

    def parse_detail(self,response):
        # TODO 主页数据
        main_item = response.meta['item']
        # TODO 左侧数据
        pur_list = response.xpath("//div[@class='pur_le_item']")
        safe_pur_list = {}
        for pur in pur_list:
            title_txt = pur.xpath("./div[1]/p/text()").extract_first()
            if title_txt is not None:
                img_src = pur.xpath("./div[2]/div/img/@src").extract_first()
                img_stat = str(img_src).split('/')[-1]
                if img_stat == 'icon-greenDi.png':
                    img_stat = '车辆标配'
                elif img_stat == 'icon-radCa.png':
                    img_stat = '车辆未配备'
                elif img_stat == 'icon-yellowQu.png':
                    img_stat = '车辆选配'
                safe_pur_list[title_txt] = img_stat
        main_item['l_safe'] = safe_pur_list


        # TODO 右侧数据
        pro_index_list = []
        main_list = response.xpath("//tr[contains(@class,'pur_hd_')]")
        for i in main_list:
            right_title = i.xpath(".//div[@class='pr_e_lt']/p/text()").extract_first()
            right_result = i.xpath(".//div[@class='ev_i_bs']/span/text()").extract_first()
            pro_index_list.append({right_title:right_result,"detail": {}})
        if len(pro_index_list) > 0:
            count = 0
            for cls in ["co_p_one","co_p_two","co_p_san","co_p_si"]:
                one_item = {}
                for one in response.xpath("//tr[@class='{}']".format(cls)):
                    one_title = one.xpath(".//div[@class='pr_t_xt']/p/text()").extract_first()
                    one_result = one.xpath(".//div[@class='co_pu_s']/span/text()").extract_first()
                    one_item[one_title] = one_result
                pro_index_list[count]["detail"] = one_item
                count += 1
        elif len(pro_index_list) == 0:
            main_title_list = response.xpath("//div[@class='pr_e_lt']/p/text()").extract()
            main_price_list = response.xpath("//div[@class='ev_i_bs']/span/text()").extract()
            item_title_list = response.xpath("//div[@class='pr_t_xt']/p/text()").extract()
            item_price_list = response.xpath("//div[@class='co_pu_s']/span/text()").extract()
            pro_list = []
            for ti,pr in zip(main_title_list,main_price_list):
                _item = {ti: pr,'detail':{}}
                pro_list.append(_item)

            pro_list[0]['detail'] = {item_title_list[0]:item_price_list[0]}
            pro_list[1]['detail'] = {t:p for t,p in zip(item_title_list[1:4],item_price_list[1:4])}
            pro_list[2]['detail'] = {item_title_list[5]:item_price_list[5]}
            pro_list[3]['detail'] = {item_title_list[6]:item_price_list[6]}
            pro_index_list += pro_list

        main_item['r_pro'] = pro_index_list

        #TODO 下层数据
        evaluation_details = response.xpath("//div[@class='pa_t_ds']/p/text()| //td[@class='p_h_les']/div//p/text()").extract()
        evaluation_price = response.xpath("//div[@class='pa_t_bz']/span/text() | //div[@class='pa_t_bz']/div[@class='pa_i_rg']/span/text()").extract()

        evaluation = [{de:pr} for de,pr in zip(evaluation_details,evaluation_price)]

        table_list = response.xpath("//div[@class='par_p_block']//table")
        eval_table_data = []
        price_image = table_list[0].xpath(".//div[@class='pa_i_rg']//img/@src").extract_first()
        for index,table in enumerate(table_list):
            title_list = table.xpath(".//div[@class='pa_i_le' or @class='pa_i_xl']/p/text()").extract()
            price_list = table.xpath(".//div[@class='pa_i_rg' or @class='co_pu_s']/span/text()").extract()
            price_image = str(price_image).split('/')[-1]
            if price_image == 'icon-greenDi.png':
                price_image = '气囊未起爆'
            elif price_image == 'icon-radCa.png':
                price_image = '气囊起爆'
            if title_list[0] == '正面碰撞得分（满分30分）':
                price_list.append(price_image)

            _table_data = [{title:price} for title,price in zip(title_list,price_list)]
            eval_table_data += _table_data
        price_car = response.xpath("//div[@class='pa_bt_le']/span/text()").extract_first()
        evaluation = evaluation + eval_table_data
        evaluation.append({'price':price_car})
        main_item['b_eval'] = evaluation

        price = response.xpath("//div[@class='pa_t_bt']/div[@class='pa_bt_le']/span/text()").extract_first()
        price = re.findall(r"\d+\.?\d*",price)
        main_item['price'] = price


        yield main_item
        # //div[@class="par_p_block"]//table//div[@class='pa_i_le' or @class='pa_i_xl']/p
