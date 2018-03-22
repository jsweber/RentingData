# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class RentingdataItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class LianjiaItem(scrapy.Item):
    id = scrapy.Field() #url => md5
    url = scrap.Field()
    main_title = scrapy.Field()
    price = scrapy.Field()
    price_unit = scrapy.Filed()  #价格单位
    size = scrapy.Field() #房子尺寸
    floor = scrapy.Field() #楼层
    house_type = scrapy.Field() #户型
    house_orientation = scrapy.Field() #房屋朝向
    subway = scrapy.Field() 
    community = scrapy.Field() #小区
    location = scrapy.Field() #位置
    publish_time = scrapy.Field() #房屋发布时间
    contact = scrapy.Field()
    contact_man = scrapy.Field() #联系人    
