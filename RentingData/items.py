# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst, Join
from scrapy.loader import ItemLoader
import time
import re

class RentingdataItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class RentingItemLoader(ItemLoader):
    #自定义itemloader
    default_output_processor = TakeFirst()

phone_match = re.compile('\s|\\n')
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

        params = (self['id'], self['url'], self['main_title'], self['price'], self['price_unit'],    
        self['size'], self['floor'], self['house_type'], self['house_orientation'],
        self['subway'], self['community'], self['location'], self['publish_time'], self['update_time'], self['seen_num'], self['contact'])

        return insert_sql, params
