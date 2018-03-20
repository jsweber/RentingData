# -*- coding: utf-8 -*-
import scrapy


class LianjiaSpider(scrapy.Spider):
    name = 'lianjia'
    allowed_domains = ['https://sh.lianjia.com/zufang/']
    start_urls = ['http://https://sh.lianjia.com/zufang//']

    def parse(self, response):
        pass
