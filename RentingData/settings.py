# -*- coding: utf-8 -*-

# Scrapy settings for RentingData project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html
import re,sys,os

BOT_NAME = 'RentingData'

SPIDER_MODULES = ['RentingData.spiders']
NEWSPIDER_MODULE = 'RentingData.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'RentingData (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'RentingData.middlewares.RentingdataSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    'RentingData.middlewares.RandomUserAgentMiddleware': 1000,
    'RentingData.middlewares.RentingdataDownloaderMiddleware': 543,
}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
#    'RentingData.pipelines.MysqlTwistedPipline': 300,
   'RentingData.pipelines.ESPipline': 300,
}

DOWNLOAD_TIMEOUT = 15
DOWNLOAD_TIMEOUT = 15
REDIRECT_ENABLED = False
DEPTH_LIMIT=0

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
sys.path.insert(0, os.path.dirname(__file__))
MYSQL_HOST='127.0.0.1'
MYSQL_DBNAME='renting_data'
MYSQL_USER='root'
MYSQL_PASSWORD='ecust2014'

SQL_DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'
SQL_DATE_FORMAT = '%Y-%m-%d'

IP_CRAWL_NUM = 10000
IP_POOLS_FILE_NAME = 'ip_pools.txt'
#猎聘爬虫2用，把日期解析成struct_time
timeStrpStr = '%Y年%m月%d日'

#re.match只匹配字符串的开始，如果字符串开始不符合正则表达式，则匹配失败，函数返回None；而re.search匹配整个字符串，直到找到一个匹配。

#解析字段的正则
phone_match = re.compile(r'[\s\n]+')
salaryPattern = re.compile(u".*?([\u4e00-\u9fa5]+|[0-9-]+?[\u4e00-\u9fa5]+).*")

#下面正则猎聘2用,推荐用search，因为不要求完全匹配
#薪水解析
salaryPattern2 = re.compile(r'([\d\.]+)-([\d\.]+)万.*') #面议是匹配不到的，设置-1（面议）
salaryStrPattern = re.compile(r'([\d\.]+-[\d\.]+万).*')
#工作经验解析
workExpPattern = re.compile(r'^(\d+).*') #工作经验不限是匹配不到的，设置-1(不限) 
#学历
degreePattern = re.compile(r'本科|大专|高中|硕士|研究生|中专|技校|博士|博士后|修士|留学|初中|小学|211|985')
#经验
agePattern = re.compile(r'^(\d+).*')
#城市
cityPattern = re.compile(r'-')

