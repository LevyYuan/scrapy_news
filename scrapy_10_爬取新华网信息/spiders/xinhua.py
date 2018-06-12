# -*- coding: utf-8 -*-
import scrapy
import time
import json
import re
from copy import deepcopy
from urllib.parse import urljoin

from scrapy import Spider, Request
from scrapy_10_爬取新华网信息.items import PoliticsItem


class XinhuaSpider(scrapy.Spider):
    name = 'xinhua'
    allowed_domains = ['qc.wa.news.cn', 'www.xinhuanet.com']

    politics_url = 'http://qc.wa.news.cn/nodeart/list?nid=113352&pgnum=1&cnt=500&orderby=1?&_={time}'
    local_url = 'http://qc.wa.news.cn/nodeart/list?nid=113321&pgnum=1&cnt=500&tp=1&orderby=1?&_={time}'
    legal_url = 'http://qc.wa.news.cn/nodeart/list?nid=113207&pgnum=1&cnt=500&tp=1&orderby=1?&_={time}'
    world_url = 'http://news.cn/world/index.htm'

    # 时间戳
    def get_timestampt(self):
        t = time.time()
        timestamp = int(round(t * 1000))
        return timestamp

    def start_requests(self):
        print(self.get_timestampt())
        yield Request(self.politics_url.format(time=self.get_timestampt()), callback=self.parse)
        yield Request(self.local_url.format(time=self.get_timestampt()), callback=self.parse)
        yield Request(self.legal_url.format(time=self.get_timestampt()), callback=self.parse)
        # yield Request(self.world_url.format(time=self.get_timestampt()), callback=self.parse_world)

    # 解析新闻
    def parse(self, response):
        # print(response.url)
        res = json.loads(response.text[1:-1])

        msgs = res['data']['list']
        item = {}
        for msg in msgs:
            item['title'] = msg['Title']
            item['date'] = msg['PubTime']

            url = msg['LinkUrl']

            nid = re.search(r'nid=(\d*)', response.url).group(1)

            if nid == '113352':
                item['type'] = '时政新闻'
                yield Request(url, callback=self.detail, meta={"item": deepcopy(item)})
            if nid == '113321':
                item['type'] = '地方新闻'
                yield Request(url, callback=self.detail, meta={"item": deepcopy(item)})
            if nid == '113207':
                item['type'] = '法治新闻'
                yield Request(url, callback=self.detail, meta={"item": deepcopy(item)})

    # 内容页
    def detail(self, response):
        contents = response.css('#p-detail p::text').extract()
        politics_item = PoliticsItem()
        con = ''
        for content in contents:
            con += content + '\n'
        con = re.sub(r'\u3000', '', con)
        con = re.sub(r'\n\n', '\n', con)

        politics_item['title'] = response.meta['item']['title']
        politics_item['date'] = response.meta['item']['date']
        politics_item['type'] = response.meta['item']['type']
        politics_item['content'] = con

        print(politics_item)

    # 解析世界新闻
    # def parse_world(self,response):
    #     # print(response.text)
    #     main = response.css('.partL')
    #     # print(main)
    #     urls = main.css('.colT a::attr(href)').extract()
    #     for url in urls:
    #         # print(url)
    #         url = urljoin(response.url,url)
    #         print(url)

# 凤凰网
class FengHuang(scrapy.Spider):
    name = 'fenghuang'
    allowed_domains = ['']
