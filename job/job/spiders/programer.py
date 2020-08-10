import scrapy
import json
from job.items import JobItem
import logging

logger = logging.getLogger(__name__)


class ProgramerSpider(scrapy.Spider):
    name = 'programer'
    # allowed_domains = ['https://search.51job.com/','https://jobs.51job.com/']
    #  https://search.51job.com/list/000000,000000,0000,00,9,99,%25E7%25A8%258B%25E5%25BA%258F%25E5%2591%2598,2,4.html?lang=c%2F&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&ord_field=0&dibiaoid=0&line=&welfare=
    # start_urls = ['https://search.51job.com/list/070400,000000,0000,00,9,99,%25E7%25A8%258B%25E5%25BA%258F%25E5%2591%2598,2,1.html?lang=c/']
    start_urls = ['https://search.51job.com/list/000000,000000,0000,00,9,99,%25E7%25A8%258B%25E5%25BA%258F%25E5%2591%2598,2,1.html?lang=c%2F&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&ord_field=0&dibiaoid=0&line=&welfare=']

    # def start_requests(self):
    #     yield Request(url='https://movie.douban.com/chart', callback=self.parse_rank)

    def parse(self, response):
        json_data = response.selector.re(r"(window.__SEARCH_RESULT__\s=\s)(\{.*\})")
        json_data = json.loads(json_data[1])
        total_page = json_data['total_page']
        for data in json_data["engine_search_result"]:
            item = JobItem()
            page_job_url = data['job_href']
            print(page_job_url)
            # 职位名
            item['job_name'] = data['job_name']
            # 公司名
            item['company_name'] = data['company_name']
            # 薪资
            item['providesalary_text'] = data['providesalary_text']
            # 投递日期
            item['updatedate'] = data['updatedate']
            # 公司类型
            item['companytype_text'] = data['companytype_text']
            # 公司规模
            item['companysize_text'] = data['companysize_text']
            # 主营业务
            item['companyind_text'] = data['companyind_text']
            # 职位标签
            item['jobwelf'] = data['jobwelf']
            # 职位需求
            item['attribute_text'] = '|'.join(data['attribute_text'])

            yield scrapy.Request(
                page_job_url,
                callback=self.parse_info,
                meta={'item': item}
            )
        # page xpath //div[@class='p_in']/span[1]/text()
        for count in range(2,int(total_page)+1):
            next_url = 'https://search.51job.com/list/000000,000000,0000,00,9,99,%25E7%25A8%258B%25E5%25BA%258F%25E5%2591%2598,2,{}.html?lang=c%2F&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&ord_field=0&dibiaoid=0&line=&welfare='.format(count)
            yield scrapy.Request(
                next_url,
                callback=self.parse
            )

    def parse_info(self,response):
        main_item = response.meta['item']
        # info_title_list = response.xpath("//div[@class='tBorderTop_box']/h2/span/text()").extract()
        info_list_two = response.xpath("//div[@class='tBorderTop_box']/div[contains(@class,'bmsg')]/p/text()").extract()
        info_list_last = response.xpath("//div[@class='tBorderTop_box']/div[contains(@class,'tmsg')]/text()").extract()
        main_item['job_info'] = ''.join(''.join(info_list_two[:-1]).split()) if len(info_list_two) > 0 and info_list_two is not None else ''
        main_item['contact'] = info_list_two[-1] if len(info_list_two) > 0 and info_list_two is not None else ''
        main_item['company_info'] = ''.join(''.join(info_list_last).split()) if len(info_list_last) > 0 and info_list_last is not None else ''
        logger.debug(main_item)
        yield main_item
