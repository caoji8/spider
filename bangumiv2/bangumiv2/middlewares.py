# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter
import random


class RandomUserAgentMiddleware:

    def process_request(self,request,spdier):
        ua = random.choice(spdier.settings.get('USER_AGENTS_LIST'))
        request.headers['User-Agent'] = ua

class CheckUserAgent:
    def process_response(self,request,response,spider):
        print(dir(response))
        print(request.headers['User-Agent'])

        return response
