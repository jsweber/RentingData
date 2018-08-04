# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst, Join
from scrapy.loader import ItemLoader
import time, datetime
from datetime import datetime, timedelta
import re
from RentingData.settings import SQL_DATETIME_FORMAT, SQL_DATE_FORMAT, phone_match, salaryPattern, timeStrpStr,salaryPattern2, salaryStrPattern, workExpPattern, degreePattern, agePattern, cityPattern
from RentingData.models.Job import Job

class RentingdataItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class RentingItemLoader(ItemLoader):
    #自定义itemloader
    default_output_processor = TakeFirst()

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



#猎聘item

class LiepinItemLoader(ItemLoader):
    #自定义itemloader
    default_output_processor = TakeFirst()

def getSalary(s):
    salary = re.match(salaryPattern, s)
    if salary:
        return salary.group(1)
    else:
        return '面议'

def clearDefaultAction(d):
    return d

class LiepinItem(scrapy.Item):
    job_id = scrapy.Field()
    job_url = scrapy.Field()
    job_name = scrapy.Field()
    company = scrapy.Field()
    salary = scrapy.Field()
    work_location = scrapy.Field()
    publish_time = scrapy.Field()
    required_list = scrapy.Field(
        input_processor = Join(',')
    )
    welfare_list = scrapy.Field(
        input_processor = Join(',')
    )
    job_describe = scrapy.Field(
        output_processor = Join('\n')
    )

    def get_insert_sql(self):
        insert_sql = 'insert into liepin_2018_4(job_id, job_url, job_name, company, salary, work_location, publish_time, required_list, welfare_list, job_describe, crawl_time) values( %s, %s, %s,%s, %s, %s, %s, %s, %s,  %s, now()) ON DUPLICATE KEY UPDATE crawl_time=values(crawl_time), publish_time=values(publish_time), salary=values(salary)'
        
        salary_val = getSalary(self.get('salary', '面议'))

        try:
            publish_time_array = time.strptime(self['publish_time'], '%Y年%m月%d日')
            publish_time = time.strftime(SQL_DATETIME_FORMAT, publish_time_array)
        except Exception as e:
            publish_time = datetime.now().strftime(SQL_DATETIME_FORMAT)

        params = (self['job_id'], self['job_url'], self.get('job_name', '无数据'), self.get('company','无数据'), salary_val, self.get('work_location', '无数据'), publish_time, self.get('required_list', '无数据'), self.get('welfare_list', '无数据'), self.get('job_describe', '无数据'))

        return insert_sql, params


def strpSalary(v):
    r = salaryStrPattern.search(v)
    if r:
        return r.group(1)
    return None

class LiepinItemv2(scrapy.Item):
    job_id = scrapy.Field()
    url = scrapy.Field()
    job_name = scrapy.Field()
    location = scrapy.Field()
    orginal_salary = scrapy.Field(
        input_processor = MapCompose(strpSalary)
    )
    publish_time = scrapy.Field()
    welfare = scrapy.Field(
        input_processor = Join(',')
    )
    describe = scrapy.Field(
        input_processor = Join('')
    )
    company = scrapy.Field()
    degree = scrapy.Field()
    exp = scrapy.Field()
    language = scrapy.Field()
    age = scrapy.Field()

    def save_to_es(self):
        job = Job()
        job.job_id = self['job_id']
        job.url = self['url']
        job.job_name = self['job_name']

        job.location = self['location']
        if self.get('location'):
            cs = cityPattern.split(self.get('location'))
            try:
                job.city = cs[0]
            except Exception as e:
                job.city = '其它'

        job.orginal_salary = self.get('orginal_salary')
        if self.get('orginal_salary'):  
            salarys = salaryPattern2.search(self['orginal_salary'])
            minVal = int(salarys.group(1))
            maxVal = int(salarys.group(2))
            job.low_salary = minVal
            job.high_salary = maxVal
            job.middle_salary = (minVal + maxVal)/2
        else:
            job.low_salary = -1
            job.high_salary = -1
            job.middle_salary = -1

        if self.get('publish_time'):
            struct_time = time.strptime(self['publish_time'], timeStrpStr)
            job.publish_time = time.strftime(SQL_DATETIME_FORMAT,struct_time)
        else:
            job.publish_time = time.strftime(SQL_DATETIME_FORMAT, time.localtime())

        job.crawl_time = time.strftime(SQL_DATETIME_FORMAT, time.localtime())
        job.welfare = self['welfare']
        job.describe = self['describe']
        job.company = self['company']

        exp = -1  #不限
        expObj = workExpPattern.search(self['exp'])
        if expObj:
            exp = expObj.group(1)

        #35-65岁
        degree = '不限'
        degreeObj = degreePattern.search(self['degree'])
        if degreeObj:
            degree = degreeObj.group()

        age = -1 #不限
        ageObj = agePattern.search(self['age'])
        if ageObj:
            age = ageObj.group(1)
            

        job.requires = {
            'degree': degree,
            'orginal_degree': self['degree'],
            'exp': int(exp),
            'orginal_exp': self['exp'],
            'language':self['language'],
            'age': int(age),
            'orginal_age': self['age']
        }
        job.save()

        return


