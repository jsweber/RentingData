#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'du'

import requests
from scrapy.selector import Selector
import pymysql.cursors
from fake_useragent import UserAgent
import sys
import os
import time
import pickle
import random
import sys

projectdir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
sys.path.insert(0,projectdir)
from settings import MYSQL_HOST, MYSQL_DBNAME, MYSQL_USER, MYSQL_PASSWORD, IP_CRAWL_NUM, IP_POOLS_FILE_NAME
from utils.common import get_md5

log_file_path = os.path.join(projectdir, 'logs', 'xici_ip.'+ str(time.time()) +'.log')    

conn = pymysql.connect(host=MYSQL_HOST, user=MYSQL_USER, password=MYSQL_PASSWORD, db=MYSQL_DBNAME, charset='utf8')
ua = UserAgent()

def crawl_ips():
    host = 'http://www.xicidaili.com/nn/%s'
    start_index = 1
    disabled_next_btn = []
    headers = {
        'User-Agent': ua.random
    }
    ip_list = []
    with open(log_file_path, 'w') as log_file:
         #next_page不存在时才说明有下一页
        while len(disabled_next_btn)==0 and len(ip_list)<IP_CRAWL_NUM:
            ''' 这层循环是新页面 '''
            print('---------------- 第%d页 -------------------' % start_index, file=log_file)
            re = requests.get(host % start_index, headers=headers)
            selector = Selector(text=re.text)
            disabled_next_btn = selector.css('.next_page.disabled')  #当到达最后一页时，next_page会不能使用
            start_index +=1

            all_trs = selector.css('#ip_list tr')
            for tr in all_trs[1:]:
                ''' 这层循环是处理表格中的行 '''
                all_tr_text = tr.css('td::text').extract()
                if 'HTTP' in all_tr_text:
                    net_prot = all_tr_text[all_tr_text.index('HTTP')]
                elif 'HTTPS' in all_tr_text:
                    net_prot = all_tr_text[all_tr_text.index('HTTPS')]

                if 'HTTP' in all_tr_text or 'HTTPS' in all_tr_text:
                    ip = all_tr_text[0]
                    port = all_tr_text[1]
                    times = tr.css('.bar::attr(title)').extract()

                    if len(times) ==2:
                        speed_time = float(times[0].split('秒')[0])
                        connect_time = float(times[1].split('秒')[0])
                    else:
                        speed_time = 0
                        connect_time = 0

                    ip_list.append((ip, port, net_prot, speed_time, connect_time))
                print(len(ip_list), file=log_file)
            
            time.sleep(3)
            print('disabled按钮',disabled_next_btn, file=log_file)
        
        #存入数据库
        print('开始插入数据', file=log_file)
        try:
            with conn.cursor() as cursor:
                for ip_info in ip_list:
                    print(ip_info, file=log_file)
                    cursor.execute('insert low_priority into ip_pools(ip, port, net_prot, speed_time, connect_time) values(%s, %s, %s, %s, %s)',ip_info)
                    conn.commit()
        except Exception as e:
            print('[mysql err]', e)
        finally:
            conn.close()
            print('插入数据end', file=log_file)

class GetIp(object):
    ips = set()
    count = 0
    def __init__(self):
        self.cursor = conn.cursor()

        try:
            with open(os.path.join(projectdir,IP_POOLS_FILE_NAME ), 'rb') as f:
                ip_set = pickle.load(f)
                self.ip_list = list(ip_set)
        except Exception as e:
            print(e)
            self.ip_list = []

        self.ip_list_len = len(self.ip_list)

    def delete_ip(self, id):
        del_sql = 'delete from ip_pools where id=%s'
        self.cursor.execute(del_sql, id)
        conn.commit()
        print('del '+str(id)+' success')
        return True

    def judge_ip(self, url, id='', timeout=15):
        test_url = 'https://www.liepin.com/'
        try:
            proxy_dict = {
                'http': url,
                'https': url
            }
            resp = requests.get(test_url, proxies=proxy_dict, timeout=timeout)
        except Exception as e:
            print(url + ' is invalid')
            if id != '':
                self.delete_ip(id)
            return False
        else:
            code = resp.status_code
            if code >=200 and code <300:
                print(url + ' can be used')
                return True
            else:
                print(url + ' is invalid')
                if id != '':
                    self.delete_ip(id)
                return False
    def check(self, check_num=-1):
        if check_num > 0:
            limit_num = ' limit '+str(check_num)
        else:
            limit_num = ''
        get_all_sql = r'select id, concat(lower(net_prot), "://",ip, ":" ,port) as url from ip_pools'+limit_num
        print(get_all_sql)
        self.cursor.execute(get_all_sql)
        rs = self.cursor.fetchall()
        for r in rs:
            if self.judge_ip(r[1], r[0]):
                self.ips.add(r[1])

        with open(os.path.join(projectdir,IP_POOLS_FILE_NAME ), 'wb') as f:
            pickle.dump(self.ips, f)
        return 'end'
                

    def random_ip_by_sql(self):
        random_sql = r'select id, concat(lower(net_prot), "://",ip, ":" ,port) as url from ip_pools order by rand() limit 1;'
        self.cursor.execute(random_sql)
        result = self.cursor.fetchone()
        id = result[0]
        url = result[1]
        if self.judge_ip(url, id): 
            return url
        else:
            return self.random_ip_by_sql()
    
    def random_ip_fast(self):
        if self.ip_list_len == 0:
            print('no fast ip')
            return self.random_ip_by_sql()
        else:
            if len(self.ip_list)>0:
                url = self.ip_list.pop()
            else:
                return 'http://localhost'
            if self.judge_ip(url, timeout=10): 
                return url
            else:
                return self.random_ip_fast()
            
        


if __name__ == '__main__':
    args = sys.argv
    #第一参数是文件名，真正有用的参数从下标1开始
    is_start_crawl = False
    is_start_check = False
    check_num = -1

    for i in range(1, len(args)):
        print(args[i])
        if args[i] == 'help':
            print('1.crawl 命令开始爬取 | ', '2.check [int 验证的ip数量] 命令开始验证爬取的ip | ', '3.注意每次只能输入一个命令，不支持同时执行')
        if args[i] == 'crawl':
            is_start_crawl = True
        if args[i] == 'check':
            is_start_check = True
            try:
                check_num = int(args[i+1])
            except Exception as e:
                pass

    if is_start_crawl and (not is_start_check):
        print('开始爬取西刺')
        crawl_ips()
        print('执行完毕')

    if (not is_start_crawl) and is_start_check:
        print('开始检查')
        getip = GetIp()
        getip.check(check_num=check_num)
        print('检查结束')
    
