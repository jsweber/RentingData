# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from RentingData.utils.common import get_md5
from RentingData.tools.send_emai import send_email
from RentingData.items import LiepinItemLoader, LiepinItemv2
from urllib import parse
import re
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals

class LiepinSpider(CrawlSpider):
    name = 'liepinv2'
    allowed_domains = ['www.liepin.com']
    start_urls = ['https://www.liepin.com/zhaopin', 'https://www.liepin.com/it/']
    custom_settings = {
        'COOKIES_ENABLED': False,
        'DOWNLOAD_DELAY': 3,
        'AUTOTHROTTLE_ENABLED': True,
        'AUTOTHROTTLE_MAX_DELAY':15 
        'JOBDIR': 'job_info/liepinv2_1'    
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

        item_loader = LiepinItemLoader(item=LiepinItemv2(), response=response)

        item_loader.add_value('job_id', get_md5(response.url))
        item_loader.add_value('url', response.url)
        item_loader.add_css('job_name', '.title-info h1::text')
        item_loader.add_css('location', '.basic-infor span a::text')
        item_loader.add_css('orginal_salary', '.job-item-title::text')#'面议\r\n'
        item_loader.add_css('publish_time', '.basic-infor time::attr(title)')#2018年07月31日
        item_loader.add_css('welfare', '.tag-list span::text')#['领导好', '岗位晋升', '五险一金', '公司规模大', '带薪年假', '定期体检', '技能培训', '节日礼物', '休闲餐点', '发展空间大', '上市公司', '免费班车', '包吃', '扁平管理', '国际化项目', '健身房']
        item_loader.add_css('describe', '.job-description .content::text')
        item_loader.add_css('company', '.title-info h3 a::text')
        item_loader.add_css('degree', '.job-qualifications span:nth-of-type(1)::text')
        item_loader.add_css('exp', '.job-qualifications span:nth-of-type(2)::text')
        item_loader.add_css('language', '.job-qualifications span:nth-of-type(3)::text')
        item_loader.add_css('age', '.job-qualifications span:nth-of-type(4)::text')

        job_item = item_loader.load_item()
        return job_item
