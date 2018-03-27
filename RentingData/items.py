# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst, Join
from scrapy.loader import ItemLoader

class RentingdataItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class RentingItemLoader(ItemLoader):
    #自定义itemloader
    default_output_processor = TakeFirst()

class LianjiaItem(scrapy.Item):
    id = scrapy.Field() #url => md5
    url = scrapy.Field()
    main_title = scrapy.Field()
    price = scrapy.Field()
    price_unit = scrapy.Field()  #价格单位
    decoration = scrapy.Field() #装修程度
    size = scrapy.Field() #房子尺寸
    floor = scrapy.Field() #楼层
    house_type = scrapy.Field() #户型
    house_orientation = scrapy.Field() #房屋朝向
    subway = scrapy.Field() 
    community = scrapy.Field() #小区
    location = scrapy.Field() #位置
    publish_time = scrapy.Field() #房屋发布时间
    update_time = scrapy.Field() #更新时间
    seen_num = scrapy.Field() #看过的人
    contact = scrapy.Field()  
