# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from RentingData.utils.common import get_md5
from RentingData.tools.send_emai import send_email
from RentingData.items import LiepinItemLoader, LiepinItem
from urllib import parse
import re
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals

class LiepinSpider(CrawlSpider):
    name = 'liepin'
    allowed_domains = ['www.liepin.com']
    start_urls = ['https://www.liepin.com/zhaopin', 'https://www.liepin.com/it/']
    custom_settings = {
        'COOKIES_ENABLED': False,
        'DOWNLOAD_DELAY': 5,
        'AUTOTHROTTLE_ENABLED': True,
        'JOBDIR': 'job_info/liepin003'    
    }

    rules = (
        Rule(LinkExtractor(deny=(r'/job/.+?html$')), follow=True),
        Rule(LinkExtractor(allow=(r'/job/.+?html$')), callback="parse_item", follow=True),
    )

    def __init__(self, *a, **kw):
        super(LiepinSpider, self).__init__(*a, **kw)
        self.fails_urls = []
        dispatcher.connect(self.handle_spider_closed, signals.spider_closed)

    def handle_spider_closed(self, spider, reason):
        self.crawler.stats.set_value('failed_urls', ','.join(self.fails_urls))
        send_email('liepin爬虫运行结束')

    def parse_item(self, response):
        if response.status == 404:
            self.fail_urls.append(response.url)
            self.crawler.stats.inc_value('fail_url_number')

        if response.status == 403 or response.status == 401:
            pass

        item_loader = LiepinItemLoader(item=LiepinItem(), response=response)

        item_loader.add_value('job_id', get_md5(response.url))
        item_loader.add_value('job_url', response.url)
        item_loader.add_css('job_name', '.title-info h1::text')
        item_loader.add_css('company', '.title-info h3 a::text')
        item_loader.add_css('salary', '.job-item-title::text')
        item_loader.add_css('work_location', '.basic-infor span a::text')
        item_loader.add_css('publish_time', '.basic-infor time::attr(title)')#2018年04月10日
        item_loader.add_css('required_list', '.job-qualifications span::text')
        item_loader.add_css('welfare_list', '.tag-list span::text')
        item_loader.add_css('job_describe', '.job-description .content::text')

        job_item = item_loader.load_item()
        return job_item
