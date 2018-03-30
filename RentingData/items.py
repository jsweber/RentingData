# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst, Join
from scrapy.loader import ItemLoader
import time
from datetime import datetime, timedelta
import re
from RentingData.settings import SQL_DATETIME_FORMAT, SQL_DATE_FORMAT

class RentingdataItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class RentingItemLoader(ItemLoader):
    #自定义itemloader
    default_output_processor = TakeFirst()

phone_match = re.compile(r'[\s\n]+')
def dealContact(val):
    return re.sub(phone_match, '', v)

def set_default_val(arr):
    if len(arr) == 0:
        return '未知'
    else:
        return arr[0]
    
def get_seen_num(arr):
    if len(arr) == 0:
        return 0
    else:
        return int(arr[0])

class LianjiaItem(scrapy.Item):
    '''
    output_processor里传给函数的值都是数组的元素并不是整个数组
    '''
    id = scrapy.Field() #url => md5
    url = scrapy.Field()
    main_title = scrapy.Field()
    price = scrapy.Field(
        input_processor=MapCompose(lambda x: float(x)),
        output_processor=TakeFirst()
    )
    price_unit = scrapy.Field()  #价格单位


    size = scrapy.Field() #房子尺寸
    floor = scrapy.Field() #楼层
    house_type = scrapy.Field() #户型
    house_orientation = scrapy.Field() #房屋朝向

    subway = scrapy.Field() 
    community = scrapy.Field() #小区
    location = scrapy.Field(
        output_processor=Join('.')
    ) #位置
    publish_time = scrapy.Field() #房屋发布时间
    update_time = scrapy.Field() #更新时间

    seen_num = scrapy.Field(
        input_processor=MapCompose(lambda x: int(x)),
        output_processor=TakeFirst()
    ) #看过的人
    contact = scrapy.Field(
        intput_processor=MapCompose(dealContact),
        output_processor=Join('-')
    )  

    def get_insert_sql(self):
        insert_sql = 'insert into lianjia_data(id, url, main_title, price, price_unit, size, floor, house_type, house_orientation, subway, community, location, publish_time, update_time, seen_num, contact, crawl_time) values( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, now()) ON DUPLICATE KEY UPDATE update_time=values(update_time), seen_num=values(seen_num), price=values(price)'

        contact = re.sub(phone_match,'', self['contact'])
        publish_time_match = re.match(r'\d+', self['publish_time'])
        if publish_time_match:
            days = int(publish_time_match.group(0))
            publish_time = datetime.now() - timedelta(days=days)
            publish_time = publish_time.strftime(SQL_DATETIME_FORMAT)
        else:
            publish_time = datetime.now().strftime(SQL_DATETIME_FORMAT)

        try:
            update_time_array = time.strptime(self['update_time'], '%Y.%m.%d')
            update_time = time.strftime(SQL_DATETIME_FORMAT, update_time_array)
        except Exception as e:
            update_time = datetime.now().strftime(SQL_DATETIME_FORMAT)

        params = (self['id'], self['url'], self['main_title'], self['price'], self['price_unit'],    
        self['size'], self['floor'], self['house_type'], self['house_orientation'],
        self['subway'], self['community'], self['location'], publish_time, update_time, self['seen_num'], contact)

        return insert_sql, params
