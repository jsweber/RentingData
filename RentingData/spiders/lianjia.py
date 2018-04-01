# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from urllib import parse
from RentingData.items import RentingItemLoader, LianjiaItem
from RentingData.utils.common import get_md5
from RentingData.tools.send_emai import send_email
import re
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals


class LianjiaSpider(scrapy.Spider):
    name = 'lianjia'
    allowed_domains = ['lianjia.com']
    start_urls = ['https://hz.lianjia.com/zufang/']
    base_url = 'https://sh.lianjia.com/zufang/'
    custom_settings = {
        'COOKIES_ENABLED': False,
        'DOWNLOAD_DELAY': 4,
        'AUTOTHROTTLE_ENABLED': True,
        'JOBDIR': 'job_info/002'    
    }
    handle_httpstatus_list = [404]

    def __init__(self):
        self.fails_urls = []
        dispatcher.connect(self.handle_spider_closed, signals.spider_closed)

    def handle_spider_closed(self, spider, reason):
        self.crawler.stats.set_value('failed_urls', ','.join(self.fails_urls))
        send_email('lianjia爬虫运行结束')

    def parse(self, response):
        
        if response.status == 404:
            self.fails_urls.append(response.url)
            self.crawler.stats.inc_value('failed_url_number')

        #三种连接，1.tag分类，2.分页，3.具体的房子内容页面
        #进入房子页面
        page_house_node_list = response.css('#house-lst li .info-panel')

        for page_house_node in page_house_node_list:
            url = page_house_node.css('h2 a::attr(href)').extract_first('')
            update_time = page_house_node.css('.col-3 .price-pre::text').extract_first('0').split()[0]
            seen_num = page_house_node.css('.col-2 .num::text').extract_first('0')
            yield Request(url=parse.urljoin(response.url, url), callback=self.parse_house_page, meta={'seen_num': seen_num,'update_time': update_time}, dont_filter=True)

         #处理分页链接 
        page_str = response.css('.page-box.house-lst-page-box::attr("page-data")').extract_first('') #{"totalPage":100,"curPage":1}
        page_match = re.match(r'{"totalPage":(\d+),"curPage":(\d+)}', page_str)
        if page_match:
            all_page = int(page_match.group(1))
            current_page = int(page_match.group(2)) + 1
            print('****************************************',all_page,current_page,'*********************************')
            if current_page < all_page:
                yield Request(url=parse.urljoin(response.url, '/zufang/pg%d/' % current_page), callback=self.parse,dont_filter=True)

        
        # 处理地区，租金等分类
        # tag_links = response.css('.option-list a::text').extract()
        # print('')
        # for tag_link in tag_links:
        #     yield Request(url=parse.urljoin(response.url,tag_link), callback=self.parse)

    def parse_house_page(self, response):
        item_loader = RentingItemLoader(item=LianjiaItem(), response=response)

        item_loader.add_value('id', get_md5(response.url))
        item_loader.add_value('url', response.url)
        item_loader.add_css('main_title', '.title-wrapper .title .main::text')
        item_loader.add_css('price', '.overview .price .total::text')
        item_loader.add_css('price_unit', '.overview .price .unit span::text')

        item_loader.add_css('size', '.overview .zf-room p:nth-of-type(1)::text')
        item_loader.add_css('house_type', '.overview .zf-room p:nth-of-type(2)::text')
        item_loader.add_css('floor', '.overview .zf-room p:nth-of-type(3)::text')
        item_loader.add_css('house_orientation', '.overview .zf-room p:nth-of-type(4)::text')
        item_loader.add_css('subway', '.overview .zf-room p:nth-of-type(5)::text')
        item_loader.add_css('community', '.overview .zf-room p:nth-of-type(6) a::text')
        item_loader.add_css('location', '.overview .zf-room p:nth-of-type(7) a::text')#这个不能取第一项['闸北', '大宁']
        item_loader.add_css('publish_time', '.overview .zf-room p:nth-of-type(8)::text')
        item_loader.add_value('update_time', response.meta.get('update_time', 0))
        item_loader.add_value('seen_num', response.meta.get('seen_num', 0))
        item_loader.add_css('contact', '.overview .brokerInfo .phone::text')#['\n              4008761855\n                              ', '\n                40200\n                          ']

        house_item = item_loader.load_item()
        
        yield house_item


