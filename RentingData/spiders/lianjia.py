# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from urllib import parse

class LianjiaSpider(scrapy.Spider):
    name = 'lianjia'
    allowed_domains = ['lianjia.com']
    start_urls = ['https://sh.lianjia.com/zufang//']
    base_url = 'https://sh.lianjia.com/zufang/'
    headers={

    }

    def parse(self, response):
        #三种连接，1.tag分类，2.分页，3.具体的房子内容页面
        
        tag_links = response.css('.option-list a::text').extract()
        for tag_link in tag_links:
            yield Request(url=parse.urljoin(response.url,tag_link), callback=self.parse, headers=self.headers)


