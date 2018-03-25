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

projectdir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
sys.path.insert(0,projectdir)
from settings import MYSQL_HOST, MYSQL_DBNAME, MYSQL_USER, MYSQL_PASSWORD
from utils.common import get_md5

log_file_path = os.path.join(projectdir, 'logs', 'xici_ip.'+ str(time.time()) +'.log')    

conn = pymysql.connect(host=MYSQL_HOST, user=MYSQL_USER, password=MYSQL_PASSWORD, db=MYSQL_DBNAME, charset='utf8')
ua = UserAgent

def crawl_ips():
    host = 'http://www.xicidaili.com/nn/%s'
    start_index = 1
    disabled_next_btn = []
    headers = {
        'User-Agent': UserAgent().random
    }
    ip_list = []
    with open(log_file_path, 'w') as log_file:
         #next_page不存在时才说明有下一页
        while len(disabled_next_btn)==0 and len(ip_list)<1000:
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
                    id = get_md5(ip+port+net_prot)

                    ip_list.append((id, ip, port, net_prot, speed_time, connect_time))
                print(len(ip_list), file=log_file)
            
            time.sleep(1)
            print('disabled按钮',disabled_next_btn, file=log_file)
        
        #存入数据库
        print('开始插入数据', file=log_file)
        try:
            with conn.cursor() as cursor:
                for ip_info in ip_list:
                    print(ip_info, file=log_file)
                    cursor.execute('insert into ip_pools(id, ip, port, net_prot, speed_time, connect_time) values(%s, %s, %s, %s, %s, %s)',ip_info)
                    conn.commit()
        except Exception as e:
            print('[mysql err]', e)
        finally:
            conn.close()
            print('插入数据end', file=log_file)

class GetIp(object):
    def delete_ip(self, ip):
        pass


    def judge_ip(self, ip, port, net_prot):
        pass

    def random(self):
        pass


if __name__ == '__main__':
    crawl_ips()
    print('执行完毕')

    
